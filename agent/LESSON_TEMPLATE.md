---
layout: default
title: Focused Lesson Template
---

# Focused Lesson Template

Use with [the skill](SKILL.md) and [the method](INTERVIEW_METHOD.md). This is a template, not a delivered lesson. Replace every placeholder with source-grounded content; do not register this file in state. The default is **one objective in 30–45 minutes**, with at least half reserved for practice/retrieval. Optional depth is outside that budget.

Full lesson includes all solutions, separately expandable and closed by default. Interactive presents A and the first challenge, registers once and **waits** before revealing answers. Resume that same lesson ID. Review reuses an existing ID and records a separate evidence-backed review. Mock asks one question at a time before model answers or assessment.

## Front matter

Save as `lessons/YYYY-MM-DD-topic-id.md`. Remove the code fence in the actual file. Keep ISO dates quoted.

```yaml
---
layout: lesson
lesson_format: focused-v1
title: "<Concrete problem the learner will solve>"
lesson_id: "YYYY-MM-DD-<topic_id>"
topic_id: "<catalog topic ID>"
domain: "<catalog domain>"
level: foundation
mode: full-lesson
created_at: "YYYY-MM-DD"
status: generated
primary_objective: "<One observable capability, not a list of independent topics>"
duration_minutes: 40
practice_minutes: 28
prerequisites_note: "<Actual prior knowledge and runtime needed; do not assume mastery>"
objectives:
  - "<Catalog primary objective, copied exactly>"
  - "<Catalog supporting acceptance criterion, copied exactly>"
concept_fingerprint:
  - "<catalog-concept-1>"
  - "<catalog-concept-2>"
  - "<catalog-concept-3>"
source_refs:
  - "sources/<file>.md#<exact-section>"
  - "https://<official-behavior-reference>"
---
```

Use catalog level `foundation | senior | architect`, 2–4 objectives and 3–7 fingerprint concepts. All criteria serve the single main capability. Identity/objectives/fingerprint agree exactly with the catalog; add a narrowly scoped, source-linked entry first if an existing topic is too broad. Compare primary objectives semantically across delivered lessons, including pending ones. Never relabel an old objective as new.

The layout displays the title, objective, duration and prerequisites: **do not add another H1 in the body**. Metadata is the generation snapshot. Keep `status: generated`; actual attempts, completion, scores and reviews belong in state. Do not rewrite original delivery dates when refactoring.

The following six H2s and explicit Kramdown IDs are required for navigation. Copy their IDs unchanged. End every step with a meaningful next action. Keep questions/tasks outside disclosure sections. Scope, dependencies and any unverified behavior must be visible near the relevant task.

