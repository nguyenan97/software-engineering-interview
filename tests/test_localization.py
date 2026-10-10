"""Reject realistic translation drift before it changes routing or lab behavior."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from localization import validate_localization

ROOT = Path(__file__).resolve().parents[1]


class LocalizationContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copy(ROOT / '_config.yml', self.root / '_config.yml')
        shutil.copytree(ROOT / '_data', self.root / '_data')
        name = '2026-10-08-messaging-idempotent-consumer.md'
        for directory in ('lessons', 'vi/lessons'):
            (self.root / directory).mkdir(parents=True)
            shutil.copy(ROOT / directory / name, self.root / directory / name)
        self.en = self.root / 'lessons' / name
        self.vi = self.root / 'vi/lessons' / name

    def tearDown(self):
        self.temp.cleanup()

    def edit_meta(self, path, **values):
        _, header, body = path.read_text().split('---', 2)
        meta = yaml.safe_load(header)
        meta.update(values)
        path.write_text('---\n' + yaml.safe_dump(meta, allow_unicode=True) + '---' + body)

    def test_paired_lesson_is_one_group_not_two_deliveries(self):
        result = validate_localization(self.root)
        self.assertEqual(result['groups'], 1)
        self.assertEqual(result['translated_lessons'], 1)

    def test_missing_extra_empty_or_nonstring_ui_values_are_rejected(self):
        path = self.root / '_data/i18n/vi.yml'
        original = path.read_text()
        for mutation in ('missing', 'extra', 'empty', 'nonstring'):
            data = yaml.safe_load(original)
            if mutation == 'missing':
                del data['messages']['resume']
            elif mutation == 'extra':
                data['unexpected'] = 'A key with no English counterpart'
            elif mutation == 'empty':
                data['messages']['resume'] = ' '
            else:
                data['messages']['resume'] = 4
            path.write_text(yaml.safe_dump(data, allow_unicode=True))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_localization(self.root)

    def test_unsupported_locale_or_missing_group_is_rejected(self):
        original = self.vi.read_text()
        for values in ({'locale': 'fr'}, {'translation_key': None}):
            self.vi.write_text(original)
            self.edit_meta(self.vi, **values)
            with self.subTest(values=values), self.assertRaises(ValueError):
                validate_localization(self.root)

    def test_duplicate_group_and_orphan_translation_are_rejected(self):
        duplicate = self.vi.with_name('duplicate.md')
        shutil.copy(self.vi, duplicate)
        with self.assertRaisesRegex(ValueError, 'Duplicate locale'):
            validate_localization(self.root)
        duplicate.unlink()
        self.en.unlink()
        with self.assertRaises(OSError):
            validate_localization(self.root)

    def test_code_answer_and_step_drift_are_rejected(self):
        original = self.vi.read_text()
        cases = [original.replace('lab-code/atomic-inbox-solution.md', 'lab-code/wrong-solution.md'),
                 original.replace('interview/inbox-30s.md', 'interview/wrong-answer.md'),
                 original.replace('python labs/atomic-inbox/verify.py --solution', 'python labs/atomic-inbox/verify.py --exercise'),
                 original.replace('{: #practice }', '{: #thuc-hanh }')]
        for text in cases:
            self.assertNotEqual(text, original)
            self.vi.write_text(text)
            with self.subTest(text=text[:30]), self.assertRaises(ValueError):
                validate_localization(self.root)

    def test_translation_cannot_override_canonical_duration_or_fingerprint(self):
        original = self.vi.read_text()
        for values in ({'duration_minutes': 15}, {'concept_fingerprint': ['another-concept']},
                       {'canonical_lesson': '../outside.md'}):
            self.vi.write_text(original)
            self.edit_meta(self.vi, **values)
            with self.subTest(values=values), self.assertRaises(ValueError):
                validate_localization(self.root)

    def test_english_only_page_is_valid_without_inventing_a_route(self):
        (self.root / 'guide.md').write_text('---\nlayout: default\nlocale: en\ntitle: English guide\n---\nGuide.\n')
        self.assertEqual(validate_localization(self.root)['groups'], 1)


if __name__ == '__main__':
    unittest.main()
