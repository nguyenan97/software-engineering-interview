#!/usr/bin/env python3
"""Validate and render source-traceable EN/VI question pages; never write learner state."""
import argparse
from collections import Counter
import hashlib
import html
import json
import os
from pathlib import Path
import re
import string

import yaml

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('foundation', 'mechanism', 'application', 'failure', 'tradeoff', 'production')
TEXT_FIELDS = {'question', 'explanation', 'intent', 'scope', 'senior_signals', 'pitfalls', 'followups'}
QUESTION_LIST_FIELDS = {'senior_signals', 'pitfalls', 'followups'}
GROUP_FIELDS = {'title', 'goal', 'competencies', 'bridge', 'scenario', 'rubric'}
RUBRIC_FIELDS = {'basic', 'senior', 'evidence_missing'}
COUNT_FIELDS = {'numbered_source_questions', 'source_scenarios', 'source_units', 'canonical_questions',
                'merge_sets', 'groups', 'domains', 'unprocessed'}
SCENARIOS = (
    ('02-aspnet-api-ef.md', 'large-file-processing-scenario', 'Large-file processing scenario', 'S02-SC001'),
    ('03-sql-data-performance.md', 'query-optimization', 'Query optimization', 'S03-SC001'),
    ('04-architecture-distributed-systems.md', 'production-scenario', 'Production scenario', 'S04-SC001'),
    ('06-frontend-behavioral.md', 'cross-stack-request-flow', 'Cross-stack request flow', 'S06-SC001'),
)
# Structural headings in the normalized corpus are classification boundaries,
# not an exemption for arbitrary new interview prompts written as headings.
SOURCE_SECTIONS = {
    '01-csharp-dotnet.md': {'C# fundamentals', '.NET runtime and asynchronous programming',
                          'Dependency Injection and SOLID', 'Patterns', 'Performance and caching'},
    '02-aspnet-api-ef.md': {'ASP.NET Core request pipeline', 'HTTP and API design',
                          'Background processing', 'LINQ and EF Core'},
    '03-sql-data-performance.md': {'SQL objects', 'Indexing', 'Transactions and concurrency',
                                 'Bulk data', 'SQL exercises'},
    '04-architecture-distributed-systems.md': {'Architecture discussion', 'Microservices',
                                              'API Gateway', 'Messaging', 'DDD and CQRS', 'Distributed consistency'},
    '05-security-cloud-devops.md': {'JWT and identity', 'Transport and web security', 'Azure and cloud services',
                                  'Observability', 'Docker and delivery', 'Background and operational reliability'},
    '06-frontend-behavioral.md': {'Angular and frontend architecture', 'TypeScript and JavaScript',
                               'Engineering communication', 'Interview answer structure'},
}


