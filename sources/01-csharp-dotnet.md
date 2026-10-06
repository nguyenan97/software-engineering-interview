---
layout: default
title: C# and .NET Interview Topics
---

# C# and .NET Interview Topics

> Privacy-safe normalization of interview notes. Identifying names, organizations, projects and personal answers are intentionally excluded.

## C# fundamentals

1. What is the difference between `static readonly` and `const`?
2. What is the difference between an empty string literal and `String.Empty`?
3. What is the difference between a property and a field?
4. Explain boxing and unboxing.
5. What is the difference between `==` and `Equals()`?
6. Compare an abstract class and an interface.
7. Compare virtual methods and abstract methods.
8. Explain the `is` and `as` operators.
9. Compare `IEnumerable`, arrays, `IList`, and `List`.
10. Compare `IEnumerable` and `IQueryable`.
11. Explain value types and reference types.
12. What class types are available in C# and how do they differ?
13. Explain `internal` accessibility.
14. Explain accessibility rules for interface members.
15. What is a static constructor used for?
16. Compare an abstract class with a regular class.
17. Explain restrictions involving `abstract`, `sealed`, and `static` classes.
18. Compare overriding and overloading.
19. Compare `string` and `StringBuilder`.
20. Explain equality semantics for value and reference types.
21. What collections do you commonly use and why?
22. When would you choose `Dictionary` or `HashSet`?
23. Explain delegates, `Action`, `Func`, and `Predicate`.

## .NET runtime and asynchronous programming

1. How does `async`/`await` work?
2. Compare `Task` and `Thread`.
3. How does asynchronous I/O differ from traditional threading?
4. When can blocking asynchronous code cause deadlocks or ThreadPool starvation?
5. How would you diagnose a memory leak in a .NET application?
6. What roles do Garbage Collector, `IDisposable`, and deterministic cleanup play?
7. How do exceptions propagate through asynchronous code?
8. When should CPU-bound work use parallelism rather than asynchronous I/O?

## Dependency Injection and SOLID

1. Compare Dependency Inversion, Inversion of Control, and Dependency Injection.
2. Explain `Transient`, `Scoped`, and `Singleton` lifetimes.
3. What problems occur when a longer-lived service captures a shorter-lived dependency?
4. Explain the SOLID principles with production examples.
5. Compare Liskov Substitution and Interface Segregation.
6. Explain Dependency Inversion versus Dependency Injection.
7. Give an example of violating Open/Closed Principle and how you would refactor it.

## Patterns

1. Explain Repository Pattern, Generic Repository Pattern, and Unit of Work.
2. EF Core already implements repository/unit-of-work-like behavior. When does an additional repository abstraction help, and when does it add unnecessary complexity?
3. When would you use Factory, Strategy, or Template Method?
4. Explain Clean Architecture and dependency direction.

## Performance and caching

1. What caching approaches are available in .NET applications?
2. Compare in-memory cache and distributed cache.
3. What changes when the application runs on multiple replicas?
4. How would you identify a bottleneck under a large number of concurrent requests?
5. Discuss load balancing, caching, queues, backpressure, and horizontal scaling as different responses to load.
