# Mission Control experiment runner and Stage A findings

## Stage A (completed)

The Stage A 9,300-run study tested MC establishment targets 10–40 (300 identical seeds per target, 400–699), Lions/Red, Salamander, attenuation enabled, continuous construction, dynamic selectivity, reserve 3, batch 2, through Wave 83. Results: `stage-a-results/raw.csv`, `summary.csv`, and `paired.csv`. At Wave 83 target 40 led observed HV mean 56.4967 (SD 22.5742), versus target 20 mean 53.39; paired improvement +3.1067 ±1.4328 (approximate 95% mean CI). At Wave 63 target 40 led 28.6133 versus target 20 26.48; paired improvement +2.1333 ±0.7674. Target 40 is the **boundary**, not a proven optimum. MC built at Wave 83 averaged 48.5033 for target 40 versus 44.27 for target 20. All values are conditional model outputs, not calibrated game probabilities. This study is distinct from faction/commander chain-establishment experiments.

## Configurable runner

`tools/run_mc_experiment.py` accepts `--config PATH --output DIRECTORY`. Configuration JSON specifies `trials`, `seed_start`, `waves`, `checkpoints`, common `defaults`, named `scenarios` with individual `WaveConfig` overrides, and optional `comparisons` with `scenario`/`reference` names. All current `WaveConfig` fields are supported, including faction, commander flags, Amplifier assumptions, MC 3A timing, offensive package, attenuation, MC establishment target, reserve, batch, replenishment source, construction policy and dynamic selectivity. Invalid unknown fields and invalid horizons are rejected. The same seed values are used in every scenario. Outputs: `raw.csv` (per-seed checkpoints) and `results.json` (descriptive mean/SD/median/p10/p90/approximate mean CI and paired-seed differences). A scenario is flushed to raw CSV before the next scenario begins; JSON is written only on successful completion. Results are not automatically inserted into the PDF or historical report.

Example:

```bash
cd /home/pcastaneda/Documents/tower-dominion-analysis
python3 tools/run_mc_experiment.py \
  --config docs/tasks/mission-control-chain/chain-establishment-experiment.json \
  --output docs/tasks/mission-control-chain/chain-establishment-results
```

## Chain-establishment rerun design

`chain-establishment-experiment.json` defines 15 scenarios × 1,000 seeds = 15,000 runs through Wave 103. Five natural scenarios (Baseline, Lions/Red, Eleanor, Tander, Magel), five saved-Tier-I counterparts, and five modern chain scenarios (Salamander, attenuation, target 40, reserve 3, batch 2, continuous construction, dynamic selectivity). Checkpoints: 20,35,40,50,60,63,64,83,103. Comparisons include commanders versus baseline and each chain policy versus its natural counterpart. The natural and saved-Tier-I cases deliberately reproduce the **historical runner's default `faction='Lions'` even when `red=False`**; they are not valid cross-faction Iron/Pargan comparisons. `red` represents the Lions Blueprint duplication mechanic; `eleanor`, `tander`, and `magel` are modeled commander effects and do not by themselves change the Blueprint roster. Therefore the scenario labels must be read as *commander-effect comparisons under the historical Lions roster*, not independently verified faction-specific eligibility. True faction-by-commander matrix should be a separate controlled study with explicit roster and valid commander combinations.

The historical report (`ANALYSIS-REPORT.md`, `SIMULATION-1000-RUNS.json`, `REPORT-SECTION-*.txt`, and PDF) remains unchanged until rerun outputs are validated. Its previous immediate-build assumptions must not be silently equated with the modern reserve-management strategy. No commit or push requested.

## Genuine Doctrine-exhaustion soft locks

The game can soft-lock when the ordinary reinforcement screen requests a Doctrine and the eligible Doctrine pool is exhausted. This is a **valid outcome**, not a generator defect and not a reason to substitute another reward category. `simulate_run` now records `state.softlock_wave` and stops at that wave while preserving earlier checkpoint history. This is distinct from `state.censored`, which represents the MC special-draft cap. The configurable runner includes `softlocks` (scenario → seed → wave), `softlock_rates`, and checkpoint-specific `observed` denominators in `results.json`. A missing checkpoint after a soft lock must not be counted as a successful run or silently imputed as zero MC. Note that the simulator stops on the **first** exhausted Doctrine request; further game behavior is not modeled. Regression tests in `model/test_mc_softlock.py` cover this and unrelated error propagation. All 161 tests passed on 2026-10-10.

Rerun process PID **1659160** launched with `chain-establishment-experiment.json` after soft-lock handling was added. Results pending. The existing report and PDF have not been revised. No commit or push.

## Faction roster comparison (2026-10-10)

The follow-up experiment config `faction-establishment-experiment.json` uses `Iron`, `Lions`, `Pargan` (the actual Doctrine-model faction identifiers) and the corresponding asset-derived Blueprint rosters (`Faction1`, `Faction2`, `Faction3`). Two policies per faction: Natural full-MC and Chain (Salamander, target 40, reserve 3, batch 2, continuous, dynamic selectivity, attenuation). Lions alone has Red ordinary Blueprint doubling enabled; Iron and Pargan have **no added commander bonuses**. Therefore this is a **faction roster plus Lions bonus comparison**, not a controlled roster-only ablation or complete commander roster comparison. Six scenarios × 1,000 seeds, W103 horizon.

Runner adds policy-independent `all_hv_offense`, `all_hv_support`, `all_hv_total` metrics from cumulative `blueprint_acquisitions`, classifying Salamander Position as offense and SUPPORTS as support. This metric includes all modeled acquisition sources, unlike the prior `hv_*` special-draft-only metrics; it is a **count of acquired copies**, not a unique-identity count or combat value. The `all_hv_*` metrics are directly comparable between Natural and Chain within this fixed package definition. Historical `chain-establishment-results/results.json` retains its previous metric schema and was not overwritten. Median computation corrected to use `statistics.median`.

Process PID **1660031** launched after 161 passing tests; results destination `faction-establishment-results/`. Report update pending results. No commits/pushes.
