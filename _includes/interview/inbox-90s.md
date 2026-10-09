> I would identify the logical credit with a stable event ID, then put the inbox marker and balance update in the same database transaction. The key invariant is that a committed marker means that the business effect committed too.
>
> If a failure happens between the two writes, both roll back and the same event can be retried. If the database commits but the broker acknowledgment fails, a later delivery finds the marker and skips the credit. Reusing that ID with different business data is a contract error that I would reject.
>
> In this lab, the failure-after-marker test distinguishes the correct transaction from two separate commits. For the project's SQL Server implementation, I would also test concurrent workers and uncertain commit responses rather than infer those guarantees from SQLite. The trade-offs are database writes, contention and keeping deduplication records for the replay horizon. An external side effect has a separate failure boundary.
