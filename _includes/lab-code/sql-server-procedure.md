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
