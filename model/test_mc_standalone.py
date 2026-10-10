"""Standalone CLI lifecycle and safe preset handling."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tools/mc_experiment.py'

class StandaloneTests(unittest.TestCase):
    def call(self, *args):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True)

    def test_preset_and_full_lifecycle(self):
        self.assertIn('quick-comparison', self.call('presets').stdout)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)
            config, output = path / 'experiment.json', path / 'run'
            result = self.call('init', 'quick-comparison', '--config', config)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotEqual(self.call('init', 'quick-comparison', '--config', config).returncode, 0)
            spec = json.loads(config.read_text())
            spec['trials'] = 2
            spec['waves'] = 3
            spec['checkpoints'] = [1, 3]
            config.write_text(json.dumps(spec))
            self.assertEqual(self.call('validate', '--config', config).returncode, 0)
            preview = self.call('preview', '--config', config)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertEqual(json.loads(preview.stdout)['total_runs'], 6)
            run = self.call('run', '--config', config, '--output', output)
            self.assertEqual(run.returncode, 0, run.stderr)
            for name in ('run_manifest.json', 'raw.csv', 'results.json', 'report.md', 'report.pdf', 'charts.json'):
                self.assertTrue((output / name).is_file(), name)
            self.assertNotEqual(self.call('run', '--config', config, '--output', output).returncode, 0)
            self.assertNotEqual(self.call('init', '../invalid', '--config', path / 'other.json').returncode, 0)

if __name__ == '__main__':
    unittest.main()
