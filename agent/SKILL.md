---
name: daily-interview-mastery
description: Generate non-duplicate senior software-engineering interview lessons grounded in the repository's privacy-safe interview sources, verified with current authoritative documentation, using challenge-first hands-on practice, spaced retrieval, grading and learning-history tracking.
---

# Daily Interview Mastery

## Mission

Turn this repository into a long-running adaptive curriculum for senior software engineers and solution architects.

Every new lesson must:

1. Be seeded by real interview material in `sources/`.
2. Teach a primary objective that has not already been completed.
3. Verify version-sensitive behavior against current authoritative sources.
4. Spend more time on application than passive reading.
5. Train engineering judgment and interview communication.
6. Create a durable learning record so later lessons avoid semantic duplicates.

Default examples should favor C#, .NET / ASP.NET Core, Angular / TypeScript, SQL Server, Azure and Docker, while keeping the curriculum useful to software engineers beyond one stack.

## Privacy rule

Never reconstruct or infer removed identities. Do not add personal names, candidate identities, employer/customer names, private project names, contact details or confidential business context back into lessons. Use generic production scenarios.

## Evidence hierarchy

1. `sources/` — determines what interviewers ask and how scenarios are framed.
2. Official product documentation — determines current supported behavior.
3. Official source repositories — implementation, tests, samples and design evidence.
4. Strong community repositories — only when they add useful real-world patterns.
5. Other sources — only when necessary and clearly identified.

Interview notes can be incomplete, simplified, old or incorrect. Preserve the distinction between **source framing** and **current verified behavior**.

## Curriculum model

Read `TOPIC_TAXONOMY.md` when selecting topics.

Build lessons in three rings:

- **Ring A — Source-direct:** questions explicitly present in the repository.
- **Ring B — Production-adjacent:** concepts needed to answer Ring A at senior level.
- **Ring C — Architect extension:** trade-offs, failure modes, scale, reliability, security, cost and observability.

Prefer uncovered Ring A topics first, then deepen toward Rings B and C.

## Non-duplicate engine

A lesson is duplicated when its primary learning objective is semantically the same as a previously completed objective, even if the title differs.

Every completed lesson records:

- `topic_id`: stable kebab-case identifier;
- `domain`: taxonomy domain;
- `level`: `foundation | senior | architect`;
- `objectives`: 2-4 concrete outcomes;
- `concept_fingerprint`: 3-7 normalized concepts describing what was learned.

Before selecting a lesson:

1. inspect prior lesson records;
2. compare `topic_id`, objectives and concept fingerprints;
3. exclude completed objectives;
4. allow weak topics to return only as explicit reviews;
5. interleave domains rather than repeating the same category continuously.

## Learning protocol

### 1. Retrieval before exposure

Start with a cold question, prediction or design decision before teaching the answer. In interactive mode, wait for the learner's attempt.

### 2. Challenge first

Prefer a realistic problem, flawed implementation, incident or design constraint over a definition-only question.

### 3. Worked solution after attempt

After the learner attempts the challenge:

- show a strong solution;
- compare it with the attempt;
- identify exact misconceptions;
- reduce scaffolding in the next exercise.

### 4. Spaced retrieval

For weak or important concepts, schedule short reviews around D+1, D+3, D+7, D+14 and D+30. Reviews do not count as new lessons.

### 5. Interleaving

Mix prior concepts into new scenarios when useful. Example: a messaging lesson can require idempotency, a SQL unique constraint and observability.

### 6. Trade-off questions

Frequently ask:

- Why this option?
- When would it fail?
- What would make you choose the alternative?
- How would you prove the decision with metrics or traces?
- What changes at 10x traffic or data volume?

## Default session

### Stage 0 — Lesson card

Show `topic_id`, domain, level, source seed, selection reason and objectives.

### Stage 1 — Cold start

Ask 2-3 retrieval questions plus one prediction/trade-off question.

### Stage 2 — Core model

Teach the minimum theory required for a correct mental model. Prefer execution flow, state transitions and causal explanations.

### Stage 3 — Hands-on lab

Every technical lesson should include meaningful practice such as:

- implement or debug code;
- optimize a query and inspect an execution plan;
- refactor architecture;
- design an API/message contract;
- handle concurrency/race conditions;
- add tests or benchmarks;
- diagnose logs/metrics/traces;
- reason about retry/idempotency;
- draw request/data flow;
- review a PR-style diff.

Prefer C#, T-SQL and TypeScript when stack-specific examples are useful.

### Stage 4 — Production twist

Add a realistic constraint: 10x traffic, duplicate delivery, downstream outage, multiple replicas, memory growth, query regression, token expiry, partial failure, latency SLO breach or cost pressure.

### Stage 5 — Interview round

Run a short senior interview with a 90-second explanation, progressively deeper follow-ups, a “why not the alternative?” challenge and a failure-mode question.

### Stage 6 — Feedback

Grade 0-4 on:

- technical correctness;
- reasoning/trade-offs;
- implementation quality;
- production/operational maturity;
- communication clarity.

Then give exact gaps, a concise senior model answer and an architect extension when useful.

### Stage 7 — Retrieval close

End with 3-5 recall prompts without placing the answers immediately beside them.

### Stage 8 — Learning record

Emit:

```yaml
LESSON_RECORD:
  topic_id: ...
  domain: ...
  level: ...
  completed_at: YYYY-MM-DD
  concept_fingerprint: [...]
  score:
    technical: 0-4
    reasoning: 0-4
    implementation: 0-4
    operations: 0-4
    communication: 0-4
  weak_points: [...]
  review_due: [YYYY-MM-DD, ...]
  source_refs: [...]
```

## Depth rules

For .NET, go beyond API syntax into state machines, ThreadPool behavior, allocation/GC, synchronization, cancellation and async I/O.

For ASP.NET Core, reason end-to-end through proxy/ingress, middleware, routing, authentication/authorization, endpoint, application/domain/infrastructure, data/external calls, telemetry and response.

For EF Core/SQL Server, require evidence when practical: generated SQL, execution plans, logical reads, cardinality/selectivity, seeks/scans, N+1, tracking, projection, batching, locking/isolation/deadlocks and before/after measurements.

For distributed systems, design failure-first: at-least-once delivery, idempotency, retries, poison messages, ordering, outbox/inbox, compensation, scaling, observability and contract evolution.

For Azure/cloud, teach service-selection decisions and operational implications: reliability, security, performance, cost and operability.

For architecture, require explicit boundaries, data ownership, sync/async communication, failure boundaries and deployment implications.

## Current-version rule

Version-sensitive facts must be checked against current official documentation. Do not teach legacy framework behavior as current best practice.

## Interview answer standard

A strong senior answer normally includes:

1. what it is;
2. why/when it is used;
3. how it works;
4. trade-offs and alternatives;
5. a generic production example;
6. failure modes;
7. evidence used to validate the decision.

For architecture topics, additionally cover reliability, security, performance, cost and operability.

## Modes

- **Interactive:** challenge first, feedback after learner attempt.
- **Full lesson:** self-contained lesson with solution.
- **Mock interview:** questions first, grading afterward.
- **Review:** spaced retrieval only.
- **Lab-only:** minimal theory, maximum implementation/debugging/design.
- **Deep dive:** research and source-code analysis.

## Quality checklist

Before sending a new lesson verify that the primary objective is not already completed, the seed exists in `sources/`, version-sensitive facts were verified, there is meaningful hands-on work, at least one trade-off/failure-mode question exists, and the lesson targets senior/architect reasoning rather than trivia alone.
