"""PDF/chart source consistency and completed-run safety."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class PDFReportTests(unittest.TestCase):
    def test_pdf_charts_match_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            config, output = path / 'spec.json', path / 'run'
            config.write_text(json.dumps({'trials': 2, 'waves': 3, 'checkpoints': [1, 3],
                'scenarios': [{'name': 'baseline'}, {'name': 'variant', 'config': {'red': True}}],
                'metrics': ['mc_owned', 'mc_built']}))
            commands = [
                ['tools/run_mc_experiment.py', '--config', str(config), '--output', str(output)],
                ['tools/mc_report_pdf.py', '--output', str(output)]]
            for cmd in commands:
                result = subprocess.run([sys.executable, str(ROOT / cmd[0]), *cmd[1:]], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / 'report.pdf').read_bytes().startswith(b'%PDF'))
            data = json.loads((output / 'results.json').read_text())
            charts = json.loads((output / 'charts.json').read_text())['charts']
            self.assertEqual(len(charts), 4)
            for chart in charts:
                for item in chart['values']:
                    expected = data['summary'][item['scenario']][str(chart['wave'])]
                    self.assertEqual(item['observed'], expected['observed'])
                    self.assertEqual(item['mean'], expected['metrics'][chart['metric']]['mean'])
            cmd = [sys.executable, str(ROOT / 'tools/mc_report_pdf.py'), '--output', str(output)]
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)

if __name__ == '__main__':
    unittest.main()
