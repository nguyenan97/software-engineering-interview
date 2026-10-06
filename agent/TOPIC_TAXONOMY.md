# Topic Taxonomy

Use this taxonomy to classify interview prompts, create stable `topic_id` values and interleave lessons. The taxonomy intentionally expands beyond the raw source notes toward production and architect-level reasoning.

## A. Architecture & Distributed Systems

- modular monolith vs microservices
- service boundaries and bounded contexts
- Clean / Onion / Hexagonal architecture
- dependency direction vs call direction
- API Gateway / reverse proxy
- synchronous vs asynchronous communication
- REST / gRPC / messaging trade-offs
- DDD aggregates and domain events
- CQRS and when not to use it
- Saga orchestration/choreography
- transactional outbox/inbox
- idempotency and deduplication
- distributed consistency and compensation
- API/message versioning
- resiliency, backpressure and load shedding
- horizontal scaling and data ownership

Example IDs: `architecture-modular-monolith-vs-microservices`, `messaging-idempotent-consumer`, `distributed-transactional-outbox`.

## B. C# & .NET Runtime

- async state machine
- ThreadPool and starvation
- I/O-bound vs CPU-bound
- cancellation and timeout propagation
- synchronization and race conditions
- Task scheduling and exception behavior
- GC / LOH / allocation pressure
- `IDisposable` / `IAsyncDisposable`
- value/reference semantics and equality
- collections and complexity
- delegates/events

Example IDs: `dotnet-async-state-machine`, `dotnet-threadpool-starvation`, `dotnet-gc-loh-allocation-pressure`.

## C. ASP.NET Core & API Engineering

- middleware ordering
- endpoint routing
- filters vs middleware
- DI lifetime / captive dependency
- `HttpClientFactory` and connection pooling
- rate limiting and caching
- validation and Problem Details
- background processing and graceful shutdown
- health checks
- API versioning and idempotency keys
- pagination / large responses
- OpenAPI contract design
- performance profiling

## D. EF Core & LINQ

- query translation and deferred execution
- projection
- tracking vs no-tracking
- identity resolution
- N+1
- split vs single queries
- optimistic concurrency
- batching/bulk operations
- `DbContext` lifetime/pooling
- transactions and raw SQL boundaries
- repository abstraction trade-offs

## E. SQL Server & Data Engineering

- clustered/nonclustered indexes
- composite indexes and key order
- covering indexes / `INCLUDE`
- selectivity/cardinality
- SARGability
- seeks/scans/lookups
- statistics and execution plans
- transaction isolation and row versioning
- blocking/deadlocks
- optimistic/pessimistic concurrency
- batching/bulk copy
- query monitoring

## F. Messaging & Event-Driven Systems

- queue vs topic/subscription
- competing consumers
- delivery guarantees
- retry/backoff
- DLQ / poison messages
- duplicate detection and idempotent consumers
- ordering vs throughput
- prefetch/batching/concurrency
- schema evolution
- correlation/causation IDs
- outbox/inbox
- exactly-once trade-offs

## G. Azure & Cloud Architecture

- App Service and deployment slots
- Functions and trigger behavior
- Service Bus
- Blob Storage
- Azure SQL
- Key Vault and Managed Identity
- API Management
- Front Door / Application Gateway
- Redis
- Application Insights / Azure Monitor
- autoscaling
- networking/private endpoints
- reliability/SLA/SLO
- cost/performance trade-offs
- infrastructure as code

## H. Security & Identity

- OAuth 2.0 / OIDC
- access vs refresh tokens
- JWT validation
- claims/roles/policies
- token rotation/revocation
- browser token-storage trade-offs
- BFF
- service-to-service identity
- TLS
- secrets management
- OWASP API risks
- CORS / CSRF / XSS
- least privilege and audit logging

## I. Observability, Performance & Reliability

- logs/metrics/traces
- distributed tracing
- correlation and W3C trace context
- OpenTelemetry
- p95/p99 latency
- SLI/SLO/error budgets
- profiling and memory dumps
- load testing and capacity planning
- retries/timeouts/circuit breaker
- retry storms and bulkheads
- graceful degradation
- incident diagnosis

## J. DevOps, Containers & Delivery

- image layers and multi-stage builds
- containers vs VMs
- config/secrets per environment
- immutable deployment
- CI/CD gates
- database migration deployment
- blue/green / canary / slot swap
- rollback strategy
- health/readiness/liveness
- supply-chain scanning
- GitHub Actions / Azure DevOps
- infrastructure as code

## K. Angular, TypeScript & Frontend Architecture

- component/change-detection model
- Signals/RxJS where relevant
- dependency injection
- routing/lazy loading
- HTTP interceptors
- state management
- forms/validation
- auth flow and browser storage
- caching and rendering performance
- bundle/code splitting
- TypeScript type system
- async browser behavior

## L. Algorithms, Coding & Debugging

- arrays/hash maps/sets
- strings
- stacks/queues
- trees/graphs
- sorting/searching and complexity
- concurrency coding
- SQL exercises
- refactoring/debugging/code review
- test design

## M. Engineering Process & Communication

- requirement clarification
- impact analysis and estimation
- code review
- QA/engineering disagreement resolution
- incident communication
- ADR communication
- explaining architecture concisely
- technical English
- senior/lead decision communication

## Interleaving guidance

Avoid long runs of one category. Revisit weak concepts through spaced reviews rather than repeating the same primary objective under a new title.
