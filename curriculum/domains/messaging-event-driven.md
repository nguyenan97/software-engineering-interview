---
layout: default
title: "Messaging & Event-Driven Systems"
---

# Messaging & Event-Driven Systems

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="messaging-delivery-recovery"></a>
### Delivery, competing consumers and dead-letter recovery

`messaging-delivery-recovery` · Ring A · foundation

**Learning objectives**

- Choose queue or topic/subscription delivery from recipient requirements.
- Explain competing consumers and processing-failure redelivery.
- Design retry and dead-letter recovery responsibilities.

**Concept fingerprint:** `queue-topic`, `competing-consumers`, `at-least-once`, `retry`, `dead-letter`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q019](../../sources/04-architecture-distributed-systems.md#q019)
- [04-architecture-distributed-systems · q020](../../sources/04-architecture-distributed-systems.md#q020)
- [04-architecture-distributed-systems · q021](../../sources/04-architecture-distributed-systems.md#q021)
- [04-architecture-distributed-systems · q022](../../sources/04-architecture-distributed-systems.md#q022)
- [04-architecture-distributed-systems · q023](../../sources/04-architecture-distributed-systems.md#q023)
- [05-security-cloud-devops · q047](../../sources/05-security-cloud-devops.md#q047)

## Senior

<a id="messaging-idempotent-consumer"></a>
### Atomic inbox and idempotent consumer

`messaging-idempotent-consumer` · Ring A · senior

**Learning objectives**

- Implement an atomic SQL Server inbox and business update that handles concurrent deliveries and conflicting event identities.
- Explain redelivery after a successful database commit and identify the acknowledgment failure window.
- Verify rollback, retries, and unknown commit outcomes without assuming every timeout means failure.
- Deliver a concise interview answer with a defensible guarantee, trade-offs, and an honest follow-up bridge.

**Concept fingerprint:** `at-least-once-delivery`, `stable-event-identity`, `transactional-inbox`, `atomic-business-update`, `concurrent-consumers`, `commit-acknowledgment-gap`, `failure-injection`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q024](../../sources/04-architecture-distributed-systems.md#q024)
- [04-architecture-distributed-systems · q025](../../sources/04-architecture-distributed-systems.md#q025)
- [04-architecture-distributed-systems · q026](../../sources/04-architecture-distributed-systems.md#q026)
- [04-architecture-distributed-systems · production-scenario](../../sources/04-architecture-distributed-systems.md#production-scenario)

<a id="messaging-ordering-correlation"></a>
### Ordering, throughput and asynchronous results

`messaging-ordering-correlation` · Ring A · senior

**Learning objectives**

- Choose ordering boundaries without assuming global order.
- Design asynchronous result correlation and status visibility.
- Distinguish event identity, correlation and causation identifiers.

**Concept fingerprint:** `message-ordering`, `throughput`, `correlation-id`, `causation-id`, `asynchronous-results`.

**Prerequisites:** [Delivery, competing consumers and dead-letter recovery](messaging-event-driven.md#messaging-delivery-recovery)

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q027](../../sources/04-architecture-distributed-systems.md#q027)
- [04-architecture-distributed-systems · q028](../../sources/04-architecture-distributed-systems.md#q028)
- [04-architecture-distributed-systems · q029](../../sources/04-architecture-distributed-systems.md#q029)

## Architect

<a id="messaging-outbox"></a>
### Transactional outbox and external-effect boundaries

`messaging-outbox` · Ring C · architect

**Learning objectives**

- Define the local transaction boundary for business state and an outgoing event.
- Explain dispatcher retry and duplicate delivery failure windows.
- Identify downstream idempotency or reconciliation needs for remote effects.

**Concept fingerprint:** `transactional-outbox`, `local-transaction`, `dispatcher-retry`, `remote-side-effect`, `reconciliation`.

**Prerequisites:** [Atomic inbox and idempotent consumer](messaging-event-driven.md#messaging-idempotent-consumer)

**Source prompts** (question framing; answers still require verification)

- [04-architecture-distributed-systems · q030](../../sources/04-architecture-distributed-systems.md#q030)

**Scope note:** The source explicitly asks about outbox/inbox. Remote-effect reconciliation extends that prompt to architect-level failure reasoning; verify the chosen downstream system independently.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Broker-specific prefetch/batching settings, schema evolution and exact-once product claims.
