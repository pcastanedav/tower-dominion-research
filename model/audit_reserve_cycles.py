"""Wave-by-wave audit of reserve-based MC acquisition and construction."""
from collections import Counter
from statistics import mean, median
from mc_wave60 import WaveConfig, simulate_run

N = 100
for label, threshold, reserve in [('B', 15, 5), ('C', 20, 6)]:
    runs = []
    for seed in range(N):
        _, history = simulate_run(None, None, waves=83, seed=seed,
            config=WaveConfig(faction='Lions', red=True, package='salamander',
                attenuation_enabled=True, mc_build_target=threshold,
                mc_reserve_target=reserve))
        runs.append(history)
    modes = Counter()
    batches = Counter()
    replenish_lengths = []
    threshold_reached = []
    reserve_ready = []
    construction_after_established = []
    transition_matrix = Counter()
    for history in runs:
        first = next((h['wave'] for h in history if h['mc_established']), None)
        if first is not None:
            threshold_reached.append(first)
        for i, h in enumerate(history):
            if first is None or h['wave'] <= first:
                continue
            mode = 'selective' if h['mc_selective_this_wave'] else 'replenish'
            modes[mode] += 1
            if h['mc_selective_this_wave']:
                reserve_ready.append(h['wave'])
            prev = history[i-1]
            built = h['mc_built'] - prev['mc_built']
            if built:
                batches[built] += 1
                construction_after_established.append(h['wave'])
            if i > 1 and prev['wave'] > first:
                prev_mode = 'selective' if prev['mc_selective_this_wave'] else 'replenish'
                transition_matrix[(prev_mode, mode)] += 1
        streak = 0
        for h in history:
            if first is None or h['wave'] <= first:
                continue
            if not h['mc_selective_this_wave']:
                streak += 1
            elif streak:
                replenish_lengths.append(streak)
                streak = 0
        if streak:
            replenish_lengths.append(streak)
    print('\nPOLICY', label, 'threshold', threshold, 'reserve', reserve)
    print('ESTABLISHED', len(threshold_reached), 'of', N,
          'mean_wave', round(mean(threshold_reached), 2) if threshold_reached else None,
          'median_wave', median(threshold_reached) if threshold_reached else None)
    print('MODES', dict(modes), 'selective_fraction',
          round(modes['selective'] / sum(modes.values()), 3) if modes else None)
    print('BATCHES', dict(sorted(batches.items())), 'total', sum(batches.values()))
    print('REPLENISH_STREAKS', len(replenish_lengths), 'mean',
          round(mean(replenish_lengths), 2) if replenish_lengths else None,
          'median', median(replenish_lengths) if replenish_lengths else None,
          'max', max(replenish_lengths) if replenish_lengths else None)
    print('TRANSITIONS', dict(transition_matrix))
    print('SELECTED_WAVE_TRACE seed=0: wave mode reserve built deltaMC deltaSalamander')
    hist = runs[0]
    for i, h in enumerate(hist):
        if h['wave'] not in (20, 30, 39, 40, 41, 42, 43, 44, 45, 50, 60, 70, 80, 83):
            continue
        p = hist[i-1] if i else None
        db = h['mc_built'] - (p['mc_built'] if p else 0)
        ds = h['blueprint_acquisitions'].get('BPCB21', 0) - (p['blueprint_acquisitions'].get('BPCB21', 0) if p else 0)
        print(h['wave'], 'S' if h['mc_selective_this_wave'] else 'M',
              h['mc_in_hand'], h['mc_built'], db, ds)
