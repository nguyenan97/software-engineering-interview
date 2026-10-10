---
layout: default
title: Topic Taxonomy
---

# Topic Taxonomy

This taxonomy classifies interview prompts and interleaves lessons. The [catalog](../curriculum/catalog.json) is the source-grounded selection inventory; [source coverage](../curriculum/source-coverage.md) records gaps. An extension listed here is not evidence that it appeared in the source notes.

## Levels and rings

- `foundation`: define a causal mental model and apply it to a bounded example.
- `senior`: choose and validate behavior under production constraints, concurrency and failure.
- `architect`: reason across ownership, deployment, consistency, security and cost boundaries.
- Ring `A`: question/scenario directly appears in the source corpus.
- Ring `B`: supporting practice adjacent to a source question.
- Ring `C`: architect extension seeded by a source question.

Level and ring are independent. A source-direct Saga question can be architect-level. Distinct source wording may share a canonical topic; similar fingerprints still require comparing objectives.

## Stable domains

| Domain slug | Name | Curriculum |
|---|---|---|
| `architecture-distributed` | Architecture & Distributed Systems | [Topics](../curriculum/domains/architecture-distributed.md) |
| `dotnet-runtime` | C# & .NET Runtime | [Topics](../curriculum/domains/dotnet-runtime.md) |
| `aspnet-api` | ASP.NET Core & API Engineering | [Topics](../curriculum/domains/aspnet-api.md) |
| `ef-linq` | EF Core & LINQ | [Topics](../curriculum/domains/ef-linq.md) |
| `sql-data` | SQL Server & Data Engineering | [Topics](../curriculum/domains/sql-data.md) |
| `messaging-event-driven` | Messaging & Event-Driven Systems | [Topics](../curriculum/domains/messaging-event-driven.md) |
| `azure-cloud` | Azure & Cloud Architecture | [Topics](../curriculum/domains/azure-cloud.md) |
| `security-identity` | Security & Identity | [Topics](../curriculum/domains/security-identity.md) |
| `observability-reliability` | Observability, Performance & Reliability | [Topics](../curriculum/domains/observability-reliability.md) |
| `devops-delivery` | DevOps, Containers & Delivery | [Topics](../curriculum/domains/devops-delivery.md) |
| `frontend-typescript` | Angular, TypeScript & Frontend Architecture | [Topics](../curriculum/domains/frontend-typescript.md) |
| `algorithms-debugging` | Algorithms, Coding & Debugging | [Topics](../curriculum/domains/algorithms-debugging.md) |
| `engineering-communication` | Engineering Process & Communication | [Topics](../curriculum/domains/engineering-communication.md) |

## A. Architecture & Distributed Systems

**Domain:** `architecture-distributed`

**Source-grounded topics**

