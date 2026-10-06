---
layout: default
title: ASP.NET Core, API, EF Core and LINQ
---

# ASP.NET Core, API, EF Core and LINQ

> Technical content only. Personal, organization and project identifiers were removed during normalization.

## ASP.NET Core request pipeline

1. What is middleware and how does the middleware pipeline work?
2. How do you implement custom middleware?
3. How does middleware ordering affect routing, authentication, authorization and exception handling?
4. Compare middleware and MVC filters.
5. What are action filters and when should they be used?
6. Draw the end-to-end lifecycle of a request from client to API, application layer, database/external dependency and response.
7. Explain MVC routing.
8. Explain the MVC request/page lifecycle.
9. How do you handle unhandled exceptions in an API?
10. How should validation be implemented for incoming models?
11. What is the difference between RESTful APIs and server-rendered MVC?
12. What are the advantages and trade-offs of REST APIs?

## HTTP and API design

1. Which HTTP method should be used for file upload and why?
2. When is session state appropriate?
3. Which HTTP status codes represent redirects and how do temporary and permanent redirects differ?
4. Explain `ViewData`, `ViewBag`, and `TempData` in MVC-style applications.
5. How would you design a long-running API operation so the caller does not wait for processing to complete?
6. How do you make an API operation idempotent when clients can retry or spam the same request?

## Background processing

1. When should work move from the request path to a background job?
2. Compare `IHostedService`, `BackgroundService`, scheduled jobs and external queue-based workers.
3. How would you schedule recurring work?
4. How do you handle retries, cancellation, graceful shutdown and duplicate execution?
5. What changes when multiple application instances run the same scheduler?

## LINQ and EF Core

1. Compare `First`, `FirstOrDefault`, `Single`, and `SingleOrDefault`.
2. Compare `IEnumerable` and `IQueryable` from an execution perspective.
3. Explain deferred execution and query translation.
4. Compare Lazy Loading, Eager Loading, and Explicit Loading.
5. How do you configure Eager Loading?
6. What does `AsNoTracking()` do and when should it be used?
7. Explain server-side versus client-side evaluation.
8. How do projection and generated SQL affect performance?
9. What causes N+1 queries and how do you detect them?
10. Explain optimistic concurrency and row-version based conflict detection.
11. How should `DbContext` lifetime be managed in a web application?
12. When is raw SQL or a stored procedure justified instead of LINQ?

## Large-file processing scenario

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
