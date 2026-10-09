---
layout: default
title: Security, Azure, Observability and DevOps
---

# Security, Azure, Observability and DevOps

> Privacy-safe technical material extracted and normalized from the interview corpus.

**Source status:** normalized interview prompts, not verified technical answers. Stable IDs preserve this privacy-safe corpus; no removed identities are reconstructed.

Questions are grouped by learning level inside their original sections. Canonical curriculum links consolidate overlapping wording into one topic. Level labels express intended lesson depth, not a claim about any interviewer.

[Curriculum index](../curriculum/index.md) · [Source coverage and gaps](../curriculum/source-coverage.md)

## JWT and identity

### Senior

<a id="q001"></a>
**S05-Q001** · original question 1 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

What are the parts of a JWT?

<a id="q002"></a>
**S05-Q002** · original question 2 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

What makes a token valid?

<a id="q003"></a>
**S05-Q003** · original question 3 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

What information belongs in claims?

<a id="q004"></a>
**S05-Q004** · original question 4 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

Explain authentication versus authorization.

<a id="q005"></a>
**S05-Q005** · original question 5 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

Explain role-based and policy/permission-based authorization.

<a id="q006"></a>
**S05-Q006** · original question 6 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

Explain access tokens versus refresh tokens.

<a id="q007"></a>
**S05-Q007** · original question 7 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

How does refresh-token rotation work?

