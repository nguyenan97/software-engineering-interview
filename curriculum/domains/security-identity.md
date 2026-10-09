---
layout: default
title: "Security & Identity"
---

# Security & Identity

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="security-browser-transport"></a>
### TLS, browser boundaries and least privilege

`security-browser-transport` · Ring A · foundation

**Learning objectives**

- Explain HTTPS and the TLS handshake at an appropriate architectural depth.
- Distinguish CORS, CSRF and XSS threats and controls.
- Choose browser storage and logging behavior from security requirements.

**Concept fingerprint:** `tls`, `cors`, `csrf`, `xss`, `browser-storage`, `sensitive-logs`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [05-security-cloud-devops · q013](../../sources/05-security-cloud-devops.md#q013)
- [05-security-cloud-devops · q014](../../sources/05-security-cloud-devops.md#q014)
- [05-security-cloud-devops · q015](../../sources/05-security-cloud-devops.md#q015)
- [05-security-cloud-devops · q017](../../sources/05-security-cloud-devops.md#q017)

## Senior

<a id="security-token-lifecycle"></a>
### JWT validation, claims and token lifecycle

`security-token-lifecycle` · Ring A · senior

**Learning objectives**

- Explain token structure and validation without treating decoding as verification.
- Separate authentication from role or policy authorization.
- Design access/refresh expiry, rotation, revocation and reuse handling.

**Concept fingerprint:** `jwt-validation`, `claims`, `authentication-authorization`, `access-refresh-token`, `rotation-revocation`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [05-security-cloud-devops · q001](../../sources/05-security-cloud-devops.md#q001)
- [05-security-cloud-devops · q002](../../sources/05-security-cloud-devops.md#q002)
- [05-security-cloud-devops · q003](../../sources/05-security-cloud-devops.md#q003)
- [05-security-cloud-devops · q004](../../sources/05-security-cloud-devops.md#q004)
- [05-security-cloud-devops · q005](../../sources/05-security-cloud-devops.md#q005)
- [05-security-cloud-devops · q006](../../sources/05-security-cloud-devops.md#q006)
- [05-security-cloud-devops · q007](../../sources/05-security-cloud-devops.md#q007)
- [05-security-cloud-devops · q008](../../sources/05-security-cloud-devops.md#q008)

## Architect

<a id="security-service-identity"></a>
### OAuth/OIDC, secrets and service identities

`security-service-identity` · Ring A · architect

**Learning objectives**

- Draw SPA-to-API and service-to-service identity flows.
- Explain OAuth and OpenID Connect responsibilities.
- Apply least privilege and managed-identity or secret-store choices.

**Concept fingerprint:** `oauth-oidc`, `service-identity`, `managed-identity`, `secret-management`, `least-privilege`.

**Prerequisites:** [JWT validation, claims and token lifecycle](security-identity.md#security-token-lifecycle) · [TLS, browser boundaries and least privilege](security-identity.md#security-browser-transport)

**Source prompts** (question framing; answers still require verification)

- [05-security-cloud-devops · q009](../../sources/05-security-cloud-devops.md#q009)
- [05-security-cloud-devops · q010](../../sources/05-security-cloud-devops.md#q010)
- [05-security-cloud-devops · q011](../../sources/05-security-cloud-devops.md#q011)
- [05-security-cloud-devops · q012](../../sources/05-security-cloud-devops.md#q012)
- [05-security-cloud-devops · q016](../../sources/05-security-cloud-devops.md#q016)
- [05-security-cloud-devops · q023](../../sources/05-security-cloud-devops.md#q023)

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- BFF architecture, audit-log design and an OWASP API risk catalog.
