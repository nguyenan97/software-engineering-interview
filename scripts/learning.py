#!/usr/bin/env python3
"""Durable lesson bookkeeping; an agent supplies teaching and semantic review."""
import argparse
from datetime import date, timedelta
import json
import os
from pathlib import Path
import tempfile

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError
import yaml

ROOT = Path(__file__).resolve().parents[1]
OFFSETS = (1, 3, 7, 14, 30)
DIMENSIONS = ("technical", "reasoning", "implementation", "operations", "communication")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_state(state):
    schema = load_json(ROOT / "learning/state.schema.json")
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(state)
    ids = [item["lesson_id"] for item in state["lessons"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate lesson_id in learning state")
    topics = [item["topic_id"] for item in state["lessons"]]
    fingerprints = [frozenset(item["concept_fingerprint"]) for item in state["lessons"]]
    if len(topics) != len(set(topics)) or len(fingerprints) != len(set(fingerprints)):
        raise ValueError("Duplicate delivered topic or fingerprint in learning state")
    review_ids = [item["review_id"] for item in state["reviews"]]
    if len(review_ids) != len(set(review_ids)):
        raise ValueError("Duplicate review_id in learning state")
    review_slots = [(r["lesson_id"], r["scheduled_for"]) for r in state["reviews"]]
    if len(review_slots) != len(set(review_slots)):
        raise ValueError("Duplicate lesson/review interval in learning state")
    lessons = {item["lesson_id"]: item for item in state["lessons"]}
    plans = {key: review_dates(item["completed_at"]) if item["completed_at"] else []
             for key, item in lessons.items()}
    previous_adjustment = None
    for change in state.get("review_adjustments", []):
        parent = lessons.get(change["lesson_id"])
        if not parent or parent["status"] != "completed":
            raise ValueError("Review adjustments require a completed lesson")
        if (change["adjusted_at"] < parent["completed_at"] or
                (previous_adjustment and change["adjusted_at"] < previous_adjustment) or
                not state["last_updated"] or change["adjusted_at"] > state["last_updated"]):
            raise ValueError("Review adjustment dates must preserve chronology")
        previous_adjustment = change["adjusted_at"]
        plan = plans[change["lesson_id"]]
        if change["from_due"] not in plan:
            raise ValueError("Review adjustment must reference a planned interval")
        if (change["lesson_id"], change["from_due"]) in review_slots:
            raise ValueError("Cannot reschedule a performed review")
        if change["to_due"] < change["adjusted_at"] or change["to_due"] in plan:
            raise ValueError("New review date must be today or later and distinct")
        if not change["reason"].strip():
            raise ValueError("Review adjustment needs a reason")
        plan[plan.index(change["from_due"])] = change["to_due"]
        plan.sort()
    for item in state["lessons"]:
        if item["completed_at"] and item["completed_at"] < item["created_at"]:
            raise ValueError("Completion precedes creation")
        expected = plans[item["lesson_id"]]
        if item["review_due"] != expected:
            raise ValueError("Review dates must follow completion and audited adjustments")
        if any(value is not None for value in item["score"].values()) and not item["evidence"]:
            raise ValueError("Scores require learner evidence")
    for review in state["reviews"]:
        parent = lessons.get(review["lesson_id"])
        if not parent or parent["status"] != "completed":
            raise ValueError("Reviews must reference completed lessons")
        if review["reviewed_at"] < parent["completed_at"]:
            raise ValueError("Review precedes completion")
        if review["reviewed_at"] < review["scheduled_for"]:
            raise ValueError("Review precedes its scheduled interval")
        if review["scheduled_for"] not in parent["review_due"]:
            raise ValueError("Review must reference a planned review date")


def review_dates(completed_at):
    day = date.fromisoformat(completed_at)
    return [(day + timedelta(days=n)).isoformat() for n in OFFSETS]


def save_state(path, state):
    validate_state(state)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Atomic replacement protects against partial writes, not concurrent agents.
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as f:
        temporary = f.name
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")
    try:
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def metadata(path):
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("Lesson requires YAML front matter")
    return yaml.safe_load(text.split("---", 2)[1])


def null_scores():
    return dict.fromkeys(DIMENSIONS)


def assessment(path):
    if not path:
        return null_scores(), []
    data = load_json(path)
    scores = data.get("score", {})
    if set(scores) != set(DIMENSIONS):
        raise ValueError("Assessment requires exactly the five score dimensions")
    if any(v is not None and (type(v) is not int or not 0 <= v <= 4) for v in scores.values()):
        raise ValueError("Scores must be integers 0-4 or null")
    weak = data.get("weak_points", [])
    if not isinstance(weak, list) or any(not isinstance(v, str) or not v.strip() for v in weak):
        raise ValueError("weak_points must be a list of nonempty strings")
    return scores, weak


def evidence_path(path):
    target = Path(path).resolve()
    if not target.is_file() or not target.read_text(encoding="utf-8").strip():
        raise ValueError("Evidence must be an existing, nonempty learner-attempt file")
    try:
        return target.relative_to(ROOT).as_posix()
    except ValueError:
        return str(target)


def due_reviews(state, today):
    done = {(r["lesson_id"], r["scheduled_for"]) for r in state["reviews"]}
    return sorted([
        {"lesson_id": item["lesson_id"], "scheduled_for": day}
        for item in state["lessons"] if item["status"] == "completed"
        for day in item["review_due"]
        if day <= today and (item["lesson_id"], day) not in done
    ], key=lambda x: (x["scheduled_for"], x["lesson_id"]))


def select_next(catalog, state, today):
    delivered = state["lessons"]
    used = {item["topic_id"] for item in delivered}
    completed = {item["topic_id"] for item in delivered if item["status"] == "completed"}
    fingerprints = {frozenset(item["concept_fingerprint"]) for item in delivered}
    # Exact normalized objective matches catch obvious retitling, not paraphrases.
    objectives = {s.strip().casefold() for item in delivered for s in item["objectives"]}
    recent = sorted(delivered, key=lambda x: (x["created_at"], x["lesson_id"]))[-2:]
    recent_domains = [item["domain"] for item in recent]
    counts = {}
    for item in delivered:
        counts[item["domain"]] = counts.get(item["domain"], 0) + 1
    candidates = [item for item in catalog["topics"]
                  if item["topic_id"] not in used
                  and frozenset(item["concept_fingerprint"]) not in fingerprints
                  and item["objectives"][0].strip().casefold() not in objectives
                  and set(item["prerequisites"]) <= completed]
    def rank(item):
        return ("ABC".index(item["ring"]),
                item["domain"] in recent_domains,
                counts.get(item["domain"], 0),
                ("foundation", "senior", "architect").index(item["level"]),
                item["topic_id"])
    candidates.sort(key=rank)
    return {
        "date": today,
        "candidate": candidates[0] if candidates else None,
        "alternatives": [t["topic_id"] for t in candidates[1:4]],
        "due_reviews": due_reviews(state, today),
        "pending_lessons": [item["lesson_id"] for item in delivered if item["status"] != "completed"],
        "selection_note": "Heuristic shortlist: agent must compare objectives semantically with all delivered lessons. Prerequisites require completion; a pending lesson can be resumed explicitly.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=ROOT / "learning/state.json")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("next", "record", "start", "complete", "review", "reschedule"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--date", required=True, help="Learner-local ISO date; never inferred from host timezone")
        if name == "record":
            cmd.add_argument("--lesson", type=Path, required=True)
        elif name in ("start", "complete", "review", "reschedule"):
            cmd.add_argument("lesson_id")
        if name in ("complete", "review", "reschedule"):
            cmd.add_argument("--evidence", type=Path, required=True)
        if name in ("complete", "review"):
            cmd.add_argument("--assessment", type=Path)
        if name == "reschedule":
            cmd.add_argument("--from-date", required=True)
            cmd.add_argument("--to-date", required=True)
            cmd.add_argument("--reason", required=True)
    args = parser.parse_args(argv)
    if date.fromisoformat(args.date).isoformat() != args.date:
        raise ValueError("Date must use canonical YYYY-MM-DD format")
    if args.command == "reschedule":
        for day in (args.from_date, args.to_date):
            if date.fromisoformat(day).isoformat() != day:
                raise ValueError("Date must use canonical YYYY-MM-DD format")
    state = load_json(args.state)
    validate_state(state)
    catalog = load_json(ROOT / "curriculum/catalog.json")
    if args.command == "next":
        print(json.dumps(select_next(catalog, state, args.date), indent=2))
        return
    if args.command == "record":
        path = args.lesson.resolve()
        relative = path.relative_to(ROOT).as_posix()
        if not relative.startswith("lessons/") or path.suffix != ".md":
            raise ValueError("Lessons must be Markdown files inside lessons/")
        meta = metadata(path)
        topic = next((t for t in catalog["topics"] if t["topic_id"] == meta["topic_id"]), None)
        if not topic:
            raise ValueError("Register a source-grounded catalog topic before recording a lesson")
        for key in ("domain", "level", "objectives", "concept_fingerprint"):
            if meta[key] != topic[key]:
                raise ValueError(f"Lesson {key} differs from its catalog entry")
        if str(meta["created_at"]) != args.date or meta["status"] != "generated":
            raise ValueError("New lesson metadata must use the delivery date and generated status")
        if meta["lesson_id"] != f'{args.date}-{meta["topic_id"]}':
            raise ValueError("lesson_id must be YYYY-MM-DD-topic_id")
        if any(t["topic_id"] == meta["topic_id"] for t in state["lessons"]):
            raise ValueError("Topic already delivered: resume or review it, or register a distinct objective")
        if any(set(t["concept_fingerprint"]) == set(meta["concept_fingerprint"])
               for t in state["lessons"]):
            raise ValueError("Concept fingerprint already delivered")
        previous_objectives = {s.strip().casefold() for t in state["lessons"] for s in t["objectives"]}
        if meta["objectives"][0].strip().casefold() in previous_objectives:
            raise ValueError("Primary objective already delivered")
        completed = {t["topic_id"] for t in state["lessons"] if t["status"] == "completed"}
        if not set(topic["prerequisites"]) <= completed:
            raise ValueError("Prerequisites have not been completed")
        record = {key: meta[key] for key in ("lesson_id", "topic_id", "domain", "level", "objectives", "concept_fingerprint", "source_refs")}
        record.update(status="generated", created_at=args.date, completed_at=None,
                      mode=meta.get("mode", "full-lesson"), lesson_path=relative,
                      score=null_scores(), weak_points=[], evidence=[], review_due=[])
        state["lessons"].append(record)
    else:
        record = next((t for t in state["lessons"] if t["lesson_id"] == args.lesson_id), None)
        if not record:
            raise ValueError("Unknown lesson_id")
        if args.date < record["created_at"]:
            raise ValueError("Action date precedes lesson creation")
        if args.command == "start":
            if record["status"] == "completed":
                raise ValueError("Completed lesson must be reviewed, not restarted")
            record["status"] = "in_progress"
        elif args.command == "complete":
            if record["status"] == "completed":
                raise ValueError("Already completed: use review")
            evidence = evidence_path(args.evidence)
            scores, weak = assessment(args.assessment)
            record.update(status="completed", completed_at=args.date, score=scores,
                          weak_points=weak, evidence=[evidence], review_due=review_dates(args.date))
        elif args.command == "reschedule":
            if record["status"] != "completed":
                raise ValueError("Complete the lesson before adjusting a review")
            evidence = evidence_path(args.evidence)
            if args.to_date < args.date or args.to_date in record["review_due"]:
                raise ValueError("New review date must be today or later and distinct")
            # Validation replays this audit trail against the completion anchor.
            state.setdefault("review_adjustments", []).append({
                "lesson_id": args.lesson_id, "adjusted_at": args.date,
                "from_due": args.from_date, "to_due": args.to_date,
                "reason": args.reason, "evidence": [evidence],
            })
            if args.from_date not in record["review_due"]:
                raise ValueError("Review adjustment must reference a planned interval")
            record["review_due"][record["review_due"].index(args.from_date)] = args.to_date
            record["review_due"].sort()
        else:
            if record["status"] != "completed":
                raise ValueError("Complete the lesson before recording a spaced review")
            pending = [r for r in due_reviews(state, args.date) if r["lesson_id"] == args.lesson_id]
            if not pending:
                raise ValueError("No scheduled review is due for this lesson")
            # One retrieval attempt satisfies one interval, not every overdue slot.
            scheduled = pending[0]["scheduled_for"]
            scores, weak = assessment(args.assessment)
            state["reviews"].append({
                "review_id": f'{args.date}-{args.lesson_id}-{scheduled}',
                "lesson_id": args.lesson_id, "scheduled_for": scheduled,
                "reviewed_at": args.date, "evidence": [evidence_path(args.evidence)],
                "score": scores, "weak_points": weak,
            })
    if state["last_updated"] and args.date < state["last_updated"]:
        raise ValueError("Action date precedes the latest state update")
    state["last_updated"] = args.date
    save_state(args.state, state)
    print(f"Saved {args.command} to {args.state}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, yaml.YAMLError, ValidationError) as exc:
        raise SystemExit(str(exc)) from exc
