---
layout: default
title: ASP.NET Core, API, EF Core and LINQ
---

# ASP.NET Core, API, EF Core and LINQ

> Technical content only. Personal, organization and project identifiers were removed during normalization.

**Source status:** normalized interview prompts, not verified technical answers. Stable IDs preserve this privacy-safe corpus; no removed identities are reconstructed.

Questions are grouped by learning level inside their original sections. Canonical curriculum links consolidate overlapping wording into one topic. Level labels express intended lesson depth, not a claim about any interviewer.

[Curriculum index](../curriculum/index.md) · [Source coverage and gaps](../curriculum/source-coverage.md)

## ASP.NET Core request pipeline

### Foundation

<a id="q001"></a>
**S02-Q001** · original question 1 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

What is middleware and how does the middleware pipeline work?

<a id="q002"></a>
**S02-Q002** · original question 2 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

How do you implement custom middleware?

<a id="q003"></a>
**S02-Q003** · original question 3 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

How does middleware ordering affect routing, authentication, authorization and exception handling?

<a id="q004"></a>
**S02-Q004** · original question 4 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

Compare middleware and MVC filters.

<a id="q005"></a>
**S02-Q005** · original question 5 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

What are action filters and when should they be used?

<a id="q006"></a>
**S02-Q006** · original question 6 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

Draw the end-to-end lifecycle of a request from client to API, application layer, database/external dependency and response.

<a id="q007"></a>
**S02-Q007** · original question 7 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

Explain MVC routing.

<a id="q008"></a>
**S02-Q008** · original question 8 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

Explain the MVC request/page lifecycle.

<a id="q009"></a>
**S02-Q009** · original question 9 · [Request pipeline, middleware and filters](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline)

How do you handle unhandled exceptions in an API?

