"""Locale identity and canonical lesson paths; no learner-state writes."""
from pathlib import Path
import re
import yaml

SUPPORTED_LANGUAGES = ('en', 'vi')
IDENTITY_KEYS = ('lesson_id', 'topic_id')


def metadata(path):
    text = Path(path).read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError('Document requires YAML front matter')
    return yaml.safe_load(text.split('---', 2)[1])


def canonical_lesson(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    relative = path.relative_to(root)
    meta = metadata(path)
    locale = meta.get('locale', 'en')
    if locale not in SUPPORTED_LANGUAGES:
        raise ValueError('Unsupported lesson locale')
    if meta.get('canonical_lesson'):
        if locale == 'en' or relative.parts[:2] != (locale, 'lessons'):
            raise ValueError('Translations belong under LOCALE/lessons/')
        canonical = (root / meta['canonical_lesson']).resolve()
        if canonical.relative_to(root).parts[0] != 'lessons':
            raise ValueError('Canonical path must stay inside lessons/')
        master = metadata(canonical)
        if master.get('canonical_lesson') or master.get('locale', 'en') != 'en':
            raise ValueError('Translation must reference the English canonical lesson directly')
        for key in IDENTITY_KEYS:
            if meta.get(key) != master.get(key):
                raise ValueError('Translation identity differs from canonical lesson: ' + key)
        if meta.get('translation_key') != master.get('translation_key', master['lesson_id']):
            raise ValueError('Translation group differs from canonical lesson')
        for key in ('domain', 'level', 'mode', 'created_at', 'status', 'objectives',
                    'concept_fingerprint', 'source_refs', 'duration_minutes', 'practice_minutes', 'checked_at'):
            if key in meta and meta[key] != master.get(key):
                raise ValueError('Translation must not override shared metadata: ' + key)
        path = canonical
    elif locale != 'en':
        raise ValueError('Translated lessons require canonical_lesson')
    relative = path.relative_to(root)
    if relative.parts[0] != 'lessons' or path.suffix != '.md':
        raise ValueError('Canonical lessons must be Markdown files inside lessons/')
    return path


def lesson_variant(root, canonical, language):
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError('Unsupported language')
    root = Path(root).resolve()
    canonical = canonical_lesson(root, canonical)
    master = metadata(canonical)
    if language == 'en':
        return canonical, False
    matches = []
    for path in (root / language / 'lessons').glob('*.md'):
        meta = metadata(path)
        if meta.get('lesson_id') == master['lesson_id']:
            if canonical_lesson(root, path) != canonical:
                raise ValueError('Translation points to another logical lesson')
            matches.append(path)
    if len(matches) > 1:
        raise ValueError('Duplicate locale variant for one logical lesson')
    return (matches[0], False) if matches else (canonical, True)


def strings(value, prefix=''):
    if isinstance(value, dict):
        result = {}
        for key, child in value.items():
            result.update(strings(child, prefix + '.' + str(key)))
        return result
    if isinstance(value, list):
        result = {}
        for index, child in enumerate(value):
            result.update(strings(child, prefix + '.' + str(index)))
        return result
    if not isinstance(value, str) or not value.strip():
        raise ValueError('UI translation must be a nonempty string: ' + prefix)
    return {prefix: value}


def code_contract(path):
    text = Path(path).read_text()
    includes = set(re.findall(r'{%\s*include\s+((?:lab-code|interview)/[^\s%]+)\s*%}', text))
    blocks = re.findall(r'^```([^\n]+)\n(.*?)^```[ \t]*$', text, re.M | re.S)
    return includes, blocks


def validate_localization(root):
    root = Path(root).resolve()
    config = yaml.safe_load((root / '_config.yml').read_text())
    if config.get('default_locale') != 'en' or tuple(config.get('supported_locales', [])) != SUPPORTED_LANGUAGES:
        raise ValueError('Site locale configuration must match supported English/Vietnamese languages')
    names = yaml.safe_load((root / '_data/locales.yml').read_text())
    if set(names) != set(SUPPORTED_LANGUAGES):
        raise ValueError('Native language names must match supported locales')
    strings(names)
    dictionaries = {lang: strings(yaml.safe_load((root / '_data/i18n' / (lang + '.yml')).read_text())) for lang in SUPPORTED_LANGUAGES}
    if dictionaries['en'].keys() != dictionaries['vi'].keys():
        raise ValueError('UI translation keys differ between locales')
    groups = {}
    translated_lessons = 0
    for path in root.rglob('*.md'):
        if any(part in {'.git', '_site', 'work', '.venv', '_includes'} for part in path.relative_to(root).parts):
            continue
        if not path.read_text().startswith('---\n'):
            continue
        meta = metadata(path)
        language = meta.get('locale', 'en')
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError('Unsupported page locale: ' + str(path))
        if language != 'en' and path.relative_to(root).parts[0] != language:
            raise ValueError('Translated pages must live under their locale directory')
        key = meta.get('translation_key')
        if language != 'en' and not key:
            raise ValueError('Translated pages need a stable translation_key')
        if key:
            if not isinstance(key, str) or not re.fullmatch(r'[a-z0-9-]+', key):
                raise ValueError('Invalid translation_key')
            group = groups.setdefault(key, {})
            if language in group:
                raise ValueError('Duplicate locale page in translation group: ' + key)
            group[language] = path
        if meta.get('lesson_id'):
            canonical = canonical_lesson(root, path)
            if key and key != metadata(canonical)['lesson_id']:
                raise ValueError('Lesson translation_key must equal its logical lesson_id')
            if path != canonical:
                translated_lessons += 1
                if meta.get('layout') != 'lesson' or not meta.get('primary_objective') or not meta.get('prerequisites_note'):
                    raise ValueError('Translated lesson needs localized header and lesson layout')
                content = path.read_text()
                if not all('{: #' + step + ' }' in content for step in ('goal', 'predict', 'model', 'practice', 'verify', 'recall')):
                    raise ValueError('Translated lesson must preserve the six step IDs')
                if code_contract(path) != code_contract(canonical):
                    raise ValueError('Locale lesson code or shared answer references differ')
    if any('en' not in group for group in groups.values()):
        raise ValueError('Translation group has no English canonical page')
    return {'groups': len(groups), 'translated_lessons': translated_lessons, 'ui_strings': len(dictionaries['en'])}
