# Mission Control Chain — Analysis Report

**Tower Dominion | 9 October 2026 | Exploratory Monte Carlo model**

## Executive summary

This report analyzes how Mission Control (MC, Blueprint `BPSB07`) acquisition compounds through persistent Blueprint rarity bonuses, Amplifiers, reinforcement choices, and the MC 3A special Blueprint drafts. The standard assumption is **3A access beginning on Wave 40**, with the run followed through **Wave 103**. Results are simulated conditional on the documented strategic policy; they are **not empirically calibrated odds of an average game**.

Across 500 seeded simulations per commander, the natural-Amplifier model produced the following average total MC ownership (built plus in hand):

| Scenario | W83 mean | W83 median | P(MC >= 20 at W83) | W103 mean | W103 median |
|---|---:|---:|---:|---:|---:|
| Baseline (no commander bonus) | 16.79 | 14 | 30.6% | 27.74 | 24 |
| Red | 36.48 | 31.5 | 76.8% | 56.49 | 51 |
| Eleanor | 26.61 | 24 | 64.6% | 41.63 | 37 |
| Tander | 22.45 | 19 | 49.8% | 35.59 | 32 |

All 2,000 runs reached W103 without hitting the special-draft censoring cap. The user independently described runs with roughly 20–30 MC by W83 and at least five in hand. **No model parameters were adjusted to fit that observation.** The simulator immediately builds acquired MCs, so its in-hand count is always zero and cannot be compared to the observed held inventory.

## 1. Model introduction and scope

The model uses asset-derived eligible Blueprint entries and wave-dependent rarity weights, a dynamic ordinary-Doctrine pool, generated ordinary reinforcement cards, commander-specific reward opportunities, and recursive MC 3A Blueprint drafts. Each seeded run advances one wave at a time, generates available rewards, selects a card under a deterministic MC-oriented policy, applies its contents, builds strategic buildings, and resolves special drafts. Reported MC count is `mc_built + mc_in_hand`.

This is a **conditional strategic acquisition model**, not a complete game simulation: combat, resources, geometry, build slots, building-sale economics, and the full Doctrine/Blueprint reward system are not reproduced. See `model/mc_wave60.py`, `model/mc_state.py`, `model/mc_scenarios.py`, and `docs/MECHANICS.md`.

## 2. Core assumptions and acquisition rules

1. **Blueprint pool.** The asset-derived roster contains 32 normal reinforcement-eligible Blueprints: 12 Tier 1, 10 Tier 2, and 10 Tier 3. MC is a Tier 3 Blueprint. Weighted selection is per Blueprint identity, not a prior tier draw. Tier 3 rarity starts at -8 and increases by 1 each wave before modifiers and clamping.
2. **Ordinary reinforcement.** Standard rewards present three cards, each with two items. Candidate category base weights are Supply 10, Recon 4, Blueprint 57, and Doctrine 29. Selected cards award **both** contained items. The model prioritizes MC-containing cards, otherwise its current choice score favors a *first* Amplifier-granting Doctrine when no Amplifier is owned. That priority is **not** a blanket guarantee to choose a second Amplifier over all competing rewards.
3. **Mission Control 1A.** Each built MC adds **+2 raw rarity weight to every eligible Tier 2 and Tier 3 Blueprint**. Contributions from multiple built MCs stack and persist on subsequent waves. They increase competitors' weights as well as MC's own weight.
4. **Amplifiers.** Two independently eligible ordinary Doctrines, `D1_45` and `D2_42`, can grant an Amplifier; neither is gated by a placed building family. Amplifiers may be acquired before MC, held, and built when MC becomes available. The simulation applies each built Amplifier to MC immediately. Two Amplifiers contribute additive +200% to MC's targeted Blueprint weight (3x base after the raw rarity calculation), versus +100% (2x) for one. Grant quantity is provisionally one per Doctrine.
5. **MC 3A.** On **Wave 40**, all built MCs are assumed affordable to upgrade to 3A; newly acquired MCs are immediately built/upgraded on that wave and thereafter. Each 3A generates two special five-choice Blueprint drafts. If MC appears in a draft, the model selects it, builds it, and resolves any additional 3A drafts recursively. This is a deliberate optimistic economic assumption, not a measured Supply/Recon budget.
6. **Special draft selection.** Five distinct weighted Blueprint candidates are modeled through rejection sampling. The precise game's special-reward candidate law has not been definitively verified.
7. **Doctrine pool.** Ordinary Doctrine availability is dynamic, accounting for owned Doctrines and certain known weight changes. Other placed building families can dilute the pool, but the present MC-targeted runs do not reproduce all realistic family placement/pollution.
8. **Run horizon.** Standard simulation now evaluates through W103; the `WaveConfig` default is `tier3_wave=40`. The script/module name `mc_wave60.py` is historical and does not impose a 60-wave limit.

