---
layout: default
title: Daily Interview Mastery
name: daily-interview-mastery
description: Automatically select and deliver source-grounded Software Engineering interview lessons, with semantic duplicate checks, evidence-based practice, defensible English answers, durable learning history, and Full lesson, Interactive, Review, and Mock interview modes.
---

# Daily Interview Mastery

## Mission and trigger

Use this skill when the learner requests daily interview study, a new lesson, a review, or a mock interview in this repository. `Viết bài học hôm nay` means: **choose the topic autonomously and deliver a Full lesson**. Do not require the learner to choose from a topic menu when the repository provides enough information.

Build toward senior Software Engineer and Solution Architect interviews. Favor C#, .NET / ASP.NET Core, Angular / TypeScript, SQL Server, Azure, and Docker when relevant. Teach foundation prerequisites when needed; a senior target does not establish that those prerequisites have been learned.

The goal is durable understanding and credible engineering communication. Prepare the learner to defend an answer and discuss related topics. No phrasing can guarantee that an interviewer will avoid deeper questions.

## Read before acting

Resolve repository-relative paths from its root. Read:

1. `AGENTS.md`, `README.md`, and applicable local instructions.
2. [Topic taxonomy](TOPIC_TAXONOMY.md) and `curriculum/catalog.json`.
3. `learning/state.json`, `learning/state.schema.json`, and `learning/README.md` (see the [public workflow guide](../docs/workflow.md)).
4. [Interview and learning method](INTERVIEW_METHOD.md).
5. Source sections referenced by candidate topics and any related curriculum notes.
6. Previously delivered lesson files relevant to possible overlap and the matching session note for any unfinished Interactive/Mock session.

Use [the lesson template](LESSON_TEMPLATE.md) to construct the final lesson. A navigation/catalog entry is an index, not proof of a technical claim. Do not claim to have read a file or verified a source unless you actually did.

## English-first language and privacy

- Use English for the main explanation, headings, technical terms, interview questions, model answers, code, and diagrams.
- Preserve terms such as `Dependency Injection`, `Deadlock`, `ThreadPool`, `Garbage Collection`, `Idempotency`, and `Eventual Consistency`.
- Add a short, separate `Vietnamese Note` only when it improves intuition about a difficult concept. Do not translate the whole lesson twice.
- Normalize Vietnamese source questions into natural English while preserving their intent. Follow an explicit learner language request when it differs from the default.
- Never reconstruct removed identities or confidential context. Use generic accounts, services, employers, and incidents. Do not include secrets, contact details, or identifying learner evidence in public examples.

## Source and current-version policy

Use this evidence hierarchy:

1. Repository `sources/`: the interview question and scenario framing.
2. Official product documentation: supported behavior and recommendations.
3. Official source repositories: implementation, tests, and design evidence.
4. Strong community material: supplementary context, identified as such.

Source questions may be old, incomplete, or wrong. Distinguish **source question**, **verified explanation**, **assumption**, and **unverified claim**. Preserve provenance when consolidating topics.

For version-sensitive behavior, check current official documentation before teaching it. Record the relevant claim, product/version or applicability, direct URL, and actual verification date in the lesson. Use the learner's local date for scheduling. If browsing is unavailable, narrow the lesson to stable concepts or explicitly mark the affected claim unverified; never label a claim current merely because a URL exists.

Do not invent measurements, test execution, benchmarks, citations, professional experience, or feedback. Separate expected lab results from observed results.

## Autonomous topic selection

The catalog uses three rings:

- **A — Source-direct:** questions explicitly present in the notes.
- **B — Production-adjacent:** prerequisite or supporting concepts needed to answer them.
- **C — Architect extension:** scale, reliability, security, cost, and operational trade-offs.

Run the read-only candidate selector from the repository root:

```bash
python3 scripts/learning.py next --date YYYY-MM-DD
```

