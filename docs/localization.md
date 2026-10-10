---
layout: default
locale: en
title: Localization Architecture and Authoring
---

# Localization Architecture and Authoring

English remains the default at every existing URL. Vietnamese pages live under `vi/`; no old URL was removed or redirected. Layouts/includes are shared. `_data/i18n/en.yml` and `vi.yml` contain UI strings, prompts and runtime messages; Markdown contains translated teaching. No translation service or new UI runtime dependency is used.

## Page identity and routing

A page pair shares `translation_key`, with `locale: en` or `vi`. Each locale has one page per key. The layout resolves counterparts from Jekyll pages, emits a self-canonical URL and reciprocal hreflang links, plus English x-default. Pages without a translation show a clear notice and link to their own English content. Never manufacture a Vietnamese route for a missing translation.

Core paired pages: daily desk, lesson index, review, mock interview, workflow, repository guide, curriculum overview, learning method and the sample lesson. Domain routes, source inventories and implementation references remain English unless a real translation is authored. Their language switch states the fallback explicitly.

The daily desk and lesson index iterate canonical lessons only, then resolve the selected locale. A translated page does not increase lesson count or become a different latest lesson. A missing lesson translation uses that exact canonical lesson with a visible language badge.

## One lesson, one record

English `lessons/YYYY-MM-DD-topic-id.md` remains the canonical artifact referenced by `learning/state.json`. Keep its IDs, objectives, fingerprint, dates, source refs and status snapshot unchanged when translating.

A Vietnamese lesson under `vi/lessons/` needs:

```yaml
layout: lesson
locale: vi
translation_key: YYYY-MM-DD-topic-id
lesson_id: YYYY-MM-DD-topic-id
topic_id: topic-id
canonical_lesson: lessons/YYYY-MM-DD-topic-id.md
title: "<Natural Vietnamese problem title>"
primary_objective: "<Same capability, explained in Vietnamese>"
prerequisites_note: "<Same prerequisites and runtime>"
translated_at: "YYYY-MM-DD"
```

Identity is shared. The layout reads timing, level and other shared metadata from the canonical page. Do not repeat or translate machine objectives/fingerprints in a competing metadata block. The validator rejects contradictory shared metadata, wrong canonical references, orphan/duplicate locale pages and changed lab code.

Use all six stable anchors: `goal`, `predict`, `model`, `practice`, `verify`, `recall`. Localize explanation, tasks, rubric and retrieval, preserving assumptions, expected states and unverified boundaries. Keep version-verification dates from the original; `translated_at` is not a new verification or delivery date. Translation requires human technical comparison; structural validators cannot prove semantic equivalence.

## Shared executable material

`labs/atomic-inbox/` owns the runnable Python solution and retained SQL scripts. `python scripts/render_lesson_code.py` generates fenced snippets in `_includes/lab-code/`; CI checks byte correspondence. Both language versions include the same files. The SQL files were extracted unchanged from the original lesson and remain runtime-unverified; extracting them does not establish execution evidence.

Interview model answers can be shared in `_includes/interview/`, marked `lang="en"` inside Vietnamese teaching. Explain the argument in Vietnamese after the English answer instead of duplicating the entire lesson. Do not translate IDs, SQL parameters, outputs or error contracts. A new lesson may use different shared snippets, but both locales must reference the same executable contract.

## Preferences, resume and history

Browser keys are independent:

- `interview-practice:language:v1`: explicitly selected locale only.
- `interview-practice:reading-place:v1`: the existing lesson ID/path, stable step and timestamp.

Language links preserve the current fragment. Direct URLs never automatically redirect, preserving intentional English links and back/forward. A remembered preference is offered as a link when the counterpart exists. Continue resolves the stored logical ID to the preferred language; unavailable variants fall back to the same English lesson. Unknown languages, corrupt bookmarks, mismatched ID/path and external URLs are ignored. Neither key writes to GitHub or changes learning progress.

The repo profile optionally stores `learner_profile.preferred_language` through:

```sh
python scripts/learning.py language --language vi --date YYYY-MM-DD
python scripts/learning.py next --language vi --date YYYY-MM-DD
python scripts/learning.py lesson-path LESSON_ID --language vi --date YYYY-MM-DD
```

Only `language` writes the preference and update date. `next`/`lesson-path` are read-only. Request overrides preference; absent preference defaults to English. Existing v2 states remain valid without the new optional field. Passing a valid translated file to `record` resolves to canonical metadata and registers one logical lesson; a second registration is rejected. Completion and review always use the shared ID and actual evidence.

Session notes store optional `teaching_language`, `interview_language` and `feedback_language` alongside the existing step/question. Preserve the cursor when switching, and keep pending solutions withheld in Interactive. Changing language never invokes start/complete/review by itself.

For Interactive/Mock, translate the teaching and unanswered challenge already revealed. Do not publish its pending solution in either locale: closed disclosures are readable. The complete bilingual publication contract applies when delivering a Full lesson, not as permission to reveal future Interactive answers.

## Add a page or language

For a new translation, author the real Markdown page under its locale, copy the canonical translation key/identity, localize human metadata, preserve step IDs, use shared code, then validate and inspect both rendered pages. No route registry or layout copy is needed. Source files keep their original provenance.

For an additional language, extend the supported locale list and native names, add a complete dictionary with the same key structure, author paired pages, and update the CLI/schema language allowlists. Reuse existing layouts/includes/JS; do not duplicate routing or lifecycle logic. English stays default. Add missing-translation and browser tests before claiming support.

## Checks

Run content/state tests, `python scripts/render_lesson_code.py --check`, Jekyll build and `python scripts/check_site.py _site`. Browser tests exercise both locales, metadata, same-step switching, reload/back/forward, preference/resume, no-JS links, missing translations, blocked storage/clipboard, responsive layout and accessibility. CI screenshots show English and Vietnamese.

[Workflow](workflow.md) · [Vietnamese workflow](../vi/docs/workflow.md) · [Verification commands](verification.md)
