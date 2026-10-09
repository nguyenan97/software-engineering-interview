---
layout: default
title: Lesson Template
---

# Lesson Template

Use this template with [the skill](SKILL.md) and [the learning/interview method](INTERVIEW_METHOD.md). Replace every placeholder with source-grounded content. This file is a template, not a generated lesson; do not register it in learning state.

The following stages describe a **Full lesson**. For Interactive, deliver the card and first challenge, register that session once, then wait for an attempt. Resume the same lesson ID on later turns. For Review, use an existing lesson ID and separate review history. For Mock interview, ask one question at a time before showing model answers or grades.

## File metadata

Save the completed lesson as `lessons/YYYY-MM-DD-topic-id.md`. Begin it with YAML front matter in this format (remove the surrounding code fence in the actual file):

```yaml
---
layout: default
title: "<Clear problem-oriented title>"
lesson_id: "YYYY-MM-DD-<topic_id>"
topic_id: "<stable catalog topic ID>"
domain: "<catalog domain>"
level: "foundation"
created_at: "YYYY-MM-DD"
status: generated
mode: full-lesson
objectives:
  - "<Observable outcome 1, copied exactly from the selected catalog topic>"
  - "<Observable outcome 2, copied exactly from the selected catalog topic>"
concept_fingerprint:
  - "<catalog-concept-1>"
  - "<catalog-concept-2>"
  - "<catalog-concept-3>"
source_refs:
  - "sources/<source-file>.md"
  - "https://<direct-official-documentation-url>"
---
```

Use `foundation | senior | architect` for level, 2–4 objectives, and 3–7 fingerprint concepts. Identity, objectives, and fingerprint must agree exactly with `curriculum/catalog.json`; extend the catalog first for a genuinely new topic. Match the local delivery date to `lesson_id`, filename, `created_at`, and the record command. Quote ISO dates so that the YAML parser treats them as strings.

The front matter is the **generation snapshot**, not the current learner state. Keep `status: generated` in the original file; `learning/state.json` records later attempts, completion, assessment, and reviews. Do not confuse a populated solution with evidence of completion.

## Stage 0 — Lesson Card

| Field | Value |
| --- | --- |
| Lesson ID | `<date-topic_id>` |
| Topic ID | `<topic_id>` |
| Domain / level / ring | `<domain>` / `<foundation, senior, or architect>` / `<A, B, or C>` |
| Mode | Full lesson |
| Time budget | `<practical duration; reserve most time for application>` |
| Source seed | `<relative link and exact source section/question>` |
| Prerequisites | `<completed catalog prerequisites; optional foundation support>` |

**Selection reason:** State which source question this develops, why it is appropriate now, and how its primary objectives differ from delivered lessons. Distinguish a new objective from a supporting concept being reinforced.

**By the end, you should be able to:**

1. `<Observable outcome 1>`
2. `<Observable outcome 2>`
3. `<Optional outcome 3>`
4. `<Optional outcome 4>`

State important scope assumptions: framework/product version when relevant, ownership, workload, and what the lesson's guarantee covers.

## Stage 1 — Cold Start

Spend `<short time budget>` answering without notes before reading the explanation.

1. `<Retrieve prerequisite or previously learned concept>`
2. `<Explain a causal mechanism or compare two related options>`
3. `<Optional application question>`

**Challenge:** Present a realistic faulty implementation, incident, query, design, or behavioral situation. Give concrete inputs, constraints, and the observable task. Ask the learner to predict an outcome and justify it before offering the solution.

Record confidence separately from correctness. An unanswered question identifies a possible need for teaching; it is not proof of a weakness or a score of zero.

## Stage 2 — Core Model

Explain the minimum theory needed to solve the challenge:

- Define the concept in clear language.
- State the invariant or the decision the mechanism supports.
- Trace a concrete input through execution/state/data ownership.
- Show one interruption, invalid input, or alternative condition.
- Explain the boundary of the guarantee.

Use a compact diagram if it improves the explanation. Connect abstract terms to the concrete trace. Place direct official citations near version-sensitive claims.

**Self-explanation prompt:** `<Ask why one critical step works and what breaks if it is removed.>`

### Vietnamese Note (optional)

`<Short semantic clarification for a difficult mental model; preserve established English terms. Remove this block when unnecessary.>`

## Stage 3 — Hands-On Lab

### Setup and task

Specify dependencies, versions/applicability, setup instructions, sample data, safe scope, and the task. Use meaningful code, queries, diagnostics, a design artifact, or a truthful behavioral response. State the required invariant or acceptance criteria.

**Attempt first:** `<A concrete implementation/debugging/design task with a time budget.>`

### Worked solution

Provide a complete, usable solution and explain why its important steps meet the constraints. Include exact commands or code where relevant. Do not label pseudocode executable. Distinguish prerequisites for running from commands actually run.

### Verification

| Case | Expected result | What to inspect |
| --- | --- | --- |
| Normal input | `<result>` | `<observable artifact>` |
| Boundary or invalid input | `<result>` | `<observable artifact>` |
| Concurrent/repeated/failed execution where relevant | `<result>` | `<observable artifact>` |

**Checks performed while preparing:** `<Actual checks and results, or a clear statement that execution was unavailable.>`

