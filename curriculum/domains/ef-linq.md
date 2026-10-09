---
layout: default
title: "EF Core & LINQ"
---

# EF Core & LINQ

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="ef-query-execution"></a>
### LINQ execution and query translation

`ef-query-execution` · Ring A · foundation

**Learning objectives**

- Predict execution timing for IEnumerable and IQueryable pipelines.
- Choose terminal operators from cardinality requirements.
- Inspect generated SQL and distinguish translation from local evaluation.

**Concept fingerprint:** `ienumerable-iqueryable`, `deferred-execution`, `query-translation`, `terminal-operators`, `generated-sql`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q010](../../sources/01-csharp-dotnet.md#q010)
- [02-aspnet-api-ef · q024](../../sources/02-aspnet-api-ef.md#q024)
- [02-aspnet-api-ef · q025](../../sources/02-aspnet-api-ef.md#q025)
- [02-aspnet-api-ef · q026](../../sources/02-aspnet-api-ef.md#q026)

## Senior

<a id="ef-loading-performance"></a>
### EF loading, tracking and query shape

`ef-loading-performance` · Ring A · senior

**Learning objectives**

- Detect N+1 queries from command evidence.
- Compare loading, projection and tracking choices for one workload.
- Validate query changes using generated SQL and before/after measurements.

**Concept fingerprint:** `n-plus-one`, `loading-strategies`, `projection`, `tracking`, `query-shape`.

**Prerequisites:** [LINQ execution and query translation](ef-linq.md#ef-query-execution)

**Source prompts** (question framing; answers still require verification)

- [02-aspnet-api-ef · q027](../../sources/02-aspnet-api-ef.md#q027)
- [02-aspnet-api-ef · q028](../../sources/02-aspnet-api-ef.md#q028)
- [02-aspnet-api-ef · q029](../../sources/02-aspnet-api-ef.md#q029)
- [02-aspnet-api-ef · q030](../../sources/02-aspnet-api-ef.md#q030)
- [02-aspnet-api-ef · q031](../../sources/02-aspnet-api-ef.md#q031)
- [02-aspnet-api-ef · q032](../../sources/02-aspnet-api-ef.md#q032)

<a id="ef-context-concurrency"></a>
### DbContext, optimistic concurrency and repository boundaries

`ef-context-concurrency` · Ring A · senior

**Learning objectives**

- Define a DbContext lifetime that fits the unit of work.
- Handle an optimistic-concurrency conflict explicitly.
- Justify repository abstractions or raw SQL from real requirements.

**Concept fingerprint:** `dbcontext-lifetime`, `optimistic-concurrency`, `row-version`, `repository`, `unit-of-work`, `raw-sql`.

**Prerequisites:** [LINQ execution and query translation](ef-linq.md#ef-query-execution)

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q039](../../sources/01-csharp-dotnet.md#q039)
- [01-csharp-dotnet · q040](../../sources/01-csharp-dotnet.md#q040)
- [02-aspnet-api-ef · q033](../../sources/02-aspnet-api-ef.md#q033)
- [02-aspnet-api-ef · q034](../../sources/02-aspnet-api-ef.md#q034)
- [02-aspnet-api-ef · q035](../../sources/02-aspnet-api-ef.md#q035)

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Identity resolution, split-query behavior and DbContext pooling.
