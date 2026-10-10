"""Compatibility and preflight checks for declarative experiment specifications."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from mc_experiment_spec import resolve_spec
from mc_wave60 import WaveConfig

DOCS = ROOT / 'docs/tasks/mission-control-chain'
RUNNER = ROOT / 'tools/run_mc_experiment.py'


class ExperimentSpecTests(unittest.TestCase):
    def setUp(self):
        self.spec = {'trials': 2, 'waves': 4, 'checkpoints': [2, 4],
                     'defaults': {'faction': 'Lions'},
                     'scenarios': [{'name': 'baseline'}, {'name': 'variant', 'config': {'red': True}}],
                     'comparisons': [{'scenario': 'variant', 'reference': 'baseline'}]}

    def invalid(self, mutate, expected):
        spec = copy.deepcopy(self.spec)
        mutate(spec)
        with self.assertRaisesRegex(ValueError, expected):
            resolve_spec(spec)

    def test_legacy_configs_resolve_to_waveconfig(self):
        for filename in ('experiment-a-policy-ablation.json', 'experiment-a8-attenuation.json',
                         'chain-establishment-experiment.json', 'faction-establishment-experiment.json',
                         'package-establishment-experiment.json'):
            with self.subTest(filename=filename):
                spec = json.loads((DOCS / filename).read_text())
                result = resolve_spec(spec)
                self.assertEqual(result['total_runs'], spec['trials'] * len(spec['scenarios']))
                self.assertEqual(result['checkpoints'], spec['checkpoints'])
                for old, new in zip(spec['scenarios'], result['scenarios']):
                    expected = asdict(WaveConfig(**{**spec.get('defaults', {}), **old.get('config', {})}))
                    self.assertEqual(new['config'], expected)
                    self.assertEqual(new['name'], old['name'])

    def test_reject_bad_structure_and_references(self):
        self.invalid(lambda s: s.update(trials=True), 'trials and waves')
        self.invalid(lambda s: s.update(checkpoints=[2, 2]), 'unique')
        self.invalid(lambda s: s.update(checkpoints=[5]), 'horizon')
        self.invalid(lambda s: s.update(seed_start=False), 'seed_start')
        self.invalid(lambda s: s['scenarios'].append({'name': 'baseline'}), 'duplicate')
        self.invalid(lambda s: s['scenarios'][0].update(config={'typo': 1}), 'unknown WaveConfig')
        self.invalid(lambda s: s['scenarios'][0].update(config={'faction': 'invalid'}), 'invalid faction')
        self.invalid(lambda s: s['comparisons'][0].update(reference='missing'), 'unknown scenario')
        self.invalid(lambda s: s.update(schema_version=2), 'schema_version')

    def test_reject_invalid_model_constraints(self):
        self.invalid(lambda s: s['scenarios'][0].update(config={'tier3_wave': 0}), 'tier3_wave')
        self.invalid(lambda s: s['scenarios'][0].update(config={'eleanor': True, 'eleanor_cadence': 0}), 'cadence')
        self.invalid(lambda s: s['scenarios'][0].update(config={'mc_reserve_target': 3}), 'reserve requires')
        self.invalid(lambda s: s['scenarios'][0].update(config={'package': 'sphd_fortress', 'faction': 'Iron'}), 'Fortress')

    def test_sweep_grid_and_one_factor(self):
        spec = copy.deepcopy(self.spec)
        spec['sweeps'] = [
            {'name': 'grid', 'mode': 'grid', 'base': {'mc_build_target': 40},
             'parameters': {'mc_build_target': [10, 20], 'red': [False, True]}, 'include_base': True},
            {'name': 'ablate', 'mode': 'one_factor', 'base': {'red': True},
             'parameters': {'red': [False], 'attenuation_enabled': [True]}, 'reference': 'baseline'}]
        resolved = resolve_spec(spec)
        self.assertEqual(len(resolved['scenarios']), 9)
        self.assertEqual(len(resolved['comparisons']), 7)
        self.assertEqual(resolved['total_runs'], 18)
        self.assertEqual(resolved['scenarios'][3]['config']['mc_build_target'], 10)
        self.assertEqual(resolved['scenarios'][3]['config']['red'], False)

    def test_sweep_errors_and_limits(self):
        self.invalid(lambda s: s.update(sweeps=[{'name': 'x', 'mode': 'grid', 'parameters': {'red': []}}]), 'nonempty values')
        self.invalid(lambda s: s.update(sweeps=[{'name': 'x', 'mode': 'bad', 'parameters': {'red': [True]}}]), 'mode')
        self.invalid(lambda s: s.update(sweeps=[{'name': 'x', 'mode': 'grid', 'parameters': {'red': [True]}, 'reference': 'missing'}]), 'unknown scenario')
        self.invalid(lambda s: s.update(sweeps=[{'name': 'x', 'mode': 'grid', 'parameters': {'mc_build_target': list(range(300))}}]), 'safety limit')

    def test_experiment_a_reproducible_as_declarative_ablation(self):
        original = json.loads((DOCS / 'experiment-a-policy-ablation.json').read_text())
        baseline = original['scenarios'][0]['config']
        spec = {k: original[k] for k in ('trials', 'seed_start', 'waves', 'checkpoints', 'defaults')}
        spec['scenarios'] = [original['scenarios'][0], original['scenarios'][6]]
        spec['sweeps'] = [{'name': 'ablation', 'mode': 'one_factor', 'base': baseline,
                           'reference': 'A0 Reference', 'parameters': {
                               'attenuation_enabled': [False], 'mc_reserve_target': [0],
                               'mc_construction_policy': ['threshold'], 'mc_dynamic_selectivity': [False],
                               'amplifier_effect_enabled': [False]}}]
        resolved = resolve_spec(spec)
        actual = [row['config'] for row in resolved['scenarios']]
        expected = [asdict(WaveConfig(**{**original.get('defaults', {}), **row['config']})) for row in original['scenarios']]
        self.assertEqual(len(actual), 7)
        self.assertEqual(set(json.dumps(x, sort_keys=True) for x in actual), set(json.dumps(x, sort_keys=True) for x in expected))
        self.assertEqual(len(resolved['comparisons']), 5)

    def test_sweep_runner_execution_and_comparisons(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            config = temp / 'sweep.json'
            output = temp / 'results'
            spec = {'trials': 2, 'waves': 3, 'checkpoints': [1, 3],
                    'scenarios': [{'name': 'reference'}],
                    'sweeps': [{'name': 'policy', 'mode': 'one_factor',
                                'parameters': {'red': [True], 'attenuation_enabled': [True]},
                                'reference': 'reference'}]}
            config.write_text(json.dumps(spec))
            run = subprocess.run([sys.executable, str(RUNNER), '--config', str(config),
                                  '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads((output / 'results.json').read_text())
            self.assertEqual(len(result['summary']), 3)
            self.assertEqual(len(result['paired']), 2)
            self.assertEqual(result['resolved_configuration']['total_runs'], 6)
            self.assertEqual(result['summary']['reference']['3']['observed'], 2)
            self.assertEqual(len((output / 'raw.csv').read_text().splitlines()), 13)

    def test_dry_run_and_invalid_preflight_do_not_write_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            config = temp / 'spec.json'
            output = temp / 'results'
            config.write_text(json.dumps(self.spec))
            run = subprocess.run([sys.executable, str(RUNNER), '--config', str(config), '--dry-run', '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['total_runs'], 4)
            self.assertFalse(output.exists())
            bad = copy.deepcopy(self.spec)
            bad['scenarios'][0]['config'] = {'typo': 1}
            config.write_text(json.dumps(bad))
            run = subprocess.run([sys.executable, str(RUNNER), '--config', str(config), '--output', str(output)], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
