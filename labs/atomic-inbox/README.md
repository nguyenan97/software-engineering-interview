# Atomic inbox lab

One task: move the marker and credit into one transaction so a failed operation
can be retried safely. Requires Python 3.10+ with its `sqlite3` module; no pip
packages, database server, Docker or account are needed.

If downloaded as a ZIP, unzip it, enter `atomic-inbox/`, then run
`python verify.py`. After your attempt, `python verify.py --solution` runs the
reference. The repository-relative commands below apply to a checkout.

From the repo root:

```sh
python labs/atomic-inbox/verify.py
```

The starter deliberately fails **two** of five checks: injected failure retains
the marker, and a missing account also retains it. Predict these outcomes before
running. Edit only `exercise.py`; do not delete checks. Make all five pass, then
explain why the transaction boundary changed the outcome.

After an attempt, compare with `solution.py` or run:

```sh
python labs/atomic-inbox/verify.py --solution
```

Transfer task: adapt the operation to reserve inventory instead of crediting an
account. A failed reservation must leave neither mutation nor marker. Reuse the
same identity on retry. Write a new failure check before editing the operation.

The lab uses isolated, in-memory SQLite databases and integer cents, with one
consumer and explicit SQL transaction control. It models redelivery by calling
the function again; it does not run a message broker or prove SQL Server lock
behavior. SQLite serializes writers differently from SQL Server. The lesson
includes an optional SQL Server adaptation with its separate execution status.

[Focused lesson](../../lessons/2026-10-08-messaging-idempotent-consumer.md)