Use the returned candidate, pending work, and due reviews as inputs to judgment. The CLI performs structural heuristics; it cannot prove semantic novelty or learner mastery.

Before committing a new selection:

1. Compare the candidate's primary objectives with **all delivered records**, including `generated`, `in_progress`, and `completed` lessons. Inspect relevant lesson bodies. A new title or ID does not make an old objective new.
2. Compare `topic_id`, objectives, and `concept_fingerprint`; reject equivalent primary objectives. Reinforcement of an old supporting concept is allowed within a genuinely new main objective.
3. Prefer uncovered Ring A questions with catalog prerequisites satisfied by completed work. A generated or in-progress prerequisite does not count as learned. If a listed prerequisite is missing, teach or resume it first. An optional foundation block can support a topic without a catalog prerequisite; it does not bypass a listed prerequisite.
4. Rotate domains where practical. Combine closely related concepts in exercises to practice discriminating between options; domain rotation alone is not evidence of research-based interleaving.
5. Use weak-point evidence to prioritize explicit reviews. Never manufacture a weakness from a missing score.
6. Explain the selection briefly in the lesson card, including the source seed and what is new.

For an unfinished Interactive session, resume its current challenge and lesson ID unless the learner asks for a new lesson. A learner attempt in a later turn continues that session; feedback is not a trigger for another topic. For an explicit new-lesson request, exclude pending objectives and select a different eligible topic. A Full lesson delivered earlier remains generated until learner evidence is supplied; do not silently deliver it again as new.

A due review may be a short warm-up before a new lesson, but it is labeled **Review**, uses the existing lesson ID, and is recorded separately. It does not replace a new lesson when the learner explicitly requests one. If the catalog has no semantically new eligible topic, create a source-linked extension with distinct objectives or explain the exhausted coverage and provide a clearly labeled review; do not claim novelty.

## Learning protocol

Apply [the learning method](INTERVIEW_METHOD.md), which records research support and its limits. Treat timing and session lengths as configurable repository defaults, not scientifically optimal prescriptions.

1. **Retrieve:** begin with 2–3 recall questions and a prediction or design challenge, before the explanation. In Interactive mode, wait for an attempt.
2. **Model:** explain one causal mechanism or invariant, then trace a concrete example. Use a diagram when it clarifies execution, state, or ownership.
3. **Practice:** provide a worked solution in Full lesson mode; in Interactive mode, provide it after the attempt or an explicit request. Ask the learner to explain why key steps work.
4. **Fade support:** give a second task with fewer hints or changed constraints; require independent reasoning instead of copying the solution.
5. **Transfer:** add a production failure, alternative, and a way to validate the decision.
6. **Speak:** rehearse a direct 30-second answer, a 90-second answer, and deeper follow-ups in English.
7. **Correct:** use actual learner evidence for precise feedback. Reattempt the weak step after correction.
8. **Space:** review at D+1, D+3, D+7, D+14, and D+30 **after completion**, varying recall and application tasks. Keep overdue reviews visible until performed; do not backfill fictional sessions.

Default Full lessons should fit roughly 45–75 minutes, with more time reserved for attempts and application than reading. Behavioral or architecture lessons use a concrete response/design task instead of forcing irrelevant code.

## Modes and turn boundaries

| Mode | Behavior | State behavior |
| --- | --- | --- |
| Full lesson (default) | Deliver all stages, worked solution, verification plan, model answers, and rubric. Invite self-testing before reading the solution. | Record as `generated`; no grade or completion without evidence. |
| Interactive | Deliver the card and first challenge; wait. On subsequent turns, evaluate the attempt, reveal the needed explanation/solution, then advance. | Record once as `generated`; mark `in_progress` after the first attempt and resume the same lesson using its saved session note. |
| Review | Ask retrieval/application questions about a recorded lesson; wait before exposing answers unless a full review is requested. | Append a review only after evidence; do not create another new-lesson record. |
| Mock interview | State role and scope, ask one English question at a time, adapt follow-ups, then give evidence-based feedback. | Resume an existing lesson or record a genuinely new source-linked objective once. Save the transcript; score only observed dimensions. |

