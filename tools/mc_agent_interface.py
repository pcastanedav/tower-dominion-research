#!/usr/bin/env python3
"""Machine-readable agent contract for Mission Control experiments (v1)."""
import argparse
import json
import subprocess
import sys
from dataclasses import fields
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'model'))
from mc_wave60 import WaveConfig
from mc_experiment_spec import resolve_spec, CHOICES, MAX_SCENARIOS
from mc_metric_registry import METRIC_REGISTRY, METRICS, compile_metrics
from mc_run_lifecycle import verify_completed

CONTRACT_VERSION = 1


def capabilities():
    return {'contract_version': CONTRACT_VERSION, 'spec_schema_version': 1,
            'operations': ['capabilities', 'validate', 'preview', 'run', 'report'],
            'required_spec_fields': ['trials', 'waves', 'checkpoints'],
            'scenario_shape': {'name': 'string', 'config': 'WaveConfig overrides'},
            'sweep_modes': ['grid', 'one_factor'], 'max_scenarios': MAX_SCENARIOS,
            'comparison_modes': ['paired', 'unpaired'],
            'config_fields': {f.name: {'default': f.default if isinstance(f.default, (str, int, float, bool, type(None))) else str(f.default),
                                       **({'choices': sorted(CHOICES[f.name], key=str)} if f.name in CHOICES else {})} for f in fields(WaveConfig)},
            'metrics': METRIC_REGISTRY,
            'derived_metric_operators': ['+', '-', '*', '/', 'unary +', 'unary -'],
            'outputs': ['run_manifest.json', 'raw.csv', 'results.json', 'report.md', 'report.pdf', 'charts.json'],
            'limitations': ['conditional, uncalibrated probabilities', 'no combat survival or complete economy',
                            'no placement simulation', 'paired seeds can diverge in RNG consumption',
                            'Doctrine exhaustion may cause genuine softlocks']}


def checked_spec(path):
    spec = json.loads(Path(path).read_text())
    resolved = resolve_spec(spec)
    metrics, derived = compile_metrics(spec)
    return spec, resolved, metrics, derived


def invoke(script, args):
    completed = subprocess.run([sys.executable, str(ROOT / 'tools' / script), *args],
                               capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError('%s failed: %s' % (script, completed.stderr.strip() or completed.stdout.strip()))


def execute(args):
    if args.operation == 'capabilities':
        return capabilities()
    if args.operation in ('validate', 'preview', 'run'):
        spec, resolved, metrics, derived = checked_spec(args.config)
        result = {'contract_version': CONTRACT_VERSION, 'valid': True,
                  'selected_metrics': metrics, 'derived_metrics': list(derived),
                  'total_runs': resolved['total_runs'], 'scenario_count': len(resolved['scenarios'])}
        if args.operation == 'preview':
            result['resolved_configuration'] = resolved
        if args.operation == 'run':
            invoke('run_mc_experiment.py', ['--config', str(args.config), '--output', str(args.output)])
            result['manifest'] = verify_completed(args.output)
            result['output_directory'] = str(args.output)
        return result
    if args.operation == 'report':
        manifest = verify_completed(args.output)
        if args.format in ('markdown', 'both'):
            invoke('mc_standard_report.py', ['--output', str(args.output)])
        if args.format in ('pdf', 'both'):
            invoke('mc_report_pdf.py', ['--output', str(args.output)])
        return {'contract_version': CONTRACT_VERSION, 'status': 'completed',
                'source_checksums': manifest['checksums'],
                'artifacts': [str(args.output / name) for name in ('report.md', 'report.pdf', 'charts.json') if (args.output / name).exists()]}
    raise ValueError('unknown operation')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['capabilities', 'validate', 'preview', 'run', 'report'])
    parser.add_argument('--config', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--format', choices=['markdown', 'pdf', 'both'], default='both')
    args = parser.parse_args()
    try:
        if args.operation in ('validate', 'preview', 'run') and args.config is None:
            raise ValueError('--config required')
        if args.operation in ('run', 'report') and args.output is None:
            raise ValueError('--output required')
        print(json.dumps({'ok': True, 'data': execute(args)}, default=str))
    except (ValueError, OSError, RuntimeError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({'ok': False, 'error': {'type': type(error).__name__, 'message': str(error)}}))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
