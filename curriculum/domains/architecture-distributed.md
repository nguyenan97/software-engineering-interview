---
layout: default
title: "Architecture & Distributed Systems"
---

# Architecture & Distributed Systems

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Senior

<a id="architecture-boundaries"></a>
### Dependency direction and service boundaries

`architecture-boundaries` · Ring A · senior

**Learning objectives**

- Draw ownership and dependency boundaries for a generic system.
- Compare layered, Clean, Onion, Hexagonal and modular-monolith choices.
- Explain when independent deployment justifies microservice complexity.

**Concept fingerprint:** `dependency-direction`, `modular-monolith`, `microservices`, `service-boundaries`, `data-ownership`.

**Prerequisites:** [DI lifetimes and SOLID design](dotnet-runtime.md#dotnet-di-solid)

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q042](../../sources/01-csharp-dotnet.md#q042)
- [04-architecture-distributed-systems · q003](../../sources/04-architecture-distributed-systems.md#q003)
- [04-architecture-distributed-systems · q004](../../sources/04-architecture-distributed-systems.md#q004)
- [04-architecture-distributed-systems · q005](../../sources/04-architecture-distributed-systems.md#q005)
- [04-architecture-distributed-systems · q006](../../sources/04-architecture-distributed-systems.md#q006)
- [04-architecture-distributed-systems · q007](../../sources/04-architecture-distributed-systems.md#q007)
- [04-architecture-distributed-systems · q008](../../sources/04-architecture-distributed-systems.md#q008)
- [04-architecture-distributed-systems · q009](../../sources/04-architecture-distributed-systems.md#q009)
- [04-architecture-distributed-systems · q010](../../sources/04-architecture-distributed-systems.md#q010)

<a id="architecture-cache-replicas"></a>
### Caching and shared state across replicas

`architecture-cache-replicas` · Ring A · senior

**Learning objectives**

- Choose in-memory or distributed caching from ownership and replica requirements.
- Explain how multiple replicas change cache consistency and invalidation decisions.
- Compare latency, stale-data tolerance and operational cost in a concrete caching scenario.

**Concept fingerprint:** `in-memory-cache`, `distributed-cache`, `multiple-replicas`, `cache-consistency`, `cache-invalidation`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q043](../../sources/01-csharp-dotnet.md#q043)
- [01-csharp-dotnet · q044](../../sources/01-csharp-dotnet.md#q044)
- [01-csharp-dotnet · q045](../../sources/01-csharp-dotnet.md#q045)

<a id="architecture-communication"></a>
### Synchronous and asynchronous service communication

`architecture-communication` · Ring A · senior

**Learning objectives**

- Compare REST, gRPC and messaging for a concrete interaction.
- Trace failure and latency boundaries across services.
- Explain scaling and backpressure consequences of the chosen interaction.

**Concept fingerprint:** `synchronous-asynchronous`, `rest-grpc-messaging`, `failure-boundaries`, `horizontal-scaling`, `backpressure`.

**Prerequisites:** [Dependency direction and service boundaries](architecture-distributed.md#architecture-boundaries)

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q011](../../sources/04-architecture-distributed-systems.md#q011)
- [04-architecture-distributed-systems · q014](../../sources/04-architecture-distributed-systems.md#q014)

<a id="architecture-api-gateway"></a>
### Gateway responsibilities and routing change

`architecture-api-gateway` · Ring A · senior

**Learning objectives**

- Separate gateway policy and routing from domain business logic.
- Design downstream routing and configuration ownership.
- Explain coupling introduced by gateway changes and deployment.

**Concept fingerprint:** `api-gateway`, `reverse-proxy`, `routing-configuration`, `policy-boundaries`.

**Prerequisites:** [Request pipeline, middleware and filters](aspnet-api.md#aspnet-request-pipeline)

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q015](../../sources/04-architecture-distributed-systems.md#q015)
- [04-architecture-distributed-systems · q016](../../sources/04-architecture-distributed-systems.md#q016)
- [04-architecture-distributed-systems · q017](../../sources/04-architecture-distributed-systems.md#q017)
- [04-architecture-distributed-systems · q018](../../sources/04-architecture-distributed-systems.md#q018)
- [05-security-cloud-devops · q024](../../sources/05-security-cloud-devops.md#q024)

## Architect

<a id="architecture-ddd-cqrs"></a>
### DDD boundaries, aggregates and CQRS

`architecture-ddd-cqrs` · Ring A · architect

**Learning objectives**

- Explain ubiquitous language, bounded contexts and aggregate ownership.
- Relate domain events to business boundaries.
- Justify separate read/write models or explain why CQRS is unnecessary.

**Concept fingerprint:** `bounded-context`, `ubiquitous-language`, `aggregate`, `domain-event`, `cqrs`.

**Prerequisites:** [Dependency direction and service boundaries](architecture-distributed.md#architecture-boundaries)

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q031](../../sources/04-architecture-distributed-systems.md#q031)
- [04-architecture-distributed-systems · q032](../../sources/04-architecture-distributed-systems.md#q032)
- [04-architecture-distributed-systems · q033](../../sources/04-architecture-distributed-systems.md#q033)
- [04-architecture-distributed-systems · q034](../../sources/04-architecture-distributed-systems.md#q034)
- [04-architecture-distributed-systems · q035](../../sources/04-architecture-distributed-systems.md#q035)
- [04-architecture-distributed-systems · q036](../../sources/04-architecture-distributed-systems.md#q036)
- [04-architecture-distributed-systems · q037](../../sources/04-architecture-distributed-systems.md#q037)
- [04-architecture-distributed-systems · q038](../../sources/04-architecture-distributed-systems.md#q038)

<a id="architecture-saga-compensation"></a>
### Distributed consistency and compensation

`architecture-saga-compensation` · Ring A · architect

**Learning objectives**

- Explain why independently owned databases complicate one ACID transaction.
- Compare Saga orchestration and choreography for partial failure.
- Distinguish compensation from rollback and design recoverable progress.

**Concept fingerprint:** `eventual-consistency`, `saga`, `orchestration`, `choreography`, `compensation`, `partial-failure`.

**Prerequisites:** [Synchronous and asynchronous service communication](architecture-distributed.md#architecture-communication) · [Transactional outbox and external-effect boundaries](messaging-event-driven.md#messaging-outbox)

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q039](../../sources/04-architecture-distributed-systems.md#q039)
- [04-architecture-distributed-systems · q040](../../sources/04-architecture-distributed-systems.md#q040)
- [04-architecture-distributed-systems · q041](../../sources/04-architecture-distributed-systems.md#q041)
- [04-architecture-distributed-systems · q042](../../sources/04-architecture-distributed-systems.md#q042)
- [04-architecture-distributed-systems · q043](../../sources/04-architecture-distributed-systems.md#q043)

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- API/message contract versioning beyond the original question set.