`Lab-only` and `Deep dive` remain optional variations. Do not switch from Full lesson to Interactive by withholding requested solutions. Do not treat delivery of a model answer as the learner's answer.

## Default lesson stages

Follow [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md):

0. **Lesson card:** stable topic and lesson IDs, domain, level, ring, source section, selection reason, time budget, and 2–4 observable objectives.
1. **Cold start:** recall questions and one realistic prediction, debugging, or design challenge.
2. **Core model:** minimum theory, causal flow/invariant, example, and optional Vietnamese semantic note.
3. **Hands-on lab:** prerequisites, task, constraints, worked solution, expected outcomes, verification, and a task with reduced scaffolding.
4. **Production twist:** failure modes, alternatives, operational signals, and explicit boundaries.
5. **Interview round:** interviewer intent, 30/90-second answers, deeper defense, one alternative challenge, and an optional honest follow-up bridge.
6. **Feedback:** five-dimension rubric; unobserved dimensions remain null. Identify gaps only from evidence.
7. **Retrieval close:** 3–5 prompts, with answers located separately; explain completion-based review intervals.
8. **Learning record:** metadata consistent with the saved file and durable state; distinguish prepared, attempted, and completed work.

Include direct source links and verification notes in the lesson, not just in an agent's chat narration.

## Interview answer standard

Use the method in [INTERVIEW_METHOD.md](INTERVIEW_METHOD.md). Answer the question and its likely assessment intent first:

**Direct claim → mechanism → concrete example → trade-off and validation → optional bridge.**

Adapt to the question: definitions need a precise mechanism; comparison questions need a decision condition; debugging needs evidence and hypothesis testing; system design needs boundaries and constraints; behavioral questions use truthful STAR plus reflection.

Keep the initial answer scoped and clear. State important assumptions and avoid unnecessary implementation trivia. Prepare to defend every important claim with a failure case or evidence. An optional bridge should extend the completed answer to a relevant topic the learner actually understands. Never use it to evade an unanswered follow-up or hide uncertainty.

Use honest boundaries: “For the database effect, this transaction protects the invariant; a remote call requires a separate strategy.” If experience is hypothetical, say “I would” or “In this lab”; do not write “I implemented in production” without learner-supplied evidence.

## Technical depth

- **.NET:** state machines, ThreadPool, async I/O, allocation/GC, synchronization, cancellation, and exception behavior rather than API syntax alone.
- **ASP.NET Core:** trace proxy/ingress, middleware, routing, authentication/authorization, endpoint, application/domain/infrastructure, data/external calls, telemetry, and response.
- **EF Core / SQL Server:** use generated SQL, plans, logical reads, selectivity, seeks/scans, tracking/projection, N+1, batching, transactions, locking, isolation, and deadlock evidence where practical. Do not infer performance from query shape alone.
- **Distributed systems:** consider retries, partial failure, duplicate delivery, poison messages, ordering, outbox/inbox, compensation, contracts, scaling, and observability.
- **Azure / cloud:** compare service fit and implications for reliability, security, performance, cost, and operability.
- **Architecture:** make data ownership, communication, dependency direction, transaction/failure boundaries, and deployment consequences explicit.
- **Frontend:** explain browser execution, state/reactivity, rendering, API/auth boundaries, and observable performance; verify framework-version behavior.

## Durable state workflow

The authoritative state is `learning/state.json` with `schema_version: 2`; read local `learning/state.schema.json` and `learning/README.md` before mutating it. The [public guide](../docs/workflow.md) summarizes the workflow. Its `lessons` and `reviews` are distinct histories.

