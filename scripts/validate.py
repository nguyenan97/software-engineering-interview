#!/usr/bin/env python3
"""Validate curriculum, source links, lesson metadata and durable learning state."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

from learning import ROOT, load_json, metadata, validate_state
from localization import validate_localization

DOMAINS = {
    "architecture-distributed", "dotnet-runtime", "aspnet-api", "ef-linq", "sql-data",
    "messaging-event-driven", "azure-cloud", "security-identity", "observability-reliability",
    "devops-delivery", "frontend-typescript", "algorithms-debugging", "engineering-communication",
}


def body(text):
    if text.startswith("---\n"):
        text = text.split("---", 2)[2]
    return re.sub(r"^(`{3,}|~{3,}).*?^\1\s*$", "", text, flags=re.M | re.S)


def anchors(path):
    text = body(path.read_text(encoding="utf-8"))
    values = set(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    values.update(re.findall(r'^\{:\s*#([\w-]+)\s*\}', text, re.M))
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        clean = re.sub(r"[`*_]", "", heading).lower()
        values.add(re.sub(r"[^\w\- ]", "", clean).replace(" ", "-"))
    return values


def check_ref(ref, relative_to):
    parts = urlsplit(ref)
    if parts.scheme or parts.netloc or ref.startswith("{{"):
        return
    target = (relative_to / unquote(parts.path)).resolve() if parts.path else relative_to
    if not target.exists():
        raise ValueError(f"Missing local target: {ref} (from {relative_to})")
    if parts.fragment and target.is_file() and target.suffix == ".md":
        if unquote(parts.fragment) not in anchors(target):
            raise ValueError(f"Missing anchor: {ref}")


def main():
    locale_report = validate_localization(ROOT)
    catalog = load_json(ROOT / "curriculum/catalog.json")
    assert catalog["schema_version"] == 1
    topics = catalog["topics"]
    ids = {topic["topic_id"] for topic in topics}
    assert len(ids) == len(topics), "Duplicate catalog topic IDs"
    assert {t["domain"] for t in topics} == DOMAINS, "All taxonomy domains need coverage"
    objectives = set()
    for topic in topics:
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", topic["topic_id"])
        assert topic["level"] in {"foundation", "senior", "architect"}
        assert topic["ring"] in {"A", "B", "C"}
        assert 2 <= len(topic["objectives"]) <= 4
        assert 3 <= len(set(topic["concept_fingerprint"])) <= 7
        primary = topic["objectives"][0].strip().casefold()
        assert primary not in objectives, "Duplicate primary objective"
        objectives.add(primary)
        assert set(topic["prerequisites"]) <= ids
        assert topic["topic_id"] not in topic["prerequisites"]
        assert topic["source_refs"], "Topic needs a source seed"
        for ref in topic["source_refs"]:
            assert ref.startswith("sources/"), "Catalog seed must trace to local source"
            check_ref(ref, ROOT)
    def visit(topic_id, trail):
        if topic_id in trail:
            raise ValueError(f"Prerequisite cycle: {trail + [topic_id]}")
        for dependency in next(t for t in topics if t["topic_id"] == topic_id)["prerequisites"]:
            visit(dependency, trail + [topic_id])
    for topic_id in ids:
        visit(topic_id, [])
    state = load_json(ROOT / "learning/state.json")
    validate_state(state)
    validate_state(load_json(ROOT / "agent/LEARNING_STATE_TEMPLATE.json"))
    for record in state["lessons"]:
        path = ROOT / record["lesson_path"]
        meta = metadata(path)
        topic = next(t for t in topics if t["topic_id"] == record["topic_id"])
        for key in ("lesson_id", "topic_id", "domain", "level", "objectives", "concept_fingerprint", "source_refs"):
            assert record[key] == meta[key], f"State/lesson mismatch: {key}"
        for key in ("domain", "level", "objectives", "concept_fingerprint"):
            assert record[key] == topic[key], f"State/catalog mismatch: {key}"
        assert str(meta["created_at"]) == record["created_at"]
        assert record["lesson_id"] == f'{record["created_at"]}-{record["topic_id"]}'
        assert meta["status"] == "generated", "Front matter must preserve the generation snapshot"
        assert any(ref in topic["source_refs"] for ref in record["source_refs"]), "Lesson needs a catalog source seed"
        for ref in record["source_refs"]:
            check_ref(ref, ROOT)
        content = path.read_text(encoding="utf-8")
        if record["mode"] == "full-lesson":
            if meta.get("lesson_format") == "focused-v1":
                assert meta.get("layout") == "lesson", "Focused lessons use the lesson layout"
                assert isinstance(meta.get("primary_objective"), str) and meta["primary_objective"].strip(), "One primary objective is required"
                duration, practice = meta.get("duration_minutes"), meta.get("practice_minutes")
                assert type(duration) is int and 30 <= duration <= 45, "Focused sessions take 30–45 minutes"
                assert type(practice) is int and duration / 2 <= practice <= duration, "At least half the budget is active practice"
                assert meta.get("prerequisites_note"), "Show prerequisites before starting"
                assert {"goal", "predict", "model", "practice", "verify", "recall"} <= anchors(path), "Six stable step anchors are required"
                assert "data-answer" in content and "<details" in content, "Full lesson answers must be available separately"
            else:
                assert all(f"Stage {i}" in content for i in range(9)), "Legacy full lesson must contain all stages"
    registered = {record["lesson_path"] for record in state["lessons"]}
    saved_lessons = {p.relative_to(ROOT).as_posix() for p in (ROOT / "lessons").glob("*.md") if p.name != "index.md"}
    assert registered == saved_lessons, "Saved lessons and learning-state records must agree"
    # Validate published Markdown links, excluding code examples and front matter.
    documents = sorted(p for p in ROOT.rglob("*.md") if not any(part in {".git", "_site", "work", ".venv"} for part in p.parts))
    for path in documents:
        text = body(path.read_text(encoding="utf-8"))
        for ref in re.findall(r"(?<!!)\[[^\]]+\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            if ref.startswith("#"):
                check_ref(path.name + ref, path.parent)
            else:
                check_ref(ref.strip("<>"), path.parent)
    for path in ROOT.glob(".github/workflows/*.yml"):
        yaml.safe_load(path.read_text(encoding="utf-8"))
    print(f"Validated {len(topics)} topics, {len(documents)} Markdown documents, {len(state['lessons'])} logical lesson record(s), state schema, links and prerequisite graph; localization: {locale_report}.")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, OSError, KeyError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
