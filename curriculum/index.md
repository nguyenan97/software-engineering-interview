---
layout: default
title: Daily Interview Curriculum
locale: en
translation_key: curriculum
---

# Daily Interview Curriculum

A source-grounded progression for daily Software Engineering interview practice. The catalog indexes questions; generated lessons explain and verify answers.

[Daily agent skill](../agent/SKILL.md) · [Topic taxonomy](../agent/TOPIC_TAXONOMY.md) · [Source coverage and gaps](source-coverage.md) · [Machine-readable catalog](catalog.json)

## How to choose a lesson

Use the agent skill to inspect learning history before selecting a topic. Prefer an uncovered source-direct objective, check its prerequisites, rotate domains and select a manageable lab. Existing generated lessons remain available; completion and review depend on learner evidence.

Foundation develops the mental model; senior applies it to failure, concurrency and evidence; architect examines system boundaries and operational consequences. Level and source ring are independent.

- **Ring A:** a question or scenario is explicit in the source corpus.
- **Ring B:** practice or supporting detail is adjacent to an explicit question.
- **Ring C:** a source-seeded architect extension adds system-level scope.

The catalog currently contains 47 topics. Ring A can be architect-level when the source already asks an architect-level question.

## Domains

| Domain | Foundation | Senior | Architect | Source coverage |
|---|---:|---:|---:|---|
| [Architecture & Distributed Systems](domains/architecture-distributed.md) | 0 | 4 | 2 | 01, 04, 05 |
| [C# & .NET Runtime](domains/dotnet-runtime.md) | 4 | 4 | 0 | 01 |
| [ASP.NET Core & API Engineering](domains/aspnet-api.md) | 2 | 2 | 0 | 02, 04, 05 |
| [EF Core & LINQ](domains/ef-linq.md) | 1 | 2 | 0 | 01, 02 |
| [SQL Server & Data Engineering](domains/sql-data.md) | 2 | 3 | 0 | 02, 03 |
| [Messaging & Event-Driven Systems](domains/messaging-event-driven.md) | 1 | 2 | 1 | 04, 05 |
| [Azure & Cloud Architecture](domains/azure-cloud.md) | 0 | 1 | 1 | 05 |
| [Security & Identity](domains/security-identity.md) | 1 | 1 | 1 | 05 |
| [Observability, Performance & Reliability](domains/observability-reliability.md) | 0 | 2 | 0 | 01, 04, 05, 06 |
| [DevOps, Containers & Delivery](domains/devops-delivery.md) | 1 | 1 | 0 | 05 |
| [Angular, TypeScript & Frontend Architecture](domains/frontend-typescript.md) | 1 | 2 | 0 | 06 |
| [Algorithms, Coding & Debugging](domains/algorithms-debugging.md) | 3 | 0 | 0 | 01, 03 |
| [Engineering Process & Communication](domains/engineering-communication.md) | 0 | 2 | 0 | 04, 06 |

## Source and answer boundaries

Source files preserve normalized questions, scenario constraints and the existing answer-structure advice. They do not certify a technical solution. Stable IDs and anchors survive regrouping; canonical topic links merge the learning route while retaining meaningful source wording.

Every lesson must distinguish source framing, official-documentation verification and exercise assumptions. Never reconstruct removed personal or employer context. Version-sensitive runtime, framework, database, broker and browser behavior must be checked against official documentation at lesson generation time.

## Catalog contract

`catalog.json` has `schema_version: 1` and a `topics` array. Each entry contains a stable `topic_id`, title, domain, level, ring, 2–4 objectives, 3–7 concept fingerprints, repository-relative source references and prerequisite topic IDs. Existing topic IDs must not be repurposed to different objectives.

A shared concept fingerprint is a clue to compare objectives, not proof that two lessons duplicate each other. For example, API request idempotency and atomic consumer processing have different contracts and failure windows.

## Suggested starting branches

- Request pipeline → background jobs → idempotent import submission.
- LINQ execution → loading performance or DbContext concurrency.
- Index design → evidence-led query optimization.
- Delivery and recovery → idempotent consumer → outbox → distributed compensation.
- Token lifecycle → service identity; TypeScript semantics → Angular or HTTP interceptors.

The idempotent-consumer topic intentionally has no catalog prerequisite so its self-contained worked lesson is usable immediately. Its cold start introduces the necessary transaction and delivery assumptions.