Expected results are a test plan, not observed evidence. Include a failure injection or contrasting case when it tests the mechanism more meaningfully than another happy-path example.

### Reduced-support task

Change one important constraint and remove hints: `<Independent task requiring transfer rather than copying.>`

Provide an answer guide later in the Full lesson so it remains self-contained. In Interactive mode, wait for the learner's independent attempt before showing it.

## Stage 4 — Production Twist

Introduce a realistic constraint such as more replicas, a dependency outage, duplicate delivery, query regression, token expiry, increasing data volume, or a cost ceiling.

| Option | Suitable condition | Principal cost/failure boundary | Validation |
| --- | --- | --- | --- |
| `<Preferred option>` | `<condition>` | `<cost or failure>` | `<test/metric/trace>` |
| `<Alternative>` | `<condition changing the choice>` | `<cost or failure>` | `<test/metric/trace>` |

Explain observable signals, the recovery path, and one decision that changes under the new constraint. Do not claim a performance improvement without measurement.

**Architect extension:** `<Optional source-linked extension involving ownership, consistency, security, reliability, cost, or deployment.>` Label its objective as an extension rather than silently treating it as a completed new lesson.

## Stage 5 — Interview Round

**Primary question:** `<Natural English question matching the source intent.>`

**Likely assessment intent:** `<What the interviewer is trying to learn; identify this as an inference rather than a universal rule.>`

### 30-second answer

`<Direct claim, mechanism, important boundary; approximately 3–4 clear sentences.>`

### 90-second senior answer

`<Direct claim → mechanism → example → trade-off and validation. Include one relevant assumption. Use hypothetical wording unless learner experience is documented.>`

### Deeper follow-ups and defense

1. `<How does the mechanism work?>` — `<Defensible answer or evidence path.>`
2. `<What fails?>` — `<Specific case and resulting state.>`
3. `<Why not the alternative?>` — `<Constraint and condition changing the choice.>`
4. `<How would you validate it?>` — `<Relevant evidence without invented results.>`
5. `<What changes at scale?>` — `<Bottleneck hypothesis and measurement.>`

**Optional bridge:** `<One relevant adjacent topic after the direct answer is complete.>` Explain the connection and prepare one honest follow-up answer. Do not promise to prevent deeper questions or use the bridge to evade one.

For behavioral questions, replace the technical sequence with genuine STAR plus reflection. A fictional model is labeled fictional and must not become claimed learner experience.

## Stage 6 — Feedback and Self-Assessment

No learner evidence means **no assigned scores or diagnosed weaknesses**. Provide the rubric and criteria, then request a real attempt when assessment is wanted.

| Dimension | Evidence to assess | Score |
| --- | --- | --- |
| Technical | Correct mechanism and boundaries | `null` until observed |
| Reasoning | Justified choice and alternatives | `null` until observed |
| Implementation | Relevant code/query/design correctness and checks | `null` until observed |
| Operations | Failure handling, recovery, and observability | `null` until observed |
| Communication | Direct, clear, ordered, responsive explanation | `null` until observed |

Use the 0–4 anchors from [the interview method](INTERVIEW_METHOD.md). If evidence exists, cite the relevant part of the attempt, explain the score, correct one precise gap, and give a reattempt. Unobserved dimensions stay null.

## Stage 7 — Retrieval Close

Close the explanation and answer these prompts from memory:

1. `<Recall the invariant or mechanism.>`
2. `<Apply it to a new failure/constraint.>`
3. `<Distinguish the preferred option from an alternative.>`
4. `<Optional evidence/operations prompt.>`
5. `<Optional concise spoken-answer prompt.>`

Review at **D+1, D+3, D+7, D+14, and D+30 after completion**. Actual dates are written to learning state only when completion has supporting evidence. Use different examples and fewer hints over time. A review does not count as a new lesson.

### Answer guide

Place concise answers to the reduced-support task and retrieval close here, separate from the questions. This keeps Full lesson self-contained while allowing self-testing first. Do not include this guide in the first Interactive/Mock interview turn.

## Stage 8 — Learning Record

State whether the file and record were actually saved. Link to authoritative state when writable. At initial delivery:

```yaml
lesson_id: "<date-topic_id>"
status: generated
created_at: "YYYY-MM-DD"
completed_at: null
score:
  technical: null
  reasoning: null
  implementation: null
  operations: null
  communication: null
weak_points: []
review_due: []
evidence: []
```

The remaining identity, objectives, fingerprint, source references, and lesson path are supplied by the metadata and state record. Do not insert a second conflicting identity block. To begin, complete, or review the lesson, follow [the durable-state commands](../docs/workflow.md) with actual evidence.

If saving is blocked, include the proposed lesson metadata and exact proposed state entry/patch; say **not saved to the repository**. A generated date never stands in for the completion date.

## Sources and Verification

| Claim or seed | Source | Applicability/version | Verified on | Status |
| --- | --- | --- | --- | --- |
| Source interview question | `<relative source link and section>` | Source framing | `<read date>` | Interview seed, not an authoritative answer |
| `<Version-sensitive technical claim>` | `<direct official URL>` | `<product/version/condition>` | `<actual check date>` | Verified or explicitly unverified |

Record enough detail for another reader to assess the claim and its limits. Do not claim that every statement was independently verified merely because a bibliography exists.
