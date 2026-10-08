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


if __name__ == "__main__":
    unittest.main()
