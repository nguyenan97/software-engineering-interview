"""Run from repo root: python labs/atomic-inbox/verify.py [--solution]."""
import argparse
import sqlite3
import unittest


def connection():
    # Explicit SQL controls transactions; avoid version-dependent implicit ones.
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.executescript("""
        CREATE TABLE accounts (account_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL);
        CREATE TABLE inbox (event_id TEXT PRIMARY KEY, account_id INTEGER NOT NULL, amount INTEGER NOT NULL);
        INSERT INTO accounts VALUES (42, 0);
    """)
    return db


def suite(apply_credit):
    class AtomicInboxChecks(unittest.TestCase):
        def setUp(self):
            self.db = connection()

        def tearDown(self):
            self.db.close()

        def balance(self):
            return self.db.execute("SELECT balance FROM accounts WHERE account_id=42").fetchone()[0]

        def marker_count(self):
            return self.db.execute("SELECT COUNT(*) FROM inbox").fetchone()[0]

        def test_happy_path_and_repeat_after_commit(self):
            self.assertEqual(apply_credit(self.db, "event-1", 42, 100), "Applied")
            self.assertEqual(apply_credit(self.db, "event-1", 42, 100), "AlreadyProcessed")
            self.assertEqual((self.balance(), self.marker_count()), (100, 1))

        def test_failure_rolls_back_marker_and_retry_applies(self):
            with self.assertRaises(RuntimeError):
                apply_credit(self.db, "event-1", 42, 100, fail_after_marker=True)
            self.assertEqual((self.balance(), self.marker_count()), (0, 0))
            self.assertEqual(apply_credit(self.db, "event-1", 42, 100), "Applied")
            self.assertEqual((self.balance(), self.marker_count()), (100, 1))

        def test_missing_account_does_not_keep_marker(self):
            with self.assertRaises(ValueError):
                apply_credit(self.db, "event-2", 999, 100)
            self.assertEqual(self.marker_count(), 0)

        def test_conflicting_identity_preserves_existing_effect(self):
            apply_credit(self.db, "event-1", 42, 100)
            with self.assertRaises(ValueError):
                apply_credit(self.db, "event-1", 42, 250)
            self.assertEqual((self.balance(), self.marker_count()), (100, 1))

        def test_invalid_amount_writes_nothing(self):
            for amount in (0, -1, True, 1.5):
                with self.assertRaises(ValueError):
                    apply_credit(self.db, "invalid", 42, amount)
            self.assertEqual((self.balance(), self.marker_count()), (0, 0))

    return unittest.defaultTestLoader.loadTestsFromTestCase(AtomicInboxChecks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()
    if args.solution:
        from solution import apply_credit
    else:
        from exercise import apply_credit
    result = unittest.TextTestRunner(verbosity=2).run(suite(apply_credit))
    raise SystemExit(0 if result.wasSuccessful() else 1)
