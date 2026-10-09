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