New lesson records include `lesson_id`, `topic_id`, `domain`, `level`, `status`, `created_at`, nullable `completed_at`, `objectives`, `concept_fingerprint`, five-dimension `score` with nullable values, `weak_points`, `review_due`, `source_refs`, `lesson_path`, and `evidence`. Generation starts with all score dimensions null, `completed_at` null, `weak_points` empty, and `review_due` empty.

The lesson front matter is an immutable **generation snapshot**. Later progress lives in state: do not rewrite a lesson's original date or claim it is completed because its solution was delivered. New metadata must match catalog identity, objectives, and fingerprint exactly; make a legitimate catalog extension first when the primary objectives are new.

Use repo commands rather than manually replacing state. The global `--state` override selects another state file when appropriate; keep private learner artifacts out of a public repository.

```bash
# Read candidate recommendation; substitute the learner's date.
python3 scripts/learning.py next --date YYYY-MM-DD

# Save a new validated lesson file first, then register it once.
python3 scripts/learning.py record --lesson lessons/YYYY-MM-DD-topic-id.md --date YYYY-MM-DD

# When the learner begins attempting the registered lesson:
python3 scripts/learning.py start LESSON_ID --date YYYY-MM-DD

# Save real learner evidence before completion; assessment is optional.
python3 scripts/learning.py complete LESSON_ID --date YYYY-MM-DD --evidence /path/to/learner-attempt.md

# Add a performed review to the separate review history.
python3 scripts/learning.py review LESSON_ID --date YYYY-MM-DD --evidence /path/to/retrieval-attempt.md
```

Completion is an attempted learning session supported by evidence, not certification of mastery. Assess each dimension only when that evidence supports it; `--assessment /path/to/assessment.json` may attach an evidence-grounded assessment to completion. Never fill missing dimensions with zero. Keep historical lesson-generation metadata distinct from subsequent state transitions. Do not run completion or review commands merely because they appear in an example.

State writes must be atomic and preserve existing records. Use one writer at a time; atomic replacement does not prevent two writers from overwriting one another's changes. Re-read state before recording a choice; if another session delivered the same objective, resume it or select another. Do not overwrite a prior lesson to conceal duplication.

### Interactive and Mock session progress

Before yielding a question, save its cursor at `learning/sessions/LESSON_ID.md`
using [the session template](SESSION_TEMPLATE.md). With a separate `--state`
profile, use `sessions/LESSON_ID.md` beside that profile's state file. Store the
mode, stage, exact unanswered prompt, next action, sanitized attempt/feedback
and update date. Initial question delivery remains `generated`; call `start`
after a learner attempt. The CLI updates status, not this session note: the agent
must write the note separately, re-read it on resume, and preserve the lesson ID.
Save progress after every attempt/feedback and before yielding the next prompt.
Use temporary-file replacement with one writer. Keep private transcripts outside
the public checkout, and record only sanitized notes. If notes cannot be saved,
return the proposed note and state that durable resume is unavailable.

If filesystem access or mutation is unavailable, deliver the lesson plus the exact proposed lesson metadata/state patch and say **not saved to the repository**. Do not claim persistence, completion, or review scheduling that did not occur. Do not infer learning history from earlier assistant confidence.

## Release checklist for each lesson

- [ ] Source seed and exact section exist; source framing is distinct from the explanation.
- [ ] Primary objectives are semantically new across all delivered records, or the session is explicitly Review/extension.
- [ ] Prerequisites are handled without assuming pending work was learned.
- [ ] Version-sensitive claims have official links, scope, and a real check date, or a clear unverified label.
- [ ] A meaningful challenge, solution, verification method, and reduced-support task exist for Full lesson.
- [ ] At least one failure mode and alternative decision are explained.
- [ ] Interview answers are direct, concise, defensible, and honest about boundaries/experience.
- [ ] English is primary; optional Vietnamese support is brief and purposeful.
- [ ] Expected results are separated from checks actually run.
- [ ] Scores, completion dates, and review events are supported by learner evidence.
- [ ] Lesson metadata matches durable state; persistence succeeded or the unsaved patch is explicit.
