"""Exploratory 100-seed family-pool and acquisition sanity report."""
from collections import Counter
from statistics import mean, median
from mc_wave60 import simulate_run, WaveConfig

N = 100
samples = []
for seed in range(N):
    state, history = simulate_run(None, None, waves=83, seed=seed,
        config=WaveConfig(faction='Lions', red=True, package='salamander',
                          attenuation_enabled=True, tier3_wave=40))
    def first_family_count(count):
        return next((h['wave'] for h in history if len(h['doctrine_families']) >= count), None)
    final = history[-1]
    samples.append((state.mc_owned, final['blueprint_acquisitions'].get('BPCB21', 0),
                    first_family_count(1), first_family_count(2), first_family_count(3),
                    len(history), final['censored']))
print('RUNS', len(samples))
print('FIRST_FAMILY_WAVES', Counter(row[2] for row in samples))
print('SECOND_FAMILY_WAVES', Counter(row[3] for row in samples))
print('THIRD_FAMILY_WAVES', Counter(row[4] for row in samples))
print('MC_MEAN_MEDIAN', round(mean(row[0] for row in samples), 2), median(row[0] for row in samples))
print('SALAMANDER_BP_MEAN_MEDIAN', round(mean(row[1] for row in samples), 2), median(row[1] for row in samples))
print('CENSORED', sum(row[6] for row in samples))
print('SAMPLE_FIRST_10', samples[:10])
