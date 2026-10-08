---
layout: default
title: Source Coverage and Gaps
---

# Source Coverage and Gaps

[Curriculum index](index.md) · [Taxonomy](../agent/TOPIC_TAXONOMY.md)

## Corpus audit

Audited the six existing privacy-safe Markdown sources. No private originals were recovered. Every numbered interview prompt and all four scenario/request-flow sections remain present. The seven-part answer structure also remains intact.

| Source | Stable numbered prompt IDs | Other retained material |
|---|---:|---|
| [01-csharp-dotnet](../sources/01-csharp-dotnet.md) | 47 | — |
| [02-aspnet-api-ef](../sources/02-aspnet-api-ef.md) | 35 | Large-file processing scenario |
| [03-sql-data-performance](../sources/03-sql-data-performance.md) | 36 | Query optimization |
| [04-architecture-distributed-systems](../sources/04-architecture-distributed-systems.md) | 43 | Production scenario |
| [05-security-cloud-devops](../sources/05-security-cloud-devops.md) | 48 | — |
| [06-frontend-behavioral](../sources/06-frontend-behavioral.md) | 25 | Cross-stack request flow; Interview answer structure |

Total numbered prompts: **234**. Source IDs use `S01-Q001` style; anchors use `q001` inside each source file. The original headings and their generated anchors are preserved.

## Canonical consolidation

| Repeated source themes | Canonical learning route | Meaning retained |
|---|---|---|
| C# equality, value/reference and inheritance variants | [Type semantics](domains/dotnet-runtime.md#dotnet-type-semantics) and [members/inheritance](domains/dotnet-runtime.md#dotnet-members-inheritance) | Equality and type tests remain separate from initialization, accessibility and virtual dispatch. |
| IEnumerable/IQueryable in C# and EF | [LINQ execution](domains/ef-linq.md#ef-query-execution) | Collection interfaces remain in the C# context; query execution has one primary lesson. |
| Dependency inversion/injection variants | [DI and SOLID](domains/dotnet-runtime.md#dotnet-di-solid) | Terminology and production lifetime failures remain available. |
| Clean Architecture in C# and architecture notes | [Architecture boundaries](domains/architecture-distributed.md#architecture-boundaries) | Pattern context and system ownership context remain traceable. |
| Background processing across API and operations notes | [Background jobs](domains/aspnet-api.md#aspnet-background-jobs) | Request offloading, scheduler replication and shutdown constraints remain distinct. |
| Large imports in API, SQL and distributed scenarios | [API idempotency](domains/aspnet-api.md#aspnet-idempotent-operations), [bulk import](domains/sql-data.md#sql-bulk-import), [consumer idempotency](domains/messaging-event-driven.md#messaging-idempotent-consumer) | Job identity, row handling and broker redelivery are separate objectives, not collapsed into one answer. |
| In-memory/distributed caching and replica behavior | [Caching across replicas](domains/architecture-distributed.md#architecture-cache-replicas) | Cache placement and stale-data trade-offs are separate from communication style. |
| Retry/load handling across runtime, services and operations | [Dependency failure reliability](domains/observability-reliability.md#reliability-dependency-failures) | Local runtime diagnosis remains separate from remote retry policy. |
| Gateway in architecture and cloud | [Gateway boundaries](domains/architecture-distributed.md#architecture-api-gateway) | Routing/configuration and managed-service selection remain distinct prompts. |
| Cross-stack flow in API, architecture and frontend | [System explanation](domains/engineering-communication.md#communication-system-explanation) | Technical pipeline training and concise interview delivery remain separate objectives. |

## Coverage limitations

The corpus emphasizes .NET/ASP.NET Core, EF Core, SQL Server, Azure-oriented architecture, Angular/TypeScript and senior production reasoning. It contains few standalone algorithms exercises, limited foundational cloud implementation detail and no learner-specific evidence of strengths or weaknesses.

The existing taxonomy includes adjacent subjects absent from the original prompts. Domain pages identify them as uncovered extensions. Do not generate a lesson claiming one of these was asked in the source notes. New extensions need a source seed, distinct objectives and official references for product behavior.

Some source phrasing can conceal version assumptions: interface-member rules, LINQ client evaluation, tracking/loading behavior, SQL isolation defaults, nullable uniqueness, JWT validation, broker delivery settings and Angular rendering. The refactor preserves these as questions. It introduces no authoritative technical answer or current-version assertion.

## Traceability rules

- A source ID identifies one retained numbered prompt, even when its display level changes.
- A source scenario is referenced by its original heading anchor.
- Every catalog topic has at least one concrete repository source anchor.
- Official sources belong in lesson verification records; interview notes establish question framing.
- Keep already-normalized wording privacy-safe. Do not add employer/candidate identities or imply personal experience.

## Audit date

Corpus and catalog structure reviewed on **2026-10-08**. This date records repository review, not verification of every product behavior.