def read(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError('Cannot read question-bank JSON: ' + str(path) + ': ' + str(exc)) from exc


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def rows(value, context):
    require(isinstance(value, list), context + ': expected an array')
    require(all(isinstance(item, dict) for item in value), context + ': expected object entries')
    return value


def strings(value, context, minimum=1):
    require(isinstance(value, list) and len(value) >= minimum,
            context + ': expected a string array with at least ' + str(minimum) + ' entries')
    require(all(nonempty_string(item) for item in value), context + ': invalid string-array entry')


def index_rows(items, field, context):
    for item in items:
        require(nonempty_string(item.get(field)), context + ': missing or invalid ' + field)
    indexed = {item[field]: item for item in items}
    require(len(indexed) == len(items), 'Duplicate ' + context + ' ID')
    return indexed


def source_units(root):
    """Fail closed on source content not classified as a prompt, scenario or advice.

    The numbered grammar is deliberately strict. Independently finding identifiers
    and examining the residue prevents an unsupported new format or unnumbered
    prompt from silently disappearing, even after someone updates a file hash.
    """
    root = Path(root)
    units = {}
    numbered = re.compile(r'<a id="(q\d+)"></a>\n\*\*(S\d+-Q\d+)\*\*[^\n]*\n\n([^\n]+)')
    source_topic = re.compile(r'\(\.\./curriculum/domains/[^)#]+\.md#([a-z0-9-]+)\)')
    advice_lines = {
        'For senior-level technical questions, a useful answer shape is:',
        '1. **What** — concise definition.',
        '2. **Why / when** — the problem it solves.',
        '3. **How** — causal mechanics.',
        '4. **Trade-offs** — costs and alternatives.',
        '5. **Production example** — generic and non-confidential.',
        '6. **Failure mode** — what can go wrong.',
        '7. **Evidence** — metric, trace, execution plan, benchmark or test used to validate the decision.',
        'This structure is an explanation aid, not a promise that an interviewer will avoid follow-up questions. Support claims with evidence, state limits and invite a relevant next topic only after answering the current question.',
    }
    boilerplate = {
        '**Source status:** normalized interview prompts, not verified technical answers. Stable IDs preserve this privacy-safe corpus; no removed identities are reconstructed.',
        'Questions are grouped by learning level inside their original sections. Canonical curriculum links consolidate overlapping wording into one topic. Level labels express intended lesson depth, not a claim about any interviewer.',
        '[Curriculum index](../curriculum/index.md) · [Source coverage and gaps](../curriculum/source-coverage.md)',
        'These source questions are intentionally generalized so they can be answered without exposing personal or employer information.',
        '**Related practice:** [Collection choice and evidence-led coding](../curriculum/domains/algorithms-debugging.md#algorithms-collection-reasoning). This is an adjacent exercise, not an additional original source question.',
        '> Privacy-safe normalization of interview notes. Identifying names, organizations, projects and personal answers are intentionally excluded.',
        '> Technical content only. Personal, organization and project identifiers were removed during normalization.',
        '> Normalized interview material with identifying context removed.',
        '> Reusable technical interview content only; identifying context has been removed.',
        '> Privacy-safe technical material extracted and normalized from the interview corpus.',
        '> Only reusable interview prompts are retained. Personal biographies, employer history, named projects and organization-specific answers are excluded.',
    }
    for path in sorted((root / 'sources').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        context = path.relative_to(root).as_posix()
        front_match = re.match(r'\A---\n.*?\n---\n', text, re.DOTALL)
        require(front_match is not None, 'Unsupported source front matter: ' + context)
        try:
            metadata = yaml.safe_load(front_match[0].split('---', 2)[1])
        except yaml.YAMLError as exc:
            raise ValueError('Invalid source front matter: ' + context) from exc
        require(isinstance(metadata, dict) and nonempty_string(metadata.get('title')),
                'Missing source title: ' + context)
        headings = {'# ' + metadata['title'], '### Foundation', '### Senior', '### Architect'}
        headings |= {'## ' + heading for heading in SOURCE_SECTIONS.get(path.name, set())}
        matches = list(numbered.finditer(text))
        found_ids = re.findall(r'\bS\d+-Q\d+\b', text)
        require(Counter(found_ids) == Counter(m[2] for m in matches),
                'Unsupported numbered source format or identifier: ' + context)
        for match in matches:
            source_id = match[2]
            require(re.fullmatch(r'S\d{2}-Q\d{3}', source_id) is not None,
                    'Invalid source ID: ' + source_id)
            require(source_id[1:3] == path.name[:2] and match[1] == 'q' + source_id[-3:],
                    'Source ID/file/anchor mismatch: ' + source_id)
            require(source_id not in units, 'Duplicate source ID: ' + source_id)
            require(nonempty_string(match[3]), 'Empty source question: ' + source_id)
            topics = source_topic.findall(match[0].split('\n\n', 1)[0])
            require(len(topics) == 1, 'Missing or ambiguous source topic link: ' + source_id)
            units[source_id] = {'source_ref': context + '#' + match[1],
                                'original': match[3], 'kind': 'numbered', 'original_group_id': topics[0]}
        residue = numbered.sub('', text[front_match.end():])
        for filename, anchor, heading, source_id in SCENARIOS:
            if filename != path.name:
                continue
            section = re.compile(r'^## ' + re.escape(heading) + r'\n(.*?)(?=^## |\Z)', re.MULTILINE | re.DOTALL)
            sections = list(section.finditer(residue))
            require(len(sections) == 1, 'Missing or duplicate source scenario: ' + context + '#' + anchor)
            # Preserved sources use Jekyll/Kramdown heading IDs, not explicit <a> tags.
            require(re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-') == anchor,
                    'Source scenario heading/anchor mismatch: ' + context + '#' + anchor)
            original = sections[0][1].strip()
            require(nonempty_string(original), 'Empty source scenario: ' + source_id)
            topics = source_topic.findall(original)
            require(bool(topics), 'Missing source scenario topic link: ' + source_id)
            units[source_id] = {'source_ref': context + '#' + anchor,
                                'original': original, 'kind': 'source-scenario', 'original_group_id': topics[0]}
            residue = section.sub('', residue)
        for line_number, line in enumerate(residue.splitlines(), 1):
            line = line.strip()
            if not line or line in boilerplate:
                continue
            if line in headings:
                continue
            if path.name == '06-frontend-behavioral.md' and line in advice_lines:
                continue
            raise ValueError(f'Unclassified source content (register a question, scenario or advice): {context}:{line_number}: {line}')
    require(all(source_id in units for _, _, _, source_id in SCENARIOS), 'Missing source scenario document')
    return units


def load_bank(root=ROOT):
    root = Path(root)
    data = root / '_data/question_bank'
    inventory = read(data / 'inventory.json')
    require(isinstance(inventory, dict), 'Question inventory: expected an object')
    for field in ('source_units', 'canonical_questions', 'merge_sets', 'documents', 'retained_advice'):
        rows(inventory.get(field), 'Question inventory ' + field)
    questions = [q for path in sorted((data / 'questions').glob('*.json')) for q in rows(read(path), str(path))]
    groups = [g for path in sorted((data / 'groups').glob('*.json')) for g in rows(read(path), str(path))]
    catalog_data = read(root / 'curriculum/catalog.json')
    require(isinstance(catalog_data, dict), 'Catalog: expected an object')
    catalog = index_rows(rows(catalog_data.get('topics'), 'Catalog topics'), 'topic_id', 'catalog topic')
    for topic_id, topic in catalog.items():
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', topic_id) is not None,
                'Invalid catalog topic ID: ' + topic_id)
        require(all(nonempty_string(topic.get(k)) for k in ('title', 'domain', 'level')), 'Invalid catalog topic: ' + topic_id)
        strings(topic.get('prerequisites'), 'Catalog prerequisites: ' + topic_id, minimum=0)
        require(all(p in catalog for p in topic['prerequisites']), 'Unknown catalog prerequisite: ' + topic_id)
    return inventory, questions, groups, catalog


def localized_fields(item, fields, context):
    for language in ('en', 'vi'):
        content = item.get(language)
        require(isinstance(content, dict), context + ': missing or invalid locale: ' + language)
        require(set(content) == fields, context + ': locale fields differ: ' + language)
        for key, value in content.items():
            field_context = context + ': ' + language + '.' + key
            if key == 'rubric':
                require(isinstance(value, dict) and set(value) == RUBRIC_FIELDS, field_context + ': invalid rubric')
                require(all(nonempty_string(v) for v in value.values()), field_context + ': empty rubric')
            elif key in QUESTION_LIST_FIELDS | {'competencies'}:
                strings(value, field_context)
            else:
                require(nonempty_string(value), field_context + ': expected nonempty text')
    for key in fields:
        if isinstance(item['en'][key], (list, dict)):
            require(len(item['en'][key]) == len(item['vi'][key]), context + ': bilingual list parity: ' + key)


def validate_bank(root=ROOT):
    root = Path(root)
    inventory, questions, groups, catalog = load_bank(root)
    require(type(inventory.get('schema_version')) is int and inventory['schema_version'] == 1,
            'Unsupported question inventory schema')
    require(nonempty_string(inventory.get('audited_at')), 'Missing question inventory audit date')
    observed = source_units(root)
    units = index_rows(inventory['source_units'], 'source_id', 'inventory source')
    unit_fields = {'source_id', 'source_ref', 'kind', 'original', 'group_id', 'original_group_id', 'canonical_id'}
    for source_id, unit in units.items():
        require(set(unit) == unit_fields and all(nonempty_string(v) for v in unit.values()),
                'Invalid inventory source metadata: ' + source_id)
    require(set(units) == set(observed), 'Source coverage mismatch (missing or extra source unit)')
    for source_id, source in observed.items():
        require(all(units[source_id][k] == v for k, v in source.items()), 'Source text/anchor changed: ' + source_id)
    # Snapshot hashes protect source bodies beyond the numbered prompt line too.
    documents = index_rows(inventory['documents'], 'path', 'inventory document')
    source_paths = {p.relative_to(root).as_posix() for p in (root / 'sources').glob('*.md')}
    require({p for p, d in documents.items() if d.get('role') == 'source'} == source_paths,
            'Source document snapshot coverage mismatch')
    for document in documents.values():
        require(set(document) == {'path', 'role', 'sha256'} and nonempty_string(document['role'])
                and isinstance(document['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', document['sha256']),
                'Invalid document snapshot metadata: ' + document['path'])
        path = Path(document['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'Invalid snapshot path: ' + str(path))
        if document['role'] == 'source':
            require(hashlib.sha256((root / document['path']).read_bytes()).hexdigest() == document['sha256'],
                    'Preserved source file changed: ' + document['path'])
    canonical = index_rows(inventory['canonical_questions'], 'question_id', 'canonical question')
    annotations = index_rows(questions, 'question_id', 'question annotation')
    require(set(canonical) == set(annotations), 'Question annotation coverage mismatch')
    aliases = []
    for question_id, shared in canonical.items():
        require(set(shared) == {'question_id', 'group_id', 'source_ids', 'source_refs', 'kind', 'merge_rationale', 'related_group_ids'},
                'Invalid canonical metadata: ' + question_id)
        require(nonempty_string(shared['group_id']) and shared['group_id'] in catalog,
                'Group must reuse a catalog topic ID: ' + question_id)
        strings(shared['source_ids'], 'Canonical source IDs: ' + question_id)
        require(all(s in units for s in shared['source_ids']), 'Unknown canonical source ID: ' + question_id)
        require(shared['source_ids'] == sorted(set(shared['source_ids'])), 'Canonical source IDs must be unique and sorted: ' + question_id)
        strings(shared['source_refs'], 'Canonical source links: ' + question_id)
        strings(shared['related_group_ids'], 'Related groups: ' + question_id, minimum=0)
        require(len(set(shared['related_group_ids'])) == len(shared['related_group_ids'])
                and all(g in catalog and g != shared['group_id'] for g in shared['related_group_ids']),
                'Invalid related group ID: ' + question_id)
        require(nonempty_string(shared['kind']) and shared['kind'] in {'numbered', 'source-scenario'}
                and all(units[s]['kind'] == shared['kind'] for s in shared['source_ids']),
                'Canonical source-kind mismatch: ' + question_id)
        require((nonempty_string(shared['merge_rationale']) if len(shared['source_ids']) > 1 else shared['merge_rationale'] is None),
                'Invalid canonical merge rationale: ' + question_id)
        require(question_id == min(shared['source_ids']), 'Canonical ID must remain the lowest original stable ID')
        require(units[question_id]['group_id'] == shared['group_id'], 'Incorrect canonical home group: ' + question_id)
        related_groups = {units[s]['group_id'] for s in shared['source_ids']} - {shared['group_id']}
        require(set(shared['related_group_ids']) == related_groups, 'Incorrect related source groups: ' + question_id)
        require(shared['source_refs'] == [units[s]['source_ref'] for s in shared['source_ids']], 'Incorrect canonical source links')
        for source_id in shared['source_ids']:
            require(units[source_id]['canonical_id'] == question_id, 'Incorrect source alias mapping: ' + source_id)
            require(units[source_id]['group_id'] in catalog and units[source_id]['original_group_id'] in catalog,
                    'Incorrect source group mapping: ' + source_id)
        aliases += shared['source_ids']
        item = annotations[question_id]
        require(set(item) == {'question_id', 'phase', 'order', 'version_sensitive', 'en', 'vi'}, 'Invalid question metadata: ' + question_id)
        require(item['phase'] in PHASES and type(item['order']) is int and item['order'] >= 0, 'Invalid sequence: ' + question_id)
        require(type(item['version_sensitive']) is bool, 'Invalid version flag')
        localized_fields(item, TEXT_FIELDS, question_id)
        for lang in ('en', 'vi'):
            require(len(item[lang]['senior_signals']) == 2, 'Need two observable senior signals: ' + question_id)
            require(1 <= len(item[lang]['followups']) <= 2, 'Need one or two added follow-ups: ' + question_id)
            require(len(item[lang]['pitfalls']) >= 1, 'Need a question-specific pitfall')
    require(Counter(aliases) == Counter({s: 1 for s in units}), 'Every source must map exactly once')
    merges = index_rows(inventory['merge_sets'], 'canonical_id', 'merge record')
    require(set(merges) == {q for q, shared in canonical.items() if len(shared['source_ids']) > 1}, 'Merge report mismatch')
    for question_id, merge in merges.items():
        require(set(merge) == {'canonical_id', 'source_ids', 'rationale', 'rationale_vi'}
                and nonempty_string(merge['rationale']) and nonempty_string(merge['rationale_vi']),
                'Invalid bilingual merge rationale: ' + question_id)
        require(merge['source_ids'] == canonical[question_id]['source_ids'] and merge['rationale'] == canonical[question_id]['merge_rationale'],
                'Merge provenance mismatch: ' + question_id)
    group_map = index_rows(groups, 'group_id', 'group card')
    require(set(group_map) == {q['group_id'] for q in canonical.values()}, 'Group card coverage mismatch')
    for group_id, group in group_map.items():
        require(set(group) == {'group_id', 'representative_question_id', 'en', 'vi'}, 'Invalid group metadata')
        representative = group['representative_question_id']
        require(nonempty_string(representative) and representative in canonical and canonical[representative]['group_id'] == group_id,
                'Representative belongs to another group: ' + group_id)
        localized_fields(group, GROUP_FIELDS, group_id)
        for lang in ('en', 'vi'):
            require(2 <= len(group[lang]['competencies']) <= 4, 'Need 2–4 group competencies')
            require(set(group[lang]['rubric']) == RUBRIC_FIELDS, 'Invalid group rubric')
    validate_labels(root, catalog)
    return coverage_counts(units, canonical, merges, group_map, catalog)


def coverage_counts(units, canonical, merges, groups, catalog):
    return {'numbered_source_questions': sum(u['kind'] == 'numbered' for u in units.values()),
            'source_scenarios': sum(u['kind'] == 'source-scenario' for u in units.values()),
            'source_units': len(units), 'canonical_questions': len(canonical),
            'merge_sets': len(merges), 'groups': len(groups),
            'domains': len({catalog[g]['domain'] for g in groups}), 'unprocessed': 0}


def format_label(template, context, values):
    try:
        for _, field, spec, conversion in string.Formatter().parse(template):
            require(field is None or (field in values and not spec and conversion is None),
                    'Invalid placeholder in ' + context + ': ' + str(field))
        return template.format(**values)
    except ValueError as exc:
        raise ValueError('Invalid format template ' + context + ': ' + str(exc)) from exc


def validate_labels(root, catalog):
    labels = read(Path(root) / '_data/question_bank/labels.json')
    require(isinstance(labels, dict) and set(labels) == {'domains', 'en', 'vi'}, 'Invalid question-bank labels root')
    domains = labels['domains']
    require(isinstance(domains, dict) and set(domains) == {t['domain'] for t in catalog.values()},
            'Question-bank domain-label coverage mismatch')
    for domain, names in domains.items():
        require(isinstance(names, dict) and set(names) == {'en', 'vi'}
                and all(nonempty_string(v) for v in names.values()), 'Invalid bilingual domain label: ' + domain)
    required = {
        'back', 'level', 'boundary', 'representative', 'goal', 'prerequisites', 'no_prerequisites',
        'sequence', 'sequence_note', 'phases', 'source', 'scenario_id', 'version_note', 'original',
        'original_scenario', 'merge', 'guidance', 'explanation', 'intent', 'scope', 'senior_signals',
        'pitfalls', 'followups', 'scenario', 'rubric', 'basic', 'senior', 'evidence_missing', 'related',
        'curriculum', 'lesson', 'no_lesson', 'coverage', 'index_title', 'intro', 'counts', 'daily_title',
        'daily', 'prompt', 'domains_title', 'questions_count', 'audit_date', 'coverage_intro',
        'coverage_limits', 'numbered', 'source_scenarios', 'canonical_home', 'merge_title',
        'mapping_title', 'alias_note', 'canonical', 'group', 'scan_title', 'scan_note', 'document', 'role',
    }
    for language in ('en', 'vi'):
        content = labels.get(language)
        require(isinstance(content, dict) and set(content) == required, 'Invalid question-bank UI label fields: ' + language)
        for key, value in content.items():
            context = 'Question-bank label ' + language + '.' + key
            if key == 'phases':
                require(isinstance(value, dict) and set(value) == set(PHASES)
                        and all(nonempty_string(v) for v in value.values()), 'Invalid phase labels: ' + language)
            elif key == 'daily':
                strings(value, context)
            else:
                require(nonempty_string(value), 'Invalid text ' + context)
        format_label(content['counts'], language + '.counts', {key: 0 for key in COUNT_FIELDS})
        format_label(content['merge_title'], language + '.merge_title', {'merge_sets': 0})
        format_label(content['scan_note'], language + '.scan_note', {'document_count': 0})
        format_label(content['coverage_limits'], language + '.coverage_limits', {'catalog_topics': 0})
    require(len(labels['en']['daily']) == len(labels['vi']['daily']), 'Question-bank daily UI bilingual parity')
    return labels


def link(target, page):
    path, marker, anchor = target.partition('#')
    return os.path.relpath(ROOT / path, (ROOT / page).parent).replace(os.sep, '/') + (marker + anchor if marker else '')


def paragraph(value):
    return '<p>' + html.escape(value) + '</p>'


def bullets(values):
    return '<ul>\n' + '\n'.join('<li>' + html.escape(v) + '</li>' for v in values) + '\n</ul>'


def front(title, locale, key, **extra):
    values = dict(layout='default', title=title, locale=locale, translation_key=key, **extra)
    return '---\n' + yaml.safe_dump(values, allow_unicode=True, sort_keys=False).strip() + '\n---\n\n<!-- Generated by scripts/question_bank.py. Edit _data/question_bank/ instead. -->\n\n'


def render(root=ROOT):
    inventory, annotations, cards, catalog = load_bank(root)
    questions = {q['question_id']: q for q in annotations}
    groups = {g['group_id']: g for g in cards}
    units = {u['source_id']: u for u in inventory['source_units']}
    canonical = {q['question_id']: q for q in inventory['canonical_questions']}
    merges = {m['canonical_id']: m for m in inventory['merge_sets']}
    labels = validate_labels(root, catalog)
    report = coverage_counts(units, canonical, merges, groups, catalog)
    lessons = []
    for path in sorted((Path(root) / 'lessons').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        if text.startswith('---\n'):
            meta = yaml.safe_load(text.split('---', 2)[1])
            if meta.get('lesson_id'):
                lessons.append((path.relative_to(root).as_posix(), meta))
    output = {}
    ordered_groups = sorted(groups, key=lambda g: (list(labels['domains']).index(catalog[g]['domain']),
                                                   list(catalog).index(g)))
    for lang in ('en', 'vi'):
        t = labels[lang]
        prefix = '' if lang == 'en' else 'vi/'
        for gid in ordered_groups:
            page = prefix + 'questions/groups/' + gid + '.md'
            group, topic = groups[gid][lang], catalog[gid]
            qs = sorted((q for q in canonical.values() if q['group_id'] == gid),
                        key=lambda q: (PHASES.index(questions[q['question_id']]['phase']), questions[q['question_id']]['order'], q['question_id']))
            text = front(group['title'], lang, 'questions-' + gid, group_id=gid, domain=topic['domain'])
            text += '# ' + group['title'] + '\n\n'
            text += f'[{t["back"]}]({link(prefix + "questions/index.md", page)}) · `{gid}` · **{labels["domains"][topic["domain"]][lang]}** · {t["level"]}: {topic["level"]}\n\n'
            text += paragraph(t['boundary']) + '\n\n'
            representative = groups[gid]['representative_question_id']
            text += '## ' + t['representative'] + '\n\n'
            text += f'[{representative}](#{representative})\n\n' + paragraph(questions[representative][lang]['question']) + '\n\n'
            text += '## ' + t['goal'] + '\n\n' + paragraph(group['goal']) + '\n\n' + bullets(group['competencies']) + '\n\n'
            text += '**' + t['prerequisites'] + '**\n\n'
            if topic['prerequisites']:
                for dependency in topic['prerequisites']:
                    target = prefix + 'questions/groups/' + dependency + '.md' if dependency in groups else 'curriculum/domains/' + catalog[dependency]['domain'] + '.md#' + dependency
                    title = groups[dependency][lang]['title'] if dependency in groups else catalog[dependency]['title']
                    text += f'- [{title}]({link(target, page)})\n'
            else:
                text += t['no_prerequisites'] + '\n'
            text += '\n' + paragraph(group['bridge']) + '\n\n## ' + t['sequence'] + '\n\n'
            for phase in PHASES:
                members = [q for q in qs if questions[q['question_id']]['phase'] == phase]
                if members:
                    text += f'- **{t["phases"][phase]}:** ' + ' · '.join(f'[{q["question_id"]}](#{q["question_id"]})' for q in members) + '\n'
            text += '\n' + paragraph(t['sequence_note']) + '\n\n'
            for shared in qs:
                qid = shared['question_id']
                annotation = questions[qid]
                content = annotation[lang]
                text += f'<a id="{qid}"></a>\n\n### {qid} · {t["phases"][annotation["phase"]]}\n\n'
                for alias in shared['source_ids']:
                    if alias != qid:
                        text += f'<a id="{alias}"></a>\n\n'
                text += paragraph(content['question']) + '\n\n'
                text += '**' + t['source'] + ':** ' + ' · '.join(f'[{sid}]({link(units[sid]["source_ref"], page)})' for sid in shared['source_ids']) + '\n\n'
                if shared['kind'] == 'source-scenario':
                    text += paragraph(t['scenario_id']) + '\n\n'
                if annotation['version_sensitive']:
                    text += '<p class="scope-note">' + html.escape(t['version_note']) + '</p>\n\n'
                text += '<details markdown="1" class="question-original">\n<summary>' + t['original'] + '</summary>\n\n'
                for sid in shared['source_ids']:
                    text += f'**[{sid}]({link(units[sid]["source_ref"], page)})**\n\n'
                    if units[sid]['kind'] == 'numbered':
                        text += '<div lang="en" markdown="1">\n\n> ' + units[sid]['original'] + '\n\n</div>\n\n'
                    else:
                        text += t['original_scenario'] + '\n\n'
                if shared['merge_rationale']:
                    rationale = merges[qid]['rationale_vi'] if lang == 'vi' else shared['merge_rationale']
                    text += '**' + t['merge'] + ':** ' + html.escape(rationale) + '\n\n'
                text += '</details>\n\n<details markdown="1" class="question-guidance">\n<summary>' + t['guidance'] + '</summary>\n\n'
                for field in ('explanation', 'intent', 'scope'):
                    text += '**' + t[field] + '**\n\n' + paragraph(content[field]) + '\n\n'
                for field in ('senior_signals', 'pitfalls', 'followups'):
                    text += '**' + t[field] + '**\n\n' + bullets(content[field]) + '\n\n'
                text += '</details>\n\n'
            text += '## ' + t['scenario'] + '\n\n' + paragraph(group['scenario']) + '\n\n'
            text += '## ' + t['rubric'] + '\n\n'
            for level in ('basic', 'senior', 'evidence_missing'):
                text += '**' + t[level] + '**\n\n' + paragraph(group['rubric'][level]) + '\n\n'
            text += '## ' + t['related'] + '\n\n'
            text += f'- [{t["curriculum"]}]({link("curriculum/domains/" + topic["domain"] + ".md#" + gid, page)})\n'
            source_refs = sorted({ref for q in qs for ref in q['source_refs']})
            for path in sorted({ref.split('#')[0] for ref in source_refs}):
                text += f'- [{t["source"]}: {Path(path).stem}]({link(path, page)})\n'
            related_groups = sorted({g for q in qs for g in q['related_group_ids']})
            for related_gid in related_groups:
                text += f'- [{catalog[related_gid]["title"]}]({link("curriculum/domains/" + catalog[related_gid]["domain"] + ".md#" + related_gid, page)})\n'
            relevant_lessons = [(path, m) for path, m in lessons if m['topic_id'] == gid or set(m['source_refs']) & set(source_refs)]
            for path, meta in relevant_lessons:
                translated_path = prefix + path
                target = translated_path if (Path(root) / translated_path).exists() else path
                text += f'- [{t["lesson"]}: {meta["lesson_id"]}]({link(target, page)})\n'
            if not relevant_lessons:
                text += '- ' + t['no_lesson'] + '\n'
            text += f'\n[{t["coverage"]}]({link(prefix + "questions/coverage.md", page)})\n'
            output[page] = text
        page = prefix + 'questions/index.md'
        text = front(t['index_title'], lang, 'question-bank') + '# ' + t['index_title'] + '\n\n'
        text += paragraph(t['intro']) + '\n\n' + paragraph(format_label(t['counts'], lang + '.counts', report)) + '\n\n'
        text += f'[{t["coverage"]}](coverage.md) · [{t["curriculum"]}]({link(prefix + "curriculum/index.md", page)})\n\n'
        text += '## ' + t['daily_title'] + '\n\n'
        for action in t['daily']:
            text += '- ' + action + '\n'
        text += '\n> ' + t['prompt'] + '\n\n' + paragraph(t['boundary']) + '\n\n'
        text += '## ' + t['domains_title'] + '\n\n'
        for domain, names in labels['domains'].items():
            text += f'- [{names[lang]}](#{domain})\n'
        for domain, names in labels['domains'].items():
            text += f'\n<a id="{domain}"></a>\n\n## {names[lang]}\n\n'
            for gid in ordered_groups:
                if catalog[gid]['domain'] == domain:
                    count = sum(q['group_id'] == gid for q in canonical.values())
                    text += f'### [{groups[gid][lang]["title"]}](groups/{gid}.md)\n\n'
                    text += f'`{gid}` · {count} {t["questions_count"]} · {catalog[gid]["level"]}\n\n' + paragraph(groups[gid][lang]['goal']) + '\n\n'
        output[page] = text
        page = prefix + 'questions/coverage.md'
        text = front(t['coverage'], lang, 'question-coverage') + '# ' + t['coverage'] + '\n\n'
        text += f'[{t["back"]}](index.md) · {t["audit_date"]}: {inventory["audited_at"]}\n\n'
        text += paragraph(t['coverage_intro']) + '\n\n' + paragraph(format_label(t['counts'], lang + '.counts', report)) + '\n\n'
        text += paragraph(format_label(t['coverage_limits'], lang + '.coverage_limits', {'catalog_topics': len(catalog)})) + '\n\n'
        text += '| ' + t['source'] + ' | ' + t['numbered'] + ' | ' + t['source_scenarios'] + ' | ' + t['canonical_home'] + ' |\n|---|---:|---:|---:|\n'
        for source_path in sorted({u['source_ref'].split('#')[0] for u in units.values()}):
            source_members = [u for u in units.values() if u['source_ref'].split('#')[0] == source_path]
            prefix_id = source_members[0]['source_id'].split('-')[0]
            home_count = sum(q.startswith(prefix_id + '-') for q in canonical)
            text += f'| [{Path(source_path).stem}]({link(source_path, page)}) | {sum(u["kind"] == "numbered" for u in source_members)} | {sum(u["kind"] == "source-scenario" for u in source_members)} | {home_count} |\n'
        text += '\n## ' + format_label(t['merge_title'], lang + '.merge_title', {'merge_sets': len(merges)}) + '\n\n'
        for merge in inventory['merge_sets']:
            qid = merge['canonical_id']; target = prefix + 'questions/groups/' + canonical[qid]['group_id'] + '.md#' + qid
            rationale = merge['rationale_vi'] if lang == 'vi' else merge['rationale']
            text += f'- **[{qid}]({link(target, page)})** ← ' + ', '.join(merge['source_ids']) + ': ' + rationale + '\n'
        text += '\n## ' + t['mapping_title'] + '\n\n' + paragraph(t['alias_note']) + '\n\n'
        for source_path in sorted({u['source_ref'].split('#')[0] for u in units.values()}):
            text += '<details markdown="1">\n<summary>' + Path(source_path).stem + '</summary>\n\n'
            text += '| ' + t['source'] + ' | ' + t['canonical'] + ' | ' + t['group'] + ' |\n|---|---|---|\n'
            for sid, unit in sorted(units.items()):
                if unit['source_ref'].split('#')[0] != source_path:
                    continue
                qid = unit['canonical_id']; gid = canonical[qid]['group_id']
                target = prefix + 'questions/groups/' + gid + '.md#' + sid
                text += f'| [{sid}]({link(unit["source_ref"], page)}) | [{qid}]({link(target, page)}) | `{gid}` |\n'
            text += '\n</details>\n\n'
        text += '## ' + t['scan_title'] + '\n\n' + paragraph(format_label(t['scan_note'], lang + '.scan_note', {'document_count': len(inventory['documents'])})) + '\n\n'
        text += '| ' + t['document'] + ' | ' + t['role'] + ' |\n|---|---|\n'
        for document in inventory['documents']:
            path = document['path']
            internal = path == 'AGENTS.md' or path.startswith(('learning/', '_includes/'))
            display = '`' + path + '`' if internal else f'[{path}]({link(path, page)})'
            text += f'| {display} | {document["role"]} |\n'
        output[page] = text
    return {path: text.rstrip() + '\n' for path, text in output.items()}


def write_or_check(root=ROOT, check=False):
    root = Path(root)
    report = validate_bank(root)
    output = render(root)
    expected = set(output)
    actual = {p.relative_to(root).as_posix() for lang in ('', 'vi/') for p in (root / (lang + 'questions')).rglob('*.md')}
    require(not (actual - expected), 'Unexpected generated question page(s): ' + str(sorted(actual - expected)))
    for path, text in output.items():
        destination = root / path
        if check:
            require(destination.exists() and destination.read_text(encoding='utf-8') == text, 'Stale question page: ' + path)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding='utf-8')
            destination.chmod(0o644)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Read-only validation plus generated-page drift check')
    args = parser.parse_args()
    try:
        print(json.dumps(write_or_check(check=args.check), ensure_ascii=False))
    except ValueError as exc:
        parser.exit(1, 'Question bank validation failed: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
