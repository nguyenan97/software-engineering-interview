---
layout: default
title: Repository Guide
---

# Software Engineering Interview

A source-grounded daily interview curriculum for senior software engineers progressing toward solution architecture. Study engineering decisions and practice explaining them clearly in English, with short Vietnamese notes when they help understanding.

## Start a daily session

Open the [daily learning desk](https://nguyenan97.github.io/software-engineering-interview/) for the latest published lesson and four clear actions. To generate a new lesson, open this repository in an agent that can read its files, then say:

> **Viết bài học hôm nay.**

The [Daily Interview Mastery skill](agent/SKILL.md) reads the source prompts, curriculum and learning history, autonomously selects a fresh objective, verifies current technical behavior, writes a full lesson, and records it as **generated**. Generated content is distinct from completed learning. Each request starts a session; generation has no scheduled background job.

| Request | Behavior |
| --- | --- |
| `Viết bài học hôm nay` | Full lesson, with challenge, lab and worked solution |
| `Học interactive hôm nay` | Challenge first; waits for your attempt before teaching the solution |
| `Tiếp tục bài đang học` | Resumes the pending lesson using its saved ID |
| `Ôn tập hôm nay` | Due retrieval reviews; does not count as a new lesson |
| `Mock interview hôm nay` | English questions and follow-ups first; feedback after your answers |
| `Đánh giá bài làm này và cập nhật tiến độ` | Evidence-based rubric and completion/review bookkeeping |

Full lesson is the default. The agent chooses the topic autonomously. Explicit topic or language requests override defaults. Resume pending prerequisites when no eligible new topic remains.

## Learn and answer well

Each default lesson covers **one main objective in 30–45 minutes**, with at least half the time practicing and retrieving. Follow **A goal → B predict → C model → D practice → E verify/correct → F speak/recall**. Complete answers and advanced depth are expandable; try before opening them. Lab tasks include a happy path, a meaningful failure and a changed example with fewer hints. Reviews start at actual completion with D+1/3/7/14/30 as an adjustable default. Retrieval, spacing, worked examples and explanatory questions are supported by research linked in the [Interview Method](agent/INTERVIEW_METHOD.md). The exact calendar and domain rotation are curriculum choices.

Answer the question directly, explain the mechanism with a concrete example, state the trade-off and evidence, then offer a relevant follow-up bridge. Each lesson rehearses a short answer, a 90-second explanation and deeper defense. The method helps interviewers assess reasoning; it cannot guarantee a particular interviewer's preference or prevent deeper questions. Never invent work experience, measurements or certainty to steer the conversation.

## Browse the curriculum

- [Curriculum and domain routes](curriculum/index.md)
- [Source coverage, consolidation and gaps](curriculum/source-coverage.md)
- [Topic taxonomy](agent/TOPIC_TAXONOMY.md)
- [Lesson index](lessons/index.md)
- [Worked example: Idempotent Consumers](lessons/2026-10-08-messaging-idempotent-consumer.md)
- [Workflow and state guide](docs/workflow.md)

The corpus has **234 numbered prompts**, four scenarios/request-flow sections and its answer structure, organized into **46 topics across 13 domains**. Stable `S01-Q001` IDs preserve traceability. Overlapping prompts point to canonical topics; API request identity, SQL import behavior and consumer deduplication remain distinct objectives. Foundation/senior/architect depth is independent of source-direct/adjacent/extension rings.

## Repository layout

```text
agent/          Daily skill, interview method, lesson and state templates
curriculum/     Catalog, domain routes, source coverage
sources/        Six privacy-safe source inventories with stable anchors
lessons/        Generated lessons and public lesson index
labs/           Runnable starters, verifiers and reference solutions
practice/       Review and mock-interview entry pages
_layouts/       Daily desk and six-step lesson layouts
assets/         CSS, small browser helpers and downloadable labs
learning/       Durable state, JSON schema, persistence reference
scripts/        Candidate selection, lifecycle commands, validation
tests/          State-machine and review bookkeeping tests
docs/           Public workflow guide
AGENTS.md       Entry instructions for repository agents
```

The refactored sample remains the original generated record, with no completion or scores. Its portable Python/SQLite transaction lab has five executed checks and a deliberately broken starter; SQL Server depth is retained separately with execution unverified.

The static website does not read personal state, create lessons or save completion to GitHub. It can save only a reading step in this browser. For durable coaching progress, say **“Tiếp tục bài đang học”** to the repo agent, which reads the session cursor. Submit your own attempt to record completion. Use private profiles for sensitive evidence.

## State and checks

```sh
python -m pip install -r requirements.txt
python scripts/learning.py next --date 2026-10-08
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/package_labs.py --check
python labs/atomic-inbox/verify.py --solution
```

Replace the example date with your local date. `next` suggests a candidate; the agent performs semantic duplicate review and supplies the teaching. See [workflow](docs/workflow.md) for recording, completion and reviews. State is schema-validated and written atomically. Run one state writer at a time. If writes are unavailable, the agent returns a proposed update and says it has not been saved.

PR validation checks metadata, links, state rules, lab/download consistency, the Jekyll build and Chromium desktop/mobile accessibility and learning navigation. See [verification commands](docs/verification.md). Browser-test dependencies do not ship to the site. The existing deployment workflow publishes Pages from `main`.

## Language, privacy and evidence

English is primary for concepts, code, questions, model answers and diagrams. Keep terms such as `Dependency Injection`, `ThreadPool`, `Deadlock`, `Optimistic Concurrency`, `Idempotency` and `Eventual Consistency` in English. Vietnamese supplements difficult meaning rather than repeating the lesson.

Original identities and confidential contexts were removed before publication. Never reconstruct them. Interview notes determine question framing; official documentation and official source repositories establish current behavior. Version-sensitive lesson claims need dated references. Documentation verification is distinct from executing a lab.

This is a public repository. Learning state and evidence are excluded from Pages, but committed files remain public on GitHub. Keep private attempts outside this checkout and use sanitized records or a private local state profile.
