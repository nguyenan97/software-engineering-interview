---
layout: default
title: SQL Server and Data Performance
---

# SQL Server and Data Performance

> Normalized interview material with identifying context removed.

**Source status:** normalized interview prompts, not verified technical answers. Stable IDs preserve this privacy-safe corpus; no removed identities are reconstructed.

Questions are grouped by learning level inside their original sections. Canonical curriculum links consolidate overlapping wording into one topic. Level labels express intended lesson depth, not a claim about any interviewer.

[Curriculum index](../curriculum/index.md) · [Source coverage and gaps](../curriculum/source-coverage.md)

## SQL objects

### Foundation

<a id="q001"></a>
**S03-Q001** · original question 1 · [Stored procedures, functions, views and triggers](../curriculum/domains/sql-data.md#sql-objects-boundaries)

Compare stored procedures, functions and views.

<a id="q002"></a>
**S03-Q002** · original question 2 · [Stored procedures, functions, views and triggers](../curriculum/domains/sql-data.md#sql-objects-boundaries)

Why would you use a stored procedure?

<a id="q003"></a>
**S03-Q003** · original question 3 · [Stored procedures, functions, views and triggers](../curriculum/domains/sql-data.md#sql-objects-boundaries)

Why would you use a view?

<a id="q004"></a>
**S03-Q004** · original question 4 · [Stored procedures, functions, views and triggers](../curriculum/domains/sql-data.md#sql-objects-boundaries)

When should logic live in a stored procedure versus application code?

<a id="q005"></a>
**S03-Q005** · original question 5 · [Stored procedures, functions, views and triggers](../curriculum/domains/sql-data.md#sql-objects-boundaries)

How are parameters passed to stored procedures?

<a id="q006"></a>
**S03-Q006** · original question 6 · [Stored procedures, functions, views and triggers](../curriculum/domains/sql-data.md#sql-objects-boundaries)

What are database triggers, what types exist, and when are they appropriate?

## Indexing

### Foundation

<a id="q007"></a>
**S03-Q007** · original question 1 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

What index types are commonly used in SQL Server?

<a id="q008"></a>
**S03-Q008** · original question 2 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

Compare clustered and nonclustered indexes.

<a id="q009"></a>
**S03-Q009** · original question 3 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

What are the advantages and costs of indexes?

<a id="q010"></a>
**S03-Q010** · original question 4 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

How does an index work conceptually?

<a id="q011"></a>
**S03-Q011** · original question 5 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

When should you create an index?

<a id="q012"></a>
**S03-Q012** · original question 6 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

When can an index make the system slower?

<a id="q013"></a>
**S03-Q013** · original question 7 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

How do composite index key order and selectivity affect a query?

<a id="q014"></a>
**S03-Q014** · original question 8 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

What is a covering index and when is `INCLUDE` useful?

<a id="q015"></a>
**S03-Q015** · original question 9 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

Explain index seek, scan and key lookup.

<a id="q016"></a>
**S03-Q016** · original question 10 · [Index design and workload trade-offs](../curriculum/domains/sql-data.md#sql-index-design)

How do write-heavy workloads change your indexing strategy?

## Query optimization

**Source scenario · Senior**

Given a large database where a query joining several tables is slow, explain how you would investigate it.

Topics raised in the source material:

- inspect the generated query;
- execution plans;
- indexing;
- query profiling/monitoring;
- retrieve only required columns and rows;
- cardinality/selectivity;
- SARGability;
- statistics;
- logical reads and duration;
- compare measurements before and after a change.

Do not answer only with “add an index”; explain how evidence determines the optimization.

**Canonical topics:** [Evidence-led SQL query optimization](../curriculum/domains/sql-data.md#sql-query-investigation)

## Transactions and concurrency

### Senior

<a id="q017"></a>
**S03-Q017** · original question 1 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

Explain transactions and commit/rollback behavior.

<a id="q018"></a>
**S03-Q018** · original question 2 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

Explain database concurrency.

<a id="q019"></a>
**S03-Q019** · original question 3 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

Compare optimistic concurrency and pessimistic locking.

<a id="q020"></a>
**S03-Q020** · original question 4 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

Explain row versioning.

<a id="q021"></a>
**S03-Q021** · original question 5 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

Explain common transaction isolation levels and their trade-offs.

<a id="q022"></a>
**S03-Q022** · original question 6 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

How do higher isolation levels affect blocking and throughput?

<a id="q023"></a>
**S03-Q023** · original question 7 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

What is a deadlock?

<a id="q024"></a>
**S03-Q024** · original question 8 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

How would you diagnose the root cause of a deadlock?

<a id="q025"></a>
**S03-Q025** · original question 9 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

How would you reduce deadlock probability?

<a id="q026"></a>
**S03-Q026** · original question 10 · [Isolation, row versioning and deadlocks](../curriculum/domains/sql-data.md#sql-transactions-concurrency)

How should applications respond when SQL Server selects a deadlock victim?

## Bulk data

### Senior

<a id="q027"></a>
**S03-Q027** · original question 1 · [Bulk import, transaction size and validation](../curriculum/domains/sql-data.md#sql-bulk-import)

How would you insert 10,000+ records efficiently?

<a id="q028"></a>
**S03-Q028** · original question 2 · [Bulk import, transaction size and validation](../curriculum/domains/sql-data.md#sql-bulk-import)

Compare row-by-row insert, batching and bulk copy approaches.

<a id="q029"></a>
**S03-Q029** · original question 3 · [Bulk import, transaction size and validation](../curriculum/domains/sql-data.md#sql-bulk-import)

How do transaction size, logging, indexes and constraints affect bulk-write performance?

<a id="q030"></a>
**S03-Q030** · original question 4 · [Bulk import, transaction size and validation](../curriculum/domains/sql-data.md#sql-bulk-import)

How would you validate and import a large dataset without excessive memory usage?

<a id="q031"></a>
**S03-Q031** · original question 5 · [Bulk import, transaction size and validation](../curriculum/domains/sql-data.md#sql-bulk-import)

If processing fails late in the import, when should you rollback everything versus retain valid rows and report failures?

## SQL exercises

### Foundation

<a id="q032"></a>
**S03-Q032** · original question 1 · [Relational SQL exercises and uniqueness](../curriculum/domains/algorithms-debugging.md#algorithms-sql-relations)

Given `Department` and `Employee` in a one-to-many relationship, return departments having more than three employees.

<a id="q033"></a>
**S03-Q033** · original question 2 · [Relational SQL exercises and uniqueness](../curriculum/domains/algorithms-debugging.md#algorithms-sql-relations)

Explain whether a `LEFT JOIN` can be rewritten as a `RIGHT JOIN` and what must change for the result set to remain equivalent.

<a id="q034"></a>
**S03-Q034** · original question 3 · [Relational SQL exercises and uniqueness](../curriculum/domains/algorithms-debugging.md#algorithms-sql-relations)

Compare primary key and unique constraints.

<a id="q035"></a>
**S03-Q035** · original question 4 · [Relational SQL exercises and uniqueness](../curriculum/domains/algorithms-debugging.md#algorithms-sql-relations)

Discuss nullable values and uniqueness semantics.

### Senior

<a id="q036"></a>
**S03-Q036** · original question 5 · [Evidence-led SQL query optimization](../curriculum/domains/sql-data.md#sql-query-investigation)

Diagnose a slow stored procedure using execution evidence rather than guesswork.