<a id="q008"></a>
**S05-Q008** · original question 8 · [JWT validation, claims and token lifecycle](../curriculum/domains/security-identity.md#security-token-lifecycle)

How should token expiry, revocation and reuse be handled?

### Architect

<a id="q009"></a>
**S05-Q009** · original question 9 · [OAuth/OIDC, secrets and service identities](../curriculum/domains/security-identity.md#security-service-identity)

Draw an authentication/authorization flow from SPA to gateway/identity provider to backend APIs.

<a id="q010"></a>
**S05-Q010** · original question 10 · [OAuth/OIDC, secrets and service identities](../curriculum/domains/security-identity.md#security-service-identity)

Where should secrets, signing keys and tokens be stored?

<a id="q011"></a>
**S05-Q011** · original question 11 · [OAuth/OIDC, secrets and service identities](../curriculum/domains/security-identity.md#security-service-identity)

Explain OAuth 2.0 and OpenID Connect at the level expected for application architecture.

<a id="q012"></a>
**S05-Q012** · original question 12 · [OAuth/OIDC, secrets and service identities](../curriculum/domains/security-identity.md#security-service-identity)

What changes for service-to-service authentication?

## Transport and web security

### Foundation

<a id="q013"></a>
**S05-Q013** · original question 1 · [TLS, browser boundaries and least privilege](../curriculum/domains/security-identity.md#security-browser-transport)

Compare HTTP and HTTPS technically.

<a id="q014"></a>
**S05-Q014** · original question 2 · [TLS, browser boundaries and least privilege](../curriculum/domains/security-identity.md#security-browser-transport)

Explain the purpose of the TLS handshake at a high level.

<a id="q015"></a>
**S05-Q015** · original question 3 · [TLS, browser boundaries and least privilege](../curriculum/domains/security-identity.md#security-browser-transport)

Explain CORS, CSRF and XSS as distinct concerns.

<a id="q017"></a>
**S05-Q017** · original question 5 · [TLS, browser boundaries and least privilege](../curriculum/domains/security-identity.md#security-browser-transport)

What security-sensitive information must not be written to logs?

### Architect

<a id="q016"></a>
**S05-Q016** · original question 4 · [OAuth/OIDC, secrets and service identities](../curriculum/domains/security-identity.md#security-service-identity)

Apply least privilege to APIs and cloud identities.

## Azure and cloud services

### Senior

<a id="q018"></a>
**S05-Q018** · original question 1 · [Cloud compute, storage and messaging selection](../curriculum/domains/azure-cloud.md#azure-service-selection)

Explain when serverless functions are appropriate.

<a id="q019"></a>
**S05-Q019** · original question 2 · [Cloud compute, storage and messaging selection](../curriculum/domains/azure-cloud.md#azure-service-selection)

Explain reliable messaging with queues, topics and subscriptions.

<a id="q020"></a>
**S05-Q020** · original question 3 · [Cloud compute, storage and messaging selection](../curriculum/domains/azure-cloud.md#azure-service-selection)

Compare one-to-one and one-to-many messaging patterns.

<a id="q021"></a>
**S05-Q021** · original question 4 · [Cloud compute, storage and messaging selection](../curriculum/domains/azure-cloud.md#azure-service-selection)

Explain object/blob storage use cases.

<a id="q022"></a>
**S05-Q022** · original question 5 · [Cloud compute, storage and messaging selection](../curriculum/domains/azure-cloud.md#azure-service-selection)

Explain managed relational database use cases.

<a id="q024"></a>
**S05-Q024** · original question 7 · [Gateway responsibilities and routing change](../curriculum/domains/architecture-distributed.md#architecture-api-gateway)

Explain API management/gateway responsibilities.

### Architect

<a id="q023"></a>
**S05-Q023** · original question 6 · [OAuth/OIDC, secrets and service identities](../curriculum/domains/security-identity.md#security-service-identity)

Explain secretless authentication using managed identities.

<a id="q025"></a>
**S05-Q025** · original question 8 · [Cloud scaling, configuration and infrastructure as code](../curriculum/domains/azure-cloud.md#azure-operations-iac)

Discuss autoscaling, reliability and cost trade-offs.

<a id="q026"></a>
**S05-Q026** · original question 9 · [Cloud scaling, configuration and infrastructure as code](../curriculum/domains/azure-cloud.md#azure-operations-iac)

Explain infrastructure-as-code concepts and deployment templates.

<a id="q027"></a>
**S05-Q027** · original question 10 · [Cloud scaling, configuration and infrastructure as code](../curriculum/domains/azure-cloud.md#azure-operations-iac)

How should environment-specific configuration be managed?

## Observability

### Senior

<a id="q028"></a>
**S05-Q028** · original question 1 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

Distinguish logs, metrics and traces.

<a id="q029"></a>
**S05-Q029** · original question 2 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

How would you trace one request across frontend, gateway, multiple backend services and database calls?

<a id="q030"></a>
**S05-Q030** · original question 3 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

Explain correlation IDs and distributed trace context.

<a id="q031"></a>
**S05-Q031** · original question 4 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

How would you investigate a slow API?

<a id="q032"></a>
**S05-Q032** · original question 5 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

What telemetry would you collect for latency, errors, dependencies and resource pressure?

<a id="q033"></a>
**S05-Q033** · original question 6 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

How do you diagnose memory growth or ThreadPool starvation in production?

<a id="q034"></a>
**S05-Q034** · original question 7 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

Why are p95/p99 latency measurements more useful than averages for many production investigations?

## Docker and delivery

### Foundation

<a id="q035"></a>
**S05-Q035** · original question 1 · [Containers, image layers and runtime configuration](../curriculum/domains/devops-delivery.md#devops-container-delivery)

What problem does Docker solve in application delivery?

<a id="q036"></a>
**S05-Q036** · original question 2 · [Containers, image layers and runtime configuration](../curriculum/domains/devops-delivery.md#devops-container-delivery)

Compare containers and virtual machines.

<a id="q037"></a>
**S05-Q037** · original question 3 · [Containers, image layers and runtime configuration](../curriculum/domains/devops-delivery.md#devops-container-delivery)

Explain image layers and multi-stage builds.

<a id="q038"></a>
**S05-Q038** · original question 4 · [Containers, image layers and runtime configuration](../curriculum/domains/devops-delivery.md#devops-container-delivery)

How should configuration differ across development, staging and production without rebuilding application code?

<a id="q039"></a>
**S05-Q039** · original question 5 · [Containers, image layers and runtime configuration](../curriculum/domains/devops-delivery.md#devops-container-delivery)

What belongs in environment variables versus a secret store?

### Senior

<a id="q040"></a>
**S05-Q040** · original question 6 · [CI/CD, rollout, rollback and graceful shutdown](../curriculum/domains/devops-delivery.md#devops-safe-release)

Explain CI/CD gates.

<a id="q041"></a>
**S05-Q041** · original question 7 · [CI/CD, rollout, rollback and graceful shutdown](../curriculum/domains/devops-delivery.md#devops-safe-release)

Compare blue/green, canary and deployment-slot strategies.

<a id="q042"></a>
**S05-Q042** · original question 8 · [CI/CD, rollout, rollback and graceful shutdown](../curriculum/domains/devops-delivery.md#devops-safe-release)

What is required for safe rollback?

<a id="q043"></a>
**S05-Q043** · original question 9 · [CI/CD, rollout, rollback and graceful shutdown](../curriculum/domains/devops-delivery.md#devops-safe-release)

Explain health, readiness and graceful shutdown concerns.

## Background and operational reliability

### Foundation

<a id="q047"></a>
**S05-Q047** · original question 4 · [Delivery, competing consumers and dead-letter recovery](../curriculum/domains/messaging-event-driven.md#messaging-delivery-recovery)

What should happen to work that repeatedly fails?

### Senior

<a id="q044"></a>
**S05-Q044** · original question 1 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

When should resource-intensive work run outside the synchronous request path?

<a id="q045"></a>
**S05-Q045** · original question 2 · [Timeouts, retries, circuit breakers and backpressure](../curriculum/domains/observability-reliability.md#reliability-dependency-failures)

How should retry policies avoid retry storms?

<a id="q046"></a>
**S05-Q046** · original question 3 · [Background processing across replicas](../curriculum/domains/aspnet-api.md#aspnet-background-jobs)

How do you make scheduled/background processing safe across multiple replicas?

<a id="q048"></a>
**S05-Q048** · original question 5 · [Timeouts, retries, circuit breakers and backpressure](../curriculum/domains/observability-reliability.md#reliability-dependency-failures)

How do monitoring and alerting connect technical symptoms to an actionable incident?
