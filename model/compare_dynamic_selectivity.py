"""Paired-seed wave-latched versus dynamic MC reserve selectivity experiment."""
from statistics import mean
from mc_wave60 import WaveConfig, simulate_run

SEEDS = range(200, 400)  # Independent of earlier 0..99 exploratory sweeps.
for target in (14, 17, 18, 20):
    for construction in ('continuous', 'threshold', 'preserve'):
        for dynamic in (False, True):
            rows = []
            for seed in SEEDS:
                _, history = simulate_run(None, None, waves=83, seed=seed,
                    config=WaveConfig(faction='Lions', red=True, package='salamander',
                        attenuation_enabled=True, mc_build_target=target,
                        mc_reserve_target=3, mc_batch_size=2,
                        mc_construction_policy=construction,
                        mc_dynamic_selectivity=dynamic))
                snapshots = []
                for wave in (63, 83):
                    h = next((x for x in history if x['wave'] == wave), history[-1])
                    outcomes = h['mc_draft_outcomes']
                    offense = outcomes.get('hv_offense', 0)
                    support = outcomes.get('hv_support', 0)
                    other = outcomes.get('hv_other', 0)
                    snapshots.append((h['mc_built'], h['mc_in_hand'], offense, support,
                                      other, offense + support + other,
                                      h['drafts_resolved']))
                rows.append(snapshots)
            for i, wave in enumerate((63, 83)):
                means = [round(mean(row[i][j] for row in rows), 3) for j in range(7)]
                print('target', target, 'policy', construction, 'dynamic', dynamic,
                      'wave', wave, 'built reserve offense support other total drafts',
                      *means, flush=True)
