---
layout: lesson
locale: en
translation_key: 2026-10-10-algorithms-department-headcount
title: Count Employees, Not Joined Rows
lesson_id: 2026-10-10-algorithms-department-headcount
topic_id: algorithms-department-headcount
domain: algorithms-debugging
level: foundation
mode: full-lesson
created_at: '2026-10-10'
status: generated
lesson_format: focused-v1
primary_objective: Write and verify a department headcount query that counts the correct
  employees at one row per department.
duration_minutes: 40
practice_minutes: 28
prerequisites_note: Basic tables and SELECT. Join, grouping and NULL are introduced
  here. Python 3.10+ with sqlite3 for the portable lab; SQL Server optional.
objectives:
- Return departments with more than three employees, grouping by department identity
  rather than its display name.
- Count non-null employee identities and preserve zero-child departments when the
  reporting contract requires them.
- Verify headcount with duplicate department names, nullable employee names and exact-threshold
  boundary data.
concept_fingerprint:
- group-by
- having
- aggregation-grain
- non-null-child-count
- outer-join-preservation
- row-filter-placement
source_refs:
- sources/03-sql-data-performance.md#q032
- https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql
- https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql
- https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql
- https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql
- https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/functions/count-transact-sql.md
- https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/select-group-by-transact-sql.md
- https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/select-transact-sql.md
- https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/from-transact-sql.md
checked_at: '2026-10-10'
---

