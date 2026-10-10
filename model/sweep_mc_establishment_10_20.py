"""Sweep initial MC establishment target 10–20; continuous, reserve 3, batch 2."""
from statistics import mean, median
from mc_wave60 import WaveConfig, simulate_run

for target in range(10, 21):
    rows = []
    for seed in range(100):
        state, history = simulate_run(None, None, waves=83, seed=seed,
            config=WaveConfig(faction='Lions', red=True, package='salamander',
                attenuation_enabled=True, mc_build_target=target,
                mc_reserve_target=3, mc_batch_size=2,
                mc_construction_policy='continuous'))
        establishment = next((h['wave'] for h in history if h['mc_established']), None)
        post = [h for h in history if establishment is not None and h['wave'] > establishment]
        rows.append((state.mc_built, state.mc_in_hand,
            history[-1]['blueprint_acquisitions'].get('BPCB21', 0),
            state.drafts_resolved, establishment,
            sum(h['mc_selective_this_wave'] for h in post), len(post),
            sum(h['mc_in_hand'] == 0 for h in post)))
    reached = [r[4] for r in rows if r[4] is not None]
    print('target', target,
          'built', round(mean(r[0] for r in rows), 2),
          'reserve', round(mean(r[1] for r in rows), 2),
          'salamander', round(mean(r[2] for r in rows), 2),
          'salamander_median', median(r[2] for r in rows),
          'drafts', round(mean(r[3] for r in rows), 2),
          'established', len(reached),
          'establishment_mean', round(mean(reached), 2) if reached else None,
          'selective_pct', round(100*sum(r[5] for r in rows)/max(1,sum(r[6] for r in rows)),1),
          'empty_pct', round(100*sum(r[7] for r in rows)/max(1,sum(r[6] for r in rows)),1),
          flush=True)
