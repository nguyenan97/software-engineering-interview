---
layout: lesson
title: 'One Transaction: Make a Failed Credit Safe to Retry'
lesson_id: 2026-10-08-messaging-idempotent-consumer
topic_id: messaging-idempotent-consumer
domain: messaging-event-driven
level: senior
mode: full-lesson
created_at: '2026-10-08'
status: generated
objectives:
- Implement an atomic SQL Server inbox and business update that handles concurrent
  deliveries and conflicting event identities.
- Explain redelivery after a successful database commit and identify the acknowledgment
  failure window.
- Verify rollback, retries, and unknown commit outcomes without assuming every timeout
  means failure.
- Deliver a concise interview answer with a defensible guarantee, trade-offs, and
  an honest follow-up bridge.
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
checked_at: '2026-10-08'
lesson_format: focused-v1
duration_minutes: 40
practice_minutes: 28
refactored_at: '2026-10-09'
primary_objective: Keep the inbox marker and business update in one transaction so
  a failed credit can be retried safely.
prerequisites_note: Basic SQL transactions. Python 3.10+ with sqlite3 for the portable
  lab; SQL Server is optional.
---

## A · Set the goal — 2 minutes
{: #goal }

**After this lesson, you can repair a retry bug by committing an inbox marker and an account credit together, then prove the repair with a failed-attempt test.**

Imagine an account-credit worker crashes after recording that an event was handled, but before changing the balance. A retry must still be able to apply the credit. An **inbox marker** is a durable record of a handled logical operation; it is useful only when its meaning agrees with the committed business state.

| Lesson card | Value |
| --- | --- |
| Topic / lesson | `messaging-idempotent-consumer` / `2026-10-08-messaging-idempotent-consumer` |
| Domain / level / ring | Messaging and event-driven systems / senior / A — source-direct |
| Source seed | [Message queues and background processing, Q024–Q026](../sources/04-architecture-distributed-systems.md#q024); [credit-like production scenario](../sources/04-architecture-distributed-systems.md#production-scenario) |
| Selection | The source asks about queue failures. This existing sample is refactored around one transaction invariant; it is **not a second new lesson**. |
| Core / optional | 40 minutes, including 28 minutes of lab, verification and recall. SQL Server concurrency is an optional extension. |
| Mode | Full lesson: complete answers are available in expandable sections. Try first. |

Success means you can (1) draw the correct transaction boundary, (2) show that an injected failure leaves **no marker and no credit**, and (3) explain why the retry works. These are checks of one objective. The original catalog objectives and fingerprint remain in the generation metadata for provenance; the SQL Server implementation is retained below.

Use a disposable environment. The portable Python/SQLite lab demonstrates the same transaction invariant used by the project's SQL Server stack. It does **not** simulate a broker or validate SQL Server locking. If basic `COMMIT` and `ROLLBACK` are unfamiliar, begin with the state trace in C; a senior label does not prove prerequisites.

**Next:** [Predict the failure before opening an answer](#predict).
{: .next-step }

## B · Predict first — 4 minutes
{: #predict }

<div class="task-box" markdown="1">

Do not run the code yet. Write your prediction and one reason.

```text
BEGIN
  insert inbox(event-7, account-42, +100 cents)
COMMIT

BEGIN
  update account balance +100
COMMIT
```

1. The worker crashes between the two transactions. What are the balance and inbox contents?
2. On retry, it sees `event-7` in the inbox and skips the credit. Is the operation actually complete?
3. Would a unique event ID alone fix this bug?

**Practical challenge:** Repair the transaction boundary without removing deduplication. Start with balance `0`. A successful first attempt followed by the same event must leave balance `100`; a failure before the business update must leave balance `0` **and no inbox row**.

</div>

An unanswered prediction is a starting point for teaching, not a score or diagnosed weakness. Keep it to compare with your test output.

**Next:** [Understand the invariant](#model).
{: .next-step }

## C · Understand why — 6 minutes
{: #model }

**Problem → cause.** Retrying an operation can duplicate its effect. But recording “processed” before the effect commits creates the opposite bug: a failed operation is skipped forever. The marker and balance tell different stories.

**Mechanism.** Commit the marker and mutation in **one database transaction**. For this handler, the invariant is: a committed marker means that this event's credit committed in the same transaction.

```text
New event → BEGIN → insert marker → apply credit → COMMIT → Applied
                        │                 │
                        └── failure ──────┴── ROLLBACK → retry may apply

Same event after commit → validate stored business data → AlreadyProcessed
```

A rollback discards both changes; a successful commit keeps both. A later delivery with the same identity and business data sees the marker and skips the mutation. An identity reused with different data must be rejected, not quietly accepted.

| Attempt | Committed balance | Committed marker | Next delivery |
| --- | --- | --- | --- |
| Failure after inserting marker, before credit | 0 | None | Can apply |
| Successful credit | 100 | `event-7` | Skip the same credit |
| Same ID with a different amount | Still 100 | Original data | Reject the conflicting identity |

The portable lab uses SQLite's explicit `BEGIN IMMEDIATE`, `COMMIT`, and `ROLLBACK`. SQLite permits one write transaction at a time; starting it can fail when another writer is active. Those are [SQLite transaction semantics](https://www.sqlite.org/lang_transaction.html), not a SQL Server locking model. With Python `sqlite3`, the verifier sets `isolation_level=None` and uses explicit SQL transactions ([official Python documentation](https://docs.python.org/3/library/sqlite3.html), checked 2026-10-09).

**Boundary.** This protects one database effect. It does not atomically commit a remote HTTP call or a broker acknowledgment. Never turn the invariant into a promise that every distributed action occurs exactly once.

**Vietnamese Note:** Inbox không phải chỉ là “đã nhận tin”. Trong bài này, marker chỉ có ý nghĩa khi việc cộng tiền đã commit cùng nó. Tách hai commit có thể khiến retry bỏ qua một việc chưa làm xong.

**Next:** [Repair the starter and observe the failure](#practice).
{: .next-step }

## D · Try the lab — 16 minutes
{: #practice }

**Setup:** Python 3.10+ with the standard-library `sqlite3` module. No database server, package install, network service or credentials. The verifier creates a fresh in-memory database for each test.

<a class="button button-primary" href="{{ '/assets/labs/atomic-inbox.zip' | relative_url }}" download>Download the runnable lab (.zip)</a>

Unzip, enter the extracted `atomic-inbox/` directory, and run `python verify.py`. If using a repository checkout instead, run:

```bash
python labs/atomic-inbox/verify.py
```

Files: `exercise.py` is the intentionally broken starter; `verify.py` contains five checks; `solution.py` is the reference. See [lab setup](../labs/atomic-inbox/README.md) for scope and commands.

<div class="task-box" markdown="1">

**Your task:** Edit only `apply_credit` in `exercise.py`. Keep its signature and outcomes `Applied` / `AlreadyProcessed`. Use positive integer cents. Reject a changed account or amount under the same event ID. Make rollback remove the marker when the credit cannot happen. Do not change tests to accept the bug.

1. Run the starter. It should pass the normal retry test but fail the injected-failure and missing-account tests.
2. Move the boundary; explain what must be inside it.
3. Run again until all five tests pass. Keep your actual output and your prediction.

**Evidence question:** Which test distinguishes a correct transaction from a happy-path-only implementation?

</div>

<details markdown="1" data-answer>
<summary>Open the complete worked solution after your attempt</summary>

```python
"""Reference solution for the single-consumer SQLite learning lab."""


def apply_credit(db, event_id, account_id, amount, fail_after_marker=False):
    if type(amount) is not int or amount <= 0:
        raise ValueError("Amount must be positive integer cents")
    db.execute("BEGIN IMMEDIATE")
    try:
        existing = db.execute(
            "SELECT account_id, amount FROM inbox WHERE event_id = ?", (event_id,)
        ).fetchone()
        if existing:
            if existing != (account_id, amount):
                raise ValueError("Event identity reused with different business data")
            db.execute("COMMIT")
            return "AlreadyProcessed"

        db.execute("INSERT INTO inbox VALUES (?, ?, ?)", (event_id, account_id, amount))
        if fail_after_marker:
            raise RuntimeError("Injected failure after marker")
        updated = db.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
            (amount, account_id),
        )
        if updated.rowcount != 1:
            raise ValueError("Account not found")
        db.execute("COMMIT")
        return "Applied"
    except Exception:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
```

`BEGIN` comes before the lookup and both writes. One `COMMIT` makes the marker meaningful. On a failed account update or injected exception, `ROLLBACK` restores both tables. The existing marker is checked against the original business data, so ID reuse is not mistaken for a legitimate retry.

Compare without editing the starter:

```bash
python labs/atomic-inbox/verify.py --solution
```

From the downloaded directory, use `python verify.py --solution`. Passing the reference does not show that your own repair works: run the default command against your edited starter too.

</details>

### Transfer: reserve inventory with fewer hints

A handler must decrement available stock by `2` for one reservation ID. Change the account example to inventory. Design the transaction and a test where insufficient stock rejects the reservation. On rejection, what must remain retryable? Spend the last four minutes on a state trace or code sketch; you need not build another database.

<details markdown="1" data-answer>
<summary>Transfer answer guide</summary>

Keep the reservation marker and stock decrement in the same transaction. Update only if stock is at least the requested quantity; if no row qualifies, roll back the marker too. A rejected reservation must leave stock unchanged and no committed success marker. Once stock is replenished, a retry may succeed. A committed reservation replay must not decrement stock again. Compare the failure trace with the account-not-found test: it is the same invariant in a new setting.

</details>

**Next:** [Compare predictions with the checks](#verify).
{: .next-step }

## E · Verify and correct — 6 minutes
{: #verify }

| Check | Expected result for the repair | Evidence to inspect |
| --- | --- | --- |
| First delivery then same event | `Applied`, then `AlreadyProcessed`; balance 100, one marker | Return values and both tables |
| Failure immediately after marker | Balance 0, no marker; retry succeeds | Rollback state, then retry state |
| Missing account | Error; no marker committed | Inbox count |
| Same ID, changed business data | Error; original balance and marker retained | Stored account/amount and balance |
| Invalid amount | Error; no writes | 0, negative, boolean and fractional inputs |

**Checks actually run during preparation (2026-10-09):** the reference implementation passed all five tests. The unchanged starter failed the two intended rollback tests. These are author checks, not learner evidence. No SQL Server runtime, broker, multi-worker concurrency, process termination or unknown-commit outcome was exercised by this portable suite.

**One important misconception:** “If the normal retry passes, the handler is safe.” The starter passes that path while losing a credit after failure. Compare your B prediction with the injected-failure output. If you missed the retained marker, draw the two committed states and rerun only that scenario; then explain why the repair changes it. An agent gives feedback on your actual output, not a guessed weakness.

### Production twist: commit succeeds, acknowledgment fails

After the correct database transaction commits, a broker acknowledgment may fail and the message may return ([Service Bus settlement, V1 below](https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement)). Do not undo the committed credit simply because acknowledgment failed. The stable identity lets the retry return `AlreadyProcessed`. A database timeout or lost response can also leave the client unsure whether commit succeeded; retry the **same** identity rather than inventing a new operation.

| Decision | Suitable condition | Cost / failure boundary | Validation |
| --- | --- | --- | --- |
| Durable inbox plus business transaction | Non-idempotent database mutation may be retried | Extra writes, retained history and contention; no remote-call atomicity | Rollback/replay tests; production concurrency and recovery tests |
| Naturally idempotent update | Assigning the same intended value is safe under the domain's ordering rules | An old event may overwrite newer state unless ordering is handled | Out-of-order and replay tests |

A process-local “seen IDs” set cannot survive a restart or coordinate replicas. SQL Server locking, concurrent callers and the acknowledgment contract require additional validation; use the optional adaptation below when ready. This lesson's portable checks establish the transaction invariant in its stated environment only.

In production, track applied/replayed outcomes, identity conflicts and transaction failures; inspect the inbox and business state using a sanitized event identity when investigating a retry. Rising replay counts explain extra processing attempts, not duplicate credits by themselves. Measure contention before changing the transaction design.

**Next:** [Close answers and explain the mechanism from memory](#recall).
{: .next-step }

## F · Say it and recall — 6 minutes
{: #recall }

**Interview question:** “How would you stop a retried account-credit event from changing the balance twice?”

**Likely assessment intent:** Can you explain a durable invariant, partial failure and the boundary of your guarantee? This is an inference about the question, not a universal interviewer rubric.

Speak your own 30-second answer first. Expand to 90 seconds with the failed-attempt example, one trade-off and the test you would run. Time your speech rather than assuming a word count is exact.

<details markdown="1" data-answer>
<summary>30-second model answer</summary>

> I would use a stable event ID and commit the inbox marker together with the account credit in one database transaction. A failed attempt rolls back both, so it remains retryable. A replay after commit finds the marker and skips the credit. This protects the database effect; a remote call needs a separate strategy.

</details>

<details markdown="1" data-answer>
<summary>90-second model answer, two follow-ups and a related-topic bridge</summary>

> I would identify the logical credit with a stable event ID, then put the inbox marker and balance update in the same database transaction. The key invariant is that a committed marker means that the business effect committed too.
>
> If a failure happens between the two writes, both roll back and the same event can be retried. If the database commits but the broker acknowledgment fails, a later delivery finds the marker and skips the credit. Reusing that ID with different business data is a contract error that I would reject.
>
> In this lab, the failure-after-marker test distinguishes the correct transaction from two separate commits. For the project's SQL Server implementation, I would also test concurrent workers and uncertain commit responses rather than infer those guarantees from SQLite. The trade-offs are database writes, contention and keeping deduplication records for the replay horizon. An external side effect has a separate failure boundary.

**Follow-up 1 — Why is a unique event ID insufficient?** It prevents two committed markers but does not make the credit atomic with the marker. The broken starter proves that failure can commit the marker without any credit.

**Follow-up 2 — What if a timeout happens during commit?** A missing response does not establish rollback. Reuse the same logical ID; a committed marker leads to skipping, while no committed marker permits a fresh attempt. Connection recovery and retry policy need runtime testing.

**Optional bridge after the complete answer:** “If this handler also needs to publish an event, the next question is coordinating that publication through an outbox.” Be ready to explain the limit: the outbox records publication intent in the database transaction; a publisher can still retry, so downstream idempotency remains relevant. Answer direct follow-ups first. This bridge does not prevent deeper questions.

These answers use “I would” and “in this lab”; they do not invent production experience.

</details>

<button type="button" class="button button-secondary" data-close-answers disabled>Close answers for recall</button>
<p id="recall-status" role="status" aria-live="polite">Close the explanation or cover it. Answer without notes.</p>

1. State the invariant linking the inbox row to the account credit.
2. A reservation fails because inventory is insufficient. What must the transaction leave behind, and why?
3. Commit succeeds but acknowledgment fails. Why is a stable identity still needed?

<details markdown="1" data-answer>
<summary>Retrieval guide — open after answering</summary>

1. A committed marker means this event's credit committed in the same transaction.
2. No success marker and no stock change; otherwise a retry could skip a reservation that never happened.
3. Redelivery must identify the same logical operation so it can skip the already committed effect.

</details>

### Evidence, feedback and your next session

Save your edited function, actual test output, prediction correction and spoken-answer transcript (or a short written attempt). Ask the agent: **“Review my attempt; correct one misconception, then let me retry.”** Reading this page or running the provided reference is not a completion signal.

| Rubric dimension | Evidence | Score at delivery |
| --- | --- | --- |
| Technical | Correct transaction invariant and scope | `null` |
| Reasoning | Explains why two commits fail and compares an alternative | `null` |
| Implementation | Own repair plus meaningful failure test | `null` |
| Operations | Explains retry after failure and commit/ack gap | `null` |
| Communication | Direct 30–90-second answer, defended follow-ups | `null` |

Use the [0–4 rubric](../agent/INTERVIEW_METHOD.md#evidence-based-feedback) only for observed dimensions. Then retry the specific gap. Completion means an evidenced attempt, not a certification of mastery.

The saved record is still `generated`, created `2026-10-08`, with `completed_at: null`, all scores null, no evidence and no review dates. Refactoring on `2026-10-09` preserves that history. Your repo agent saves the attempt and session step; the public site saves at most a browser reading bookmark. See [the real state workflow](../docs/workflow.md).

After evidenced completion, reviews begin at **D+1, D+3, D+7, D+14 and D+30**. Use a different account or inventory example and answer before opening notes. The agent can adjust an unperformed review based on actual evidence and record the reason; it cannot backfill a review. **Next:** submit your attempt, or [start a review with the agent](../practice/review.md).

## Optional depth — outside the 40-minute session

<details markdown="1" data-answer>
<summary>SQL Server adaptation: durable uniqueness and concurrent callers</summary>

This retained implementation serves the project's SQL Server stack and original catalog objectives. It requires a disposable supported SQL Server instance and further tests; **it was not executed in this environment**. The portable SQLite tests do not validate these locks. In production, scope the inbox identity to the consumer contract and retain markers for the supported replay horizon.

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



Additional verification plan: concurrent identical callers must apply once; conflicting same-ID payloads must be rejected; a missing account must roll back its marker; a crash after commit must permit replay without another credit. Test deadlocks/transient retries using the same identity. A timeout is an unknown outcome until resolved; it is not evidence that rollback happened. Avoid remote calls while holding the transaction open.

For a Service Bus worker, configure the acknowledgment contract explicitly: process the database operation first and complete the broker message only after the real commit. The checked .NET processor source allows `AutoCompleteMessages = false` [V7]; do not manually complete while also relying on automatic completion. Preserve stable business identity across retries. Broker duplicate detection has a configured time window and its own scope [V2]; it does not replace atomic consumer effects.

</details>

<details markdown="1">
<summary>Source provenance and dated verification</summary>

The source questions are interview seeds, not validated answers: [Q024](../sources/04-architecture-distributed-systems.md#q024), [Q025](../sources/04-architecture-distributed-systems.md#q025), [Q026](../sources/04-architecture-distributed-systems.md#q026), [background processing](../sources/02-aspnet-api-ef.md#background-processing) and [large-file scenario](../sources/02-aspnet-api-ef.md#large-file-processing-scenario).

Portable scope checked on 2026-10-09: [SQLite transaction documentation](https://www.sqlite.org/lang_transaction.html) describes explicit transactions and the single-writer boundary; [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) describes `isolation_level=None` with explicit transaction SQL. The lab requires Python 3.10+ with `sqlite3`; no newer `autocommit` constructor option is used. Runtime evidence is the five portable checks in E, not proof about another database.

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



SQL Server execution remains unverified: the container image download was blocked by the environment's network policy. Retained Microsoft checks are dated 2026-10-08; the refactor does not falsely redate them. Official-doc checks and runtime tests are separate evidence.

</details>
