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

## Teaching language, translation and privacy

Read [the localization contract](../docs/localization.md). Resolve teaching language by **explicit request → learner_profile.preferred_language → English**. Browser preference is separate and unavailable to a repo agent unless the learner supplies it. Do not claim it was read or written to state. Commands `language --language en|vi --date YYYY-MM-DD` persist an explicit agent preference without changing lesson history.

Support `Viết bài học hôm nay`, `Viết bài học hôm nay bằng tiếng Việt`, `Write today’s lesson in English`, `Chuyển bài đang học sang tiếng Việt`, `Học interactive bằng tiếng Việt` and `Mock interview bằng English, feedback bằng tiếng Việt`.

- Create a canonical English lesson and a complete Vietnamese variant for each new public Full lesson. Use one topic/lesson ID, fingerprint, set of catalog objectives and source refs; only one delivery record. Follow [the lesson template](LESSON_TEMPLATE.md). Localize human explanations and headings naturally, not word-for-word.
- For Interactive/Mock, keep any saved teaching chunks equivalent in both languages as they are revealed. Pending answers must stay out of public artifacts in both locales; closed `<details>` are readable and do not enforce a turn boundary. A language switch translates the pending challenge, not its unrevealed answer.
- Keep runnable code and expected contracts identical, preferably in shared includes backed by lab sources. Translate explanation, challenges, solution reasoning, rubric and retrieval; preserve scope, assumptions and actual verification dates. A translated date never replaces creation or technical verification dates.
- Preserve standard technical terms; define difficult terms naturally in the selected language. In English lessons a short Vietnamese Note remains optional, not a duplicate full translation.
- Interview questions and model speech default to English, with Vietnamese reasoning/feedback when requested. Explicit learner interview-language instructions override that default. Do not require both versions to be read in one session.
- On a switch/resume, read the existing record and session note, resolve `lesson-path LESSON_ID --language en|vi --date YYYY-MM-DD`, and keep the same unanswered prompt, step and ID. Do not generate a new topic or call start/complete/review merely to change language. Keep Interactive answers withheld until the learner attempts them.
- Save session teaching/interview/feedback languages when they differ. If a variant is missing, explain the English fallback and author the real translation of that same lesson; do not substitute a different topic. If writes are blocked, return the proposed files/patch and say unsaved.
- Compare both versions for technical equivalence before saving. Validate locale identities, shared code, source links, six anchors and rendered routes. Structural checks do not establish translation accuracy.
- Never reconstruct removed identities/confidential context, invent experience, or publish sensitive learner evidence. Generic examples and private profiles remain required for privacy.

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

## Focused learning protocol

Apply [the learning method](INTERVIEW_METHOD.md). Retrieval, spacing, worked examples, self-explanation and faded practice have research support; the six-step format and calendar are repository defaults, not scientifically optimal prescriptions.

Each default lesson has **one main objective**, one causal mechanism or decision the learner can practice and verify in **30–45 minutes**. At least half the budget is practice and retrieval. Do not turn a broad catalog topic into a checklist of everything it mentions. Keep 2–4 observable acceptance criteria that serve the single objective; put independent mechanisms, scale and advanced versions in optional depth or a distinct later catalog entry. Never change a delivered record's objectives to conceal repetition.

For a catalog topic too broad for one session, add a narrowly scoped, source-linked catalog entry with distinct objectives/fingerprint before registering it. Respect its prerequisites and compare it semantically with all delivered lessons; narrowing an already taught primary objective does not make it new. Existing generation snapshots may retain broader criteria when refactored; explain this and preserve history.

Use six visible steps with stable IDs:

| Step / ID | Work | Next action |
| --- | --- | --- |
| A · `goal` | One capability, real situation, prerequisites and time budget | Predict a concrete outcome |
| B · `predict` | A faulty implementation, incident or constrained choice; attempt before explanation | Keep prediction and reason |
| C · `model` | Problem → cause → mechanism → example → boundary; one state trace/invariant | Try the lab |
| D · `practice` | Small executable/debugging/design task, inputs, constraints and success checks; then a changed example with fewer hints | Run or inspect evidence |
| E · `verify` | Happy path and failure case; compare prediction with actual checks; correct one evidenced misconception and retry | Explain without notes |
| F · `recall` | Own explanation, 30/90-second answer, two defended follow-ups and three retrieval questions | Submit evidence; schedule later retrieval |

Full lesson includes complete worked solutions, transfer answer guide, model answers and retrieval guide in separate native `<details markdown="1" data-answer>` blocks, closed by default. Questions and tasks remain outside. Advanced material and sources are expandable; important scope or unverified claims stay visible near the relevant task. In Interactive, **wait for the learner's attempt** before revealing the corresponding answer. Behavioral/architecture lessons use a concrete response/design artifact rather than irrelevant code.

