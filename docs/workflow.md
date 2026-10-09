---
layout: default
title: Daily Workflow and Learning State
locale: en
translation_key: workflow
---

# Daily Workflow and Learning State

## From request to lesson

1. Say **“Viết bài học hôm nay.”** The agent reads the skill, catalog, source seeds and current state.
2. The agent checks generated, in-progress and completed objectives, chooses a fresh eligible topic and verifies current technical claims.
3. A 30–45-minute lesson with one primary goal and six guided steps is saved in `lessons/`, linked from its index and registered as generated in `learning/state.json`.
4. Submit your attempt, lab output or spoken-answer transcript. The agent gives evidence-based feedback and records actual completion.
5. Say **“Ôn tập hôm nay.”** to retrieve due concepts, with solutions withheld until after your attempt.

Full lesson provides a self-contained solution. Interactive and Mock interview wait for learner answers. An unfinished interactive session resumes the same lesson ID; a new request can choose another eligible objective without silently completing pending work.

For Interactive/Mock sessions, the agent saves a cursor at
`learning/sessions/LESSON_ID.md` using the [session template](../agent/SESSION_TEMPLATE.md).
It records the unanswered prompt, six-step cursor, sanitized feedback and next action,
then reads that note on resume. A separate profile keeps session notes beside
its own state file. The `start` command changes status only; the agent saves the
note separately after each turn. A question without an attempt remains generated.

## Choose a teaching language

Say `Viết bài học hôm nay bằng tiếng Việt` or `Write today’s lesson in English`. Explicit requests override the optional agent preference; default is English. New public Full lessons have English and Vietnamese versions but one logical ID and delivery record. English interview model speech remains the default, with Vietnamese feedback when requested.

`Chuyển bài đang học sang tiếng Việt` preserves its pending prompt, cursor and lesson ID, including withheld Interactive solutions. Use `python scripts/learning.py lesson-path LESSON_ID --language vi --date YYYY-MM-DD` to resolve the variant read-only. Use `python scripts/learning.py language --language vi --date YYYY-MM-DD` only when an agent preference should actually be saved; it changes no learning progress.

On the site, English URLs remain unchanged and Vietnamese pages live under `vi/`. Language links retain the current step. Browser preference offers a counterpart instead of redirecting direct URLs. Continue resolves the same logical lesson in the preferred locale; missing translations open that exact English artifact with a notice. The public site does not update the agent profile. See [localization and authoring](localization.md).

## Public desk and daily actions

The [daily desk](../index.md) serves published lessons. **Start this lesson** opens the latest artifact, not a personalized recommendation. **Learn something new** copies a prompt for your repo agent. **Continue reading** uses a local browser reading step; without a bookmark it opens the latest lesson. **Review** and **Interview** provide prompts and a practice entry; your agent reads real state to choose due work or resume coaching.

The site is static: there is no generation endpoint or GitHub write integration. Copying a prompt does not run an agent. Bookmarks contain only lesson ID, published path, step and timestamp; no attempt, score or completion. They are specific to this browser and can be cleared. Blocked storage or clipboard access leaves ordinary links and selectable prompts working. No JavaScript is needed to read lessons or open answers.

For durable resume, ask **“Tiếp tục bài đang học”** in the repo agent. It reads the session note and current state. Clicking a step does not start or complete a lesson. Supply your own lab output or answer before progress is recorded.

## Persistence commands

Install dependencies with `python -m pip install -r requirements.txt`.

```sh
python scripts/learning.py next --date 2026-10-08
python scripts/learning.py record --lesson lessons/2026-10-08-messaging-idempotent-consumer.md --date 2026-10-08
python scripts/learning.py start 2026-10-08-messaging-idempotent-consumer --date 2026-10-08
```

The sample is already recorded; a repeated `record` correctly rejects it. Use the path and date of a newly generated lesson for a new entry. Dates are explicit learner-local dates; the initial profile uses Asia/Bangkok.

```sh
python scripts/learning.py complete 2026-10-08-messaging-idempotent-consumer --date 2026-10-09 --evidence /path/to/learner-attempt.md
python scripts/learning.py review 2026-10-08-messaging-idempotent-consumer --date 2026-10-10 --evidence /path/to/retrieval-attempt.md
```

Completion and review require a real nonempty evidence file. Optional `--assessment /path/to/assessment.json` supplies five rubric scores and weak points. The CLI validates structure; the agent evaluates substance. Scores are `null` until assessed. A zero is an assessed result.

Reviews are initially scheduled D+1/3/7/14/30 from actual completion. Generated lessons have no active review dates. One attempt records one due interval. A review never creates another lesson or rewrites original completion evidence.

### Adjust a future review from observed evidence

After an actual recall attempt, an agent may shorten or extend an **unperformed** interval when that evidence justifies it. These example dates assume completion on October 9 and a real review on October 10:

```sh
python scripts/learning.py reschedule 2026-10-08-messaging-idempotent-consumer --date 2026-10-10 --from-date 2026-10-12 --to-date 2026-10-11 --reason "Observed rollback gap; retry sooner" --evidence /path/to/retrieval-attempt.md
```

`review_adjustments` keeps original/new dates, adjustment date, reason and evidence. The validator reconstructs the plan from the unchanged completion date and this audit trail. A change cannot move a performed review, collide with another interval or schedule in the past. It creates no review, completion or grade. Keep the default plan when there is no evidence for changing it.

Each new adjustment records how many review entries existed at that point, preserving operation order when changes and attempts share a date. A later review on a reused date does not invalidate an earlier adjustment.

## State reference

The GitHub source files document the full schema and commands:

- [Learning-state reference](https://github.com/nguyenan97/software-engineering-interview/blob/main/learning/README.md)
- [State schema](https://github.com/nguyenan97/software-engineering-interview/blob/main/learning/state.schema.json)
- [Current state](https://github.com/nguyenan97/software-engineering-interview/blob/main/learning/state.json)
- [Empty profile template](https://github.com/nguyenan97/software-engineering-interview/blob/main/agent/LEARNING_STATE_TEMPLATE.json)

These links target the default branch and become available there when the curriculum change is merged. State is not served by Pages. For an independent profile, copy the empty template to a local path and pass `--state /path/to/state.json` before the command. Preserve existing history.

State writes use atomic replacement and require one writer at a time. If an agent cannot write, it returns a proposed state update and says it has not been saved. Chat history is not durable state.

## Privacy and verification

State, scores and attempts committed to this public repository remain public on GitHub even though excluded from Pages. Keep sensitive evidence outside the checkout or use a private local profile. Record sanitized examples and real learner evidence.

Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` after updates. See [browser, lab and build verification](verification.md). PR CI also builds the site; deployment continues through the existing `main` workflow.

[Curriculum](../curriculum/index.md) · [Lessons](../lessons/index.md) · [Skill](../agent/SKILL.md)
