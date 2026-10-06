---
layout: default
title: Architecture and Distributed Systems
---

# Architecture and Distributed Systems

> Reusable technical interview content only; identifying context has been removed.

## Architecture discussion

1. Draw a system architecture and trace a request end-to-end.
2. Explain the technology choices and why the boundaries were selected.
3. Explain Clean Architecture and dependency direction.
4. Compare layered architecture, Clean/Onion/Hexagonal approaches and a modular monolith.
5. When should a system remain a modular monolith rather than become microservices?
6. How do you identify service boundaries?
7. Explain data ownership when services are independently deployable.

## Microservices

1. Define microservices beyond “small services”.
2. What benefits justify the operational complexity?
3. What common failure modes appear after splitting a monolith?
4. Compare synchronous REST/gRPC communication with asynchronous messaging.
5. How should a service behave when a downstream dependency is unavailable?
6. Discuss timeout, retry, exponential backoff, circuit breaker and retry storms.
7. Explain horizontal scaling, load balancing, backpressure and load shedding.

## API Gateway

1. What responsibilities belong in an API Gateway or reverse proxy?
2. What configuration is typically required to route requests to downstream services?
3. How can routing/configuration change without tightly coupling every change to a gateway redeployment?
4. Which concerns should not become business logic inside the gateway?

## Messaging

1. Explain queue versus topic/subscription models.
2. Explain competing consumers.
3. How do message brokers decouple producers and consumers?
4. What happens when a message processing attempt fails?
5. Explain retry and dead-letter/poison-message handling.
6. How do you prevent duplicate processing when delivery is at-least-once?
7. How do you design an idempotent consumer?
8. How do database unique constraints help deduplication?
9. What trade-off exists between ordering and throughput?
10. How would you return a result when communication is asynchronous?
11. Explain correlation and causation identifiers.
12. Explain transactional outbox/inbox patterns.

## DDD and CQRS

1. What problem does Domain-Driven Design attempt to solve?
2. Explain Ubiquitous Language.
3. Explain Bounded Context.
4. Explain Aggregate and Aggregate Root.
5. Explain Domain Events.
6. What is CQRS?
7. When does separating read and write models help?
8. When is CQRS unnecessary complexity?

## Distributed consistency

1. Why is a single ACID transaction usually unavailable across independently owned service databases?
2. Explain eventual consistency.
3. Compare Saga orchestration and choreography.
4. What is compensation and why is it not the same as database rollback?
5. How would you handle a partial failure after one service commits successfully?

## Production scenario

A client submits the same large import request several times while the first job is still processing. Design the system so that:

- only the intended work is performed;
- retries remain safe;
- duplicated messages do not create duplicated database rows;
- failed messages are recoverable;
- processing state is observable;
- multiple worker replicas can scale horizontally.