<a id="q010"></a>
**S02-Q010** · original question 10 · [HTTP contracts, validation and MVC state](../curriculum/domains/aspnet-api.md#aspnet-http-contracts)

How should validation be implemented for incoming models?

<a id="q011"></a>
**S02-Q011** · original question 11 · [HTTP contracts, validation and MVC state](../curriculum/domains/aspnet-api.md#aspnet-http-contracts)

What is the difference between RESTful APIs and server-rendered MVC?

<a id="q012"></a>
**S02-Q012** · original question 12 · [HTTP contracts, validation and MVC state](../curriculum/domains/aspnet-api.md#aspnet-http-contracts)

What are the advantages and trade-offs of REST APIs?

## HTTP and API design

### Foundation

<a id="q013"></a>
**S02-Q013** · original question 1 · [HTTP contracts, validation and MVC state](../curriculum/domains/aspnet-api.md#aspnet-http-contracts)

Which HTTP method should be used for file upload and why?

<a id="q014"></a>
**S02-Q014** · original question 2 · [HTTP contracts, validation and MVC state](../curriculum/domains/aspnet-api.md#aspnet-http-contracts)

When is session state appropriate?

<a id="q015"></a>
**S02-Q015** · original question 3 · [HTTP contracts, validation and MVC state](../curriculum/domains/aspnet-api.md#aspnet-http-contracts)

Which HTTP status codes represent redirects and how do temporary and permanent redirects differ?

<a id="q016"></a>
**S02-Q016** · original question 4 · [HTTP contracts, validation and MVC state](../curriculum/domains/aspnet-api.md#aspnet-http-contracts)

Explain `ViewData`, `ViewBag`, and `TempData` in MVC-style applications.

### Senior

<a id="q017"></a>
**S02-Q017** · original question 5 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

How would you design a long-running API operation so the caller does not wait for processing to complete?

<a id="q018"></a>
**S02-Q018** · original question 6 · [Idempotent APIs and large-file job submission](../curriculum/domains/aspnet-api.md#aspnet-idempotent-operations)

How do you make an API operation idempotent when clients can retry or spam the same request?

## Background processing

### Senior

<a id="q019"></a>
**S02-Q019** · original question 1 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

When should work move from the request path to a background job?

<a id="q020"></a>
**S02-Q020** · original question 2 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

Compare `IHostedService`, `BackgroundService`, scheduled jobs and external queue-based workers.

<a id="q021"></a>
**S02-Q021** · original question 3 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

How would you schedule recurring work?

<a id="q022"></a>
**S02-Q022** · original question 4 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

How do you handle retries, cancellation, graceful shutdown and duplicate execution?

<a id="q023"></a>
**S02-Q023** · original question 5 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

What changes when multiple application instances run the same scheduler?

## LINQ and EF Core

### Foundation

<a id="q024"></a>
**S02-Q024** · original question 1 · [LINQ execution and query translation](../curriculum/domains/ef-linq.md#ef-query-execution)

Compare `First`, `FirstOrDefault`, `Single`, and `SingleOrDefault`.

<a id="q025"></a>
**S02-Q025** · original question 2 · [LINQ execution and query translation](../curriculum/domains/ef-linq.md#ef-query-execution)

Compare `IEnumerable` and `IQueryable` from an execution perspective.

<a id="q026"></a>
**S02-Q026** · original question 3 · [LINQ execution and query translation](../curriculum/domains/ef-linq.md#ef-query-execution)

Explain deferred execution and query translation.

### Senior

<a id="q027"></a>
**S02-Q027** · original question 4 · [EF loading, tracking and query shape](../curriculum/domains/ef-linq.md#ef-loading-performance)

Compare Lazy Loading, Eager Loading, and Explicit Loading.

<a id="q028"></a>
**S02-Q028** · original question 5 · [EF loading, tracking and query shape](../curriculum/domains/ef-linq.md#ef-loading-performance)

How do you configure Eager Loading?

<a id="q029"></a>
**S02-Q029** · original question 6 · [EF loading, tracking and query shape](../curriculum/domains/ef-linq.md#ef-loading-performance)

What does `AsNoTracking()` do and when should it be used?

<a id="q030"></a>
**S02-Q030** · original question 7 · [EF loading, tracking and query shape](../curriculum/domains/ef-linq.md#ef-loading-performance)

Explain server-side versus client-side evaluation.

<a id="q031"></a>
**S02-Q031** · original question 8 · [EF loading, tracking and query shape](../curriculum/domains/ef-linq.md#ef-loading-performance)

How do projection and generated SQL affect performance?

<a id="q032"></a>
**S02-Q032** · original question 9 · [EF loading, tracking and query shape](../curriculum/domains/ef-linq.md#ef-loading-performance)

What causes N+1 queries and how do you detect them?

<a id="q033"></a>
**S02-Q033** · original question 10 · [DbContext, optimistic concurrency and repository boundaries](../curriculum/domains/ef-linq.md#ef-context-concurrency)

Explain optimistic concurrency and row-version based conflict detection.

<a id="q034"></a>
**S02-Q034** · original question 11 · [DbContext, optimistic concurrency and repository boundaries](../curriculum/domains/ef-linq.md#ef-context-concurrency)

How should `DbContext` lifetime be managed in a web application?

<a id="q035"></a>
**S02-Q035** · original question 12 · [DbContext, optimistic concurrency and repository boundaries](../curriculum/domains/ef-linq.md#ef-context-concurrency)

When is raw SQL or a stored procedure justified instead of LINQ?

## Large-file processing scenario

**Source scenario · Senior**

Design a flow for importing a large file containing tens of thousands of records:

- avoid holding an HTTP request open until processing finishes;
- stream or chunk the input where appropriate;
- validate format and business rules;
- choose between all-or-nothing transaction and partial-success processing;
- perform bulk database writes efficiently;
- generate a validation/error report;
- prevent duplicate jobs when the same file is submitted repeatedly;
- prevent duplicate records both within the file and against existing data;
- expose processing status to the caller;
- make retries safe.

Possible technologies raised by the source notes include background jobs, message queues, `SqlBulkCopy`, EF bulk operations, unique constraints and idempotency mechanisms. Treat these as design options, not universal answers.

**Canonical topics:** [Idempotent APIs and large-file job submission](../curriculum/domains/aspnet-api.md#aspnet-idempotent-operations) · [Bulk import, transaction size and validation](../curriculum/domains/sql-data.md#sql-bulk-import)
