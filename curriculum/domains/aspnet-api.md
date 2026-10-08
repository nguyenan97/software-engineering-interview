---
layout: default
title: "ASP.NET Core & API Engineering"
---

# ASP.NET Core & API Engineering

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="aspnet-request-pipeline"></a>
### Request pipeline, middleware and filters

`aspnet-request-pipeline` · Ring A · foundation

**Learning objectives**

- Trace a request through routing, middleware, endpoint and response.
- Explain how ordering changes authentication and exception handling.
- Choose middleware or filters for a stated cross-cutting concern.

**Concept fingerprint:** `middleware`, `routing`, `filters`, `request-lifecycle`, `exception-handling`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [02-aspnet-api-ef · q001](../../sources/02-aspnet-api-ef.md#q001)
- [02-aspnet-api-ef · q002](../../sources/02-aspnet-api-ef.md#q002)
- [02-aspnet-api-ef · q003](../../sources/02-aspnet-api-ef.md#q003)
- [02-aspnet-api-ef · q004](../../sources/02-aspnet-api-ef.md#q004)
- [02-aspnet-api-ef · q005](../../sources/02-aspnet-api-ef.md#q005)
- [02-aspnet-api-ef · q006](../../sources/02-aspnet-api-ef.md#q006)
- [02-aspnet-api-ef · q007](../../sources/02-aspnet-api-ef.md#q007)
- [02-aspnet-api-ef · q008](../../sources/02-aspnet-api-ef.md#q008)
- [02-aspnet-api-ef · q009](../../sources/02-aspnet-api-ef.md#q009)

<a id="aspnet-http-contracts"></a>
### HTTP contracts, validation and MVC state

`aspnet-http-contracts` · Ring A · foundation

**Learning objectives**

- Choose HTTP methods and response semantics from the operation contract.
- Compare REST APIs and server-rendered MVC responsibilities.
- Explain validation and session or transient state choices.

**Concept fingerprint:** `http-methods`, `http-status`, `rest-mvc`, `validation`, `session-state`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [02-aspnet-api-ef · q010](../../sources/02-aspnet-api-ef.md#q010)
- [02-aspnet-api-ef · q011](../../sources/02-aspnet-api-ef.md#q011)
- [02-aspnet-api-ef · q012](../../sources/02-aspnet-api-ef.md#q012)
- [02-aspnet-api-ef · q013](../../sources/02-aspnet-api-ef.md#q013)
- [02-aspnet-api-ef · q014](../../sources/02-aspnet-api-ef.md#q014)
- [02-aspnet-api-ef · q015](../../sources/02-aspnet-api-ef.md#q015)
- [02-aspnet-api-ef · q016](../../sources/02-aspnet-api-ef.md#q016)

## Senior

<a id="aspnet-background-jobs"></a>
### Background processing across replicas

`aspnet-background-jobs` · Ring A · senior

**Learning objectives**

- Move long-running work off the synchronous request path with an explicit contract.
- Compare hosted services, schedulers and queue-based workers.
- Design retries, cancellation and shutdown for multiple instances.

**Concept fingerprint:** `background-processing`, `scheduling`, `cancellation`, `graceful-shutdown`, `multiple-replicas`.

**Prerequisites:** [Request pipeline, middleware and filters](aspnet-api.md#aspnet-request-pipeline)

**Source prompts** (question framing; answers still require verification)

- [02-aspnet-api-ef · q017](../../sources/02-aspnet-api-ef.md#q017)
- [02-aspnet-api-ef · q019](../../sources/02-aspnet-api-ef.md#q019)
- [02-aspnet-api-ef · q020](../../sources/02-aspnet-api-ef.md#q020)
- [02-aspnet-api-ef · q021](../../sources/02-aspnet-api-ef.md#q021)
- [02-aspnet-api-ef · q022](../../sources/02-aspnet-api-ef.md#q022)
- [02-aspnet-api-ef · q023](../../sources/02-aspnet-api-ef.md#q023)
- [05-security-cloud-devops · q044](../../sources/05-security-cloud-devops.md#q044)
- [05-security-cloud-devops · q046](../../sources/05-security-cloud-devops.md#q046)

<a id="aspnet-idempotent-operations"></a>
### Idempotent APIs and large-file job submission

`aspnet-idempotent-operations` · Ring A · senior

**Learning objectives**

- Define a stable request identity and repeated-submission behavior.
- Design asynchronous import submission, status and error-report contracts.
- Separate job deduplication from row-level duplicate prevention.

**Concept fingerprint:** `api-idempotency`, `import-submission`, `job-status`, `request-identity`, `validation-report`.

**Prerequisites:** [HTTP contracts, validation and MVC state](aspnet-api.md#aspnet-http-contracts) · [Background processing across replicas](aspnet-api.md#aspnet-background-jobs)

**Source prompts** (question framing; answers still require verification)

- [02-aspnet-api-ef · q018](../../sources/02-aspnet-api-ef.md#q018)
- [02-aspnet-api-ef · large-file-processing-scenario](../../sources/02-aspnet-api-ef.md#large-file-processing-scenario)
- [04-architecture-distributed-systems · production-scenario](../../sources/04-architecture-distributed-systems.md#production-scenario)

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- HttpClientFactory/connection pooling, rate limiting, Problem Details, OpenAPI, pagination and API versioning.