- [`architecture-boundaries`](../curriculum/domains/architecture-distributed.md#architecture-boundaries) — senior; Ring A.
- [`architecture-cache-replicas`](../curriculum/domains/architecture-distributed.md#architecture-cache-replicas) — senior; Ring A.
- [`architecture-communication`](../curriculum/domains/architecture-distributed.md#architecture-communication) — senior; Ring A.
- [`architecture-api-gateway`](../curriculum/domains/architecture-distributed.md#architecture-api-gateway) — senior; Ring A.
- [`architecture-ddd-cqrs`](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs) — architect; Ring A.
- [`architecture-saga-compensation`](../curriculum/domains/architecture-distributed.md#architecture-saga-compensation) — architect; Ring A.

**Adjacent or uncovered directions**

- API/message contract versioning beyond the original question set.

## B. C# & .NET Runtime

**Domain:** `dotnet-runtime`

**Source-grounded topics**

- [`dotnet-type-semantics`](../curriculum/domains/dotnet-runtime.md#dotnet-type-semantics) — foundation; Ring A.
- [`dotnet-members-inheritance`](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance) — foundation; Ring A.
- [`dotnet-collections-delegates`](../curriculum/domains/dotnet-runtime.md#dotnet-collections-delegates) — foundation; Ring A.
- [`dotnet-async-io`](../curriculum/domains/dotnet-runtime.md#dotnet-async-io) — foundation; Ring A.
- [`dotnet-threadpool-starvation`](../curriculum/domains/dotnet-runtime.md#dotnet-threadpool-starvation) — senior; Ring A.
- [`dotnet-memory-lifetime`](../curriculum/domains/dotnet-runtime.md#dotnet-memory-lifetime) — senior; Ring A.
- [`dotnet-di-solid`](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid) — senior; Ring A.
- [`dotnet-behavioral-patterns`](../curriculum/domains/dotnet-runtime.md#dotnet-behavioral-patterns) — senior; Ring A.

**Adjacent or uncovered directions**

- Cancellation propagation, synchronization internals, event-handling details, GC generations/LOH details and IAsyncDisposable behavior.

## C. ASP.NET Core & API Engineering

**Domain:** `aspnet-api`

**Source-grounded topics**

- [`aspnet-request-pipeline`](../curriculum/domains/aspnet-api.md#aspnet-request-pipeline) — foundation; Ring A.
- [`aspnet-http-contracts`](../curriculum/domains/aspnet-api.md#aspnet-http-contracts) — foundation; Ring A.
- [`aspnet-background-jobs`](../curriculum/domains/aspnet-api.md#aspnet-background-jobs) — senior; Ring A.
- [`aspnet-idempotent-operations`](../curriculum/domains/aspnet-api.md#aspnet-idempotent-operations) — senior; Ring A.

**Adjacent or uncovered directions**

- HttpClientFactory/connection pooling, rate limiting, Problem Details, OpenAPI, pagination and API versioning.

## D. EF Core & LINQ

**Domain:** `ef-linq`

**Source-grounded topics**

- [`ef-query-execution`](../curriculum/domains/ef-linq.md#ef-query-execution) — foundation; Ring A.
- [`ef-loading-performance`](../curriculum/domains/ef-linq.md#ef-loading-performance) — senior; Ring A.
- [`ef-context-concurrency`](../curriculum/domains/ef-linq.md#ef-context-concurrency) — senior; Ring A.

**Adjacent or uncovered directions**

- Identity resolution, split-query behavior and DbContext pooling.

## E. SQL Server & Data Engineering

**Domain:** `sql-data`

**Source-grounded topics**

- [`sql-objects-boundaries`](../curriculum/domains/sql-data.md#sql-objects-boundaries) — foundation; Ring A.
- [`sql-index-design`](../curriculum/domains/sql-data.md#sql-index-design) — foundation; Ring A.
- [`sql-query-investigation`](../curriculum/domains/sql-data.md#sql-query-investigation) — senior; Ring A.
- [`sql-transactions-concurrency`](../curriculum/domains/sql-data.md#sql-transactions-concurrency) — senior; Ring A.
- [`sql-bulk-import`](../curriculum/domains/sql-data.md#sql-bulk-import) — senior; Ring A.

**Adjacent or uncovered directions**

- Engine-version-specific optimizer or row-versioning defaults and tooling configuration.

## F. Messaging & Event-Driven Systems

**Domain:** `messaging-event-driven`

**Source-grounded topics**

- [`messaging-delivery-recovery`](../curriculum/domains/messaging-event-driven.md#messaging-delivery-recovery) — foundation; Ring A.
- [`messaging-idempotent-consumer`](../curriculum/domains/messaging-event-driven.md#messaging-idempotent-consumer) — senior; Ring A.
- [`messaging-outbox`](../curriculum/domains/messaging-event-driven.md#messaging-outbox) — architect; Ring C.
- [`messaging-ordering-correlation`](../curriculum/domains/messaging-event-driven.md#messaging-ordering-correlation) — senior; Ring A.

**Adjacent or uncovered directions**

- Broker-specific prefetch/batching settings, schema evolution and exact-once product claims.

## G. Azure & Cloud Architecture

**Domain:** `azure-cloud`

**Source-grounded topics**

- [`azure-service-selection`](../curriculum/domains/azure-cloud.md#azure-service-selection) — senior; Ring A.
- [`azure-operations-iac`](../curriculum/domains/azure-cloud.md#azure-operations-iac) — architect; Ring A.

**Adjacent or uncovered directions**

- Named-service configuration: App Service, Service Bus, Azure SQL, Key Vault, Front Door, Application Gateway, Redis, Application Insights and private endpoints. The sources mostly ask generic cloud-selection questions.

## H. Security & Identity

**Domain:** `security-identity`

**Source-grounded topics**

- [`security-token-lifecycle`](../curriculum/domains/security-identity.md#security-token-lifecycle) — senior; Ring A.
- [`security-browser-transport`](../curriculum/domains/security-identity.md#security-browser-transport) — foundation; Ring A.
- [`security-service-identity`](../curriculum/domains/security-identity.md#security-service-identity) — architect; Ring A.

**Adjacent or uncovered directions**

- BFF architecture, audit-log design and an OWASP API risk catalog.

## I. Observability, Performance & Reliability

**Domain:** `observability-reliability`

**Source-grounded topics**

- [`observability-request-diagnosis`](../curriculum/domains/observability-reliability.md#observability-request-diagnosis) — senior; Ring A.
- [`reliability-dependency-failures`](../curriculum/domains/observability-reliability.md#reliability-dependency-failures) — senior; Ring A.

**Adjacent or uncovered directions**

- OpenTelemetry setup, W3C propagation details, memory-dump tooling, SLI/SLO/error budgets, bulkheads and capacity planning.

## J. DevOps, Containers & Delivery

**Domain:** `devops-delivery`

**Source-grounded topics**

- [`devops-container-delivery`](../curriculum/domains/devops-delivery.md#devops-container-delivery) — foundation; Ring A.
- [`devops-safe-release`](../curriculum/domains/devops-delivery.md#devops-safe-release) — senior; Ring A.

**Adjacent or uncovered directions**

- Immutable-deployment patterns, database-migration rollout, supply-chain scanning and provider-specific CI configuration.

## K. Angular, TypeScript & Frontend Architecture

**Domain:** `frontend-typescript`

**Source-grounded topics**

- [`frontend-typescript-semantics`](../curriculum/domains/frontend-typescript.md#frontend-typescript-semantics) — foundation; Ring A.
- [`frontend-angular-architecture`](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture) — senior; Ring A.
- [`frontend-http-auth`](../curriculum/domains/frontend-typescript.md#frontend-http-auth) — senior; Ring A.

**Adjacent or uncovered directions**

- Angular Signals/RxJS version-specific APIs and current change-detection defaults.

## L. Algorithms, Coding & Debugging

**Domain:** `algorithms-debugging`

**Source-grounded topics**

- [`algorithms-collection-reasoning`](../curriculum/domains/algorithms-debugging.md#algorithms-collection-reasoning) — foundation; Ring B.
- [`algorithms-sql-relations`](../curriculum/domains/algorithms-debugging.md#algorithms-sql-relations) — foundation; Ring A.
- [`algorithms-department-headcount`](../curriculum/domains/algorithms-debugging.md#algorithms-department-headcount) — foundation; Ring A; focused Q032 slice.

**Adjacent or uncovered directions**

- Stacks, queues, trees, graphs, sorting/searching, concurrency coding, code-review and general test-design exercises.

## M. Engineering Process & Communication

**Domain:** `engineering-communication`

**Source-grounded topics**

- [`communication-system-explanation`](../curriculum/domains/engineering-communication.md#communication-system-explanation) — senior; Ring A.
- [`communication-behavioral-stories`](../curriculum/domains/engineering-communication.md#communication-behavioral-stories) — senior; Ring A.

**Adjacent or uncovered directions**

- Estimation, impact analysis, ADR templates and formal code-review processes.

## Interleaving and readiness

Read the catalog and persisted learning state before selection. Avoid long runs of one domain. Use prerequisites to sequence concepts; an existing generated lesson alone does not establish mastery. Revisit weak or due concepts as explicit reviews instead of presenting the same objective with a new title.

Prefer uncovered Ring A objectives and identify foundational needs through learner attempts. Choose a new Ring B/C topic only when its primary outcomes add scope. Do not infer a learner weakness from the absence of a score.

Cross-domain concepts are expected: the idempotent-consumer topic uses transactions, unique constraints and telemetry. Compare the primary learning contract to distinguish that lesson from API request deduplication or SQL concurrency.
