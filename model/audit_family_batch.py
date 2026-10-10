from collections import Counter
from statistics import mean, median
from mc_wave60 import WaveConfig, simulate_run

config = WaveConfig(faction='Lions', red=True, package='salamander', attenuation_enabled=True)
counts = Counter()
rows = []
for seed in range(100):
    state, hist = simulate_run(None, None, waves=83, seed=seed, config=config)
    w39, w40, w41 = (hist[i - 1] for i in (39, 40, 41))
    counts['first_mc_before_40'] += state.first_mc_wave is not None and state.first_mc_wave < 40
    counts['no_mc_by_83'] += state.first_mc_wave is None
    counts['wave40_mc_3a'] += w40['mc_from_3a_this_wave']
    counts['wave40_drafts'] += w40['drafts_resolved'] - w39['drafts_resolved']
    counts['wave41_drafts'] += w41['drafts_resolved'] - w40['drafts_resolved']
    counts['total_mc'] += state.mc_owned
    rows.append((seed, state.mc_owned, state.first_mc_wave, state.first_amplifier_wave, w39['mc_owned'], w40['mc_owned'], w40['mc_from_3a_this_wave'], w40['drafts_resolved'] - w39['drafts_resolved'], hist[-1]['blueprint_acquisitions'].get('BPCB21', 0)))
print('AVERAGE_W40_DRAFTS', counts['wave40_drafts'] / 100)
print('AVERAGE_W40_MC_FROM_3A', counts['wave40_mc_3a'] / 100)
print('AVERAGE_W41_DRAFTS', counts['wave41_drafts'] / 100)
print('MC_BEFORE_W40', counts['first_mc_before_40'])
print('NO_MC', counts['no_mc_by_83'])
print('TOP_MC_RUNS', sorted(rows, key=lambda r: -r[1])[:8])
print('BOTTOM_MC_RUNS', sorted(rows, key=lambda r: r[1])[:8])
print('MC_COUNTS_P10_P50_P90', [sorted(r[1] for r in rows)[i] for i in (9, 49, 89)])
print('FIRST_MC_WAVES', Counter(r[2] for r in rows).most_common(12))
