---
layout: default
title: "Idempotent Consumers: Safe Retries Without Duplicate Effects"
lesson_id: 2026-10-08-messaging-idempotent-consumer
topic_id: messaging-idempotent-consumer
domain: messaging-event-driven
level: senior
mode: full-lesson
created_at: "2026-10-08"
status: generated
objectives:
  - Implement an atomic SQL Server inbox and business update that handles concurrent deliveries and conflicting event identities.
  - Explain redelivery after a successful database commit and identify the acknowledgment failure window.
  - Verify rollback, retries, and unknown commit outcomes without assuming every timeout means failure.
  - Deliver a concise interview answer with a defensible guarantee, trade-offs, and an honest follow-up bridge.
concept_fingerprint:
  - at-least-once-delivery
  - stable-event-identity
  - transactional-inbox
  - atomic-business-update
  - concurrent-consumers
  - commit-acknowledgment-gap
  - failure-injection
source_refs:
  - sources/04-architecture-distributed-systems.md#q024
  - sources/04-architecture-distributed-systems.md#q025
  - sources/04-architecture-distributed-systems.md#q026
  - sources/04-architecture-distributed-systems.md#production-scenario
  - sources/02-aspnet-api-ef.md#background-processing
  - sources/02-aspnet-api-ef.md#large-file-processing-scenario
  - https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement
  - https://learn.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/set-xact-abort-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/create-unique-constraints
  - https://learn.microsoft.com/en-us/sql/t-sql/language-elements/commit-transaction-transact-sql
  - https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/servicebus/Azure.Messaging.ServiceBus/src/Processor/ServiceBusProcessorOptions.cs
checked_at: "2026-10-08"
---

# Idempotent Consumers: Safe Retries Without Duplicate Effects

## Stage 0 — Lesson card

