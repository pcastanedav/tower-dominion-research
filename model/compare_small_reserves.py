"""Paired-seed comparison of smaller MC reserve policies."""
from statistics import mean, median
from mc_wave60 import WaveConfig, simulate_run

for label, target, reserve, batch in [
    ('15/5 batch3', 15, 5, 3),
    ('15/3 batch3', 15, 3, 3),
    ('15/2 batch2', 15, 2, 2),
    ('15/3 batch2', 15, 3, 2),
    ('20/6 batch3', 20, 6, 3),
]:
    rows = []
    for seed in range(100):
        state, hist = simulate_run(None, None, waves=83, seed=seed,
            config=WaveConfig(faction='Lions', red=True, package='salamander',
                attenuation_enabled=True, mc_build_target=target,
                mc_reserve_target=reserve, mc_batch_size=batch))
        established = next((x['wave'] for x in hist if x['mc_established']), None)
        after = [x for x in hist if established is not None and x['wave'] > established]
        batches = sum(x['mc_built'] > hist[x['wave']-2]['mc_built'] for x in after)
        selective = sum(x['mc_selective_this_wave'] for x in after)
        rows.append((state.mc_built, state.mc_in_hand,
            hist[-1]['blueprint_acquisitions'].get('BPCB21', 0),
            established, batches, selective, len(after), state.drafts_resolved))
    print(label,
          'built', round(mean(x[0] for x in rows), 2),
          'reserve', round(mean(x[1] for x in rows), 2),
          'salamander', round(mean(x[2] for x in rows), 2),
          'salamander_med', median(x[2] for x in rows),
          'established', sum(x[3] is not None for x in rows),
          'batches', sum(x[4] for x in rows),
          'selective_pct', round(100 * sum(x[5] for x in rows) / max(1,sum(x[6] for x in rows)),1),
          'drafts', round(mean(x[7] for x in rows),2))
