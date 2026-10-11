"""Protect complete source coverage, bilingual contracts and side-effect-free rendering."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import question_bank

ROOT = Path(__file__).resolve().parents[1]


class QuestionBankContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('sources', '_data/question_bank', 'lessons', 'vi/lessons'):
            shutil.copytree(ROOT / directory, self.root / directory)
        (self.root / 'curriculum').mkdir()
        shutil.copyfile(ROOT / 'curriculum/catalog.json', self.root / 'curriculum/catalog.json')
        (self.root / 'learning').mkdir()
        shutil.copyfile(ROOT / 'learning/state.json', self.root / 'learning/state.json')
        self.inventory_path = self.root / '_data/question_bank/inventory.json'
        self.inventory = self.load(self.inventory_path)
        self.annotations_path = self.root / '_data/question_bank/questions/s02.json'
        self.groups_path = self.root / '_data/question_bank/groups/s02.json'

    def load(self, path):
        return json.loads(path.read_text(encoding='utf-8'))

    def save(self, path, data):
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def test_complete_bank_preserves_all_source_units_and_canonical_homes(self):
        report = question_bank.validate_bank(self.root)
        self.assertEqual(report, {
            'numbered_source_questions': 234, 'source_scenarios': 4,
            'source_units': 238, 'canonical_questions': 228,
            'merge_sets': 10, 'groups': 46, 'domains': 13, 'unprocessed': 0,
        })
        units = question_bank.source_units(self.root)
        # Existing scenario URLs are implicit heading anchors in the preserved files.
        self.assertEqual(units['S02-SC001']['source_ref'],
                         'sources/02-aspnet-api-ef.md#large-file-processing-scenario')
        self.assertEqual(units['S02-Q001']['original_group_id'], 'aspnet-request-pipeline')

    def test_dropped_source_mapping_is_rejected(self):
        self.inventory['source_units'].pop()
        self.save(self.inventory_path, self.inventory)
        with self.assertRaisesRegex(ValueError, 'Source coverage mismatch'):
            question_bank.validate_bank(self.root)

    def test_changed_source_body_is_rejected_even_if_prompt_lines_are_unchanged(self):
        source = self.root / 'sources/01-csharp-dotnet.md'
        source.write_text(source.read_text().replace('## Patterns\n', '## Patterns\n\n'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Preserved source file changed'):
            question_bank.validate_bank(self.root)

    def test_source_header_group_provenance_is_independent_of_snapshot_hash(self):
        unit = next(u for u in self.inventory['source_units'] if u['source_id'] == 'S02-Q001')
        unit['original_group_id'] = 'aspnet-http-contracts'
        self.save(self.inventory_path, self.inventory)
        with self.assertRaisesRegex(ValueError, 'Source text/anchor changed: S02-Q001'):
            question_bank.validate_bank(self.root)

    def test_merged_provenance_and_links_cannot_drift(self):
        for mutation in ('rationale', 'source_link'):
            inventory = copy.deepcopy(self.inventory)
            if mutation == 'rationale':
                inventory['merge_sets'][0]['rationale'] = 'An unrelated merge decision.'
                expected = 'Merge provenance mismatch'
            else:
                merged = next(q for q in inventory['canonical_questions'] if len(q['source_ids']) > 1)
                merged['source_refs'][1] = 'sources/02-aspnet-api-ef.md#q024'
                expected = 'Incorrect canonical source links'
            self.save(self.inventory_path, inventory)
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, expected):
                question_bank.validate_bank(self.root)

    def test_missing_empty_or_wrongly_typed_vietnamese_annotation_is_rejected(self):
        original = self.load(self.annotations_path)
        for mutation in ('missing', 'empty_object', 'blank_text', 'text_as_array',
                         'followups_as_string', 'empty_signals', 'short_followups'):
            annotations = copy.deepcopy(original)
            item = annotations[0]
            if mutation == 'missing':
                del item['vi']
            elif mutation == 'empty_object':
                item['vi'] = {}
            elif mutation == 'blank_text':
                item['vi']['scope'] = ' '
            elif mutation == 'text_as_array':
                item['vi']['question'] = ['Not a question text field.']
            elif mutation == 'followups_as_string':
                item['vi']['followups'] = 'Not an array of follow-up questions.'
            elif mutation == 'empty_signals':
                item['vi']['senior_signals'] = []
            else:
                item['vi']['followups'].pop()
            self.save(self.annotations_path, annotations)
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'S02-Q001'):
                question_bank.validate_bank(self.root)

    def test_group_rubric_shape_and_competency_parity_are_enforced(self):
        original = self.load(self.groups_path)
        for mutation in ('rubric_array', 'empty_rubric_value', 'missing_competency'):
            groups = copy.deepcopy(original)
            if mutation == 'rubric_array':
                groups[0]['vi']['rubric'] = ['Basic', 'Senior', 'Evidence']
            elif mutation == 'empty_rubric_value':
                groups[0]['vi']['rubric']['senior'] = ' '
            else:
                groups[0]['vi']['competencies'].pop()
            self.save(self.groups_path, groups)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                question_bank.validate_bank(self.root)

    def test_wrong_representative_or_wrong_type_has_clear_diagnostic(self):
        original = self.load(self.groups_path)
        wrong_member = next(q['question_id'] for q in self.inventory['canonical_questions']
                            if q['group_id'] != original[0]['group_id'])
        for value in (wrong_member, [original[0]['representative_question_id']]):
            groups = copy.deepcopy(original)
            groups[0]['representative_question_id'] = value
            self.save(self.groups_path, groups)
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'Representative belongs to another group'):
                question_bank.validate_bank(self.root)

    def test_duplicate_or_wrong_question_annotation_id_is_rejected(self):
        original = self.load(self.annotations_path)
        for mutation in ('duplicate', 'unknown'):
            annotations = copy.deepcopy(original)
            if mutation == 'duplicate':
                annotations.append(copy.deepcopy(annotations[0]))
                expected = 'Duplicate question annotation ID'
            else:
                annotations[0]['question_id'] = 'S02-Q999'
                expected = 'Question annotation coverage mismatch'
            self.save(self.annotations_path, annotations)
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, expected):
                question_bank.validate_bank(self.root)

    def test_alias_mapping_and_unique_source_membership_are_enforced(self):
        for mutation in ('wrong_home', 'duplicate_member', 'unknown_member', 'related_group'):
            inventory = copy.deepcopy(self.inventory)
            if mutation == 'wrong_home':
                alias = next(u for u in inventory['source_units'] if u['source_id'] == 'S02-Q025')
                alias['canonical_id'] = 'S02-Q024'
                expected = 'Incorrect source alias mapping'
            elif mutation == 'related_group':
                merged = next(q for q in inventory['canonical_questions'] if q['question_id'] == 'S05-Q027')
                merged['related_group_ids'] = []
                expected = 'Incorrect related source groups'
            else:
                merged = next(q for q in inventory['canonical_questions'] if len(q['source_ids']) > 1)
                merged['source_ids'].append(merged['source_ids'][0] if mutation == 'duplicate_member' else 'S99-Q999')
                expected = 'Canonical source IDs must be unique' if mutation == 'duplicate_member' else 'Unknown canonical source ID'
            self.save(self.inventory_path, inventory)
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, expected):
                question_bank.validate_bank(self.root)

    def test_unsupported_numbered_source_format_cannot_be_silently_skipped(self):
        source = self.root / 'sources/01-csharp-dotnet.md'
        source.write_text(source.read_text() + '\n<a id="q999"></a>\nS01-Q999 · a new format\n\nExplain a new invariant.\n', encoding='utf-8')
        # Exercise parsing directly: a file-hash guard must not hide this defect.
        with self.assertRaisesRegex(ValueError, 'Unsupported numbered source format'):
            question_bank.source_units(self.root)

    def test_unnumbered_prompt_without_question_mark_requires_classification(self):
        source = self.root / 'sources/01-csharp-dotnet.md'
        source.write_text(source.read_text() + '\nExplain a new production invariant.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unclassified source content'):
            question_bank.source_units(self.root)

    def test_unnumbered_prompt_as_a_heading_also_requires_classification(self):
        source = self.root / 'sources/01-csharp-dotnet.md'
        source.write_text(source.read_text() + '\n## Explain a new production invariant.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unclassified source content'):
            question_bank.source_units(self.root)

    def test_new_supported_source_unit_requires_inventory_registration(self):
        source = self.root / 'sources/01-csharp-dotnet.md'
        source.write_text(source.read_text() + '\n<a id="q999"></a>\n**S01-Q999** · original question 999 · [Type semantics](../curriculum/domains/dotnet-runtime.md#dotnet-type-semantics)\n\nExplain a new invariant.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Source coverage mismatch'):
            question_bank.validate_bank(self.root)

    def test_annotation_array_and_ui_label_schema_have_clear_errors(self):
        original_annotations = self.load(self.annotations_path)
        self.save(self.annotations_path, {'questions': original_annotations})
        with self.assertRaisesRegex(ValueError, 'expected an array'):
            question_bank.validate_bank(self.root)
        self.save(self.annotations_path, original_annotations)
        labels_path = self.root / '_data/question_bank/labels.json'
        labels = self.load(labels_path)
        labels['vi']['phases']['production'] = ' '
        self.save(labels_path, labels)
        with self.assertRaisesRegex(ValueError, 'Invalid phase labels: vi'):
            question_bank.validate_bank(self.root)

    def test_rendered_aliases_and_vietnamese_merge_rationale_preserve_identity(self):
        pages = question_bank.render(self.root)
        en = pages['questions/groups/ef-query-execution.md']
        vi = pages['vi/questions/groups/ef-query-execution.md']
        for page in (en, vi):
            self.assertIn('<a id="S01-Q010"></a>', page)
            self.assertIn('<a id="S02-Q025"></a>', page)
            self.assertIn('sources/02-aspnet-api-ef.md#q025', page)
        merge = next(m for m in self.inventory['merge_sets'] if m['canonical_id'] == 'S01-Q010')
        self.assertIn(merge['rationale'], en)
        self.assertIn(merge['rationale_vi'], vi)
        self.assertNotIn(merge['rationale'], vi)
        self.assertIn('<div lang="en" markdown="1">', vi)
        self.assertIn(merge['rationale_vi'], pages['vi/questions/coverage.md'])

    def test_missing_vietnamese_merge_rationale_is_rejected(self):
        self.inventory['merge_sets'][0]['rationale_vi'] = ' '
        self.save(self.inventory_path, self.inventory)
        with self.assertRaisesRegex(ValueError, 'Invalid bilingual merge rationale'):
            question_bank.validate_bank(self.root)

    def test_counts_and_catalog_size_are_derived_not_frozen_ui_text(self):
        catalog_path = self.root / 'curriculum/catalog.json'
        catalog = self.load(catalog_path)
        extra = copy.deepcopy(catalog['topics'][0])
        extra['topic_id'] = 'derived-test-extension'
        catalog['topics'].append(extra)
        self.save(catalog_path, catalog)
        pages = question_bank.render(self.root)
        for path in ('questions/coverage.md', 'vi/questions/coverage.md'):
            self.assertNotIn('{merge_sets}', pages[path])
            self.assertNotIn('{catalog_topics}', pages[path])
            self.assertIn(str(len(catalog['topics'])), pages[path])
        self.assertIn('238 source units', pages['questions/index.md'])
        self.assertIn('238 đơn vị nguồn', pages['vi/questions/index.md'])

    def test_unknown_count_placeholders_have_a_clear_diagnostic(self):
        path = self.root / '_data/question_bank/labels.json'
        labels = self.load(path)
        labels['vi']['counts'] = '{invented_count} đơn vị nguồn.'
        self.save(path, labels)
        with self.assertRaisesRegex(ValueError, 'Invalid placeholder.*invented_count'):
            question_bank.validate_bank(self.root)

    def test_generated_page_drift_and_unexpected_pages_are_rejected(self):
        question_bank.write_or_check(self.root)
        page = self.root / 'vi/questions/groups/aspnet-request-pipeline.md'
        page.write_text(page.read_text() + '\nUntracked editorial change.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Stale question page: vi/questions/groups/aspnet-request-pipeline.md'):
            question_bank.write_or_check(self.root, check=True)
        question_bank.write_or_check(self.root)
        unexpected = self.root / 'questions/unregistered.md'
        unexpected.write_text('An unregistered question page.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unexpected generated question page'):
            question_bank.write_or_check(self.root)

    def test_check_is_read_only_and_rendering_never_writes_learning_state(self):
        state = self.root / 'learning/state.json'
        original_state = state.read_bytes()
        original_mtime = state.stat().st_mtime_ns
        original_write = Path.write_text
        writes = []

        def observed_write(path, *args, **kwargs):
            relative = path.relative_to(self.root).as_posix()
            self.assertTrue(relative.startswith(('questions/', 'vi/questions/')), relative)
            writes.append(relative)
            return original_write(path, *args, **kwargs)

        with mock.patch.object(Path, 'write_text', autospec=True, side_effect=observed_write):
            question_bank.render(self.root)
            self.assertEqual(writes, [])
            with self.assertRaisesRegex(ValueError, 'Stale question page'):
                question_bank.write_or_check(self.root, check=True)
            self.assertEqual(writes, [])
            question_bank.write_or_check(self.root)
            self.assertEqual(len(writes), 96)
            before_check = list(writes)
            question_bank.write_or_check(self.root, check=True)
            self.assertEqual(writes, before_check)
        self.assertEqual(state.read_bytes(), original_state)
        self.assertEqual(state.stat().st_mtime_ns, original_mtime)


if __name__ == '__main__':
    unittest.main()
