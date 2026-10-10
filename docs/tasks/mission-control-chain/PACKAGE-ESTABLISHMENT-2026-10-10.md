# Offensive package comparison — 2026-10-10

## Scope and provenance

The corrected commander comparison uses 1,000 seeds per scenario, 103 waves, with Waves 63 and 83 as primary checkpoints and Wave 103 diagnostic only. Six additional packages generated 26,000 simulations (26 scenarios), plus the corrected five-commander Salamander Chain reference (5,000 runs). Results: `package-establishment-results-2026-10-10/` and `commander-salamander-eleanor-corrected-2026-10-10/`. Both contain `raw.csv` and `results.json`; the JSON includes full experiment configuration.

The model is conditional and not calibrated to measured game odds. All commander comparisons use the Lions Blueprint roster, varying commander bonuses. Tactical Fortress is restricted to Red/Lions. The corrected Eleanor setting is `eleanor_starting_mc_1a_equivalent=10`; its derived +20 Tier 2 and +20 Tier 3 raw rarity weights are not independent parameters. Eleanor starts without Tier 2/3 dampening and receives extra choose-one-of-three drafts every two waves starting at Wave 2 (draft timing and sampling provisional).

## Separate building metrics

`offense_building_1` and `offense_building_2` are cumulative acquired Blueprint copies, **not buildings constructed**. The package-to-building-name mapping is stored in `results.json` under `package_building_labels`. For single-building packages, building 2 is zero by definition. `complete_sets` is the minimum count across required offensive buildings; `has_all_required` indicates at least one of every required building; `has_only_one_required` indicates exactly one distinct required building acquired (two-building packages only). Report means and uncertainty using `summary` and raw paired seeds; completion near 100% at Wave 83 makes matched sets and individual counts more informative than binary completion.

## Wave 83 examples (mean acquisitions)

| Package | Commander | Building 1 | Building 2 |
|---|---|---:|---:|
| Howitzer + Cannon | Red | 21.6 | 24.5 |
| Howitzer + Cannon | Eleanor | 20.6 | 23.8 |
| SPHD + Rampart | Red | 24.0 | 20.0 |
| SPHD + Rampart | Eleanor | 23.2 | 18.7 |
| SPHD + Retribution | Red | 21.6 | 25.0 |
| SPHD + Retribution | Eleanor | 20.9 | 24.1 |
| SPHD + Fortress | Red | 23.6 | 20.0 |

The Wave 83 binary package completion rates are approximately 99.9–100%. At Wave 63 Eleanor leads Red in several individual-building acquisition averages; compare matched sets and paired uncertainty before drawing broader conclusions.

## Censoring and limitations

Doctrine-exhaustion softlocks are genuine model outcomes. Additional-package Magel Chain softlock rates: Howitzer 0.5%, Cannon 0.8%, SPHD + Rampart 0.6%, SPHD + Retribution 0.3%. Report observed sample counts for censored checkpoints, especially Wave 103. Commander and package findings are simulation outputs, not verified in-game acquisition probabilities. Next analysis: full package × commander comparisons at Waves 63 and 83, matched sets, per-building counts, MC ownership, support counts, paired uncertainty, and softlock rates.
