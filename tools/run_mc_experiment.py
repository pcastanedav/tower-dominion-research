#!/usr/bin/env python3
"""Configuration-driven MC experiments. JSON configuration; no report overwrites."""
import argparse
import csv
import json
import math
import sys
from dataclasses import fields
from pathlib import Path
from statistics import mean, stdev, median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'model'))
from mc_wave60 import WaveConfig, simulate_run
from mc_packages import BLUEPRINT_NAMES, SUPPORTS, PACKAGES

METRICS = ('mc_owned', 'mc_built', 'mc_in_hand', 'hv_offense', 'hv_support', 'hv_other', 'hv_total', 'drafts_resolved', 'all_hv_offense', 'all_hv_support', 'all_hv_total', 'offense_building_1', 'offense_building_2', 'complete_sets', 'has_all_required', 'has_only_one_required')
CONFIG_FIELDS = {field.name for field in fields(WaveConfig)}

def summarize(values):
    values = sorted(values)
    n = len(values)
    sd = stdev(values) if n > 1 else 0.0
    return {'mean': mean(values), 'sd': sd, 'median': median(values),
            'p10': values[int(.1*(n-1))], 'p90': values[int(.9*(n-1))],
            'ci95_halfwidth': 1.96*sd/math.sqrt(n)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.config.read_text())
    trials = spec['trials']
    waves = spec['waves']
    checkpoints = spec['checkpoints']
    seed_start = spec.get('seed_start', 1)
    if not isinstance(trials, int) or trials < 1 or not isinstance(waves, int) or waves < 1:
        raise ValueError('trials and waves must be positive integers')
    if not checkpoints or any(not isinstance(w, int) or not 1 <= w <= waves for w in checkpoints):
        raise ValueError('checkpoints must be within simulation horizon')
    if not isinstance(seed_start, int):
        raise ValueError('seed_start must be an integer')
    common = spec.get('defaults', {})
    cases = spec['scenarios']
    if not cases or len({s['name'] for s in cases}) != len(cases):
        raise ValueError('scenarios must be nonempty with unique names')
    for scenario in cases:
        unknown = set(common) | set(scenario.get('config', {}))
        unknown -= CONFIG_FIELDS
        if unknown:
            raise ValueError('unknown WaveConfig options: ' + ', '.join(sorted(unknown)))
    args.output.mkdir(parents=True, exist_ok=True)
    raw_path = args.output / 'raw.csv'
    rows = {}
    softlocks = {}
    with raw_path.open('w', newline='') as f:
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
            f.flush()
            print('Completed', name, flush=True)
    summary = {}
    for case in cases:
        name = case['name']
        summary[name] = {}
        for wave in checkpoints:
            observed = [rows[(name, seed, wave)] for seed in range(seed_start, seed_start + trials)
                        if (name, seed, wave) in rows]
            summary[name][str(wave)] = {'observed': len(observed),
                'metrics': {metric: summarize([r[i] for r in observed]) for i, metric in enumerate(METRICS)} if observed else {}}
    paired = {}
    for comparison in spec.get('comparisons', []):
        a, b = comparison['scenario'], comparison['reference']
        if a not in summary or b not in summary:
            raise ValueError('comparison references unknown scenario')
        key = a + ' - ' + b
        paired[key] = {}
        for wave in checkpoints:
            matches = [(rows[(a, seed, wave)], rows[(b, seed, wave)])
                       for seed in range(seed_start, seed_start+trials)
                       if (a, seed, wave) in rows and (b, seed, wave) in rows]
            paired[key][str(wave)] = {'paired_seeds': len(matches),
                'metrics': {metric: summarize([x[i]-y[i] for x,y in matches])
                            for i,metric in enumerate(METRICS)} if matches else {}}
    package_labels = {case['name']: list(PACKAGES[case.get('config', {}).get('package') or common.get('package') or 'salamander']) for case in cases}
    payload = {'package_building_labels': package_labels, 'configuration': spec, 'summary': summary, 'paired': paired,
               'softlocks': softlocks,
               'softlock_rates': {name: len(events)/trials for name, events in softlocks.items()},
               'note': 'Conditional simulation, not calibrated game odds; paired seeds may diverge in RNG consumption.'}
    (args.output / 'results.json').write_text(json.dumps(payload, indent=2))
    print('FINISHED', len(cases)*trials, 'runs; results:', args.output, flush=True)

if __name__ == '__main__':
    main()
