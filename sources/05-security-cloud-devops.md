---
layout: default
title: Security, Azure, Observability and DevOps
---

# Security, Azure, Observability and DevOps

> Privacy-safe technical material extracted and normalized from the interview corpus.

## JWT and identity

1. What are the parts of a JWT?
2. What makes a token valid?
3. What information belongs in claims?
4. Explain authentication versus authorization.
5. Explain role-based and policy/permission-based authorization.
6. Explain access tokens versus refresh tokens.
7. How does refresh-token rotation work?
8. How should token expiry, revocation and reuse be handled?
9. Draw an authentication/authorization flow from SPA to gateway/identity provider to backend APIs.
10. Where should secrets, signing keys and tokens be stored?
11. Explain OAuth 2.0 and OpenID Connect at the level expected for application architecture.
12. What changes for service-to-service authentication?

## Transport and web security

1. Compare HTTP and HTTPS technically.
2. Explain the purpose of the TLS handshake at a high level.
3. Explain CORS, CSRF and XSS as distinct concerns.
4. Apply least privilege to APIs and cloud identities.
5. What security-sensitive information must not be written to logs?

## Azure and cloud services

1. Explain when serverless functions are appropriate.
2. Explain reliable messaging with queues, topics and subscriptions.
3. Compare one-to-one and one-to-many messaging patterns.
4. Explain object/blob storage use cases.
5. Explain managed relational database use cases.
6. Explain secretless authentication using managed identities.
7. Explain API management/gateway responsibilities.
8. Discuss autoscaling, reliability and cost trade-offs.
9. Explain infrastructure-as-code concepts and deployment templates.
10. How should environment-specific configuration be managed?

## Observability

1. Distinguish logs, metrics and traces.
2. How would you trace one request across frontend, gateway, multiple backend services and database calls?
3. Explain correlation IDs and distributed trace context.
4. How would you investigate a slow API?
5. What telemetry would you collect for latency, errors, dependencies and resource pressure?
6. How do you diagnose memory growth or ThreadPool starvation in production?
7. Why are p95/p99 latency measurements more useful than averages for many production investigations?

## Docker and delivery

1. What problem does Docker solve in application delivery?
2. Compare containers and virtual machines.
3. Explain image layers and multi-stage builds.
4. How should configuration differ across development, staging and production without rebuilding application code?
5. What belongs in environment variables versus a secret store?
6. Explain CI/CD gates.
7. Compare blue/green, canary and deployment-slot strategies.
8. What is required for safe rollback?
9. Explain health, readiness and graceful shutdown concerns.

## Background and operational reliability

1. When should resource-intensive work run outside the synchronous request path?
2. How should retry policies avoid retry storms?
3. How do you make scheduled/background processing safe across multiple replicas?
4. What should happen to work that repeatedly fails?
5. How do monitoring and alerting connect technical symptoms to an actionable incident?
