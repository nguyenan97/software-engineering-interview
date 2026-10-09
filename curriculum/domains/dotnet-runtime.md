---
layout: default
title: "C# & .NET Runtime"
---

# C# & .NET Runtime

[Curriculum index](../index.md) · [Source coverage](../source-coverage.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md)

Each topic has one primary learning objective set. Repeated source wording points here instead of creating another lesson. Start at a suitable level; prerequisites describe useful sequencing rather than inferred learner mastery.

## Foundation

<a id="dotnet-type-semantics"></a>
### C# type, equality and member semantics

`dotnet-type-semantics` · Ring A · foundation

**Learning objectives**

- Predict assignment, boxing and equality behavior in value/reference examples.
- Choose equality, type-test and cast semantics from the input contract.
- Explain observed behavior using executable examples and explicit assumptions.

**Concept fingerprint:** `value-reference-semantics`, `equality`, `boxing`, `type-tests`, `casts`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q004](../../sources/01-csharp-dotnet.md#q004)
- [01-csharp-dotnet · q005](../../sources/01-csharp-dotnet.md#q005)
- [01-csharp-dotnet · q008](../../sources/01-csharp-dotnet.md#q008)
- [01-csharp-dotnet · q011](../../sources/01-csharp-dotnet.md#q011)
- [01-csharp-dotnet · q020](../../sources/01-csharp-dotnet.md#q020)

<a id="dotnet-members-inheritance"></a>
### C# members, inheritance and accessibility

`dotnet-members-inheritance` · Ring A · foundation

**Learning objectives**

- Choose member storage and initialization behavior for a stated requirement.
- Compare abstract classes, interfaces and virtual dispatch using a small extension example.
- Explain accessibility and inheritance restrictions for the chosen target version.

**Concept fingerprint:** `member-initialization`, `inheritance`, `interfaces`, `virtual-dispatch`, `accessibility`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q001](../../sources/01-csharp-dotnet.md#q001)
- [01-csharp-dotnet · q003](../../sources/01-csharp-dotnet.md#q003)
- [01-csharp-dotnet · q006](../../sources/01-csharp-dotnet.md#q006)
- [01-csharp-dotnet · q007](../../sources/01-csharp-dotnet.md#q007)
- [01-csharp-dotnet · q012](../../sources/01-csharp-dotnet.md#q012)
- [01-csharp-dotnet · q013](../../sources/01-csharp-dotnet.md#q013)
- [01-csharp-dotnet · q014](../../sources/01-csharp-dotnet.md#q014)
- [01-csharp-dotnet · q015](../../sources/01-csharp-dotnet.md#q015)
- [01-csharp-dotnet · q016](../../sources/01-csharp-dotnet.md#q016)
- [01-csharp-dotnet · q017](../../sources/01-csharp-dotnet.md#q017)
- [01-csharp-dotnet · q018](../../sources/01-csharp-dotnet.md#q018)

<a id="dotnet-collections-delegates"></a>
### Collections, strings and delegates

`dotnet-collections-delegates` · Ring A · foundation

**Learning objectives**

- Choose collections from lookup, ordering and mutation requirements.
- Use delegates and string-building choices in a small implementation.
- Explain the evidence needed to compare allocation and runtime costs.

**Concept fingerprint:** `collections`, `dictionary`, `hash-set`, `delegates`, `string-building`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q002](../../sources/01-csharp-dotnet.md#q002)
- [01-csharp-dotnet · q009](../../sources/01-csharp-dotnet.md#q009)
- [01-csharp-dotnet · q019](../../sources/01-csharp-dotnet.md#q019)
- [01-csharp-dotnet · q021](../../sources/01-csharp-dotnet.md#q021)
- [01-csharp-dotnet · q022](../../sources/01-csharp-dotnet.md#q022)
- [01-csharp-dotnet · q023](../../sources/01-csharp-dotnet.md#q023)

<a id="dotnet-async-io"></a>
### Asynchronous execution and exception flow

`dotnet-async-io` · Ring A · foundation

**Learning objectives**

- Trace an asynchronous operation without equating Task with a dedicated thread.
- Choose asynchronous I/O or CPU parallelism from the workload.
- Predict exception propagation through awaited operations.

**Concept fingerprint:** `async-await`, `task-thread`, `async-io`, `cpu-parallelism`, `async-exceptions`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q024](../../sources/01-csharp-dotnet.md#q024)
- [01-csharp-dotnet · q025](../../sources/01-csharp-dotnet.md#q025)
- [01-csharp-dotnet · q026](../../sources/01-csharp-dotnet.md#q026)
- [01-csharp-dotnet · q030](../../sources/01-csharp-dotnet.md#q030)
- [01-csharp-dotnet · q031](../../sources/01-csharp-dotnet.md#q031)

## Senior

<a id="dotnet-threadpool-starvation"></a>
### Diagnosing blocking asynchronous code

`dotnet-threadpool-starvation` · Ring A · senior

**Learning objectives**

- Distinguish blocking, deadlock and ThreadPool starvation hypotheses.
- Diagnose a slow API using runtime and request evidence.
- Validate a change against throughput and latency measurements.

**Concept fingerprint:** `threadpool-starvation`, `sync-over-async`, `deadlock`, `runtime-diagnostics`.

**Prerequisites:** [Asynchronous execution and exception flow](dotnet-runtime.md#dotnet-async-io)

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q027](../../sources/01-csharp-dotnet.md#q027)

<a id="dotnet-memory-lifetime"></a>
### Memory growth and deterministic cleanup

`dotnet-memory-lifetime` · Ring A · senior

**Learning objectives**

- Explain managed memory reclamation versus resource cleanup.
- Investigate retained memory using an explicit hypothesis and evidence.
- Design cleanup boundaries for owned disposable resources.

**Concept fingerprint:** `garbage-collection`, `memory-retention`, `idisposable`, `resource-ownership`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q028](../../sources/01-csharp-dotnet.md#q028)
- [01-csharp-dotnet · q029](../../sources/01-csharp-dotnet.md#q029)

<a id="dotnet-di-solid"></a>
### DI lifetimes and SOLID design

`dotnet-di-solid` · Ring A · senior

**Learning objectives**

- Identify captive dependencies and select compatible service lifetimes.
- Distinguish inversion of control, dependency inversion and injection.
- Refactor a concrete SOLID violation while explaining the trade-off.

**Concept fingerprint:** `dependency-injection`, `service-lifetimes`, `captive-dependency`, `solid`, `dependency-inversion`.

**Prerequisites:** None required by the catalog; use the lesson cold start to establish readiness.

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q032](../../sources/01-csharp-dotnet.md#q032)
- [01-csharp-dotnet · q033](../../sources/01-csharp-dotnet.md#q033)
- [01-csharp-dotnet · q034](../../sources/01-csharp-dotnet.md#q034)
- [01-csharp-dotnet · q035](../../sources/01-csharp-dotnet.md#q035)
- [01-csharp-dotnet · q036](../../sources/01-csharp-dotnet.md#q036)
- [01-csharp-dotnet · q037](../../sources/01-csharp-dotnet.md#q037)
- [01-csharp-dotnet · q038](../../sources/01-csharp-dotnet.md#q038)

<a id="dotnet-behavioral-patterns"></a>
### Factory, Strategy and Template Method

`dotnet-behavioral-patterns` · Ring A · senior

**Learning objectives**

- Select a behavioral or creation pattern from a concrete change requirement.
- Compare the chosen pattern with a simpler implementation.
- Explain dependency and testing implications without pattern-name guessing.

**Concept fingerprint:** `factory`, `strategy`, `template-method`, `change-boundaries`.

**Prerequisites:** [DI lifetimes and SOLID design](dotnet-runtime.md#dotnet-di-solid)

**Source prompts** (question framing; answers still require verification)

- [01-csharp-dotnet · q041](../../sources/01-csharp-dotnet.md#q041)

## Architect

No separate source-grounded topic is registered at this level. A production twist can deepen a lower-level topic; register a new extension only with distinct objectives and verified references.

## Uncovered extensions

These remain useful taxonomy directions. They are not claimed as original interview prompts or current verified answers.

- Cancellation propagation, synchronization internals, event-handling details, GC generations/LOH details and IAsyncDisposable behavior.