| Field | Value |
| --- | --- |
| Topic | `messaging-idempotent-consumer` |
| Lesson ID / ring | `2026-10-08-messaging-idempotent-consumer` / A — source-direct |
| Domain / level | Messaging and event-driven systems / senior |
| Mode | Full lesson, including worked solution |
| Duration | 80 minutes: 15 minutes explanation, 45 minutes lab, 20 minutes retrieval and spoken interview practice |
| Primary source | [At-least-once duplicate processing](../sources/04-architecture-distributed-systems.md#q024), [idempotent consumers](../sources/04-architecture-distributed-systems.md#q025), [unique constraints](../sources/04-architecture-distributed-systems.md#q026) (original Messaging questions 6–8) |
| Supporting sources | [Repeated import scenario](../sources/04-architecture-distributed-systems.md#production-scenario); [background processing](../sources/02-aspnet-api-ef.md#background-processing), questions 4–5; [large-file processing](../sources/02-aspnet-api-ef.md#large-file-processing-scenario) |
| Selection reason | A source-direct topic connecting messaging, transactions, concurrency, and production recovery. The repository has no completed attempt for this objective. |
| Status | Generated; learner work and assessment are pending |

By the end, you should be able to:

1. Implement an atomic SQL Server inbox and business update under concurrent delivery and conflicting identities.
2. Explain why redelivery can follow a successful database commit.
3. Verify rollback, retries, and unknown commit outcomes.
4. Give a concise interview answer with defensible boundaries and a relevant follow-up.

**Source questions are prompts, not verified answers.** The implementation below is a worked example; current product behavior is checked separately in the evidence table. This SQL and its broker integration have not been executed during preparation.

Use the learning cycle **predict → attempt → explain → verify → retrieve**. In this Full lesson, solutions are available below. Spend time attempting the challenge before reading them, then close the lesson during recall. Record observable results rather than familiarity from rereading.

## Stage 1 — Cold start

Spend five minutes answering without notes:

1. A worker commits a database update and crashes before acknowledging the message. What can happen next?
2. Two replicas both check `HasProcessed(eventId)` before either writes. What prevents two balance increases?
3. Does broker duplicate detection make the consumer database update and acknowledgment atomic?

### Prediction challenge

A broker delivers this immutable event:

```json
{
  "eventId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "accountId": 42,
  "amount": 100.00
}
```

The account balance starts at zero. The handler does this:

```csharp
if (!await HasProcessed(eventId))
{
    await IncreaseBalance(accountId, amount);
    await MarkProcessed(eventId);
}

await Acknowledge();
```

Predict the outcome if both workers pass the check, if `MarkProcessed` fails after the increase, or if acknowledgment fails after the marker is saved. Write the invariant your replacement must preserve.

The challenge is to make retries safe across several replicas while retaining failed work for recovery. Do not assume a process-local lock, broker lock, or successful send is an end-to-end guarantee.

## Stage 2 — Core model

### The broker and database have different state

```text
Receive message
      ↓
Apply business update and inbox entry
      ↓
Commit database transaction
      ↓       ← a crash or lost connection here can cause redelivery
Acknowledge message to broker
```

Acknowledgment tells the broker that processing is complete. It cannot undo a database commit. With Azure Service Bus Peek-Lock, settlement can fail after work succeeded, and expired or lost locks can permit redelivery [V1].

The engineering goal is precise:

> For one consumer and stable event identity, repeated attempts do not repeat its committed business mutation in this database, while the processed identity remains retained.

The handler can run several times. This guarantee does not promise successful processing of every message, global ordering, or exactly one external email or payment.

### Identity is a contract

Increasing a balance is naturally non-idempotent: adding 100 twice changes 0 to 200. We make that mutation conditional on a durable identity.

- Retries of the same event preserve `eventId`.
- Different legitimate events have different IDs.
- Reusing an ID with different business data is an error.
- The key includes the consumer name: independent consumers can process the same event for different purposes.
- A producer retry that creates a new event ID bypasses event-level deduplication. Use an additional business invariant, such as a unique `paymentId`, when several events can represent one logical operation.

The lab event contains only `accountId` and `amount`. Those fields are compared on a duplicate. A larger event contract needs a version-aware canonical representation or comparison of every field affecting business behavior; an arbitrary raw JSON hash can incorrectly treat equivalent payloads as different.

### The atomicity invariant

The inbox row means **business processing committed**. It does not mean the broker acknowledgment succeeded.

| Inbox row | Business mutation | Meaning |
| --- | --- | --- |
| Absent | Absent | Safe to attempt the operation |
| Present | Present | Already processed |
| Present | Absent | Work may be skipped permanently |
| Absent | Present | Retry may repeat the mutation |

The inbox insert and balance update must commit together or roll back together. A separate marker transaction cannot protect the gap between them.

### Vietnamese Note

Khoảng trống khó xử lý nằm giữa **database commit** và **broker acknowledgment**. Database đã cập nhật nhưng broker có thể chưa biết. Khi retry, worker phải đọc được bằng chứng xử lý đã commit. Vì vậy inbox và thay đổi nghiệp vụ cần nằm trong **cùng transaction**; ghi trước hoặc ghi sau bằng transaction riêng đều tạo failure window.

## Stage 3 — Hands-on lab

### Attempt first — 15 minutes

Design a consumer for `CreditAccount` events. Your solution must preserve one credit per stable event, coordinate multiple replicas, roll back the marker when business processing fails, detect conflicting reused IDs, and acknowledge only after database success.

Sketch the transaction boundary and failure timeline before reading the solution. Then implement and run the cases below for 30 minutes. SQL Server is the data owner for both tables; the lab makes no external HTTP calls.

### Database setup

Use a fresh disposable SQL Server database. The scripts use `CREATE OR ALTER PROCEDURE`; choose a supported SQL Server installation that supports this syntax. Execute batches with SSMS or another tool that understands `GO`; `GO` is a client batch separator, not SQL sent through a database command.

```sql
CREATE TABLE dbo.Accounts
(
    AccountId bigint NOT NULL
        CONSTRAINT PK_Accounts PRIMARY KEY,
    Balance decimal(19,2) NOT NULL
);

CREATE TABLE dbo.ConsumerInbox
(
    ConsumerName varchar(80) NOT NULL,
    EventId uniqueidentifier NOT NULL,
    AccountId bigint NOT NULL,
    Amount decimal(19,2) NOT NULL,
    ProcessedAt datetime2(7) NOT NULL
        CONSTRAINT DF_ConsumerInbox_ProcessedAt
        DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_ConsumerInbox
        PRIMARY KEY (ConsumerName, EventId)
);

INSERT INTO dbo.Accounts (AccountId, Balance)
VALUES (42, 0);
GO
```

The composite primary key provides a durable uniqueness boundary. A SQL Server unique constraint is another way to express a domain uniqueness rule and creates a corresponding unique index [V4].

### Worked solution

```sql
CREATE OR ALTER PROCEDURE dbo.ApplyAccountCredit
    @EventId uniqueidentifier,
    @AccountId bigint,
    @Amount decimal(19,2)
AS
BEGIN
    SET NOCOUNT ON;

    -- This procedure owns the real commit, not a nested transaction.
    IF @@TRANCOUNT <> 0 OR (2 & @@OPTIONS) = 2
    BEGIN
        THROW 50000,
            'Call without an ambient or implicit transaction.', 1;
    END;

    SET XACT_ABORT ON;

    DECLARE @ConsumerName varchar(80) = 'account-credit-v1';

    IF @EventId IS NULL
       OR @AccountId IS NULL
       OR @AccountId <= 0
       OR @Amount IS NULL
       OR @Amount <= 0
    BEGIN
        THROW 50001, 'Invalid credit event.', 1;
    END;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Protect the existing key or insertion range until commit.
        IF EXISTS
        (
            SELECT 1
            FROM dbo.ConsumerInbox WITH (UPDLOCK, HOLDLOCK)
            WHERE ConsumerName = @ConsumerName
              AND EventId = @EventId
        )
        BEGIN
            IF NOT EXISTS
            (
                SELECT 1
                FROM dbo.ConsumerInbox
                WHERE ConsumerName = @ConsumerName
                  AND EventId = @EventId
                  AND AccountId = @AccountId
                  AND Amount = @Amount
            )
            BEGIN
                THROW 50002,
                    'Event ID reused with different business data.', 1;
            END;

            COMMIT TRANSACTION;
            SELECT 'AlreadyProcessed' AS Outcome;
            RETURN;
        END;

        INSERT INTO dbo.ConsumerInbox
            (ConsumerName, EventId, AccountId, Amount)
        VALUES
            (@ConsumerName, @EventId, @AccountId, @Amount);

        UPDATE dbo.Accounts
        SET Balance = Balance + @Amount
        WHERE AccountId = @AccountId;

        IF @@ROWCOUNT <> 1
        BEGIN
            THROW 50003, 'Account not found.', 1;
        END;

        COMMIT TRANSACTION;
        SELECT 'Applied' AS Outcome;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH;
END;
GO
```

**Call contract:** use a standalone command without a caller transaction or ambient `TransactionScope`, and with implicit transactions disabled. An inner `COMMIT` does not commit an outer transaction [V6]; acknowledging before the actual outer commit would violate the design. The entry guard rejects unsupported callers. It is not a savepoint-based procedure for use inside an existing transaction. Validate amount scale at ingress because conversion to `decimal(19,2)` can round extra fractional digits before the procedure compares them.

The existence check is protected by database locking. `HOLDLOCK` has `SERIALIZABLE` semantics for the table and transaction; `UPDLOCK` keeps update locks to transaction end [V3]. The indexed key allows key-range protection when no row exists. Lock granularity can be broader depending on the plan and workload; measure contention rather than claiming every attempt takes exactly one row lock.

The primary key remains the durable uniqueness boundary. The transaction couples it to the mutation. If the account is absent or the update fails, the inbox insert rolls back. `THROW` honors `XACT_ABORT`; explicit transaction-state handling preserves rollback behavior for catchable failures [V5]. Connection loss must still be treated as an unknown outcome, not as proof of rollback.

### Worker integration

```text
Deserialize and validate the immutable event
    ↓
Execute ApplyAccountCredit with SQL parameters, no outer transaction
    ↓
Applied or AlreadyProcessed
    ↓
Acknowledge the received message
```

For a .NET Service Bus handler using explicit completion, set `ServiceBusProcessorOptions.AutoCompleteMessages = false` [V7], await the database operation, then await `CompleteMessageAsync`. Check the installed SDK version before implementation. This lesson provides integration steps rather than an executed .NET worker.

If database processing fails, do not acknowledge success. Distinguish transient failure such as a deadlock or temporary connectivity loss from a permanent invalid event or identity conflict. Missing account behavior is domain-dependent: it may require a bounded retry for eventual arrival or a dead-letter reason for an invalid reference. Avoid unbounded poison-message retry loops.

### Verification A — duplicate and conflicting payload

Run once after setup:

```sql
EXEC dbo.ApplyAccountCredit
    @EventId = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    @AccountId = 42, @Amount = 100;

EXEC dbo.ApplyAccountCredit
    @EventId = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    @AccountId = 42, @Amount = 100;

IF NOT EXISTS
    (SELECT 1 FROM dbo.Accounts WHERE AccountId = 42 AND Balance = 100)
    THROW 51001, 'Duplicate test: unexpected balance.', 1;

IF (SELECT COUNT(*) FROM dbo.ConsumerInbox
    WHERE ConsumerName = 'account-credit-v1'
      AND EventId = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa') <> 1
    THROW 51002, 'Duplicate test: unexpected inbox count.', 1;
GO

BEGIN TRY
    EXEC dbo.ApplyAccountCredit
        @EventId = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        @AccountId = 42, @Amount = 250;

    THROW 51003, 'Conflict test: expected error 50002.', 1;
END TRY
BEGIN CATCH
    IF ERROR_NUMBER() <> 50002
        THROW;
END CATCH;

IF NOT EXISTS
    (SELECT 1 FROM dbo.Accounts WHERE AccountId = 42 AND Balance = 100)
    THROW 51004, 'Conflict test: balance changed.', 1;
GO
```

Expected: `Applied`, then `AlreadyProcessed`; the conflicting reuse raises `50002` and leaves the balance unchanged.

### Verification B — rollback and invalid input

```sql
BEGIN TRY
    EXEC dbo.ApplyAccountCredit
        @EventId = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        @AccountId = 999, @Amount = 10;

    THROW 51005, 'Rollback test: expected error 50003.', 1;
END TRY
BEGIN CATCH
    IF ERROR_NUMBER() <> 50003
        THROW;
END CATCH;

IF EXISTS
    (SELECT 1 FROM dbo.ConsumerInbox
     WHERE ConsumerName = 'account-credit-v1'
       AND EventId = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb')
    THROW 51006, 'Rollback test: marker was retained.', 1;
GO

BEGIN TRY
    EXEC dbo.ApplyAccountCredit
        @EventId = 'cccccccc-cccc-cccc-cccc-cccccccccccc',
        @AccountId = 42, @Amount = NULL;

    THROW 51007, 'Validation test: expected error 50001.', 1;
END TRY
BEGIN CATCH
    IF ERROR_NUMBER() <> 50001
        THROW;
END CATCH;

IF EXISTS
    (SELECT 1 FROM dbo.ConsumerInbox
     WHERE ConsumerName = 'account-credit-v1'
       AND EventId = 'cccccccc-cccc-cccc-cccc-cccccccccccc')
    THROW 51008, 'Validation test: marker was retained.', 1;
GO
```

Expected: no marker for either event. Now create account `999` and retry event `bbbbbbbb...` unchanged. It should apply once: the failed first attempt did not falsely mark it completed.

### Verification C — concurrent replicas

Open two independent SQL connections. From both, submit the same new event at nearly the same time:

```sql
EXEC dbo.ApplyAccountCredit
    @EventId = 'dddddddd-dddd-dddd-dddd-dddddddddddd',
    @AccountId = 42, @Amount = 25;
```

In a disposable copy of the procedure, you can temporarily insert `WAITFOR DELAY '00:00:05';` immediately after the inbox insert to hold the first transaction while the second arrives. Remove that delay after the experiment. This deliberately forces overlap; simultaneous clicks alone may execute sequentially.

After both attempts succeed, or transient deadlock victims are retried with the same event ID, assert:

```sql
IF NOT EXISTS
    (SELECT 1 FROM dbo.Accounts WHERE AccountId = 42 AND Balance = 125)
    THROW 51009, 'Concurrency test: unexpected balance.', 1;

IF (SELECT COUNT(*) FROM dbo.ConsumerInbox
    WHERE ConsumerName = 'account-credit-v1'
      AND EventId = 'dddddddd-dddd-dddd-dddd-dddddddddddd') <> 1
    THROW 51010, 'Concurrency test: unexpected inbox count.', 1;
```

Record whether you observed waiting, a deadlock, or immediate completion. Repeat with fresh IDs and accounts to test additional schedules. One passing schedule is useful evidence, not an exhaustive proof.

### Verification D — commit before acknowledgment

For a broker integration test, terminate the worker immediately after the procedure returns `Applied` and before it acknowledges. Allow redelivery after the lock is released or expires. The repeated call should return `AlreadyProcessed`, then acknowledgment should succeed, with one balance increase and one inbox entry.

A SQL-only replay can verify the database behavior, but cannot demonstrate actual broker redelivery. Keep those two kinds of evidence separate.

### Verification E — unknown commit outcome

In a disposable environment, interrupt the client connection around commit, before the client receives the result. Preserve the event ID and retry. Do not infer rollback solely from a timeout.

| Actual database outcome | Expected retry outcome |
| --- | --- |
| Transaction did not commit | `Applied`, with inbox and mutation committing together |
| Transaction committed but response was lost | `AlreadyProcessed`, without another mutation |

Verify the inbox and balance from a separate connection. If a transaction is still resolving, the retry may wait or fail transiently before the outcome becomes visible. Do not acknowledge merely because the client lost its connection.

Save observations with event IDs, starting and final balances, inbox counts, errors, and whether SQL-only or broker integration was exercised. No successful runtime result is claimed for these exercises until you run them.

### Reduced-support task

Without copying the procedure, sketch an inventory-reservation handler for an event containing `reservationId`, `productId`, and `quantity`. Several event IDs may refer to one reservation. State which identity prevents transport duplicates, which domain constraint prevents repeated reservations, and which updates must be atomic. Include a condition that prevents available stock from becoming negative, then design a two-worker test for different reservations competing for the final item. Explain why event deduplication alone cannot protect that business invariant.

## Stage 4 — Production twist

### Ten times the traffic

Several replicas still coordinate through the database. A local `HashSet`, `lock`, or semaphore does not cover all replicas and does not survive process loss.

Measure processing latency, queue age, lock waits, deadlocks, retry rate, duplicate outcomes, inbox growth, and commit-success/completion-failure events. Concurrency should follow database capacity. Updates to the same account serialize even when event IDs differ; adding workers can increase contention.

Retry deadlock victims as complete operations using the same event ID, with bounded backoff and jitter. A duplicate-key error from another business table is not proof that this event completed. Check the relevant constraint and transaction outcome rather than swallowing every unique-constraint exception.

### Broker deduplication and business uniqueness

Service Bus duplicate detection filters repeated submitted message identities within its configured history window [V2]. It does not atomically couple a consumer database commit to message completion. Partitioning changes the identity used for broker detection; see the official documentation before configuring it.

| Boundary | Protection |
| --- | --- |
| Producer → broker | Broker duplicate detection can reduce duplicate accepted sends |
| Event → consumer database | Transactional inbox prevents repeated committed effects for a retained event identity |
| Business operation → domain state | A domain unique key protects one logical operation even if several event IDs represent it |

For the source import scenario, use a stable request/job identity and domain uniqueness for imported records. A filename alone may identify neither the same content nor the same intended operation.

### Retention and replay

Deleting a marker removes knowledge that the event was processed. Choose retention from the longest replay horizon, including dead-letter recovery and manual replay. Preserve a longer-lived business key or define a controlled replay policy when messages may arrive after inbox deletion.

The consumer name also matters. Renaming `account-credit-v1` creates a new namespace; old events can apply again under it. Treat namespace changes and payload evolution as a migration decision.

### External side effects — a follow-up boundary

Calling an email or payment API inside this database transaction cannot roll back the external effect. Calling it after commit creates another crash window.

An adjacent design is to insert an outbox record together with the business update, then dispatch it separately. The dispatcher still faces uncertainty between sending and recording success. A stable downstream idempotency key, an idempotent receiving consumer, or reconciliation is needed where supported. An outbox alone does not guarantee exactly one external effect.

This is a follow-up topic with a distinct objective: **reliably publish a committed business event and reconcile downstream delivery**. It is not a second lesson that merely renames the inbox objective.

## Stage 5 — Interview round

### Why the interviewer asks this

The question tests whether you can locate a failure boundary, coordinate concurrent instances, distinguish delivery from business guarantees, and prove behavior. A definition without the transaction and failure timeline leaves the most useful reasoning unstated.

Practice **direct claim → mechanism → example → trade-off → evidence → optional bridge**. Give a bounded answer first, then expand if asked. This makes your assumptions inspectable and reduces accidental overclaims. It does not prevent legitimate deep follow-ups; prepare to defend them honestly.

### 30-second model answer

> I assume a message can be redelivered after processing, because the database can commit before acknowledgment succeeds. I use a stable event ID and a consumer-specific inbox key. The inbox entry and business mutation commit in one database transaction, so retries skip a matching completed operation. I acknowledge after commit and verify the design with concurrent-delivery, rollback, and crash tests. The guarantee covers that database mutation; external effects need an additional design.

### 90-second model answer

> I would first define the guarantee: repeated deliveries of one stable event must not repeat its committed mutation in the consumer database. The failure window is between the database commit and acknowledgment. If the worker crashes there, the broker can redeliver even though the work succeeded.
>
> I use a consumer-specific inbox keyed by event ID. The inbox insert and business update happen in one SQL transaction, with database uniqueness and appropriate concurrency control. A matching existing entry means the operation already committed. Reusing the same ID with different business data is rejected. I acknowledge only after that transaction succeeds.
>
> For example, a credit event must increase an account balance once even when two replicas receive copies. A standalone existence check cannot prevent both replicas from passing. The transaction and database constraint protect the invariant. Stable IDs matter; if a producer generates a new ID for the same payment, I also need a business unique key.
>
> The trade-offs are inbox retention, storage, and lock contention. I validate duplicate delivery, failed business updates, concurrency, and a crash after commit. In production, I monitor queue age, duplicate outcomes, deadlocks, and settlement failures. This covers local database effects. If we extend the flow to publish an event or call a payment provider, I would examine an outbox and downstream idempotency next.

The example is hypothetical lab work. Replace it with your own incident or measurements only when you have evidence; do not present this model answer as personal production experience.

### Defend deeper follow-ups

| Interviewer follow-up | Defensible answer boundary |
| --- | --- |
| Why not just check before insert? | An ordinary check can race; this implementation holds database locks in the same transaction and retains a primary key. |
| Why not only rely on the broker lock? | The lock is volatile, and duplicate copies can be separate broker messages; database effects need their own invariant. |
| Why not catch any duplicate-key exception? | A different unique constraint may fail; an exception alone does not prove this event committed. |
| Does a timeout mean retry is dangerous? | The outcome can be unknown. Retry the whole operation with the same identity; it either applies or recognizes the commit. |
| What if I use a new ID on retry? | Event deduplication cannot recognize the same operation. Preserve identity and add domain uniqueness where needed. |
| Why not a distributed transaction? | It adds coordination and availability costs and only applies where all participants support the required protocol. This design needs one local owner and tolerates broker redelivery. |
| Can you promise exactly-once delivery? | No such guarantee is made here. I can defend one committed local mutation per retained stable identity, with retry/recovery requirements. |
| When can inbox rows be deleted? | After the chosen replay horizon, or with a longer-lived domain invariant and controlled replay policy. |

### An honest bridge

After answering the question fully, you may close with: **“If the next requirement is publishing the committed result to another service, the next boundary to examine is the outbox and downstream idempotency.”** This offers a relevant continuation without hiding a limitation or trying to redirect away from an unanswered question.

Record a 90-second answer. Listen for an unsupported “exactly once,” jargon before explanation, or a missing commit/acknowledgment gap. Re-record once with those gaps corrected. Then ask a partner to choose two unpredictable follow-ups from the table.

## Stage 6 — Feedback and self-assessment

No learner attempt has been submitted; all scores are unassigned. A self-rating is useful reflection but is not a verified assessment.

Use a 0–4 rubric: **0** missing or incorrect; **1** terminology without a workable model; **2** correct normal case; **3** correct handling of retries, concurrency, and failure boundaries; **4** justified alternatives and observable validation.

| Dimension | Evidence for a strong attempt |
| --- | --- |
| Technical correctness | Identifies stable identity and atomic inbox/business commit |
| Reasoning | States the guarantee and distinguishes broker, event, and domain deduplication |
| Implementation | Runs duplicate, conflict, rollback, and concurrent attempts with recorded outcomes |
| Operations | Handles transient failures, retention, unknown outcomes, and useful telemetry |
| Communication | Explains the failure window plainly within 90 seconds and answers follow-ups without overclaiming |

Submit your transaction sketch, lab output, and spoken-answer transcript for feedback. Assessment should quote the exact evidence supporting each score, identify one or two gaps, and assign a focused correction exercise. Merely reading this lesson does not establish mastery.

## Stage 7 — Retrieval close

Close the worked solution and answer without looking:

1. Which failure window makes a transactional inbox useful?
2. Which two writes must commit atomically, and what happens if either is written separately?
3. How do event identity and business identity differ?
4. Why can more worker replicas reduce throughput on a hot account?
5. What guarantee is lost after deleting the inbox entry, and what changes for an external payment call?

Explain your SQL transaction from memory, then recreate only its key control flow. Compare with the solution after your attempt. At the next review, use a different scenario, such as a repeated inventory reservation, to test transfer rather than memorized credit code.

Reviews are scheduled from **actual learner completion D**, not generation. Suggested intervals are D+1, D+3, D+7, D+14, D+30. If completion occurs on 8 October 2026 in Asia/Bangkok, those dates are 9 October, 11 October, 15 October, 22 October, and 7 November. These are conditional examples, not active review entries.

## Stage 8 — Learning record

This generated artifact has no completion evidence. Persist it as `generated`; use `in_progress` after an actual attempt and `completed` only under the learning-state completion rules. Assessment and review dates stay empty until appropriate evidence is available.

```yaml
LESSON_RECORD:
  lesson_id: 2026-10-08-messaging-idempotent-consumer
  lesson_path: lessons/2026-10-08-messaging-idempotent-consumer.md
  topic_id: messaging-idempotent-consumer
  domain: messaging-event-driven
  level: senior
  mode: full-lesson
  status: generated
  created_at: "2026-10-08"
  completed_at: null
  objectives:
    - Implement an atomic SQL Server inbox and business update that handles concurrent deliveries and conflicting event identities.
    - Explain redelivery after a successful database commit and identify the acknowledgment failure window.
    - Verify rollback, retries, and unknown commit outcomes without assuming every timeout means failure.
    - Deliver a concise interview answer with a defensible guarantee, trade-offs, and an honest follow-up bridge.
  concept_fingerprint:
    - at-least-once-delivery
    - stable-event-identity
    - transactional-inbox
    - atomic-business-update
    - concurrent-consumers
    - commit-acknowledgment-gap
    - failure-injection
  score:
    technical: null
    reasoning: null
    implementation: null
    operations: null
    communication: null
  evidence: []
  weak_points: []
  review_due: []
  source_refs:
    - sources/04-architecture-distributed-systems.md#q024
    - sources/04-architecture-distributed-systems.md#q025
    - sources/04-architecture-distributed-systems.md#q026
    - sources/04-architecture-distributed-systems.md#production-scenario
    - sources/02-aspnet-api-ef.md#background-processing
    - sources/02-aspnet-api-ef.md#large-file-processing-scenario
    - https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement
    - https://learn.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection
    - https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table
    - https://learn.microsoft.com/en-us/sql/t-sql/statements/set-xact-abort-transact-sql
    - https://learn.microsoft.com/en-us/sql/relational-databases/tables/create-unique-constraints
    - https://learn.microsoft.com/en-us/sql/t-sql/language-elements/commit-transaction-transact-sql
    - https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/servicebus/Azure.Messaging.ServiceBus/src/Processor/ServiceBusProcessorOptions.cs
```

### Runtime verification status

On 2026-10-08, an attempt to run the SQL lab on a disposable SQL Server 2022
container was blocked before container creation: image blobs redirected from
`mcr.microsoft.com` to `centralus.data.mcr.microsoft.com`, which the environment
proxy denied with HTTP 403. No SQL assertions or broker crash tests were run.
Documentation verification below is complete; runtime outcomes remain expected
results for the learner to verify. This infrastructure check is not learner
completion evidence.

### Verification evidence

`checked_at: 2026-10-08`. Microsoft Learn pages are linked for readers. Their current official MicrosoftDocs source files were read through GitHub during preparation; the claims below describe documentation verification, not lab execution.

| ID | Verified claim | Official reader reference | Official source read |
| --- | --- | --- | --- |
| V1 | Peek-Lock completion and lock operations can fail; already processed work can be redelivered | [Message transfers, locks, and settlement](https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement) | [MicrosoftDocs source](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/service-bus-messaging/message-transfers-locks-settlement.md) |
| V2 | Broker duplicate detection tracks submitted message identities within a configured time window; partitioning affects the identity | [Duplicate detection](https://learn.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection) | [MicrosoftDocs source](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/service-bus-messaging/duplicate-detection.md) |
| V3 | `HOLDLOCK` is equivalent to `SERIALIZABLE`; `UPDLOCK` keeps update locks to transaction completion | [Table hints](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table) | [MicrosoftDocs source](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/t-sql/queries/hints-transact-sql-table.md) |
| V4 | A SQL Server unique constraint prevents duplicate values and creates a corresponding unique index | [Create unique constraints](https://learn.microsoft.com/en-us/sql/relational-databases/tables/create-unique-constraints) | [MicrosoftDocs source](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/relational-databases/tables/create-unique-constraints.md) |
| V5 | `THROW` honors `SET XACT_ABORT`; runtime errors and compile errors have different handling | [SET XACT_ABORT](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-xact-abort-transact-sql) | [MicrosoftDocs source](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/t-sql/statements/set-xact-abort-transact-sql.md) |
| V6 | A nested `COMMIT` only decrements `@@TRANCOUNT`; permanence depends on the outer commit | [COMMIT TRANSACTION](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/commit-transaction-transact-sql) | [MicrosoftDocs source](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/t-sql/language-elements/commit-transaction-transact-sql.md) |
| V7 | .NET Service Bus processor automatic completion is configurable with `AutoCompleteMessages` and defaults to true in the checked source | [Official .NET SDK source](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/servicebus/Azure.Messaging.ServiceBus/src/Processor/ServiceBusProcessorOptions.cs) | Same official source |

[Lesson index](index.md) · [Daily Interview Mastery skill](../agent/SKILL.md) · [Repository guide](../README.md)
