---
layout: default
title: SQL Server and Data Performance
---

# SQL Server and Data Performance

> Normalized interview material with identifying context removed.

## SQL objects

1. Compare stored procedures, functions and views.
2. Why would you use a stored procedure?
3. Why would you use a view?
4. When should logic live in a stored procedure versus application code?
5. How are parameters passed to stored procedures?
6. What are database triggers, what types exist, and when are they appropriate?

## Indexing

1. What index types are commonly used in SQL Server?
2. Compare clustered and nonclustered indexes.
3. What are the advantages and costs of indexes?
4. How does an index work conceptually?
5. When should you create an index?
6. When can an index make the system slower?
7. How do composite index key order and selectivity affect a query?
8. What is a covering index and when is `INCLUDE` useful?
9. Explain index seek, scan and key lookup.
10. How do write-heavy workloads change your indexing strategy?

## Query optimization

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

## Transactions and concurrency

1. Explain transactions and commit/rollback behavior.
2. Explain database concurrency.
3. Compare optimistic concurrency and pessimistic locking.
4. Explain row versioning.
5. Explain common transaction isolation levels and their trade-offs.
6. How do higher isolation levels affect blocking and throughput?
7. What is a deadlock?
8. How would you diagnose the root cause of a deadlock?
9. How would you reduce deadlock probability?
10. How should applications respond when SQL Server selects a deadlock victim?

## Bulk data

1. How would you insert 10,000+ records efficiently?
2. Compare row-by-row insert, batching and bulk copy approaches.
3. How do transaction size, logging, indexes and constraints affect bulk-write performance?
4. How would you validate and import a large dataset without excessive memory usage?
5. If processing fails late in the import, when should you rollback everything versus retain valid rows and report failures?

## SQL exercises

1. Given `Department` and `Employee` in a one-to-many relationship, return departments having more than three employees.
2. Explain whether a `LEFT JOIN` can be rewritten as a `RIGHT JOIN` and what must change for the result set to remain equivalent.
3. Compare primary key and unique constraints.
4. Discuss nullable values and uniqueness semantics.
5. Diagnose a slow stored procedure using execution evidence rather than guesswork.
