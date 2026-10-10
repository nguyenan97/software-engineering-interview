# Department headcount lab

Repair `exercise.sql`: return `(DepartmentId, Name, EmployeeCount)` for departments
with **more than three** employees, ordered by DepartmentId. Count people even if
their name is NULL; identical department names do not identify the same department.
Use all employees for this source task, not only active ones.

Python 3.10+ with standard-library sqlite3 is sufficient. Each check recreates an
in-memory database; no server, credentials or persistent database is used.

From the repository root:

```sh
python labs/department-headcount/verify.py
python labs/department-headcount/verify.py --solution --extensions
```

The unmodified starter fails four of six core checks. Try and edit the starter
before opening `solution.sql`. If downloaded, unzip, enter `department-headcount/`
and use `python verify.py` / `python verify.py --solution --extensions` instead.
You can test a separate file with `python verify.py --query your-query.sql`.
Do not change the checks to accommodate a wrong answer.

Transfer: report **every** department and its active employee count, including
departments with zero employees or only inactive employees. Predict the output
after disabling all employees in department 20. Compare with `transfer.sql` after
trying; `all-departments.sql` is the intermediate unfiltered count variant.

SQL text uses syntax documented for SQL Server. Executing it here verifies the
bounded relational examples in SQLite only: it does not verify SQL Server
execution plans, performance, collation, integer limits or concurrent updates.
For SQL Server, use a disposable empty database, execute `setup.sql` once and
run the SELECT files; no SQL Server execution is claimed by this lab.

[English lesson](../../lessons/2026-10-10-algorithms-department-headcount.md) ·
[Vietnamese lesson](../../vi/lessons/2026-10-10-algorithms-department-headcount.md)