## A · Set the goal — 2 minutes
{: #goal }

**One goal:** write and prove a correct department headcount query. A dashboard's total is useful only when a result row represents the right entity and the count measures the right things.

| Lesson card | Value |
| --- | --- |
| Topic / lesson | `algorithms-department-headcount` / `2026-10-10-algorithms-department-headcount` |
| Domain / level / ring | Algorithms, coding and debugging / foundation / A |
| Source question | [S03-Q032: departments with more than three employees](../sources/03-sql-data-performance.md#q032) |
| Why now | New source-direct foundation objective, no catalog prerequisites, domain rotation after messaging. The broad relational topic was narrowed for one session. |
| Novelty check | Compared objectives, fingerprints and body against the only prior delivered lesson, `messaging-idempotent-consumer`. Counting groups is distinct from atomic inbox processing. That lesson is still `generated`; SQL overlap is supporting technology, not inferred mastery. |
| Mode / time | Full lesson; 40 minutes: A 2, B 4, C 6, D 16, E 6, F 6. D–F provide 28 minutes of practice, checking and retrieval. |

Three success checks serve this one goal: keep same-named departments separate; count employees even with missing names and preserve zero counts when required; verify zero/three/four and nullable-name boundaries. No reviews are due in current state. Read only one language version.

**Assumptions:** each employee belongs to one department; employee IDs are unique and non-null; department names need not be unique. The source question counts **all** employees. Active-only and zero-count reports below are labeled transfer practice, not new original questions.

**Next:** [Predict the output](#predict).

## B · Predict first — 4 minutes
{: #predict }

<div class="task-box" markdown="1">

Write your answer before running or opening solutions.

| DepartmentId | Name | Employees | Non-null employee names |
| --- | --- | ---: | ---: |
| 10 | Platform | 4 | 3 |
| 20 | Platform | 3 | 3 |
| 30 | Support | 0 | 0 |

The starter is:

{% include lab-code/department-headcount-exercise.md %}

1. Which rows and counts will it return? Why?
2. Does “more than three” include a department with exactly three employees?
3. If we group by department ID but keep `COUNT(e.Name)`, is department 10 fixed?

**Practical challenge:** repair the query to return `(DepartmentId, Name, EmployeeCount)`, ordered by ID, with **only** `(10, 'Platform', 4)` for this dataset. Keep your prediction for E.

</div>

**Next:** [Understand the mechanism](#model).

## C · Understand the mechanism — 6 minutes
{: #model }

Think of `GROUP BY` as putting joined rows into labeled baskets. The **aggregation grain** is what one basket represents: here, one department ID. The label displayed on a basket is not its identity; identical department names must not merge departments. This analogy explains grouping, not the database's physical execution plan.

A JOIN matches employee rows to their department. An INNER JOIN keeps matches; a LEFT JOIN also preserves departments without matches, adding a row with employee columns `NULL`. `NULL` means missing/unknown, not the number zero.

| Joined DepartmentId | EmployeeId | Employee name |
| --- | --- | --- |
| 10 | 101 | A |
| 10 | 102 | B |
| 10 | 103 | C |
| 10 | 104 | NULL |
| 20 | 201 / 202 / 203 | D / E / F — three separate rows |
| 30 | NULL | NULL — one LEFT JOIN placeholder |

The three rows for department 20 are abbreviated for space, not one joined row. The placeholder represents a department without an employee; it is not a person.

| Expression in each department group | Department 10 | Department 20 | Department 30 with LEFT JOIN |
| --- | ---: | ---: | ---: |
| `COUNT(*)`: joined rows, including null-containing rows | 4 | 3 | 1 |
| `COUNT(e.Name)`: non-null names | 3 | 3 | 0 |
| `COUNT(e.EmployeeId)`: actual non-null child IDs | 4 | 3 | 0 |

**Logical flow:** match rows (`FROM` / `ON` / `JOIN`) → filter rows (`WHERE`, if any) → make department groups (`GROUP BY`) → count each group → keep groups with count > 3 (`HAVING`) → project columns (`SELECT`) → order (`ORDER BY`). This describes query meaning and name binding, not a mandatory physical sequence. SQL Server may choose another physical plan.

Why `HAVING`? `WHERE` chooses individual input rows; `HAVING` selects aggregated groups. Write the aggregate in `HAVING`, not its SELECT alias, for SQL Server binding rules. Group both selected non-aggregate columns (`DepartmentId`, `Name`) for the documented SQL Server syntax.

**Invariant:** each result row is one department identity; every counted non-null child ID corresponds to one employee in that group. This holds with this single one-to-many join. Another one-to-many join may repeat an employee, so a non-null ID alone no longer establishes one count per person.

For **> 3**, INNER JOIN suffices: zero employees cannot qualify. A LEFT JOIN with `COUNT(e.EmployeeId) > 3` gives the same qualifying departments under these assumptions. Prefer LEFT JOIN when the contract explicitly requires zero-count departments; do not claim either form is always faster.

**Next:** [Repair and run](#practice).

## D · Practice — 16 minutes
{: #practice }

**Environment:** disposable in-memory SQLite via Python 3.10+; no account, pip dependencies or persistent database. SQL syntax is chosen for the project's SQL Server stack. SQLite execution verifies these bounded relational outputs; it does **not** verify SQL Server runtime, collation, plans, performance or concurrent-update behavior.

{% include lab-download.html path='/assets/labs/department-headcount.zip' %}

From a checkout's root, run the starter once:

```sh
python labs/department-headcount/verify.py
```

It intentionally exits nonzero. Edit only `labs/department-headcount/exercise.sql`; keep the six checks. Downloaded ZIP: unzip, enter `department-headcount/`, run `python verify.py` instead.

**Inputs:** the [setup SQL](../labs/department-headcount/setup.sql) has exactly the table above; employee 104 has `Name = NULL` and `IsActive = 0`. The other six are active. Employees 101–104 belong to 10, 201–203 to 20. Each check resets the input.

**Attempt — 10 minutes:** choose the grouping key, counted expression and group filter; add the ID to the result and order by ID. Run again. Explain which edit fixes merging and which fixes undercounting. Do not solve by renaming departments or filling missing names.

**Evidence question:** What output or failure test supports your conclusion? Save your own edited query, output, initial prediction and one explanation.

<details markdown="1" data-answer>
<summary>Complete solution — open after your attempt</summary>

{% include lab-code/department-headcount-solution.md %}

Grouping by identity prevents merging; adding Name to GROUP BY supports selecting it. `COUNT(e.EmployeeId)` counts all four employees in 10 even though one name is absent. `HAVING ... > 3` excludes department 20. INNER JOIN excludes empty department 30, which could not pass this threshold anyway. No active filter is used for the source question.

Reference checks, after trying:

```sh
python labs/department-headcount/verify.py --solution --extensions
```

Expected: six core checks pass. Base output: `(10, 'Platform', 4)`. The included reference is not your attempt; its test output is author evidence.

For a complete unfiltered department report, remove HAVING and preserve unmatched departments:

{% include lab-code/department-headcount-all.md %}

Expected counts are `4 / 3 / 0`. `COUNT(*)` would give `4 / 3 / 1`; here that is a real correctness failure. For the original > 3 requirement, it does not cause an empty department to qualify, so do not exaggerate that failure.

</details>

**Transfer — 6 minutes, fewer hints:** report **every department**, counting **only active employees**, including zero. Then disable all employees in department 20. Write the query and predict both outputs without looking back. This changes the reporting contract, not the underlying counting goal.

<details markdown="1" data-answer>
<summary>Transfer solution and check</summary>

{% include lab-code/department-headcount-transfer.md %}

Put `e.IsActive = 1` in ON: it limits qualifying matches while preserving every left-side department. In WHERE, the NULL placeholder would be filtered out, and a department with only inactive employees would also disappear. `WHERE e.IsActive = 1 OR e.EmployeeId IS NULL` does not fix the inactive-only case: its employees matched before filtering, so there was no placeholder.

Initial output: `(10, 'Platform', 3)`, `(20, 'Platform', 3)`, `(30, 'Support', 0)`. After setting all employees in 20 inactive: counts `3 / 0 / 0`. A WHERE active filter incorrectly loses department 20 and empty department 30. The extension command verifies all three count-report scenarios using the reference files. To test your own variant, replace the transfer SELECT in a disposable local copy and run the extension checks; do not treat reference execution as proof of your query.

</details>

**Next:** [Compare evidence](#verify).

## E · Verify and correct — 6 minutes
{: #verify }

| Case | Expected result | Observable evidence |
| --- | --- | --- |
| Base source task; duplicate names, nullable employee name | Only department 10, count 4 | First and nullable-name checks |
| Exactly three employees per populated department | No qualifying departments | Remove employee 104; exact-threshold check |
| Empty department / all employees removed / empty tables | None qualifies | Empty-department and empty-database checks |
| Department 20 gains employee 204 | Departments 10 and 20 separately, count 4 each | Another-department check |
| All-department report | Counts 4/3/0 | Extension assertion |
| Active report; then all employees in 20 inactive | Counts 3/3/0; then 3/0/0 | Two extension assertions |

**Actually run on 2026-10-10:** `python labs/department-headcount/verify.py` produced **four failures and two passes**; the combined-name count was 6, and the nullable-name-only case returned nothing. `python labs/department-headcount/verify.py --solution --extensions` passed **six core tests and three extension assertions**, on SQLite **3.53.1**. These are author runs, not learner completion evidence. SQL Server execution and performance were **not tested**. Stable COUNT/JOIN/grouping rules were checked in official documentation source; newer version-specific behavior is not asserted.

Compare with B: the starter returns `('Platform', 6)` because it merges two department IDs and counts six non-null names. Fix one misconception precisely: count a non-null person key, not an optional attribute. Reattempt by making *every* employee name NULL. The all-department report must still give counts 4/3/0; the original > 3 query must still return only department 10 with count 4. A mismatch is a reason to revisit C, not evidence of a learner weakness until you submit an attempt.

**Production twist:** an API adds a one-to-many `EmployeeSkill` join to show skills. An employee with two skills appears twice. Decide the counting grain before tuning; inspect joined IDs, then compare with a trusted employee-only count. This twist is an unexecuted design scenario.

| Option | When suitable | Trade-off / boundary | Validation |
| --- | --- | --- | --- |
| Count in the employee-only query; aggregate before another expanding join | Headcount is independent of skills | Extra query/subquery; later joins must still preserve the chosen grain | Fixture with one employee having two skills and another with none |
| `COUNT(DISTINCT e.EmployeeId)` with a join that preserves the intended employees | Distinct people are the exact metric | Deduplication may cost resources; DISTINCT cannot restore employees already removed by an INNER JOIN or filter | Check missing/duplicate IDs, correct row membership; measure actual plan and reads |

If you need only departments with a matching skill, membership changes intentionally; clarify that contract first. Neither option has a measured speed advantage in this lesson.

**Next:** [Close notes and speak](#recall).

## F · Say it and recall — 6 minutes
{: #recall }

**Interview question:** “Given Department and Employee in a one-to-many relationship, return departments having more than three employees.”

**Likely assessment intent (inference):** can you turn cardinality into correct grouping, explain NULL/threshold boundaries and test the result? First write the query; speaking structure does not replace working SQL.

Speak your own answer first, then compare. Aim for 30/90 seconds; time your speech rather than treating the labels as measured durations.

<details markdown="1" data-answer>
<summary>30/90-second model answers, follow-ups and bridge</summary>

**30-second target**

{% include interview/department-headcount-30s.md %}

**90-second target**

{% include interview/department-headcount-90s.md %}

**Reasoning:** start with the solution, defend the grouping key and count expression, then show a boundary and evidence plan. “I would” makes no invented production-experience claim. A senior answer adds validation and an honest performance boundary rather than more keywords.

**Follow-up 1:** “Why not COUNT(*)?” — “With the inner join in the original task and this one-to-many relationship, COUNT(*) is valid because each matched row is an employee. With a left join that includes empty departments, it counts the placeholder as one. COUNT(e.EmployeeId) remains zero for that placeholder.”

**Follow-up 2:** “Why put the active filter in ON?” — “The report must preserve every department. ON restricts which employees match before the left join preserves departments with no qualifying match. WHERE filters joined rows and drops the empty or inactive-only department.”

**Optional bridge, after the complete answer:** “That covers correctness at the department grain. If this query is slow on SQL Server, I would next inspect the actual plan and logical reads before choosing an index.” Prepared boundary: an index beginning with `Employee.DepartmentId` is a candidate for that access pattern, not a guaranteed improvement; compare representative workloads and include write cost. No benchmark or SQL Server plan was run here. Answer direct follow-ups before offering this bridge.

</details>

{% include recall-close.html %}

Without notes:

1. Why can two departments named Platform become one result? What fixes it?
2. What are the three COUNT values for an empty department after LEFT JOIN, and why?
3. How do you count active employees while keeping a department with only inactive employees? Why does WHERE plus “OR child ID IS NULL” still fail?

<details markdown="1" data-answer>
<summary>Retrieval guide — open after answering</summary>

1. Grouping by the display name merges identity groups. Group by department ID and selected non-aggregate name.
2. COUNT(*) = 1, COUNT(employee name) = 0, COUNT(employee ID) = 0: one NULL-extended placeholder, no non-null child attribute.
3. LEFT JOIN with the active condition in ON, then count employee IDs. An inactive-only department already had matches before WHERE; no NULL placeholder was created for the OR clause to rescue.

</details>

### Evidence, rubric and learning record

Submit your own SQL, test output, corrected prediction and an unassisted explanation. Use [the evidence-based 0–4 rubric](../agent/INTERVIEW_METHOD.md#evidence-based-feedback): 0 material error; 1 terms with substantial help; 2 basic correctness; 3 boundaries and evidence; 4 independent defense of alternatives and failures. Unobserved dimensions remain null.

| Dimension | Evidence for this lesson | Score at delivery |
| --- | --- | --- |
| Technical | Explain grouping grain, COUNT and > 3 correctly | `null` |
| Reasoning | Defend INNER/LEFT and active-filter placement | `null` |
| Implementation | Own query and meaningful boundary outputs | `null` |
| Operations | Detect join multiplication and propose a distinguishing check | `null` |
| Communication | Direct English answer and two defended follow-ups | `null` |

**Saved delivery:** canonical English and complete Vietnamese pages share this ID, the catalog objectives, fingerprint, code and sources. Only one record is registered in `learning/state.json`: `status: generated`, `created_at: 2026-10-10`, `completed_at: null`, all five scores null, `weak_points: []`, `evidence: []`, `review_due: []`. Previous history is preserved. Opening answers or a browser bookmark does not update completion.

**Review plan after evidenced completion only:** D+1 explain the count from memory; D+3 repair an active-only report; D+7 change to customer/order counts; D+14 diagnose a multiplying join; D+30 answer and verify a fresh fixture without notes. D is the actual completion date, not today. No calendar due dates or review events have been created.

**Next:** submit sanitized attempt evidence or follow [the durable state workflow](../docs/workflow.md). Completion records participation with evidence, not automatic mastery.

## Sources and dated verification

<details markdown="1">
<summary>Provenance, applicability and actual verification</summary>

| Claim / seed | Source | Scope / checked on | Status |
| --- | --- | --- | --- |
| Interview prompt | [S03-Q032](../sources/03-sql-data-performance.md#q032) | Read 2026-10-10 | Source question, not verified answer |
| COUNT(*) counts rows; COUNT(expression) counts non-null values | [COUNT reader page](https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql); [official Markdown](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/functions/count-transact-sql.md) | Basic SQL Server aggregation; checked 2026-10-10 | Official source read |
| Group columns and HAVING versus WHERE | [GROUP BY reader page](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql); [official Markdown](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/select-group-by-transact-sql.md) | SQL Server grouping rules; checked 2026-10-10 | Official source read |
| Logical binding order differs from physical execution | [SELECT reader page](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql); [official Markdown](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/select-transact-sql.md) | Query meaning and alias scope; checked 2026-10-10 | Official source read |
| LEFT JOIN NULL-extension; ON/WHERE difference | [FROM reader page](https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql); [official Markdown](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/from-transact-sql.md) | SQL Server join semantics; checked 2026-10-10 | Official source read |
| Lab outputs | [Runnable lab](../labs/department-headcount/README.md) | SQLite 3.53.1, executed 2026-10-10 | Six reference tests and three extension assertions passed; starter failed four as intended |

The environment could read `raw.githubusercontent.com/MicrosoftDocs/sql-docs/main/` files, not the live Learn website. The fetched COUNT source has `ms.date: 07/24/2017`; this is a document date, not today's verification date. These official source checks support stable relational rules; they do not establish current-version optimizer behavior or a SQL Server execution result. No version-specific defaults, benchmark or concurrency guarantee is asserted. Practice fixtures and transfer constraints were designed for this lesson and are not source interview facts.

</details>
