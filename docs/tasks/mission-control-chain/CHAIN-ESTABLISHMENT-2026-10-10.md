# Mission Control chain establishment — 15,000-run comparison

**Date:** 2026-10-10. **Status:** completed, conditional Monte Carlo model; not empirically calibrated game odds.

## Experiment design

- 15 scenarios: five commander conditions (Baseline, Lions/Red, Eleanor, Tander, Magel) crossed with Natural/full-MC, Saved Tier I/full-MC, and new Chain policies.
- 1,000 seeds per scenario (1–1,000), 103 waves, 15,000 simulated runs; identical seed identifiers but potentially divergent random draw streams.
- Default faction roster: `Lions` for **every** scenario. This is a comparison of modeled commander bonuses, **not** a cross-faction eligibility experiment. In particular, non-Lions commander cases are counterfactual effects on a Lions roster.
- Natural and Saved Tier I: immediate MC construction, MC-oriented rewards; Saved Tier I adds an assumed Tier I Amplifier doctrine bonus from Wave 1.
- Chain: Salamander package, attenuation enabled, MC build target 40, MC reserve 3, batch 2, continuous construction, dynamic selectivity, Wave 40 3A.
- Red doubles Blueprints from **ordinary reinforcement only**. MC 3A special drafts and Eleanor's separate drafts are not doubled.

## Main results

Means, with MC = built + held. HV is the simulator's *package-classified cumulative acquisition count*, not a full inventory or realized damage measure.

| Commander | Natural MC W83 | Chain MC W83 | Chain built W83 | Chain HV W83 | Natural MC W103 | Chain MC W103 | Chain HV W103 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 21.51 | 29.00 | 28.31 | 31.51 | 35.57 | 47.49 | 51.63 |
| Lions / Red | 48.36 | 53.40 | 52.05 | 60.52 | 75.37 | 79.27 | 91.40 |
| Eleanor | 34.99 | 41.99 | 41.01 | 46.52 | 54.75 | 64.06 | 71.23 |
| Tander | 30.37 | 36.24 | 35.44 | 39.36 | 46.64 | 55.70 | 60.42 |
| Magel | 44.49 | 49.51 | 48.01 | 50.76 | 75.68 | 76.61* | 79.53* |

*Chain/Magel W103 means condition on 996 observed runs, excluding four soft-locked before the W103 checkpoint. Do not interpret survivor-only means as unconditional expected outcomes.*

### Saved Tier I full-MC sensitivity

| Commander | Natural MC W83 | Saved Tier I MC W83 | Natural MC W103 | Saved Tier I MC W103 |
|---|---:|---:|---:|---:|
| Baseline | 21.51 | 24.21 | 35.57 | 39.13 |
| Lions / Red | 48.36 | 54.10 | 75.37 | 83.11 |
| Eleanor | 34.99 | 39.72 | 54.75 | 61.03 |
| Tander | 30.37 | 32.04 | 46.64 | 48.55 |
| Magel | 44.49 | 44.46 | 75.68 | 76.08 |

## Genuine Doctrine exhaustion / soft locks

- Chain/Magel: **4 of 1,000 (0.4%)**: seeds 91 (W103), 411 (W101), 664 (W103), 913 (W103).
- All other scenarios: **0 of 1,000** each in this experiment.
- The model stops at the first reinforcement request for a Doctrine when no eligible Doctrines remain. This is a **valid in-game soft lock**, not a candidate-generation defect.
- This differs from the simulator's `censored` flag, which tracks a special-draft processing cap. Checkpoint means after soft locks are conditional on reaching the checkpoint.

## Interpretation and limitations

1. All Chain scenarios produced higher average MC ownership than the corresponding Natural scenarios at W83 and W103. This is a *policy comparison*, not an isolated effect of reserving MCs: package choice, attenuation, construction, and selectivity change together.
2. Lions/Red leads at W83 for both MC and package-classified HV acquisition; at W103, Natural/Magel and Natural/Lions have similar MC totals, but Magel's Chain W103 values are conditional on survival.
3. Natural and Saved Tier I runs show **zero recorded HV** because the HV classifier is activated through the Chain package. These zeros are **not evidence that those strategies acquire zero useful Blueprints**. Do not compare HV between policies until a policy-independent HV classifier is implemented.
4. Same seed identifiers are paired for comparison but different commander policies consume random draws differently; paired differences are not controlled common-event-path counterfactuals.
5. Commander effects, reinforcement sampling, construction affordability, geometry, exact special draft law, and other missing mechanics remain provisional as detailed in `ANALYSIS-REPORT.md`.
6. A separate faction-eligibility experiment is required before making claims about Iron Dragoons vs Lions of Ravleski vs Pargan Assault Group. The present config sets the Lions roster for all scenarios.

## Reproducibility

Config: `chain-establishment-experiment.json`. Runner: `tools/run_mc_experiment.py`. Raw checkpoint data: `chain-establishment-results/raw.csv`. Aggregate/paired data and soft-lock seed records: `chain-establishment-results/results.json`. All 161 unit tests passed. No commits or pushes performed.

## Eleanor commander modeling — explicit source and derived effects (2026-10-10 correction)

**Independent commander parameter:** `eleanor_starting_mc_1a_equivalent = 10` when `eleanor = true`. This is a *rarity-weight equivalent only*: it does not grant ten Mission Controls, construction, upgrades, MC 3A draft triggers, or any other MC ownership benefit. It applies from Wave 1 to **all Blueprint selection channels**, since each uses `current_weights()`.

**Derived effects, NOT separately configurable bonuses:** each MC 1A adds +2 to raw Tier 2 and Tier 3 Blueprint rarity weights. Eleanor's ten equivalents therefore yield `10 × 2 = +20` raw rarity weight for each of Tier 2 and Tier 3. Actual MC 1A upgrades stack additively with this amount, as do other tier-weight currencies. This is *not* a +20% multiplier and must never be counted twice. The final type-based percentage modifiers (e.g. Amplifier) are a separate calculation.

**Independent starting-state restriction:** `eleanor_initial_tier23_dampening = false`. Eleanor starts with no Tier 2 or Tier 3 Blueprint dampening. The simulator explicitly rejects enabling this flag because an alternate initial-dampening mechanic has not been implemented; this flag documents and enforces the supported state, rather than adding an attenuation effect.

**Separate commander ability:** Eleanor receives one extra choose-one-of-three Blueprint draft every two waves starting at Wave 2 (`eleanor_first_wave = 2`, `eleanor_cadence = 2`); draft timing and sampling remain assumptions pending game asset verification.

**Experiment tracking:** `chain-establishment-experiment.json` records these Eleanor settings for each Eleanor scenario. Results produced before this correction lack her ten-MC-equivalent rarity bonus and must not be used as corrected Eleanor comparisons. The corrected 15,000-run experiment is saved under `commander-salamander-eleanor-corrected-2026-10-10/`; Wave 63 and Wave 83 are primary checkpoints, Wave 103 diagnostic only.
