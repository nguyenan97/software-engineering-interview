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