## A · Set the goal — 2 minutes
{: #goal }

**After this lesson, you can:** `<one mechanism/decision you can apply and verify>`.

Show the concrete production situation needing it. Define unfamiliar terms before requiring their use.

| Lesson card | Value |
| --- | --- |
| Lesson / topic IDs | `<IDs matching metadata>` |
| Domain / level / ring | `<catalog values>` |
| Source seed | `<exact source question/section with relative link>` |
| Selection | `<why now, prerequisites, and what is new compared with delivered objectives>` |
| Core / optional | `<30–45 minutes; active practice minutes; optional material excluded>` |
| Mode | Full lesson |

**Success checks:** 2–4 observable criteria supporting the one objective. Explain version/workload/ownership assumptions and boundaries. If prerequisite evidence is missing, offer the required foundation or resume it; don't assume a generated prerequisite is learned.

**Next:** [Predict the outcome](#predict).

## B · Predict first — 4 minutes
{: #predict }

Give a short faulty implementation, incident or constrained design choice. Include concrete input, starting state and one interruption. Ask for the predicted outcome and causal reason **before execution or explanation**. Add 1–2 prerequisite recall prompts if useful.

**Challenge:** `<specific repair, diagnosis or decision with success criteria>`.

Record confidence separately from correctness. An unanswered prompt is not a grade.

**Next:** [Understand the mechanism](#model).

## C · Understand why — 6 minutes
{: #model }

Explain **problem → cause → mechanism → concrete trace → boundary**. Use one invariant, execution flow or state transition. Show one failure/alternative and connect the abstract term to that state. Explain why the key step matters. Avoid introducing unrelated concepts.

Place direct official citations and scope next to version-dependent claims. A short Vietnamese Note is optional when it clarifies a difficult mental model; do not translate everything.

**Next:** [Try the task](#practice).

## D · Try the lab — 16 minutes
{: #practice }

State prerequisites, safe environment, files/sample inputs, exact commands or inspection path, acceptance criteria and expected outputs. Prefer the project's stack. Label a portable substitute's scope; it cannot validate a different runtime's behavior. Architecture/behavioral lessons may use an inspectable design or truthful answer artifact.

**Attempt:** `<one meaningful repair/query/log investigation/design task; don't ask only to copy>`.

**Evidence question:** What observation or failure test supports your conclusion?

<details markdown="1" data-answer>
<summary>Complete worked solution — open after trying</summary>

`<Full executable code/commands or complete design/response, not just hints>`

Explain why key steps preserve the invariant or meet the constraint. Distinguish pseudocode from executable code. State what was actually checked during preparation.

</details>

**Transfer:** `<same mechanism, new input/context/constraint with fewer hints>`.

<details markdown="1" data-answer>
<summary>Transfer answer guide</summary>

`<Usable solution/trace and test that distinguish understanding from copying>`

</details>

**Next:** [Check the evidence](#verify).

## E · Verify and correct — 6 minutes
{: #verify }

| Case | Expected result | Observable evidence |
| --- | --- | --- |
| Happy path | `<result>` | `<test/output/state>` |
| Meaningful failure | `<result>` | `<test/output/state>` |
| Boundary/replay/changed constraint | `<result>` | `<test/output/state>` |

**Actually run during preparation:** `<commands, date, observed results and important untested limits>`.

Compare the B prediction with the outcome. Explain one likely misconception through the trace; call it a learner weakness only if an actual attempt supports that conclusion. Correct the precise gap and ask for a reattempt of that step. Reference execution is author evidence, not learner evidence.

**Production twist:** `<one failure/constraint, recovery path and observable signal>`.

| Option | When suitable | Trade-off / guarantee boundary | Validation |
| --- | --- | --- | --- |
| `<preferred>` | `<constraint>` | `<cost/failure>` | `<evidence>` |
| `<alternative>` | `<condition changing choice>` | `<cost/failure>` | `<evidence>` |

**Next:** [Explain without notes](#recall).

## F · Say it and recall — 6 minutes
{: #recall }

**Interview question:** `<source-grounded English question>`.

**Likely assessment intent:** `<inference, not a universal interviewer rule>`.

Try an own 30-second answer, then 90 seconds. Include a direct claim, mechanism, concrete example, trade-off, failure and evidence. Measure speech time. No invented production experience.

<details markdown="1" data-answer>
<summary>Short and senior model answers, follow-ups and bridge</summary>

`<Complete 30-second and 90-second answers in English>`

**Follow-up 1:** `<deeper mechanism question and defensible answer>`.

**Follow-up 2:** `<failure/alternative question and defensible answer>`.

**Optional bridge:** `<related topic after answering completely, plus its boundary and a prepared answer>`. Answer direct follow-ups first; do not promise to avoid probing.

</details>

<button type="button" class="button button-secondary" data-close-answers disabled>Close answers for recall</button>
<p id="recall-status" role="status" aria-live="polite">Close the explanation or cover it. Answer without notes.</p>

1. `<Recall the invariant/mechanism>`
2. `<Apply it to a changed failure>`
3. `<Choose between related alternatives or defend a boundary>`

<details markdown="1" data-answer>
<summary>Retrieval guide — open after answering</summary>

`<Three concise answers, distinct from the prompts>`

</details>

### Evidence, rubric and learning record

Ask for a real attempt: own artifact/output, corrected prediction and explanation. Assess only supported dimensions with the [0–4 rubric](../agent/INTERVIEW_METHOD.md#evidence-based-feedback).

| Dimension | Evidence | Delivery score |
| --- | --- | --- |
| Technical | Correct mechanism and limits | `null` |
| Reasoning | Justified decision and alternative | `null` |
| Implementation | Own working artifact and checks | `null` |
| Operations | Failure, recovery and observation | `null` |
| Communication | Direct answer and defended follow-ups | `null` |

State whether lesson/state were actually saved. Initial record: `generated`, original delivery date, `completed_at: null`, all scores null, `weak_points: []`, `review_due: []`, `evidence: []`. Reuse metadata identity rather than adding a conflicting copy. If writes are blocked, return the exact proposed patch and say **not saved to the repository**.

Explain D+1/3/7/14/30 from evidenced completion, separate review events and evidence-backed adjustment of unperformed intervals. The public site's reading bookmark does not update repo state. **Next:** submit evidence or use [the state workflow](../docs/workflow.md).

## Optional depth and sources

<details markdown="1" data-answer>
<summary>Optional advanced extension — outside the core budget</summary>

`<Source-linked advanced implementation/scale question, its new objective and untested boundaries>`

</details>

<details markdown="1">
<summary>Provenance and dated verification</summary>

| Claim / seed | Source | Applicability | Actually checked on | Status |
| --- | --- | --- | --- | --- |
| Interview seed | `<exact local source link>` | Question framing | `<read date>` | Not an authoritative answer |
| Technical behavior | `<direct official reference>` | `<product/version/scope>` | `<actual verification date>` | Verified / unverified |

Do not redate old checks or equate documentation verification with execution. Keep significant unverified scope visible in the core as well.

</details>
