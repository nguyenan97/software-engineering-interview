---
layout: default
title: Frontend and Communication
---

# Frontend and Communication

> Only reusable interview prompts are retained. Personal biographies, employer history, named projects and organization-specific answers are excluded.

**Source status:** normalized interview prompts, not verified technical answers. Stable IDs preserve this privacy-safe corpus; no removed identities are reconstructed.

Questions are grouped by learning level inside their original sections. Canonical curriculum links consolidate overlapping wording into one topic. Level labels express intended lesson depth, not a claim about any interviewer.

[Curriculum index](../curriculum/index.md) · [Source coverage and gaps](../curriculum/source-coverage.md)

## Angular and frontend architecture

### Senior

<a id="q001"></a>
**S06-Q001** · original question 1 · [Angular rendering, routing, state and forms](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture)

Explain the core architecture of an Angular application.

<a id="q002"></a>
**S06-Q002** · original question 2 · [Angular rendering, routing, state and forms](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture)

How does Angular Dependency Injection work?

<a id="q003"></a>
**S06-Q003** · original question 3 · [Angular rendering, routing, state and forms](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture)

Explain routing and lazy loading.

<a id="q004"></a>
**S06-Q004** · original question 4 · [Interceptors, caching and token refresh](../curriculum/domains/frontend-typescript.md#frontend-http-auth)

How would you implement HTTP caching with an interceptor when caching is actually appropriate?

<a id="q005"></a>
**S06-Q005** · original question 5 · [Interceptors, caching and token refresh](../curriculum/domains/frontend-typescript.md#frontend-http-auth)

How should authentication headers and token refresh interact with HTTP interceptors?

<a id="q006"></a>
**S06-Q006** · original question 6 · [Angular rendering, routing, state and forms](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture)

Explain component rendering/change detection and common performance problems.

<a id="q007"></a>
**S06-Q007** · original question 7 · [Angular rendering, routing, state and forms](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture)

How do you structure state management for a medium or large SPA?

<a id="q008"></a>
**S06-Q008** · original question 8 · [Angular rendering, routing, state and forms](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture)

Explain reactive forms and validation.

<a id="q009"></a>
**S06-Q009** · original question 9 · [Interceptors, caching and token refresh](../curriculum/domains/frontend-typescript.md#frontend-http-auth)

How do browser storage choices affect authentication security?

<a id="q010"></a>
**S06-Q010** · original question 10 · [Angular rendering, routing, state and forms](../curriculum/domains/frontend-typescript.md#frontend-angular-architecture)

Explain bundle/code splitting and frontend performance.

## TypeScript and JavaScript

### Foundation

<a id="q011"></a>
**S06-Q011** · original question 1 · [TypeScript, JavaScript equality and browser async](../curriculum/domains/frontend-typescript.md#frontend-typescript-semantics)

Compare `==` and `===`.

<a id="q012"></a>
**S06-Q012** · original question 2 · [TypeScript, JavaScript equality and browser async](../curriculum/domains/frontend-typescript.md#frontend-typescript-semantics)

Compare `let` and `const`.

<a id="q013"></a>
**S06-Q013** · original question 3 · [TypeScript, JavaScript equality and browser async](../curriculum/domains/frontend-typescript.md#frontend-typescript-semantics)

Explain TypeScript's role in a frontend codebase.

<a id="q014"></a>
**S06-Q014** · original question 4 · [TypeScript, JavaScript equality and browser async](../curriculum/domains/frontend-typescript.md#frontend-typescript-semantics)

Explain structural typing at a practical level.

<a id="q015"></a>
**S06-Q015** · original question 5 · [TypeScript, JavaScript equality and browser async](../curriculum/domains/frontend-typescript.md#frontend-typescript-semantics)

Explain asynchronous browser behavior and Promises/Observables where relevant.

## Cross-stack request flow

**Source scenario · Senior**

Be able to explain one request from the browser through:

1. component/UI event;
2. frontend service/client;
3. authentication information;
4. gateway/reverse proxy;
5. ASP.NET Core middleware;
6. routing and authorization;
7. application/domain logic;
8. EF Core/database or external dependency;
9. telemetry;
10. HTTP response and UI state update.

**Canonical topics:** [Concise architecture explanations and evidence](../curriculum/domains/engineering-communication.md#communication-system-explanation) · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

## Engineering communication

These source questions are intentionally generalized so they can be answered without exposing personal or employer information.

### Senior

<a id="q016"></a>
**S06-Q016** · original question 1 · [Professional introduction and behavioral evidence](../curriculum/domains/engineering-communication.md#communication-behavioral-stories)

Introduce yourself professionally in 60-90 seconds.

<a id="q017"></a>
**S06-Q017** · original question 2 · [Professional introduction and behavioral evidence](../curriculum/domains/engineering-communication.md#communication-behavioral-stories)

Explain a technically challenging system without revealing confidential details.

<a id="q018"></a>
**S06-Q018** · original question 3 · [Professional introduction and behavioral evidence](../curriculum/domains/engineering-communication.md#communication-behavioral-stories)

Describe your responsibilities in terms of engineering outcomes rather than company/project names.

<a id="q019"></a>
**S06-Q019** · original question 4 · [Concise architecture explanations and evidence](../curriculum/domains/engineering-communication.md#communication-system-explanation)

Explain a design decision and the alternatives you rejected.

<a id="q020"></a>
**S06-Q020** · original question 5 · [Professional introduction and behavioral evidence](../curriculum/domains/engineering-communication.md#communication-behavioral-stories)

Describe a production problem, how you diagnosed it and what evidence confirmed the fix.

<a id="q021"></a>
**S06-Q021** · original question 6 · [Professional introduction and behavioral evidence](../curriculum/domains/engineering-communication.md#communication-behavioral-stories)

Explain a disagreement with QA/product/engineering and how evidence was used to resolve it.

<a id="q022"></a>
**S06-Q022** · original question 7 · [Professional introduction and behavioral evidence](../curriculum/domains/engineering-communication.md#communication-behavioral-stories)

Explain why you are looking for a new role without criticizing a current or former employer.

<a id="q023"></a>
**S06-Q023** · original question 8 · [Professional introduction and behavioral evidence](../curriculum/domains/engineering-communication.md#communication-behavioral-stories)

Describe how you learn an unfamiliar technology.

<a id="q024"></a>
**S06-Q024** · original question 9 · [Concise architecture explanations and evidence](../curriculum/domains/engineering-communication.md#communication-system-explanation)

Explain a technical trade-off clearly to a non-specialist.

<a id="q025"></a>
**S06-Q025** · original question 10 · [Concise architecture explanations and evidence](../curriculum/domains/engineering-communication.md#communication-system-explanation)

Answer follow-up questions with concrete constraints, failure modes and measurable evidence.

## Interview answer structure

For senior-level technical questions, a useful answer shape is:

1. **What** — concise definition.
2. **Why / when** — the problem it solves.
3. **How** — causal mechanics.
4. **Trade-offs** — costs and alternatives.
5. **Production example** — generic and non-confidential.
6. **Failure mode** — what can go wrong.
7. **Evidence** — metric, trace, execution plan, benchmark or test used to validate the decision.

This structure is an explanation aid, not a promise that an interviewer will avoid follow-up questions. Support claims with evidence, state limits and invite a relevant next topic only after answering the current question.
