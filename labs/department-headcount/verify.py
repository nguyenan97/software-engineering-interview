"""Exercise a single SELECT in an isolated SQLite database; never connect remotely."""
import argparse
from pathlib import Path
import sqlite3
import unittest

ROOT = Path(__file__).resolve().parent


def suite(query):
    class HeadcountChecks(unittest.TestCase):
        def setUp(self):
            self.db = sqlite3.connect(":memory:")
            self.db.executescript((ROOT / "setup.sql").read_text())

        def tearDown(self):
            self.db.close()

        def rows(self):
            return self.db.execute(query).fetchall()

        def test_same_names_do_not_merge_departments(self):
            self.assertEqual(self.rows(), [(10, "Platform", 4)])

        def test_null_name_is_still_an_employee(self):
            self.db.execute("DELETE FROM Employee WHERE DepartmentId = 20")
            self.assertEqual(self.rows(), [(10, "Platform", 4)])

        def test_exactly_three_does_not_qualify(self):
            self.db.execute("DELETE FROM Employee WHERE EmployeeId = 104")
            self.assertEqual(self.rows(), [])

        def test_empty_department_does_not_qualify(self):
            self.db.execute("DELETE FROM Employee")
            self.assertEqual(self.rows(), [])

        def test_empty_database_returns_no_departments(self):
            self.db.execute("DELETE FROM Employee")
            self.db.execute("DELETE FROM Department")
            self.assertEqual(self.rows(), [])

        def test_another_department_can_cross_threshold(self):
            self.db.execute("INSERT INTO Employee VALUES (204, 20, 'G', 1)")
            self.assertEqual(self.rows(), [(10, "Platform", 4), (20, "Platform", 4)])

    return unittest.defaultTestLoader.loadTestsFromTestCase(HeadcountChecks)


def verify_extensions():
    with sqlite3.connect(":memory:") as db:
        db.executescript((ROOT / "setup.sql").read_text())
        all_rows = db.execute((ROOT / "all-departments.sql").read_text()).fetchall()
        assert all_rows == [(10, "Platform", 4), (20, "Platform", 3), (30, "Support", 0)], all_rows
        active_rows = db.execute((ROOT / "transfer.sql").read_text()).fetchall()
        assert active_rows == [(10, "Platform", 3), (20, "Platform", 3), (30, "Support", 0)], active_rows
        # Changed input: a department with employees but no qualifying employees.
        db.execute("UPDATE Employee SET IsActive = 0 WHERE DepartmentId = 20")
        active_rows = db.execute((ROOT / "transfer.sql").read_text()).fetchall()
        assert active_rows == [(10, "Platform", 3), (20, "Platform", 0), (30, "Support", 0)], active_rows
        print("Extension checks: all counts 4/3/0; active counts 3/3/0; changed active counts 3/0/0.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solution", action="store_true")
    parser.add_argument("--query", type=Path, help="Your single SELECT file; overrides the default")
    parser.add_argument("--extensions", action="store_true", help="Check the two reference variants")
    args = parser.parse_args()
    path = args.query or ROOT / ("solution.sql" if args.solution else "exercise.sql")
    print(f"Runtime: SQLite {sqlite3.sqlite_version}; query: {path.name}", flush=True)
    result = unittest.TextTestRunner(verbosity=2).run(suite(path.read_text()))
    if args.extensions:
        verify_extensions()
    raise SystemExit(0 if result.wasSuccessful() else 1)
