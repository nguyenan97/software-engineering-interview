---
layout: default
title: Architecture and Distributed Systems
---

# Architecture and Distributed Systems

> Reusable technical interview content only; identifying context has been removed.

**Source status:** normalized interview prompts, not verified technical answers. Stable IDs preserve this privacy-safe corpus; no removed identities are reconstructed.

Questions are grouped by learning level inside their original sections. Canonical curriculum links consolidate overlapping wording into one topic. Level labels express intended lesson depth, not a claim about any interviewer.

[Curriculum index](../curriculum/index.md) · [Source coverage and gaps](../curriculum/source-coverage.md)

## Architecture discussion

### Senior

<a id="q001"></a>
**S04-Q001** · original question 1 · [Concise architecture explanations and evidence](../curriculum/domains/engineering-communication.md#communication-system-explanation)

Draw a system architecture and trace a request end-to-end.

<a id="q002"></a>
**S04-Q002** · original question 2 · [Concise architecture explanations and evidence](../curriculum/domains/engineering-communication.md#communication-system-explanation)

Explain the technology choices and why the boundaries were selected.

<a id="q003"></a>
**S04-Q003** · original question 3 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

Explain Clean Architecture and dependency direction.

<a id="q004"></a>
**S04-Q004** · original question 4 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

Compare layered architecture, Clean/Onion/Hexagonal approaches and a modular monolith.

<a id="q005"></a>
**S04-Q005** · original question 5 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

When should a system remain a modular monolith rather than become microservices?

<a id="q006"></a>
**S04-Q006** · original question 6 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

How do you identify service boundaries?

<a id="q007"></a>
**S04-Q007** · original question 7 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

Explain data ownership when services are independently deployable.

## Microservices

### Senior

<a id="q008"></a>
**S04-Q008** · original question 1 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

Define microservices beyond “small services”.

<a id="q009"></a>
**S04-Q009** · original question 2 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

What benefits justify the operational complexity?

<a id="q010"></a>
**S04-Q010** · original question 3 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

What common failure modes appear after splitting a monolith?

<a id="q011"></a>
**S04-Q011** · original question 4 · [Synchronous and asynchronous service communication](../curriculum/domains/architecture-distributed.md#architecture-communication)

Compare synchronous REST/gRPC communication with asynchronous messaging.

<a id="q012"></a>
**S04-Q012** · original question 5 · [Timeouts, retries, circuit breakers and backpressure](../curriculum/domains/observability-reliability.md#reliability-dependency-failures)

How should a service behave when a downstream dependency is unavailable?

<a id="q013"></a>
**S04-Q013** · original question 6 · [Timeouts, retries, circuit breakers and backpressure](../curriculum/domains/observability-reliability.md#reliability-dependency-failures)

Discuss timeout, retry, exponential backoff, circuit breaker and retry storms.

<a id="q014"></a>
**S04-Q014** · original question 7 · [Synchronous and asynchronous service communication](../curriculum/domains/architecture-distributed.md#architecture-communication)

Explain horizontal scaling, load balancing, backpressure and load shedding.

## API Gateway

### Senior

<a id="q015"></a>
**S04-Q015** · original question 1 · [Gateway responsibilities and routing change](../curriculum/domains/architecture-distributed.md#architecture-api-gateway)

What responsibilities belong in an API Gateway or reverse proxy?

<a id="q016"></a>
**S04-Q016** · original question 2 · [Gateway responsibilities and routing change](../curriculum/domains/architecture-distributed.md#architecture-api-gateway)

What configuration is typically required to route requests to downstream services?

<a id="q017"></a>
**S04-Q017** · original question 3 · [Gateway responsibilities and routing change](../curriculum/domains/architecture-distributed.md#architecture-api-gateway)

How can routing/configuration change without tightly coupling every change to a gateway redeployment?

<a id="q018"></a>
**S04-Q018** · original question 4 · [Gateway responsibilities and routing change](../curriculum/domains/architecture-distributed.md#architecture-api-gateway)

Which concerns should not become business logic inside the gateway?

## Messaging

### Foundation

<a id="q019"></a>
**S04-Q019** · original question 1 · [Delivery, competing consumers and dead-letter recovery](../curriculum/domains/messaging-event-driven.md#messaging-delivery-recovery)

Explain queue versus topic/subscription models.

<a id="q020"></a>
**S04-Q020** · original question 2 · [Delivery, competing consumers and dead-letter recovery](../curriculum/domains/messaging-event-driven.md#messaging-delivery-recovery)

Explain competing consumers.

<a id="q021"></a>
**S04-Q021** · original question 3 · [Delivery, competing consumers and dead-letter recovery](../curriculum/domains/messaging-event-driven.md#messaging-delivery-recovery)

How do message brokers decouple producers and consumers?

<a id="q022"></a>
**S04-Q022** · original question 4 · [Delivery, competing consumers and dead-letter recovery](../curriculum/domains/messaging-event-driven.md#messaging-delivery-recovery)

What happens when a message processing attempt fails?

<a id="q023"></a>
**S04-Q023** · original question 5 · [Delivery, competing consumers and dead-letter recovery](../curriculum/domains/messaging-event-driven.md#messaging-delivery-recovery)

Explain retry and dead-letter/poison-message handling.

### Senior

<a id="q024"></a>
**S04-Q024** · original question 6 · [Atomic inbox and idempotent consumer](../curriculum/domains/messaging-event-driven.md#messaging-idempotent-consumer)

How do you prevent duplicate processing when delivery is at-least-once?

<a id="q025"></a>
**S04-Q025** · original question 7 · [Atomic inbox and idempotent consumer](../curriculum/domains/messaging-event-driven.md#messaging-idempotent-consumer)

How do you design an idempotent consumer?

<a id="q026"></a>
**S04-Q026** · original question 8 · [Atomic inbox and idempotent consumer](../curriculum/domains/messaging-event-driven.md#messaging-idempotent-consumer)

How do database unique constraints help deduplication?

<a id="q027"></a>
**S04-Q027** · original question 9 · [Ordering, throughput and asynchronous results](../curriculum/domains/messaging-event-driven.md#messaging-ordering-correlation)

What trade-off exists between ordering and throughput?

<a id="q028"></a>
**S04-Q028** · original question 10 · [Ordering, throughput and asynchronous results](../curriculum/domains/messaging-event-driven.md#messaging-ordering-correlation)

How would you return a result when communication is asynchronous?

<a id="q029"></a>
**S04-Q029** · original question 11 · [Ordering, throughput and asynchronous results](../curriculum/domains/messaging-event-driven.md#messaging-ordering-correlation)

Explain correlation and causation identifiers.

### Architect

<a id="q030"></a>
**S04-Q030** · original question 12 · [Transactional outbox and external-effect boundaries](../curriculum/domains/messaging-event-driven.md#messaging-outbox)

Explain transactional outbox/inbox patterns.

## DDD and CQRS

### Architect

<a id="q031"></a>
**S04-Q031** · original question 1 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

What problem does Domain-Driven Design attempt to solve?

<a id="q032"></a>
**S04-Q032** · original question 2 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

Explain Ubiquitous Language.

<a id="q033"></a>
**S04-Q033** · original question 3 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

Explain Bounded Context.

<a id="q034"></a>
**S04-Q034** · original question 4 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

Explain Aggregate and Aggregate Root.

<a id="q035"></a>
**S04-Q035** · original question 5 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

Explain Domain Events.

<a id="q036"></a>
**S04-Q036** · original question 6 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

What is CQRS?

<a id="q037"></a>
**S04-Q037** · original question 7 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

When does separating read and write models help?

<a id="q038"></a>
**S04-Q038** · original question 8 · [DDD boundaries, aggregates and CQRS](../curriculum/domains/architecture-distributed.md#architecture-ddd-cqrs)

When is CQRS unnecessary complexity?

## Distributed consistency

### Architect

<a id="q039"></a>
**S04-Q039** · original question 1 · [Distributed consistency and compensation](../curriculum/domains/architecture-distributed.md#architecture-saga-compensation)

Why is a single ACID transaction usually unavailable across independently owned service databases?

<a id="q040"></a>
**S04-Q040** · original question 2 · [Distributed consistency and compensation](../curriculum/domains/architecture-distributed.md#architecture-saga-compensation)

Explain eventual consistency.

<a id="q041"></a>
**S04-Q041** · original question 3 · [Distributed consistency and compensation](../curriculum/domains/architecture-distributed.md#architecture-saga-compensation)

Compare Saga orchestration and choreography.

<a id="q042"></a>
**S04-Q042** · original question 4 · [Distributed consistency and compensation](../curriculum/domains/architecture-distributed.md#architecture-saga-compensation)

What is compensation and why is it not the same as database rollback?

<a id="q043"></a>
**S04-Q043** · original question 5 · [Distributed consistency and compensation](../curriculum/domains/architecture-distributed.md#architecture-saga-compensation)

How would you handle a partial failure after one service commits successfully?

## Production scenario

**Source scenario · Senior**

A client submits the same large import request several times while the first job is still processing. Design the system so that:

- only the intended work is performed;
- retries remain safe;
- duplicated messages do not create duplicated database rows;
- failed messages are recoverable;
- processing state is observable;
- multiple worker replicas can scale horizontally.

**Canonical topics:** [Atomic inbox and idempotent consumer](../curriculum/domains/messaging-event-driven.md#messaging-idempotent-consumer) · [Idempotent APIs and large-file job submission](../curriculum/domains/aspnet-api.md#aspnet-idempotent-operations) · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)
