#!/usr/bin/env python3
"""Configuration-driven MC experiments. JSON configuration; no report overwrites."""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'model'))
from mc_wave60 import WaveConfig, simulate_run
from mc_packages import BLUEPRINT_NAMES, SUPPORTS, PACKAGES
from mc_experiment_spec import resolve_spec
from mc_metric_registry import METRICS, METRIC_REGISTRY, compile_metrics, aggregate, paired_aggregate, unpaired_aggregate
from mc_run_lifecycle import initialize, update

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--dry-run', action='store_true', help='validate and print resolved experiment without simulation')
    args = parser.parse_args()
    spec = json.loads(args.config.read_text())
    resolved = resolve_spec(spec)
    selected_metrics, derived_metrics = compile_metrics(spec)
    if args.dry_run:
        print(json.dumps(resolved, indent=2))
        return
    if args.output is None:
        parser.error('--output is required unless --dry-run is specified')
    manifest = initialize(args.output, resolved, ROOT)
    try:
        execute_experiment(spec, resolved, selected_metrics, derived_metrics, args.output, manifest)
    except BaseException as exc:
        update(args.output, manifest, status='failed', error=exc)
        raise

def execute_experiment(spec, resolved, selected_metrics, derived_metrics, output, manifest):
    trials = resolved['trials']
    waves = resolved['waves']
    checkpoints = resolved['checkpoints']
    seed_start = resolved['seed_start']
    cases = resolved['scenarios']
    common = spec.get('defaults', {})
    raw_path = output / 'raw.csv'
    rows = {}
    softlocks = {}
    completed_runs = 0
    with raw_path.open('x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('scenario', 'seed', 'wave', 'censored') + METRICS)
        for case in cases:
            name = case['name']
            config = WaveConfig(**{**common, **case.get('config', {})})
            softlocks[name] = {}
            for seed in range(seed_start, seed_start + trials):
                state, history = simulate_run(None, None, waves=waves, seed=seed, config=config)
                if state.softlock_wave is not None:
                    softlocks[name][str(seed)] = state.softlock_wave
                for wave in checkpoints:
                    if len(history) < wave:
                        continue
                    h = history[wave-1]
                    o = h['mc_draft_outcomes']
                    acquired = h['blueprint_acquisitions']
                    package = config.package or 'salamander'
                    offense = sum(q for code,q in acquired.items() if BLUEPRINT_NAMES.get(code, code) in PACKAGES[package])
                    support = sum(q for code,q in acquired.items() if BLUEPRINT_NAMES.get(code, code) in SUPPORTS)
                    names = PACKAGES[package]
                    counts = [sum(q for code,q in acquired.items() if BLUEPRINT_NAMES.get(code, code) == target) for target in names]
                    first = counts[0]
                    second = counts[1] if len(counts) > 1 else 0
                    complete = min(counts)
                    has_all = int(all(counts))
                    only_one = int(len(counts) == 2 and sum(c > 0 for c in counts) == 1)
                    vals = (h['mc_owned'], h['mc_built'], h['mc_in_hand'],
                            o.get('hv_offense', 0), o.get('hv_support', 0),
                            o.get('hv_other', 0), sum(o.get('hv_'+k, 0) for k in ('offense','support','other')),
                            h['drafts_resolved'], offense, support, offense + support, first, second, complete, has_all, only_one)
                    writer.writerow((name, seed, wave, int(state.censored)) + vals)
                    rows[(name, seed, wave)] = vals
                completed_runs += 1
                f.flush()
                update(output, manifest, completed_runs=completed_runs)
            print('Completed', name, flush=True)
    summary = {}
    for case in cases:
        name = case['name']
        summary[name] = {}
        for wave in checkpoints:
            observed = [rows[(name, seed, wave)] for seed in range(seed_start, seed_start + trials)
                        if (name, seed, wave) in rows]
            summary[name][str(wave)] = {'observed': len(observed),
                'metrics': aggregate(observed, selected_metrics, derived_metrics) if observed else {}}
    paired = {}
    for comparison in resolved['comparisons']:
        a, b = comparison['scenario'], comparison['reference']
        if a not in summary or b not in summary:
            raise ValueError('comparison references unknown scenario')
        mode = comparison.get('mode', 'paired')
        key = a + ' - ' + b
        paired[key] = {}
        for wave in checkpoints:
            matches = [(rows[(a, seed, wave)], rows[(b, seed, wave)])
                       for seed in range(seed_start, seed_start+trials)
                       if (a, seed, wave) in rows and (b, seed, wave) in rows]
            first_rows = [rows[(a, seed, wave)] for seed in range(seed_start, seed_start+trials) if (a, seed, wave) in rows]
            reference_rows = [rows[(b, seed, wave)] for seed in range(seed_start, seed_start+trials) if (b, seed, wave) in rows]
            comparison_result = {'paired_seeds': len(matches) if mode == 'paired' else 0,
                'metrics': (paired_aggregate(matches, selected_metrics, derived_metrics) if matches else {}) if mode == 'paired' else unpaired_aggregate(first_rows, reference_rows, selected_metrics, derived_metrics)}
            if mode != 'paired':
                comparison_result.update({'mode': mode, 'first_observed': len(first_rows), 'reference_observed': len(reference_rows)})
            paired[key][str(wave)] = comparison_result
    package_labels = {case['name']: list(PACKAGES[case.get('config', {}).get('package') or common.get('package') or 'salamander']) for case in cases}
    payload = {'package_building_labels': package_labels, 'configuration': spec, 'resolved_configuration': resolved, 'summary': summary, 'paired': paired,
               'metric_registry': {metric: METRIC_REGISTRY.get(metric, {'id': metric, 'unit': 'derived', 'provenance': spec.get('derived_metrics', {}).get(metric), 'aggregation': 'sample distribution', 'censoring': 'observed checkpoints only'}) for metric in selected_metrics},
               'softlocks': softlocks,
               'softlock_rates': {name: len(events)/trials for name, events in softlocks.items()},
               'note': 'Conditional simulation, not calibrated game odds; paired seeds may diverge in RNG consumption.'}
    with (output / 'results.json').open('x') as result_file:
        json.dump(payload, result_file, indent=2)
    update(output, manifest, status='completed', completed_runs=len(cases)*trials)
    print('FINISHED', len(cases)*trials, 'runs; results:', output, flush=True)

if __name__ == '__main__':
    main()
