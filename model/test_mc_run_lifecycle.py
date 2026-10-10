"""Run lifecycle status, output integrity and no-overwrite regression tests."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from mc_run_lifecycle import initialize, update, verify_completed

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root / 'output'
        self.resolved = {'schema_version': 1, 'seed_start': 5, 'trials': 2, 'total_runs': 4}

    def test_no_overwrite_and_incomplete_rejected(self):
        manifest = initialize(self.out, self.resolved, self.root)
        self.assertEqual(manifest['status'], 'running')
        with self.assertRaises(ValueError):
            verify_completed(self.out)
        with self.assertRaises(FileExistsError):
            initialize(self.out, self.resolved, self.root)

    def test_success_checksums_and_tamper(self):
        manifest = initialize(self.out, self.resolved, self.root)
        (self.out / 'raw.csv').write_text('scenario,seed\na,5\n')
        (self.out / 'results.json').write_text('{}')
        update(self.out, manifest, status='completed', completed_runs=4)
        self.assertEqual(verify_completed(self.out)['completed_runs'], 4)
        (self.out / 'raw.csv').write_text('altered')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            verify_completed(self.out)

    def test_failure_status(self):
        manifest = initialize(self.out, self.resolved, self.root)
        update(self.out, manifest, status='failed', error=RuntimeError('injected failure'))
        stored = json.loads((self.out / 'run_manifest.json').read_text())
        self.assertEqual(stored['status'], 'failed')
        self.assertIn('injected failure', stored['error'])
        with self.assertRaises(ValueError):
            verify_completed(self.out)

if __name__ == '__main__':
    unittest.main()
