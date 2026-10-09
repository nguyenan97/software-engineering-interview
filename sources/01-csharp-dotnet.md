---
layout: default
title: C# and .NET Interview Topics
---

# C# and .NET Interview Topics

> Privacy-safe normalization of interview notes. Identifying names, organizations, projects and personal answers are intentionally excluded.

**Source status:** normalized interview prompts, not verified technical answers. Stable IDs preserve this privacy-safe corpus; no removed identities are reconstructed.

Questions are grouped by learning level inside their original sections. Canonical curriculum links consolidate overlapping wording into one topic. Level labels express intended lesson depth, not a claim about any interviewer.

[Curriculum index](../curriculum/index.md) · [Source coverage and gaps](../curriculum/source-coverage.md)

## C# fundamentals

### Foundation

<a id="q001"></a>
**S01-Q001** · original question 1 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

What is the difference between `static readonly` and `const`?

<a id="q002"></a>
**S01-Q002** · original question 2 · [Collections, strings and delegates](../curriculum/domains/dotnet-runtime.md#dotnet-collections-delegates)

What is the difference between an empty string literal and `String.Empty`?

<a id="q003"></a>
**S01-Q003** · original question 3 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

What is the difference between a property and a field?

<a id="q004"></a>
**S01-Q004** · original question 4 · [C# type, equality and member semantics](../curriculum/domains/dotnet-runtime.md#dotnet-type-semantics)

Explain boxing and unboxing.

<a id="q005"></a>
**S01-Q005** · original question 5 · [C# type, equality and member semantics](../curriculum/domains/dotnet-runtime.md#dotnet-type-semantics)

What is the difference between `==` and `Equals()`?

<a id="q006"></a>
**S01-Q006** · original question 6 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

Compare an abstract class and an interface.

<a id="q007"></a>
**S01-Q007** · original question 7 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

Compare virtual methods and abstract methods.

<a id="q008"></a>
**S01-Q008** · original question 8 · [C# type, equality and member semantics](../curriculum/domains/dotnet-runtime.md#dotnet-type-semantics)

Explain the `is` and `as` operators.

<a id="q009"></a>
**S01-Q009** · original question 9 · [Collections, strings and delegates](../curriculum/domains/dotnet-runtime.md#dotnet-collections-delegates)

Compare `IEnumerable`, arrays, `IList`, and `List`.

<a id="q010"></a>
**S01-Q010** · original question 10 · [LINQ execution and query translation](../curriculum/domains/ef-linq.md#ef-query-execution)

Compare `IEnumerable` and `IQueryable`.

<a id="q011"></a>
**S01-Q011** · original question 11 · [C# type, equality and member semantics](../curriculum/domains/dotnet-runtime.md#dotnet-type-semantics)

Explain value types and reference types.

<a id="q012"></a>
**S01-Q012** · original question 12 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

What class types are available in C# and how do they differ?

<a id="q013"></a>
**S01-Q013** · original question 13 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

Explain `internal` accessibility.

<a id="q014"></a>
**S01-Q014** · original question 14 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

Explain accessibility rules for interface members.

<a id="q015"></a>
**S01-Q015** · original question 15 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

What is a static constructor used for?

<a id="q016"></a>
**S01-Q016** · original question 16 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

Compare an abstract class with a regular class.

<a id="q017"></a>
**S01-Q017** · original question 17 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

Explain restrictions involving `abstract`, `sealed`, and `static` classes.

<a id="q018"></a>
**S01-Q018** · original question 18 · [C# members, inheritance and accessibility](../curriculum/domains/dotnet-runtime.md#dotnet-members-inheritance)

Compare overriding and overloading.

<a id="q019"></a>
**S01-Q019** · original question 19 · [Collections, strings and delegates](../curriculum/domains/dotnet-runtime.md#dotnet-collections-delegates)

Compare `string` and `StringBuilder`.

<a id="q020"></a>
**S01-Q020** · original question 20 · [C# type, equality and member semantics](../curriculum/domains/dotnet-runtime.md#dotnet-type-semantics)

Explain equality semantics for value and reference types.

<a id="q021"></a>
**S01-Q021** · original question 21 · [Collections, strings and delegates](../curriculum/domains/dotnet-runtime.md#dotnet-collections-delegates)

What collections do you commonly use and why?

**Related practice:** [Collection choice and evidence-led coding](../curriculum/domains/algorithms-debugging.md#algorithms-collection-reasoning). This is an adjacent exercise, not an additional original source question.

<a id="q022"></a>
**S01-Q022** · original question 22 · [Collections, strings and delegates](../curriculum/domains/dotnet-runtime.md#dotnet-collections-delegates)

When would you choose `Dictionary` or `HashSet`?

**Related practice:** [Collection choice and evidence-led coding](../curriculum/domains/algorithms-debugging.md#algorithms-collection-reasoning). This is an adjacent exercise, not an additional original source question.

<a id="q023"></a>
**S01-Q023** · original question 23 · [Collections, strings and delegates](../curriculum/domains/dotnet-runtime.md#dotnet-collections-delegates)

Explain delegates, `Action`, `Func`, and `Predicate`.

## .NET runtime and asynchronous programming

### Foundation

<a id="q024"></a>
**S01-Q024** · original question 1 · [Asynchronous execution and exception flow](../curriculum/domains/dotnet-runtime.md#dotnet-async-io)

How does `async`/`await` work?

<a id="q025"></a>
**S01-Q025** · original question 2 · [Asynchronous execution and exception flow](../curriculum/domains/dotnet-runtime.md#dotnet-async-io)

Compare `Task` and `Thread`.

<a id="q026"></a>
**S01-Q026** · original question 3 · [Asynchronous execution and exception flow](../curriculum/domains/dotnet-runtime.md#dotnet-async-io)

How does asynchronous I/O differ from traditional threading?

<a id="q030"></a>
**S01-Q030** · original question 7 · [Asynchronous execution and exception flow](../curriculum/domains/dotnet-runtime.md#dotnet-async-io)

How do exceptions propagate through asynchronous code?

<a id="q031"></a>
**S01-Q031** · original question 8 · [Asynchronous execution and exception flow](../curriculum/domains/dotnet-runtime.md#dotnet-async-io)

When should CPU-bound work use parallelism rather than asynchronous I/O?

### Senior

<a id="q027"></a>
**S01-Q027** · original question 4 · [Diagnosing blocking asynchronous code](../curriculum/domains/dotnet-runtime.md#dotnet-threadpool-starvation)

When can blocking asynchronous code cause deadlocks or ThreadPool starvation?

<a id="q028"></a>
**S01-Q028** · original question 5 · [Memory growth and deterministic cleanup](../curriculum/domains/dotnet-runtime.md#dotnet-memory-lifetime)

How would you diagnose a memory leak in a .NET application?

<a id="q029"></a>
**S01-Q029** · original question 6 · [Memory growth and deterministic cleanup](../curriculum/domains/dotnet-runtime.md#dotnet-memory-lifetime)

What roles do Garbage Collector, `IDisposable`, and deterministic cleanup play?

## Dependency Injection and SOLID

### Senior

<a id="q032"></a>
**S01-Q032** · original question 1 · [DI lifetimes and SOLID design](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid)

Compare Dependency Inversion, Inversion of Control, and Dependency Injection.

<a id="q033"></a>
**S01-Q033** · original question 2 · [DI lifetimes and SOLID design](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid)

Explain `Transient`, `Scoped`, and `Singleton` lifetimes.

<a id="q034"></a>
**S01-Q034** · original question 3 · [DI lifetimes and SOLID design](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid)

What problems occur when a longer-lived service captures a shorter-lived dependency?

<a id="q035"></a>
**S01-Q035** · original question 4 · [DI lifetimes and SOLID design](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid)

Explain the SOLID principles with production examples.

<a id="q036"></a>
**S01-Q036** · original question 5 · [DI lifetimes and SOLID design](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid)

Compare Liskov Substitution and Interface Segregation.

<a id="q037"></a>
**S01-Q037** · original question 6 · [DI lifetimes and SOLID design](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid)

Explain Dependency Inversion versus Dependency Injection.

<a id="q038"></a>
**S01-Q038** · original question 7 · [DI lifetimes and SOLID design](../curriculum/domains/dotnet-runtime.md#dotnet-di-solid)

Give an example of violating Open/Closed Principle and how you would refactor it.

## Patterns

### Senior

<a id="q039"></a>
**S01-Q039** · original question 1 · [DbContext, optimistic concurrency and repository boundaries](../curriculum/domains/ef-linq.md#ef-context-concurrency)

Explain Repository Pattern, Generic Repository Pattern, and Unit of Work.

<a id="q040"></a>
**S01-Q040** · original question 2 · [DbContext, optimistic concurrency and repository boundaries](../curriculum/domains/ef-linq.md#ef-context-concurrency)

EF Core already implements repository/unit-of-work-like behavior. When does an additional repository abstraction help, and when does it add unnecessary complexity?

<a id="q041"></a>
**S01-Q041** · original question 3 · [Factory, Strategy and Template Method](../curriculum/domains/dotnet-runtime.md#dotnet-behavioral-patterns)

When would you use Factory, Strategy, or Template Method?

<a id="q042"></a>
**S01-Q042** · original question 4 · [Dependency direction and service boundaries](../curriculum/domains/architecture-distributed.md#architecture-boundaries)

Explain Clean Architecture and dependency direction.

## Performance and caching

### Senior

<a id="q043"></a>
**S01-Q043** · original question 1 · [Caching and shared state across replicas](../curriculum/domains/architecture-distributed.md#architecture-cache-replicas)

What caching approaches are available in .NET applications?

<a id="q044"></a>
**S01-Q044** · original question 2 · [Caching and shared state across replicas](../curriculum/domains/architecture-distributed.md#architecture-cache-replicas)

Compare in-memory cache and distributed cache.

<a id="q045"></a>
**S01-Q045** · original question 3 · [Caching and shared state across replicas](../curriculum/domains/architecture-distributed.md#architecture-cache-replicas)

What changes when the application runs on multiple replicas?

<a id="q046"></a>
**S01-Q046** · original question 4 · [Tracing requests and diagnosing production latency](../curriculum/domains/observability-reliability.md#observability-request-diagnosis)

How would you identify a bottleneck under a large number of concurrent requests?

<a id="q047"></a>
**S01-Q047** · original question 5 · [Timeouts, retries, circuit breakers and backpressure](../curriculum/domains/observability-reliability.md#reliability-dependency-failures)

Discuss load balancing, caching, queues, backpressure, and horizontal scaling as different responses to load.
