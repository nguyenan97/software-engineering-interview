---
layout: default
title: "Observability, Performance & Reliability"
---

# Observability, Performance & Reliability

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Senior

<a id="observability-request-diagnosis"></a>
### Tracing requests and diagnosing production latency

`observability-request-diagnosis` · Ring A · senior

**Learning objectives**

- Correlate logs, metrics and traces across a cross-stack request.
- Investigate slow APIs, memory growth or resource pressure using hypotheses.
- Interpret tail latency and select evidence that confirms a fix.

**Concept fingerprint:** `logs-metrics-traces`, `distributed-tracing`, `correlation`, `p95-p99`, `incident-diagnosis`.

**Prerequisites:** [Request pipeline, middleware and filters](aspnet-api.md#aspnet-request-pipeline)

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q046](../../sources/01-csharp-dotnet.md#q046)
- [04-architecture-distributed-systems · production-scenario](../../sources/04-architecture-distributed-systems.md#production-scenario)
- [05-security-cloud-devops · q028](../../sources/05-security-cloud-devops.md#q028)
- [05-security-cloud-devops · q029](../../sources/05-security-cloud-devops.md#q029)
- [05-security-cloud-devops · q030](../../sources/05-security-cloud-devops.md#q030)
- [05-security-cloud-devops · q031](../../sources/05-security-cloud-devops.md#q031)
- [05-security-cloud-devops · q032](../../sources/05-security-cloud-devops.md#q032)
- [05-security-cloud-devops · q033](../../sources/05-security-cloud-devops.md#q033)
- [05-security-cloud-devops · q034](../../sources/05-security-cloud-devops.md#q034)
- [06-frontend-behavioral · cross-stack-request-flow](../../sources/06-frontend-behavioral.md#cross-stack-request-flow)

<a id="reliability-dependency-failures"></a>
### Timeouts, retries, circuit breakers and backpressure

`reliability-dependency-failures` · Ring A · senior

**Learning objectives**

- Design downstream-failure behavior from an explicit latency and load budget.
- Explain retry storms and select bounded retry, circuit-breaker or load-shedding behavior.
- Connect repeated failures to recovery paths, telemetry and actionable alerts.

**Concept fingerprint:** `timeouts`, `retry-backoff`, `retry-storm`, `circuit-breaker`, `backpressure`, `load-shedding`.

**Prerequisites:** [Tracing requests and diagnosing production latency](observability-reliability.md#observability-request-diagnosis)

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q047](../../sources/01-csharp-dotnet.md#q047)
- [04-architecture-distributed-systems · q012](../../sources/04-architecture-distributed-systems.md#q012)
- [04-architecture-distributed-systems · q013](../../sources/04-architecture-distributed-systems.md#q013)
- [05-security-cloud-devops · q045](../../sources/05-security-cloud-devops.md#q045)
- [05-security-cloud-devops · q048](../../sources/05-security-cloud-devops.md#q048)

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- OpenTelemetry setup, W3C propagation details, memory-dump tooling, SLI/SLO/error budgets, bulkheads and capacity planning.