## 3. Commander comparisons

- **Baseline:** MC-first ordinary reward selection, natural acquisition of both Amplifier Doctrines if selected, immediate build, W40 3A.
- **Red:** Doubles Blueprint quantities acquired from **ordinary reinforcement**; it does not double every special draft.
- **Eleanor:** Adds a choose-one-of-three Blueprint opportunity every other wave. Its cadence phase and exact higher-tier weighting are provisional; the implemented scenario does not fully establish all of Eleanor's in-game effects.
- **Tander:** Presents four rather than three ordinary reinforcement cards (eight rather than six candidate items).

The W83 and W103 results above use 500 seeds (1–500) per scenario, with W40 3A and naturally acquired stacking Amplifiers. All have zero censored runs. Different scenarios consume random draws differently, so shared seed numbers do not guarantee identical event streams; small differences should not be overinterpreted.

## 4. Amplifier sensitivity at Wave 60

A separate 500-run comparison isolates Amplifier assumptions while retaining W40 3A:

| Scenario | W20 mean | W35 mean | W40 mean | W45 mean | W50 mean | W60 mean | P(MC >= 5 at W60) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Both naturally acquired Amplifiers can stack | 0.180 | 0.930 | 2.206 | 3.168 | 4.348 | 7.172 | 60.8% |
| One additional saved Amplifier bonus from the start **plus** natural acquisition | 0.380 | 1.846 | 5.936 | 8.522 | 11.414 | 19.316 | 91.8% |
| No Amplifier weight effect | 0.172 | 0.784 | 1.312 | 1.728 | 2.208 | 3.182 | 23.4% |

**Interpretation:** The naturally acquired, potentially two-Amplifier scenario is the standard. The saved-Amplifier row is an **extra guaranteed +100% bonus from Wave 1** on top of any naturally acquired Amplifiers, not simply the ordinary practice of holding an Amplifier found before MC appears. The no-effect row disables Amplifier's weight contribution, but does not remove its Doctrine/reward events; it is an effect-ablation experiment rather than a fully reoptimized no-Amplifier strategy. None of these results should be treated as measured gameplay frequencies.

An earlier one-Amplifier-capped natural model reported W60 mean 6.854 and P(>=5) 60.2%. Those figures are **superseded** by the corrected two-Amplifier-stacking natural results (7.172 and 60.8%). Likewise, an earlier 'full Amplifier' result of 9.01 MC at W60 referred to a constant single +100% effect, **not** to naturally acquiring both Amplifiers; it should not be used as the standard comparison.

## 5. Mechanics not yet incorporated

- **Pit** contributions and their acquisition/timing.
- **Reactive** stacking of targeted +10% Blueprint weight effects, subject to placement/adjacency; this interacts nonlinearly with recursive 3A drafts.
- **Calculator** acquisition and its reward/weight effect; its internal asset identity and acquisition route are not yet established.
- Complete building-family Doctrine pollution, geometry, economy, inventory retention, and precise special reward implementation.
- Other reward-generating Doctrines and commander effects not yet fully integrated or verified.

These are **unmodeled effects**, not correction factors. In particular, the model should not be fitted to the observed W83 totals. Each mechanic should be independently verified and introduced as a separate testable model slice.

## 6. Reproducibility and cautions

