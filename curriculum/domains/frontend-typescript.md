---
layout: default
title: "Angular, TypeScript & Frontend Architecture"
---

# Angular, TypeScript & Frontend Architecture

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="frontend-typescript-semantics"></a>
### TypeScript, JavaScript equality and browser async

`frontend-typescript-semantics` · Ring A · foundation

**Learning objectives**

- Predict equality and variable-binding behavior in small JavaScript examples.
- Explain structural typing and TypeScript boundaries.
- Trace asynchronous browser behavior with Promises or Observables.

**Concept fingerprint:** `javascript-equality`, `let-const`, `structural-typing`, `typescript`, `browser-async`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [06-frontend-behavioral · q011](../../sources/06-frontend-behavioral.md#q011)
- [06-frontend-behavioral · q012](../../sources/06-frontend-behavioral.md#q012)
- [06-frontend-behavioral · q013](../../sources/06-frontend-behavioral.md#q013)
- [06-frontend-behavioral · q014](../../sources/06-frontend-behavioral.md#q014)
- [06-frontend-behavioral · q015](../../sources/06-frontend-behavioral.md#q015)

## Senior

<a id="frontend-angular-architecture"></a>
### Angular rendering, routing, state and forms

`frontend-angular-architecture` · Ring A · senior

**Learning objectives**

- Trace Angular components, dependency injection and routing.
- Choose state and form boundaries for a medium or large SPA.
- Investigate rendering and bundle performance with concrete evidence.

**Concept fingerprint:** `angular-di`, `routing-lazy-loading`, `change-detection`, `state-management`, `reactive-forms`, `bundle-splitting`.

**Prerequisites:** [TypeScript, JavaScript equality and browser async](frontend-typescript.md#frontend-typescript-semantics)

**Source prompts** (question framing; answers still require verification)

- [06-frontend-behavioral · q001](../../sources/06-frontend-behavioral.md#q001)
- [06-frontend-behavioral · q002](../../sources/06-frontend-behavioral.md#q002)
- [06-frontend-behavioral · q003](../../sources/06-frontend-behavioral.md#q003)
- [06-frontend-behavioral · q006](../../sources/06-frontend-behavioral.md#q006)
- [06-frontend-behavioral · q007](../../sources/06-frontend-behavioral.md#q007)
- [06-frontend-behavioral · q008](../../sources/06-frontend-behavioral.md#q008)
- [06-frontend-behavioral · q010](../../sources/06-frontend-behavioral.md#q010)

<a id="frontend-http-auth"></a>
### Interceptors, caching and token refresh

`frontend-http-auth` · Ring A · senior

**Learning objectives**

- Design interceptor responsibilities for authentication and refresh.
- Choose HTTP caching only when the response contract permits it.
- Explain browser storage security and failure behavior across the request flow.

**Concept fingerprint:** `http-interceptors`, `http-caching`, `token-refresh`, `browser-token-storage`, `frontend-request-flow`.

**Prerequisites:** [JWT validation, claims and token lifecycle](security-identity.md#security-token-lifecycle) · [TypeScript, JavaScript equality and browser async](frontend-typescript.md#frontend-typescript-semantics)

**Source prompts** (question framing; answers still require verification)

- [06-frontend-behavioral · q004](../../sources/06-frontend-behavioral.md#q004)
- [06-frontend-behavioral · q005](../../sources/06-frontend-behavioral.md#q005)
- [06-frontend-behavioral · q009](../../sources/06-frontend-behavioral.md#q009)

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Angular Signals/RxJS version-specific APIs and current change-detection defaults.
