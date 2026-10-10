"""End-to-end report generation and integrity tests."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReportTests(unittest.TestCase):
    def test_report_from_completed_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / 'config.json'
            output = root / 'run'
            config.write_text(json.dumps({'question': 'Does this change MC ownership?', 'trials': 2,
                'waves': 3, 'checkpoints': [1, 3], 'scenarios': [{'name': 'base'}, {'name': 'variant', 'config': {'red': True}}],
                'comparisons': [{'scenario': 'variant', 'reference': 'base'}], 'metrics': ['mc_owned', 'build_rate'],
                'derived_metrics': {'build_rate': 'mc_built / mc_owned'}}))
            runner = subprocess.run([sys.executable, str(ROOT / 'tools/run_mc_experiment.py'), '--config', str(config), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(runner.returncode, 0, runner.stderr)
            command = [sys.executable, str(ROOT / 'tools/mc_standard_report.py'), '--output', str(output)]
            report = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(report.returncode, 0, report.stderr)
            content = (output / 'report.md').read_text()
            for token in ('Does this change MC ownership?', 'Resolved scenario matrix', 'Wave 3', 'build_rate', 'Softlocks and censoring', 'Provenance'):
                self.assertIn(token, content)
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            (output / 'results.json').write_text('{}')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)

if __name__ == '__main__':
    unittest.main()
