---
layout: default
title: "Algorithms, Coding & Debugging"
---

# Algorithms, Coding & Debugging

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="algorithms-collection-reasoning"></a>
### Collection choice and evidence-led coding

`algorithms-collection-reasoning` · Ring B · foundation

**Learning objectives**

- Implement a generic duplicate-detection or lookup exercise using appropriate collections.
- Explain correctness before comparing resource costs.
- State which complexity claims require implementation or workload assumptions.

**Concept fingerprint:** `arrays`, `hash-map`, `hash-set`, `duplicate-detection`, `coding-evidence`.

**Prerequisites:** [Collections, strings and delegates](dotnet-runtime.md#dotnet-collections-delegates)

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q021](../../sources/01-csharp-dotnet.md#q021)
- [01-csharp-dotnet · q022](../../sources/01-csharp-dotnet.md#q022)

**Scope note:** The coding exercise is production-adjacent practice derived from collection-choice questions; the original corpus does not contain this exact coding task.

<a id="algorithms-sql-relations"></a>
### Relational SQL exercises and uniqueness

`algorithms-sql-relations` · Ring A · foundation

**Learning objectives**

- Write a grouped department/employee query from cardinality requirements.
- Reason about equivalent outer-join rewrites.
- Compare primary keys, unique constraints and nullable-value semantics.

**Concept fingerprint:** `group-by`, `having`, `outer-join`, `primary-key`, `unique-constraint`, `null-semantics`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [03-sql-data-performance · q032](../../sources/03-sql-data-performance.md#q032)
- [03-sql-data-performance · q033](../../sources/03-sql-data-performance.md#q033)
- [03-sql-data-performance · q034](../../sources/03-sql-data-performance.md#q034)
- [03-sql-data-performance · q035](../../sources/03-sql-data-performance.md#q035)

<a id="algorithms-department-headcount"></a>
### Department headcount at the correct aggregation grain

`algorithms-department-headcount` · Ring A · foundation

**Learning objectives**

- Return departments with more than three employees, grouping by department identity rather than its display name.
- Count non-null employee identities and preserve zero-child departments when the reporting contract requires them.
- Verify headcount with duplicate department names, nullable employee names and exact-threshold boundary data.

**Concept fingerprint:** `group-by`, `having`, `aggregation-grain`, `non-null-child-count`, `outer-join-preservation`, `row-filter-placement`.

**Prerequisites:** None required; the lesson introduces join rows and grouping before practice.

**Source prompt:** [03-sql-data-performance · q032](../../sources/03-sql-data-performance.md#q032).

**Scope note:** A focused slice of `algorithms-sql-relations`, added on 2026-10-10
for one 40-minute session. It answers Q032; zero-count and active-count reports
are labeled transfer practice, not additional original interview questions.
It does not teach outer-join rewrites or unique-constraint semantics. The broader
entry remains for source indexing; selection must compare objectives to avoid
teaching this slice again through that entry.

## Senior

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Stacks, queues, trees, graphs, sorting/searching, concurrency coding, code-review and general test-design exercises.