Repository: `/home/pcastaneda/Documents/tower-dominion-analysis`. Core modules: `model/mc_wave60.py`, `model/mc_state.py`, `model/mc_doctrines.py`, `model/mc_reinforcement.py`, `model/mc_roster.py`, `model/mc_weights.py`. The W103 comparison was run using `simulate_run(load_blueprint_roster(), None, waves=103, seed=seed, config=WaveConfig(...))` for seeds 1–500, collecting W83 history and W103 final state. Amplifier W60 sensitivity used `summarize_scenario(trials=500, config=WaveConfig(...))`. All 128 existing unit tests passed at the last execution, though new stack-specific regression tests have not yet been added. Changes are uncommitted.

**Important policy limitation:** The current card selector's `need_amp` test becomes false after the first Amplifier, so although a second Amplifier *can* be granted and its bonus stacks, the choice policy does not systematically pursue the second one. This report describes the implementation actually simulated, not a stronger hypothetical 'always choose both Amplifiers' policy.

## 7. Next research question

Establish **Calculator acquisition** from its localized building name, internal Blueprint/Doctrine identity, bundle eligibility, and other reward sources before estimating its probability or adding it to MC simulations.

## 8. Update — 10 October 2026: 15,000-run chain establishment experiment

**Newer results supersede the older 500-seed figures for like-for-like 1,000-seed commander comparisons, but do not retroactively change the historical experiment.** See [CHAIN-ESTABLISHMENT-2026-10-10.md](CHAIN-ESTABLISHMENT-2026-10-10.md) for full tables, assumptions, soft-lock details, and reproducibility.

The new experiment crossed Baseline, Lions/Red, Eleanor, Tander, and Magel with Natural/full-MC, Saved Tier I/full-MC, and the newer continuous-construction/Salamander-package strategy (target 40, reserve 3, batch 2, dynamic selectivity, attenuation). At W83, Natural vs Chain average MC ownership was: Baseline **21.51 vs 29.00**; Lions **48.36 vs 53.40**; Eleanor **34.99 vs 41.99**; Tander **30.37 vs 36.24**; Magel **44.49 vs 49.51**. At W103: Baseline **35.57 vs 47.49**; Lions **75.37 vs 79.27**; Eleanor **54.75 vs 64.06**; Tander **46.64 vs 55.70**; Magel **75.68 vs 76.61**, with the latter Chain mean based on **996** surviving seeds.

**Valid soft locks:** Chain/Magel exhausted the eligible Doctrine pool in **4/1,000 runs (0.4%)**, at waves 101 or 103; all other scenarios had zero observed soft locks. These are now recorded as game outcomes, distinct from simulation censoring. The natural/full-MC HV metric is not comparable with the Chain HV metric because the former does not enable package-oriented classification. All scenarios use the **Lions roster**, so this is a commander-effect comparison, **not** a genuine three-faction roster comparison. The existing PDF is not yet regenerated and continues to reflect its original source experiment.

## 9. Update — 10 October 2026: cross-faction roster experiment

The six-scenario, 6,000-run faction experiment has completed. See [FACTION-ESTABLISHMENT-2026-10-10.md](FACTION-ESTABLISHMENT-2026-10-10.md) for tables, paired uncertainty estimates, and assumptions. Each faction was run using its asset-filtered eligible Blueprint roster. Lions alone received its ordinary reinforcement Blueprint doubling bonus; **this is not a pure faction-roster-only comparison**.

At Wave 83, Natural vs Chain average MC ownership: Iron **20.78 vs 27.52**, Lions **48.36 vs 53.40**, Pargan **21.88 vs 28.82**. At Wave 103: Iron **35.30 vs 45.30**, Lions **75.37 vs 79.27**, Pargan **36.57 vs 47.53**. Using the same Salamander-offense-plus-support Blueprint acquisition classifier for both policies, Wave 83 averages were Iron **14.65 vs 45.88**, Lions **31.03 vs 94.55**, Pargan **14.64 vs 46.80**. All six scenarios had complete 1,000-seed W103 observations and zero observed soft locks. The model's Blueprint copy counts are not a measure of realized combat power.

Paired W83 MC improvements (Chain minus Natural; approximate 95% CI halfwidth) were Iron **+6.736 ± 1.250**, Lions **+5.032 ± 2.053**, and Pargan **+6.934 ± 1.285**. The older PDF remains unchanged; it documents a different historical simulation.
