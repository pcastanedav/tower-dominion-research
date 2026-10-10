"""Stage A: 10..40 MC establishment targets, 300 paired seeds, Waves 63/83."""
import csv
import math
from pathlib import Path
from statistics import mean, stdev
from mc_wave60 import WaveConfig, simulate_run

OUT = Path('docs/tasks/mission-control-chain/stage-a-results')
OUT.mkdir(parents=True, exist_ok=True)
SEEDS = range(400, 700)
TARGETS = range(10, 41)
WAVES = (63, 83)
METRICS = ('mc_built', 'mc_in_hand', 'hv_offense', 'hv_support', 'hv_other', 'hv_total', 'drafts')
records = {}
with (OUT / 'raw.csv').open('w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(('target', 'seed', 'wave') + METRICS)
    for target in TARGETS:
        for seed in SEEDS:
            _, history = simulate_run(None, None, waves=83, seed=seed,
                config=WaveConfig(faction='Lions', red=True, package='salamander',
                    attenuation_enabled=True, mc_build_target=target,
                    mc_reserve_target=3, mc_batch_size=2,
                    mc_construction_policy='continuous', mc_dynamic_selectivity=True))
            for wave in WAVES:
                h = next(x for x in history if x['wave'] == wave)
                o = h['mc_draft_outcomes']
                values = (h['mc_built'], h['mc_in_hand'], o.get('hv_offense', 0),
                          o.get('hv_support', 0), o.get('hv_other', 0),
                          sum(o.get('hv_' + k, 0) for k in ('offense', 'support', 'other')),
                          h['drafts_resolved'])
                records[(target, seed, wave)] = values
                writer.writerow((target, seed, wave) + values)
        file.flush()
        print('Completed target', target, flush=True)

def summary(vals):
    avg = mean(vals)
    sd = stdev(vals)
    ordered = sorted(vals)
    n = len(vals)
    return (round(avg, 4), round(sd, 4), round(ordered[int(.10 * (n-1))], 4),
            round(ordered[int(.50 * (n-1))], 4), round(ordered[int(.90 * (n-1))], 4),
            round(1.96 * sd / math.sqrt(n), 4))

with (OUT / 'summary.csv').open('w', newline='') as file:
    w = csv.writer(file)
    w.writerow(('target', 'wave', 'metric', 'mean', 'sd', 'p10', 'median', 'p90', 'ci95_halfwidth'))
    for target in TARGETS:
        for wave in WAVES:
            for i, metric in enumerate(METRICS):
                w.writerow((target, wave, metric) + summary([records[(target, seed, wave)][i] for seed in SEEDS]))

with (OUT / 'paired.csv').open('w', newline='') as file:
    w = csv.writer(file)
    w.writerow(('target', 'reference_target', 'wave', 'metric', 'mean_difference', 'sd_difference',
                'p10_difference', 'median_difference', 'p90_difference', 'ci95_halfwidth'))
    for target in TARGETS:
        for reference in sorted(set((20, target-1)) & set(TARGETS)):
            if target == reference:
                continue
            for wave in WAVES:
                for i, metric in enumerate(METRICS):
                    deltas = [records[(target, seed, wave)][i] - records[(reference, seed, wave)][i]
                              for seed in SEEDS]
                    w.writerow((target, reference, wave, metric) + summary(deltas))
print('FINISHED', len(TARGETS) * len(SEEDS), 'runs', flush=True)
