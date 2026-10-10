import contextlib
from copy import deepcopy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import learning


def topic(topic_id="topic-a", domain="dotnet-runtime", prerequisites=None):
    return {
        "topic_id": topic_id, "title": topic_id, "domain": domain,
        "level": "foundation", "ring": "A", "prerequisites": prerequisites or [],
        "objectives": [f"Explain {topic_id}.", f"Apply {topic_id}."],
        "concept_fingerprint": [topic_id, "failure", "evidence"],
        "source_refs": ["sources/example.md#question"],
    }


class LearningWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for directory in ("learning", "curriculum", "lessons"):
            (self.root / directory).mkdir()
        schema = learning.load_json(learning.ROOT / "learning/state.schema.json")
        self.write_json("learning/state.schema.json", schema)
        self.state = learning.load_json(learning.ROOT / "agent/LEARNING_STATE_TEMPLATE.json")
        self.write_json("learning/state.json", self.state)
        self.catalog = {"schema_version": 1, "topics": [topic(), topic("topic-b", "sql-data", ["topic-a"])]}
        self.write_json("curriculum/catalog.json", self.catalog)
        meta = deepcopy(self.catalog["topics"][0])
        meta.pop("prerequisites")
        meta.pop("ring")
        meta.update(lesson_id="2026-10-08-topic-a", created_at="2026-10-08", status="generated", mode="full-lesson")
        self.lesson = self.root / "lessons/2026-10-08-topic-a.md"
        self.lesson.write_text("---\n" + yaml.safe_dump(meta) + "---\nA real lesson body.\n")
        self.patcher = patch.object(learning, "ROOT", self.root)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temporary.cleanup()

    def write_json(self, path, data):
        (self.root / path).write_text(json.dumps(data))

    def run_cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()):
            learning.main(["--state", str(self.root / "learning/state.json"), *args])
        return learning.load_json(self.root / "learning/state.json")

    def record(self):
        return self.run_cli("record", "--lesson", str(self.lesson), "--date", "2026-10-08")

    def evidence(self):
        path = self.root / "learner-attempt.md"
        path.write_text("I explain the commit/acknowledgment gap and tested a concurrent retry.")
        return str(path)

    def translated_lesson(self, **overrides):
        meta = learning.metadata(self.lesson)
        translated = {
            'locale': 'vi', 'translation_key': meta['lesson_id'],
            'lesson_id': meta['lesson_id'], 'topic_id': meta['topic_id'],
            'canonical_lesson': self.lesson.relative_to(self.root).as_posix(),
            **overrides,
        }
        path = self.root / 'vi/lessons' / self.lesson.name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('---\n' + yaml.safe_dump(translated) + '---\nBài học.\n')
        return path

    def read_cli(self, *args):
        before = (self.root / 'learning/state.json').read_bytes()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            learning.main(['--state', str(self.root / 'learning/state.json'), *args])
        self.assertEqual(before, (self.root / 'learning/state.json').read_bytes())
        return json.loads(output.getvalue())

    def test_language_change_preserves_evidence_assessment_and_review_history(self):
        self.record()
        self.write_json('assessment.json', {'score': dict.fromkeys(learning.DIMENSIONS, 3),
                                         'weak_points': ['Explain the failure window.']})
        self.run_cli('complete', '2026-10-08-topic-a', '--date', '2026-10-09',
                     '--evidence', self.evidence(), '--assessment', str(self.root / 'assessment.json'))
        old = self.run_cli('review', '2026-10-08-topic-a', '--date', '2026-10-10', '--evidence', self.evidence())
        new = self.run_cli('language', '--language', 'vi', '--date', '2026-10-11')
        expected = deepcopy(old)
        expected['learner_profile']['preferred_language'] = 'vi'
        expected['last_updated'] = '2026-10-11'
        self.assertEqual(new, expected)

    def test_optional_preference_is_compatible_and_explicit_next_override_is_read_only(self):
        learning.validate_state(self.state)
        default = self.read_cli('next', '--date', '2026-10-08')
        self.assertEqual(default['language'], 'en')
        self.run_cli('language', '--language', 'vi', '--date', '2026-10-08')
        preferred = self.read_cli('next', '--date', '2026-10-09')
        explicit = self.read_cli('next', '--language', 'en', '--date', '2026-10-09')
        self.assertEqual(preferred['language'], 'vi')
        self.assertEqual(explicit['language'], 'en')
        self.assertEqual(preferred['candidate'], explicit['candidate'])
        invalid = deepcopy(self.state)
        invalid['learner_profile']['preferred_language'] = 'fr'
        from jsonschema.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            learning.validate_state(invalid)

    def test_lesson_path_switch_and_missing_translation_keep_same_id_read_only(self):
        self.record()
        fallback = self.read_cli('lesson-path', '2026-10-08-topic-a', '--language', 'vi', '--date', '2026-10-09')
        self.assertTrue(fallback['fallback'])
        self.assertEqual(fallback['language'], 'en')
        self.assertEqual(fallback['lesson_path'], self.lesson.relative_to(self.root).as_posix())
        vi = self.translated_lesson()
        mapped = self.read_cli('lesson-path', '2026-10-08-topic-a', '--language', 'vi', '--date', '2026-10-09')
        self.assertFalse(mapped['fallback'])
        self.assertEqual(mapped['lesson_id'], fallback['lesson_id'])
        self.assertEqual(mapped['lesson_path'], vi.relative_to(self.root).as_posix())

    def test_recording_translation_registers_canonical_metadata_once(self):
        vi = self.translated_lesson(title='Tiêu đề khác, cùng bài học')
        state = self.run_cli('record', '--lesson', str(vi), '--date', '2026-10-08')
        self.assertEqual(len(state['lessons']), 1)
        item = state['lessons'][0]
        self.assertEqual(item['lesson_path'], self.lesson.relative_to(self.root).as_posix())
        self.assertEqual(item['concept_fingerprint'], self.catalog['topics'][0]['concept_fingerprint'])
        before = (self.root / 'learning/state.json').read_bytes()
        for path in (self.lesson, vi):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'already delivered'):
                self.run_cli('record', '--lesson', str(path), '--date', '2026-10-08')
            self.assertEqual(before, (self.root / 'learning/state.json').read_bytes())
        self.assertIsNone(item['completed_at'])
        self.assertEqual(item['review_due'], [])

    def test_translation_cannot_override_identity_or_shared_contract(self):
        before = (self.root / 'learning/state.json').read_bytes()
        for override in ({'topic_id': 'other'}, {'lesson_id': 'another-id'},
                         {'concept_fingerprint': ['translated-title']}, {'created_at': '2026-10-09'},
                         {'canonical_lesson': 'vi/lessons/2026-10-08-topic-a.md'}, {'locale': 'fr'}):
            with self.subTest(override=override), self.assertRaises(ValueError):
                self.run_cli('record', '--lesson', str(self.translated_lesson(**override)), '--date', '2026-10-08')
            self.assertEqual(before, (self.root / 'learning/state.json').read_bytes())

    def test_delivery_is_pending_and_blocks_redelivery(self):
        state = self.record()
        entry = state["lessons"][0]
        self.assertEqual(entry["status"], "generated")
        self.assertIsNone(entry["completed_at"])
        self.assertEqual(entry["review_due"], [])
        self.assertTrue(all(value is None for value in entry["score"].values()))
        with self.assertRaisesRegex(ValueError, "already delivered"):
            self.record()

    def test_pending_prerequisite_does_not_unlock_topic(self):
        state = self.record()
        result = learning.select_next(self.catalog, state, "2026-10-09")
        self.assertIsNone(result["candidate"])
        self.assertEqual(result["pending_lessons"], ["2026-10-08-topic-a"])

    def test_complete_and_review_require_actual_evidence(self):
        self.record()
        self.run_cli("start", "2026-10-08-topic-a", "--date", "2026-10-08")
        empty = self.root / "empty.md"
        empty.write_text(" ")
        before = (self.root / "learning/state.json").read_text()
        with self.assertRaisesRegex(ValueError, "nonempty"):
            self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", str(empty))
        self.assertEqual(before, (self.root / "learning/state.json").read_text())
        state = self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        item = state["lessons"][0]
        self.assertEqual(item["completed_at"], "2026-10-09")
        self.assertEqual(item["review_due"], ["2026-10-10", "2026-10-12", "2026-10-16", "2026-10-23", "2026-11-08"])
        self.assertTrue(all(value is None for value in item["score"].values()))
        self.assertEqual(learning.select_next(self.catalog, state, "2026-10-10")["candidate"]["topic_id"], "topic-b")
        with self.assertRaisesRegex(ValueError, "No scheduled review"):
            self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        reviewed = self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-16", "--evidence", self.evidence())
        self.assertEqual(len(reviewed["lessons"]), 1)
        self.assertEqual(reviewed["reviews"][0]["scheduled_for"], "2026-10-10")
        self.assertEqual(len(learning.due_reviews(reviewed, "2026-10-16")), 2)

    def test_no_fabricated_completion_or_restart(self):
        self.record()
        with self.assertRaisesRegex(ValueError, "Complete the lesson"):
            self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        with self.assertRaisesRegex(ValueError, "Already completed"):
            self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-10", "--evidence", self.evidence())
        with self.assertRaisesRegex(ValueError, "must be reviewed"):
            self.run_cli("start", "2026-10-08-topic-a", "--date", "2026-10-10")

    def test_selection_excludes_retitle_and_rotates_domains(self):
        state = self.record()
        renamed = topic("renamed")
        renamed["concept_fingerprint"] = state["lessons"][0]["concept_fingerprint"]
        repeated = topic("same-objective")
        repeated["objectives"][0] = state["lessons"][0]["objectives"][0].upper()
        catalog = {"topics": [renamed, repeated, topic("dotnet-new"), topic("sql-new", "sql-data")]}
        result = learning.select_next(catalog, state, "2026-10-09")
        self.assertEqual(result["candidate"]["topic_id"], "sql-new")
        self.assertEqual(result["alternatives"], ["dotnet-new"])

    def test_invalid_score_and_backdated_action_do_not_write(self):
        self.record()
        self.write_json("invalid-assessment.json", {"score": dict.fromkeys(learning.DIMENSIONS, True)})
        before = (self.root / "learning/state.json").read_text()
        with self.assertRaisesRegex(ValueError, "integers"):
            self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence(), "--assessment", str(self.root / "invalid-assessment.json"))
        with self.assertRaisesRegex(ValueError, "precedes"):
            self.run_cli("start", "2026-10-08-topic-a", "--date", "2026-10-07")
        self.assertEqual(before, (self.root / "learning/state.json").read_text())

    def test_invalid_state_is_not_written(self):
        state = self.record()
        state["lessons"][0]["completed_at"] = "2026-10-09"
        before = (self.root / "learning/state.json").read_text()
        with self.assertRaises(Exception):
            learning.save_state(self.root / "learning/state.json", state)
        self.assertEqual(before, (self.root / "learning/state.json").read_text())

    def test_noncanonical_dates_are_rejected(self):
        for day in ("20261008", "2026-W41-4"):
            with self.subTest(day=day), self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                self.run_cli("next", "--date", day)

    def test_record_rejects_retitle_fingerprint_or_objective(self):
        self.record()
        for repeated_key in ("concept_fingerprint", "objectives"):
            with self.subTest(key=repeated_key):
                duplicate = topic("retitled")
                duplicate[repeated_key] = self.catalog["topics"][0][repeated_key]
                self.write_json("curriculum/catalog.json", {"schema_version": 1, "topics": [*self.catalog["topics"], duplicate]})
                duplicate.update(lesson_id="2026-10-09-retitled", created_at="2026-10-09", status="generated", mode="full-lesson")
                path = self.root / "lessons/2026-10-09-retitled.md"
                path.write_text("---\n" + yaml.safe_dump(duplicate) + "---\nA lesson.\n")
                with self.assertRaisesRegex(ValueError, "already delivered"):
                    self.run_cli("record", "--lesson", str(path), "--date", "2026-10-09")

    def test_review_slots_unique_and_not_early(self):
        self.record()
        self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        state = self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-10", "--evidence", self.evidence())
        duplicate = deepcopy(state["reviews"][0])
        duplicate["review_id"] = "different-id-same-slot"
        state["reviews"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "Duplicate lesson/review"):
            learning.validate_state(state)
        state["reviews"].pop()
        state["reviews"][0]["reviewed_at"] = "2026-10-09"
        with self.assertRaisesRegex(ValueError, "scheduled interval"):
            learning.validate_state(state)

    def test_evidenced_review_adjustment_preserves_history_and_due_flow(self):
        self.record()
        completed = self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        reviewed = self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-10", "--evidence", self.evidence())
        state = self.run_cli("reschedule", "2026-10-08-topic-a", "--date", "2026-10-10",
                             "--from-date", "2026-10-12", "--to-date", "2026-10-11",
                             "--reason", "Recall missed the failure boundary; retry sooner.", "--evidence", self.evidence())
        self.assertEqual(state["lessons"][0]["completed_at"], completed["lessons"][0]["completed_at"])
        self.assertEqual(state["reviews"], reviewed["reviews"])
        self.assertEqual(len(state["lessons"]), 1)
        self.assertEqual(state["lessons"][0]["score"], completed["lessons"][0]["score"])
        self.assertEqual(learning.due_reviews(state, "2026-10-11"), [{"lesson_id": "2026-10-08-topic-a", "scheduled_for": "2026-10-11"}])
        state = self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-11", "--evidence", self.evidence())
        self.assertEqual(len(state["reviews"]), 2)
        self.assertEqual(state["reviews"][-1]["scheduled_for"], "2026-10-11")
        learning.validate_state(state)

    def test_review_adjustments_reject_invalid_changes_without_writing(self):
        self.record()
        self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-10", "--evidence", self.evidence())
        before = (self.root / "learning/state.json").read_text()
        cases = [("2026-10-10", "2026-10-11", "performed"),
                 ("2026-10-12", "2026-10-16", "distinct"),
                 ("2026-10-12", "2026-10-09", "today or later"),
                 ("2026-10-20", "2026-10-11", "planned interval")]
        for old, new, error in cases:
            with self.subTest(old=old, new=new), self.assertRaisesRegex(ValueError, error):
                self.run_cli("reschedule", "2026-10-08-topic-a", "--date", "2026-10-10",
                             "--from-date", old, "--to-date", new, "--reason", "Observed recall gap", "--evidence", self.evidence())
            self.assertEqual(before, (self.root / "learning/state.json").read_text())
        empty = self.root / "no-attempt.md"
        empty.write_text(" ")
        with self.assertRaisesRegex(ValueError, "nonempty"):
            self.run_cli("reschedule", "2026-10-08-topic-a", "--date", "2026-10-10",
                         "--from-date", "2026-10-12", "--to-date", "2026-10-11", "--reason", "Earlier", "--evidence", str(empty))
        with self.assertRaisesRegex(ValueError, "reason"):
            self.run_cli("reschedule", "2026-10-08-topic-a", "--date", "2026-10-10",
                         "--from-date", "2026-10-12", "--to-date", "2026-10-11", "--reason", " ", "--evidence", self.evidence())
        self.assertEqual(before, (self.root / "learning/state.json").read_text())

    def test_reusing_a_vacated_date_does_not_invalidate_later_reviews(self):
        self.record()
        self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        for old, new in (("2026-10-12", "2026-10-11"), ("2026-10-16", "2026-10-12")):
            self.run_cli("reschedule", "2026-10-08-topic-a", "--date", "2026-10-10",
                         "--from-date", old, "--to-date", new, "--reason", "Observed recall evidence", "--evidence", self.evidence())
        for day in ("2026-10-10", "2026-10-11", "2026-10-12"):
            state = self.run_cli("review", "2026-10-08-topic-a", "--date", day, "--evidence", self.evidence())
        self.assertEqual([r["scheduled_for"] for r in state["reviews"]], ["2026-10-10", "2026-10-11", "2026-10-12"])
        self.assertEqual(len(state["lessons"]), 1)
        self.assertEqual([c["review_count"] for c in state["review_adjustments"]], [0, 0])
        learning.validate_state(state)
        # Older v2 adjustments with date-only ordering remain readable.
        for change in state["review_adjustments"]:
            del change["review_count"]
        learning.validate_state(state)

    def test_same_day_adjustment_before_review_preserves_operation_order(self):
        self.record()
        self.run_cli("complete", "2026-10-08-topic-a", "--date", "2026-10-09", "--evidence", self.evidence())
        for old, new in (("2026-10-10", "2026-10-11"), ("2026-10-12", "2026-10-10")):
            self.run_cli("reschedule", "2026-10-08-topic-a", "--date", "2026-10-10",
                         "--from-date", old, "--to-date", new, "--reason", "Observed attempt justifies timing", "--evidence", self.evidence())
        state = self.run_cli("review", "2026-10-08-topic-a", "--date", "2026-10-10", "--evidence", self.evidence())
        self.assertEqual(state["reviews"][0]["scheduled_for"], "2026-10-10")
        learning.validate_state(state)
        before = (self.root / "learning/state.json").read_text()
        with self.assertRaisesRegex(ValueError, "performed"):
            self.run_cli("reschedule", "2026-10-08-topic-a", "--date", "2026-10-10",
                         "--from-date", "2026-10-10", "--to-date", "2026-10-13", "--reason", "Cannot rewrite an actual review", "--evidence", self.evidence())
        self.assertEqual(before, (self.root / "learning/state.json").read_text())
        state["review_adjustments"][0]["review_count"] = 2
        with self.assertRaisesRegex(ValueError, "recorded review order"):
            learning.validate_state(state)


if __name__ == "__main__":
    unittest.main()
