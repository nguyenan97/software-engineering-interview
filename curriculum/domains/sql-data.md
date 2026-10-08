---
layout: default
title: "SQL Server & Data Engineering"
---

# SQL Server & Data Engineering

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="sql-objects-boundaries"></a>
### Stored procedures, functions, views and triggers

`sql-objects-boundaries` · Ring A · foundation

**Learning objectives**

- Compare SQL object contracts and parameter usage.
- Choose database-side or application-side logic from ownership and maintenance constraints.
- Explain trigger risks and when their behavior is required.

**Concept fingerprint:** `stored-procedure`, `sql-function`, `view`, `trigger`, `logic-ownership`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [03-sql-data-performance · q001](../../sources/03-sql-data-performance.md#q001)
- [03-sql-data-performance · q002](../../sources/03-sql-data-performance.md#q002)
- [03-sql-data-performance · q003](../../sources/03-sql-data-performance.md#q003)
- [03-sql-data-performance · q004](../../sources/03-sql-data-performance.md#q004)
- [03-sql-data-performance · q005](../../sources/03-sql-data-performance.md#q005)
- [03-sql-data-performance · q006](../../sources/03-sql-data-performance.md#q006)

<a id="sql-index-design"></a>
### Index design and workload trade-offs

`sql-index-design` · Ring A · foundation

**Learning objectives**

- Explain clustered, nonclustered and covering index roles.
- Choose composite key order from the access pattern.
- Compare seek, scan and lookup evidence with write-maintenance cost.

**Concept fingerprint:** `clustered-index`, `nonclustered-index`, `composite-index`, `covering-index`, `seek-scan-lookup`, `write-cost`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [03-sql-data-performance · q007](../../sources/03-sql-data-performance.md#q007)
- [03-sql-data-performance · q008](../../sources/03-sql-data-performance.md#q008)
- [03-sql-data-performance · q009](../../sources/03-sql-data-performance.md#q009)
- [03-sql-data-performance · q010](../../sources/03-sql-data-performance.md#q010)
- [03-sql-data-performance · q011](../../sources/03-sql-data-performance.md#q011)
- [03-sql-data-performance · q012](../../sources/03-sql-data-performance.md#q012)
- [03-sql-data-performance · q013](../../sources/03-sql-data-performance.md#q013)
- [03-sql-data-performance · q014](../../sources/03-sql-data-performance.md#q014)
- [03-sql-data-performance · q015](../../sources/03-sql-data-performance.md#q015)
- [03-sql-data-performance · q016](../../sources/03-sql-data-performance.md#q016)

## Senior

<a id="sql-query-investigation"></a>
### Evidence-led SQL query optimization

`sql-query-investigation` · Ring A · senior

**Learning objectives**

- Investigate a slow join or stored procedure using plans and measurements.
- Relate cardinality, statistics and SARGability to observed query behavior.
- Prove an optimization with logical reads and duration before and after.

**Concept fingerprint:** `execution-plan`, `cardinality`, `statistics`, `sargability`, `logical-reads`, `query-duration`.

**Prerequisites:** [Index design and workload trade-offs](sql-data.md#sql-index-design)

**Source prompts** (question framing; answers still require verification)

- [03-sql-data-performance · query-optimization](../../sources/03-sql-data-performance.md#query-optimization)
- [03-sql-data-performance · q036](../../sources/03-sql-data-performance.md#q036)

<a id="sql-transactions-concurrency"></a>
### Isolation, row versioning and deadlocks

`sql-transactions-concurrency` · Ring A · senior

**Learning objectives**

- Explain the consistency and throughput consequences of isolation choices.
- Compare optimistic concurrency with pessimistic locking.
- Diagnose a deadlock and design a safe application response.

**Concept fingerprint:** `transaction-atomicity`, `isolation`, `row-versioning`, `blocking`, `deadlock`, `concurrency`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [03-sql-data-performance · q017](../../sources/03-sql-data-performance.md#q017)
- [03-sql-data-performance · q018](../../sources/03-sql-data-performance.md#q018)
- [03-sql-data-performance · q019](../../sources/03-sql-data-performance.md#q019)
- [03-sql-data-performance · q020](../../sources/03-sql-data-performance.md#q020)
- [03-sql-data-performance · q021](../../sources/03-sql-data-performance.md#q021)
- [03-sql-data-performance · q022](../../sources/03-sql-data-performance.md#q022)
- [03-sql-data-performance · q023](../../sources/03-sql-data-performance.md#q023)
- [03-sql-data-performance · q024](../../sources/03-sql-data-performance.md#q024)
- [03-sql-data-performance · q025](../../sources/03-sql-data-performance.md#q025)
- [03-sql-data-performance · q026](../../sources/03-sql-data-performance.md#q026)

<a id="sql-bulk-import"></a>
### Bulk import, transaction size and validation

`sql-bulk-import` · Ring A · senior

**Learning objectives**

- Compare row inserts, batching and bulk copy for a large import.
- Design bounded-memory validation and duplicate-record prevention.
- Justify all-or-nothing or partial-success behavior and recovery.

**Concept fingerprint:** `bulk-copy`, `batching`, `bounded-memory`, `import-validation`, `transaction-size`, `partial-success`.

**Prerequisites:** [Isolation, row versioning and deadlocks](sql-data.md#sql-transactions-concurrency)

**Source prompts** (question framing; answers still require verification)

- [02-aspnet-api-ef · large-file-processing-scenario](../../sources/02-aspnet-api-ef.md#large-file-processing-scenario)
- [03-sql-data-performance · q027](../../sources/03-sql-data-performance.md#q027)
- [03-sql-data-performance · q028](../../sources/03-sql-data-performance.md#q028)
- [03-sql-data-performance · q029](../../sources/03-sql-data-performance.md#q029)
- [03-sql-data-performance · q030](../../sources/03-sql-data-performance.md#q030)
- [03-sql-data-performance · q031](../../sources/03-sql-data-performance.md#q031)

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Engine-version-specific optimizer or row-versioning defaults and tooling configuration.
