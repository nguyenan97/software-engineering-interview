---
layout: default
title: "DevOps, Containers & Delivery"
---

# DevOps, Containers & Delivery

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="devops-container-delivery"></a>
### Containers, image layers and runtime configuration

`devops-container-delivery` · Ring A · foundation

**Learning objectives**

- Compare containers and virtual machines for application delivery.
- Explain image layers and multi-stage build responsibilities.
- Separate runtime configuration and secrets without rebuilding application code.

**Concept fingerprint:** `containers-vms`, `image-layers`, `multi-stage-build`, `runtime-configuration`, `secret-store`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [05-security-cloud-devops · q035](../../sources/05-security-cloud-devops.md#q035)
- [05-security-cloud-devops · q036](../../sources/05-security-cloud-devops.md#q036)
- [05-security-cloud-devops · q037](../../sources/05-security-cloud-devops.md#q037)
- [05-security-cloud-devops · q038](../../sources/05-security-cloud-devops.md#q038)
- [05-security-cloud-devops · q039](../../sources/05-security-cloud-devops.md#q039)

## Senior

<a id="devops-safe-release"></a>
### CI/CD, rollout, rollback and graceful shutdown

`devops-safe-release` · Ring A · senior

**Learning objectives**

- Define evidence-driven CI/CD gates for a release.
- Compare blue/green, canary and deployment-slot rollout strategies.
- Explain rollback, readiness and graceful shutdown requirements.

**Concept fingerprint:** `ci-cd-gates`, `blue-green`, `canary`, `deployment-slots`, `rollback`, `readiness-shutdown`.

**Prerequisites:** [Containers, image layers and runtime configuration](devops-delivery.md#devops-container-delivery)

**Source prompts** (question framing; answers still require verification)

- [05-security-cloud-devops · q040](../../sources/05-security-cloud-devops.md#q040)
- [05-security-cloud-devops · q041](../../sources/05-security-cloud-devops.md#q041)
- [05-security-cloud-devops · q042](../../sources/05-security-cloud-devops.md#q042)
- [05-security-cloud-devops · q043](../../sources/05-security-cloud-devops.md#q043)

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Immutable-deployment patterns, database-migration rollout, supply-chain scanning and provider-specific CI configuration.
