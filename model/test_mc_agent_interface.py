"""Agent contract end-to-end without simulator implementation knowledge."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
INTERFACE = ROOT / 'tools/mc_agent_interface.py'

class AgentInterfaceTests(unittest.TestCase):
    def call(self, *args):
        result = subprocess.run([sys.executable, str(INTERFACE), *map(str, args)], capture_output=True, text=True)
        return result, json.loads(result.stdout)

    def test_discover_preview_run_report(self):
        result, capabilities = self.call('capabilities')
        self.assertEqual(result.returncode, 0)
        self.assertIn('mc_build_target', capabilities['data']['config_fields'])
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            spec = directory / 'experiment.json'
            output = directory / 'results'
            spec.write_text(json.dumps({'trials': 2, 'waves': 3, 'checkpoints': [1, 3],
                'scenarios': [{'name': 'reference'}], 'sweeps': [{'name': 'change', 'mode': 'one_factor',
                'parameters': {'red': [True]}, 'reference': 'reference'}],
                'metrics': ['mc_owned']}))
            for operation in ('validate', 'preview'):
                result, response = self.call(operation, '--config', spec)
                self.assertEqual(result.returncode, 0, response)
                self.assertEqual(response['data']['total_runs'], 4)
            result, response = self.call('run', '--config', spec, '--output', output)
            self.assertEqual(result.returncode, 0, response)
            self.assertEqual(response['data']['manifest']['status'], 'completed')
            result, response = self.call('report', '--output', output, '--format', 'both')
            self.assertEqual(result.returncode, 0, response)
            self.assertEqual(len(response['data']['artifacts']), 3)
            result, response = self.call('run', '--config', spec, '--output', output)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(response['ok'])

    def test_invalid_spec_json_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            path.write_text('{"trials": 0}')
            result, response = self.call('preview', '--config', path)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(response['ok'])
            self.assertIn('positive integers', response['error']['message'])

if __name__ == '__main__':
    unittest.main()
