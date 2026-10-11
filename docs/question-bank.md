---
layout: default
title: Question Bank Contract
locale: en
translation_key: question-bank-guide
---

# Question Bank Contract

The [question bank](../questions/index.md) is a source interpretation layer over the existing curriculum, not another topic taxonomy. English and Vietnamese share identity and provenance; the generated pages offer readable questions and expandable guidance, not verified model answers. Use the [coverage report](../questions/coverage.md) to trace every source unit.

## One source of truth for each kind of data

| Data | Authoritative location | Contract |
| --- | --- | --- |
| Original interview framing | `sources/*.md` | Preserve bodies, numbered IDs, URLs and anchors; never reconstruct removed context |
| Domain, group identity, level, prerequisites | `curriculum/catalog.json` | A group ID is an existing topic ID; no competing taxonomy |
| Source inventory and semantic merges | `_data/question_bank/inventory.json` | Schema version 1; source units, canonical mapping, exact original text, ten merge rationales in EN/VI, pre-edit document roles/hashes |
| Question annotations | `_data/question_bank/questions/s01.json` … `s06.json` | One annotation per canonical ID, bilingual content and shared phase/order/version-sensitive flag |
| Group cards | `_data/question_bank/groups/s01.json` … `s06.json` | Shared group/representative IDs; bilingual objective, 2–4 competencies, introduction, added production task and rubric |
| Presentation labels | `_data/question_bank/labels.json` | Equivalent EN/VI labels and domain names, with unchanged slugs |
| Published pages | `questions/`, `vi/questions/` | Derived by `scripts/question_bank.py`; edit data, regenerate and commit both locales |
| Learner progress | `learning/state.json` or private profile | Separate lifecycle; question-bank tools never read/write progress or infer completion |

## Inventory and identity

A source unit has `source_id`, exact `source_ref`, `kind` (`numbered` or `source-scenario`), `original`, `group_id`, `original_group_id` and `canonical_id`. Each canonical question has `question_id`, home `group_id`, all `source_ids`/`source_refs`, `kind`, optional `merge_rationale` and `related_group_ids`. Every source ID maps exactly once; the lowest stable source ID names each merged question. Aliases remain anchors on both language pages.

Four unnumbered scenarios receive editorial IDs `S02-SC001`, `S03-SC001`, `S04-SC001`, `S06-SC001`. Their bullets describe one scenario's constraints; they are not additional interview questions. The S06 answer structure remains advice. The 62-file pre-edit snapshot classifies guidance, curriculum, generated lessons, templates, lab material and shared examples, so derived practice questions do not inflate source coverage.

`algorithms-department-headcount` is the existing focused home for S03-Q032. The older source link to the broader SQL-relations topic still works. `algorithms-collection-reasoning` remains derived Ring B practice in the 47-topic catalog and therefore has no canonical source-question group. These decisions change navigation, not source IDs or catalog learning objectives.

## Annotation schema and sequence

Each question contains `question_id`, `phase`, integer `order`, boolean `version_sensitive`, and complete `en`/`vi` objects with:

- `question`: focused natural wording without the solution.
- `explanation`, `intent`, `scope`: what to clarify, inferred observable capability and consequential assumptions.
- `senior_signals`: two concrete criteria; `pitfalls`: at least one relevant shallow answer or misconception.
- `followups`: one or two related questions, displayed explicitly as agent additions.

The primary phase sorts as `foundation → mechanism → application → failure → tradeoff → production`, then `order`, then stable ID. Only phases supported by actual member questions appear. A representative question introduces the group before the full route. Group rubrics use `basic`, `senior`, `evidence_missing`; no score is assigned automatically. Semantic translation quality and prerequisite progression require human/agent review as well as structural checks.

Source framing, editorial criteria and version-verified explanations are different evidence. This bank intentionally makes no version-specific model-answer claims. Its version flags require checking the actual runtime, framework/provider and official documentation when teaching or answering. A later lesson must record the actual claim, applicability, direct official URL and check date under the existing skill policy; no date is manufactured by rendering a question.

## Update and verify

```sh
python scripts/question_bank.py
python scripts/question_bank.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/check_site.py _site
python tests/questions_browser_check.py --site _site --axe work/browser-checks/node_modules/axe-core/axe.min.js
```

Install existing requirements and build Jekyll before rendered-site/browser checks; see [verification](verification.md). The generator does not fetch documentation or write state. `--check` rejects missing coverage, incorrect aliases, stale pages, mismatched locale metadata and changes to preserved source hashes. Source changes require an explicit reviewed inventory migration, including fresh full-source reading; do not simply replace hashes to pass validation.

Regenerate after publishing or translating a lesson too: related-lesson links are derived from public lesson metadata. Refreshing these links creates no lesson record or completion. Groups are multi-question study routes and may span several sessions; select one focused objective for each daily lesson.

For everyday study, choose one question, attempt it before opening guidance, explain a mechanism, check a changed/failing case, correct one gap and speak a direct answer. Ask the [daily skill](../agent/SKILL.md) for a focused full lesson when needed. Generated bank pages and editorial review are neither learner evidence nor completed lessons.