Each lab needs an explicit run/inspection path, expected outputs, a happy path, at least one meaningful failure and the question **“What evidence supports your conclusion?”** Prefer the project stack. A lightweight portable lab may isolate its invariant, but label the substitution and guarantee boundary; do not infer SQL Server, broker or concurrent-worker behavior from a different runtime. Label prepared tests, actual author execution and learner evidence separately.

Adapt difficulty using actual attempts: repair a missing prerequisite, correct one precise misconception and let the learner retry the weak step with fewer hints. Never infer proficiency from a title or from reading an answer. Review D+1/3/7/14/30 after evidenced completion; vary examples and keep overdue work visible. Adjust only unperformed review dates with evidence and a recorded reason; no fictional sessions.

## Modes and turn boundaries

| Mode | Behavior | State behavior |
| --- | --- | --- |
| Full lesson (default) | Deliver all stages, worked solution, verification plan, model answers, and rubric. Invite self-testing before reading the solution. | Record as `generated`; no grade or completion without evidence. |
| Interactive | Deliver the card and first challenge; wait. On subsequent turns, evaluate the attempt, reveal the needed explanation/solution, then advance. | Record once as `generated`; mark `in_progress` after the first attempt and resume the same lesson using its saved session note. |
| Review | Ask retrieval/application questions about a recorded lesson; wait before exposing answers unless a full review is requested. | Append a review only after evidence; do not create another new-lesson record. |
| Mock interview | State role and scope, ask one English question at a time, adapt follow-ups, then give evidence-based feedback. | Resume an existing lesson or record a genuinely new source-linked objective once. Save the transcript; score only observed dimensions. |

`Lab-only` and `Deep dive` remain optional variations. Do not switch from Full lesson to Interactive by withholding requested solutions. Do not treat delivery of a model answer as the learner's answer.

## Lesson presentation and navigation

Follow [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md), using `layout: lesson` and `lesson_format: focused-v1`. Put the primary objective, duration and prerequisites in front matter for the lesson header. Use the six stable step IDs so the sidebar, next actions and browser reading bookmark work. Include identity, domain/level/ring, source seed and selection reason in A; supporting acceptance criteria must all serve the main objective.

The public [daily desk](../index.md) offers new lesson, continue reading, review and mock actions. It serves published artifacts, not personalized learner status. New/review/mock prompts are pasted into an agent with repo access; they do not invoke a server. The browser can save a reading step only. Authoritative completion, scores and due dates come from the selected repo state profile. Interactive/Mock resume uses the saved session note, not a browser bookmark.

Keep version verification, provenance, production trade-offs, rubric and learning record in the lesson. Collapse extra detail rather than dropping it. Legacy nine-stage lessons remain readable; new lessons use the focused template.

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

To change an unperformed interval after observing recall evidence, use:

```bash
python3 scripts/learning.py reschedule LESSON_ID --date YYYY-MM-DD --from-date YYYY-MM-DD --to-date YYYY-MM-DD --reason "Observed gap and reason for timing" --evidence /path/to/retrieval-attempt.md
```

This preserves the original completion anchor and an adjustment audit trail; it never creates a review, score or completion. Leave intervals unchanged when evidence does not justify adjustment.

Completion is an attempted learning session supported by evidence, not certification of mastery. Assess each dimension only when that evidence supports it; `--assessment /path/to/assessment.json` may attach an evidence-grounded assessment to completion. Never fill missing dimensions with zero. Keep historical lesson-generation metadata distinct from subsequent state transitions. Do not run completion or review commands merely because they appear in an example.

State writes must be atomic and preserve existing records. Use one writer at a time; atomic replacement does not prevent two writers from overwriting one another's changes. Re-read state before recording a choice; if another session delivered the same objective, resume it or select another. Do not overwrite a prior lesson to conceal duplication.

### Interactive and Mock session progress

Before yielding a question, save its cursor at `learning/sessions/LESSON_ID.md`
using [the session template](SESSION_TEMPLATE.md). With a separate `--state`
profile, use `sessions/LESSON_ID.md` beside that profile's state file. Store the
mode, six-step cursor, exact unanswered prompt, next action, sanitized attempt/feedback
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
- [ ] One primary objective fits 30–45 minutes; at least half is practice/retrieval.
- [ ] Six stable steps, next actions, prerequisites and closed answer sections are present.
- [ ] A meaningful challenge, complete solution, happy/failure checks and reduced-support task exist for Full lesson.
- [ ] At least one failure mode and alternative decision are explained.
- [ ] Interview answers are direct, concise, defensible, and honest about boundaries/experience.
- [ ] Both locale versions preserve the same technical contract; requested teaching language is respected and interview-language defaults are explicit.
- [ ] Expected results are separated from checks actually run.
- [ ] Scores, completion dates, and review events are supported by learner evidence.
- [ ] Lesson metadata matches durable state; persistence succeeded or the unsaved patch is explicit.
