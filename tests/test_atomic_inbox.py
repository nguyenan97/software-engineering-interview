"""Check the teaching failure, reference repair, and downloadable lab together."""
import importlib.util
import io
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'labs/atomic-inbox'


def module(name):
    spec = importlib.util.spec_from_file_location('lab_' + name, LAB / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class RunnableLabTests(unittest.TestCase):
    def check_implementation(self, name):
        suite = module('verify').suite(module(name).apply_credit)
        return unittest.TextTestRunner(stream=io.StringIO()).run(suite)

    def test_starter_fails_only_the_two_transaction_boundary_checks(self):
        result = self.check_implementation('exercise')
        self.assertEqual(result.testsRun, 5)
        self.assertEqual(result.errors, [])
        names = {test._testMethodName for test, _ in result.failures}
        self.assertEqual(names, {'test_failure_rolls_back_marker_and_retry_applies', 'test_missing_account_does_not_keep_marker'})

    def test_reference_passes_same_happy_failure_and_contract_checks(self):
        result = self.check_implementation('solution')
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(result.testsRun, 5)

    def test_download_contains_the_checked_lab_not_stale_copies(self):
        with zipfile.ZipFile(ROOT / 'assets/labs/atomic-inbox.zip') as archive:
            self.assertEqual(set(archive.namelist()), {'atomic-inbox/' + name for name in ('exercise.py', 'solution.py', 'verify.py', 'README.md')})
            for name in ('exercise.py', 'solution.py', 'verify.py', 'README.md'):
                self.assertEqual(archive.read('atomic-inbox/' + name), (LAB / name).read_bytes())
