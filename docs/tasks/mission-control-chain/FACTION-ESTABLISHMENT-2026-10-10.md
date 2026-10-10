# Faction establishment experiment — 6,000 runs

**Date:** 2026-10-10. **Status:** completed, conditional Monte Carlo simulation; not calibrated gameplay probabilities.

## Design

Six scenarios: Iron, Lions, Pargan × Natural/full-MC or Chain/Salamander. Each uses 1,000 seeds, Waves 1–103, with Wave 40 3A access. Blueprint eligibility is filtered to faction-specific asset rosters. Chain uses target 40, reserve 3, batch 2, continuous construction, dynamic selectivity, and attenuation. **Only Lions has Red ordinary reinforcement Blueprint doubling enabled.** Iron/Pargan use no extra commander effect. Thus cross-faction differences confound roster eligibility and Red doubling; do not attribute them solely to roster.

Common acquisition measure: `all_hv_total = all_hv_offense + all_hv_support`, cumulative copies of Salamander Position and four support Blueprints (Air Command, Omega Emitter, Ammo Depot, Division Relay), from all modeled acquisition channels, applied identically to both policies. This is not a unique-identity count, realized combat performance, or necessarily faction-usable inventory.

## Mean outcomes

| Faction | Natural MC W63 | Chain MC W63 | Natural MC W83 | Chain MC W83 | Chain MC built W83 | Natural common HV W83 | Chain common HV W83 | Natural MC W103 | Chain MC W103 | Natural common HV W103 | Chain common HV W103 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Iron | 9.65 | 12.24 | 20.78 | 27.52 | 26.82 | 14.65 | 45.88 | 35.30 | 45.30 | 20.78 | 69.62 |
| Lions | 23.99 | 28.57 | 48.36 | 53.40 | 52.05 | 31.03 | 94.55 | 75.37 | 79.27 | 43.22 | 135.74 |
| Pargan | 9.94 | 12.92 | 21.88 | 28.82 | 28.06 | 14.64 | 46.80 | 36.57 | 47.53 | 20.70 | 71.44 |

## Paired Chain minus Natural effects

| Faction | MC W83 difference ± 95% CI halfwidth | Common HV W83 difference ± 95% CI halfwidth | MC W103 difference ± 95% CI halfwidth | Common HV W103 difference |
|---|---:|---:|---:|---:|
| Iron | +6.736 ± 1.250 | +31.230 ± 0.805 | +9.996 ± 1.828 | +48.835 |
| Lions | +5.032 ± 2.053 | +63.521 ± 1.246 | +3.895 ± 2.858 | +92.519 |
| Pargan | +6.934 ± 1.285 | +32.157 ± 0.818 | +10.960 ± 1.794 | +50.733 |

CI halfwidth uses normal approximation `1.96 * sample SD / sqrt(1000)` on matched-seed differences. Shared seed identifiers do not ensure matched RNG event paths; interpret as paired-by-seed simulation contrasts, not identical-opportunity counterfactuals. No multiplicity adjustment.

## Completeness and failure outcomes

All six scenarios have 1,000 observed Wave 83 and Wave 103 checkpoints. **Zero observed Doctrine-exhaustion soft locks** in 6,000 runs; zero observations does not establish zero underlying probability. The separate commander comparison had four Chain/Magel soft locks and remains preserved.

## Interpretation and caveats

1. Chain beats Natural on modeled mean MC ownership and the **same** common offensive/support Blueprint acquisition metric within each faction at W83 and W103.
2. Lions' large raw totals incorporate the Red doubling rule; this experiment does **not** isolate roster eligibility from faction bonus. A roster-only ablation should run Lions with Red disabled, and commander-specific comparisons should be modeled separately.
3. The package classifier is based on known Blueprint names; verify which named targets are actually available to each faction before using cross-faction acquisition totals as a measure of viable combat power.
4. MC build target 40 is an experimentally chosen boundary, not an established universal optimum across factions. Economic, geometry, build-slot, and exact draft-law assumptions remain provisional.
5. The Natural-vs-Chain contrast changes multiple strategic components at once; it does not attribute gains to any one component.

## Reproducibility

Configuration: `faction-establishment-experiment.json`. Runner: `tools/run_mc_experiment.py`. Raw observations: `faction-establishment-results/raw.csv`. Aggregates, paired contrasts, and soft-lock details: `faction-establishment-results/results.json`. The original `chain-establishment-results/` and older report are preserved. All 161 existing unit tests passed before execution. No commits or pushes.
