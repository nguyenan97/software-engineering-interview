---
layout: default
title: "Azure & Cloud Architecture"
---

# Azure & Cloud Architecture

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Senior

<a id="azure-service-selection"></a>
### Cloud compute, storage and messaging selection

`azure-service-selection` · Ring A · senior

**Learning objectives**

- Choose functions, messaging, blob storage or relational storage from workload requirements.
- Compare one-to-one and one-to-many messaging use cases.
- Explain reliability and cost implications without assuming one universal service.

**Concept fingerprint:** `serverless-functions`, `cloud-messaging`, `blob-storage`, `managed-database`, `service-selection`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [05-security-cloud-devops · q018](../../sources/05-security-cloud-devops.md#q018)
- [05-security-cloud-devops · q019](../../sources/05-security-cloud-devops.md#q019)
- [05-security-cloud-devops · q020](../../sources/05-security-cloud-devops.md#q020)
- [05-security-cloud-devops · q021](../../sources/05-security-cloud-devops.md#q021)
- [05-security-cloud-devops · q022](../../sources/05-security-cloud-devops.md#q022)

## Architect

<a id="azure-operations-iac"></a>
### Cloud scaling, configuration and infrastructure as code

`azure-operations-iac` · Ring A · architect

**Learning objectives**

- Explain autoscaling trade-offs across reliability, performance and cost.
- Separate environment configuration from infrastructure definitions.
- Design an infrastructure-as-code deployment boundary and verification plan.

**Concept fingerprint:** `autoscaling`, `cloud-cost`, `infrastructure-as-code`, `environment-configuration`, `operability`.

**Prerequisites:** [Cloud compute, storage and messaging selection](azure-cloud.md#azure-service-selection)

**Source prompts** (question framing; answers still require verification)

- [05-security-cloud-devops · q025](../../sources/05-security-cloud-devops.md#q025)
- [05-security-cloud-devops · q026](../../sources/05-security-cloud-devops.md#q026)
- [05-security-cloud-devops · q027](../../sources/05-security-cloud-devops.md#q027)

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Named-service configuration: App Service, Service Bus, Azure SQL, Key Vault, Front Door, Application Gateway, Redis, Application Insights and private endpoints. The sources mostly ask generic cloud-selection questions.
