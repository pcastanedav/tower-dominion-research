# Wave-35 Super Weapon Expertise experiments — design and implementation plan

Status: DESIGN / NOT YET EXECUTED. No simulated completion rates are claimed.

## Question
Estimate the probability of obtaining a chosen Tier-3 Super Weapon's Expertise I/II/III progression by Wave 35, comparing Eleanor with non-Eleanor and alternative schedules of unrelated doctrine-bearing building families. Distinguish Blueprint acquisition from construction and Doctrine progression.

## Fixed assumptions
- 35-wave horizon; the target is a verified T3 building family with an Expertise progression; verify target ID, its exact branch and eligibility from asset/code evidence before execution.
- **Wave 10 is an accepted resource constraint, not a cost-model verification task.** Target construction occurs at `max(10, blueprint_acquisition_wave)`; if never acquired, target cannot be constructed. Do not investigate or simulate building costs to justify this floor.
- Same faction, eligible Blueprint roster, selection policy and seed set across commander comparisons. Use paired seeds; RNG streams may diverge when Eleanor adds drafts.
- Once target family is placed, the Expertise branch follows the documented TB-family progression. Verify which D4/D5/D6 node corresponds to the requested Expertise levels for each target rather than assuming names alone.
- No combat-survival or complete economy simulation. Wave-10 construction floor is externally imposed; other building timing is a policy assumption.
- **Amplifier policy in every strategy:** prioritize acquiring an Amplifier whenever its granting Doctrine is offered (existing research maps `D1_45` and `D2_42` to Amplifier). If the target is built, assign the Amplifier to the target immediately; if not built, retain it and assign upon target construction. Apply its target-family **Blueprint and building-Doctrine** weighting when assigned: each Amplifier contributes +100% to both targeted weights (one = 2x, two = 3x under additive stacking). Use `amplified_families` in `dynamic_doctrine_pool_fast` or equivalent; never boost ordinary Doctrines or unrelated families. Record whether it was offered, acquired, saved, and ultimately assigned, and the corresponding waves.
- **Attenuator observation:** track offers and acquisitions of Attenuator-granting Doctrines (`D1_44`, `D2_41` in the existing model), including zero-offer runs and count of distinct offers/acquisitions. Report the observed counts independently of whether Attenuators are used. Default experiment does not assume an Attenuator deployment/targeting policy; introduce one only as a separately identified scenario.
- Eleanor's modeled higher-tier Blueprint bonus is resolved in the corrected Mission Control analysis: ten MC-1A rarity equivalents give +20 raw Tier 2 and +20 raw Tier 3 weights from Wave 1, additive rather than a +20% multiplier. Use the corrected implementation; do not reintroduce the obsolete percentage ambiguity. Grande Ecole draft phase/sampling still require game-asset validation.

## Primary matrix
For each policy run Eleanor off/on:
1. Isolated: target only.
2. Minimal: target + one competing family placed early.
3. Moderate: target + three competing families placed early.
4. Broad: target + five competing families placed early.
5. Delayed: one competing family early, two additional at Wave 20.
6. Late: one competing family early, four additional at Wave 25.

Define 'early' explicitly in executable config (proposed Wave 1) and enforce eligibility. These policies are controlled counterfactuals, not claims that the game economy allows every placement.

## Essential controls
A. Guaranteed Blueprint possession with target placed Wave 10 for both commanders: isolates Doctrine-family competition. Since Eleanor's verified effects are Blueprint-side, expect no direct Doctrine benefit in this control unless another mechanism is identified.
B. Modeled Blueprint acquisition, earliest target placement Wave 10: measures Eleanor's indirect advantage through earlier target access. Never force the non-Eleanor scenario to build before it obtains the Blueprint.
C. Sensitivity: compare target family identity and separately declared Amplifier/Attenuator policy variants. Keep the Wave-10 floor and corrected Eleanor rarity arithmetic fixed; no cost verification or obsolete +20% sensitivity.

## Metrics
- Cumulative P(Expertise I, II, III owned) at Waves 10, 15, 20, 25, 30, 35, with 95% uncertainty intervals.
- P(target Blueprint acquired), P(target constructed), median acquisition/construction/completion wave, P(III | target constructed), and P(III | constructed by Wave 10).
- Observed denominators, softlock/censored rates, and paired difference versus corresponding non-Eleanor policy.
- Distinguish failure to acquire/build target from failure to progress Doctrines after construction.
- Amplifier: count runs with an offer, acquisition, saved-before-target, assignment to target; wave of first offer/acquisition/assignment; amplification-active exposure by wave and count of Amplifiers assigned (0/1/2).
- Attenuator: number of offered grant Doctrines and number acquired per run, first offer/acquisition wave, counts and proportions of runs with 0/1/2+ offers and 0/1/2 acquisitions. Preserve offer counts even when selection goes elsewhere.
- Compare outcomes stratified by Amplifier acquired/assigned and Attenuator offers, but label these observational correlations rather than randomized causal effects.

## Implementation slices
1. Verify exact Super Weapon IDs, their Expertise nodes, faction eligibility, and whether their building family has the standard TB progression. Record source evidence and assumptions.
2. Implement a dedicated stateful 35-wave target-Blueprint acquisition/placement/Doctrine progression simulator reusing existing `mc_roster`, `mc_weights`, and `reinforcement_model` components where appropriate; do not use the MC experiment runner unchanged because it does not model this objective.
3. Add deterministic policy schedules and Eleanor/no-Eleanor comparison with paired seeds, including guaranteed-Wave-10 control, persistent Amplifier reservation/target assignment, and Attenuator offer/acquisition counters.
4. Add unit tests for Wave-10 construction floor (without cost verification), eligibility, Doctrine prerequisites, removal persistence, pool competition, Eleanor draft schedule, Amplifier saved-before-build/assigned-after-build behavior and 1x/2x/3x targeted Doctrine weight regression, Attenuator offer counts (including unselected offers), and completion metrics.
5. Execute 1,000 seeds per scenario as a pilot; inspect softlocks and performance, then scale if uncertainty is too wide.
6. Produce numerical comparisons, limitations and a reproducible report; review before committing/publishing.

## Source anchors
`docs/MECHANICS.md` sections 5 and 10; `docs/OPEN_QUESTIONS.md`; `maps/blueprints.json`; `maps/ordinary-doctrines.json`; `model/reinforcement_model.py` (`tb_active_nodes`, `DoctrineRunState`, `state_doctrine_pool`); `model/mc_roster.py`; `model/mc_weights.py`; `docs/tasks/mission-control-chain/CHAIN-ESTABLISHMENT-2026-10-10.md` (Eleanor correction).

## Implementation checkpoint (2026-10-17)
- Initial conditional simulator: `model/expertise_wave35.py`; tests: `model/test_expertise_wave35.py` (5 passing).
- Implemented Wave-10 floor, six family schedules, Eleanor +20/+20 raw Blueprint weight and provisional even-wave 1-of-3 drafts, normal three-card/two-item reinforcement, target Expertise D4/D5/D6 tracking, 0/1/2 Amplifier additive target-Doctrine weights, and Attenuator offer/acquisition counters.
- **Do not treat pilot outputs as validated odds yet.** The runner currently uses a simplified card priority, does not resolve all nested ordinary-Doctrine effects, and does not model all Doctrine-derived Blueprint weight changes. The target Expertise D4/D5/D6 mapping is a provisional hypothesis requiring per-building source verification. Its amplified Blueprint weighting is applied after construction but not before; this is intentional because assignment requires a built target. Eleanor draft timing/sampling remain provisional. No costs need verifying: Wave 10 is fixed by user assumption.
- Next: validate target Expertise IDs and selection/side-effect fidelity; add reporting and run pilot after those checks. No commit or push performed.

## Implementation checkpoint 3 (2026-10-17)
- Fixed building family identity handling: use actual family codes (e.g. `CB14`) and Doctrine IDs (`TBCB14D4`) rather than abstract integer `14`/`TB14D4`. Earlier 30-seed smoke-test outputs are **invalidated** by this correction.
- Ordinary Doctrine side effects now modeled for `D1_19` (+6 T2 eligibility weight), `D2_40` (+4 building Doctrine multiplier and nested 1-of-2 draft), `D2_06` (two nested 1-of-3 drafts), `D2_01` (+10 T2 Blueprint raw weight), `D3_11` (+5 T3 Blueprint raw weight). Nested drafts recalculate their pools after each selection and prioritize target progression or Amplifier. Nested Amplifier/Attenuator offers are counted.
- Eleonor's extra draft now samples three *distinct* weighted Blueprint candidates; this is a modeling assumption pending exact live-selector confirmation. It occurs on Waves 2,4,...,34.
- Seven dedicated tests passing. Prior full repository suite (before two additional tests): 185 passing. Amplifier target-family weighting remains additive (+100% each, up to two) and Wave 10 remains a fixed assumption.
- A 1,000-seed-per-scenario pilot was initiated for guaranteed and modeled Blueprint acquisition, targeting CB14/Lions. Outputs are conditional model estimates, not empirical game probabilities; report must disclose incomplete side effects, target selection bias, family schedules, and draft-sampling assumptions.

## Pilot review and policy correction (2026-10-17)
- The original 24,000-run pilot is preserved under `pilot/`; its generated Wilson-interval analysis is `REPORT.md` (generator: `model/expertise_report.py`). The full repository suite passed 187 tests.
- Review found original ordinary-card and nested-draft policy sometimes preferred Expertise over an available Amplifier, conflicting with the user instruction to acquire Amplifier whenever offered. Corrected both to prioritize unowned Amplifier-granting Doctrines. Started a fresh 24,000-run matched-seed pilot under `pilot-amplifier-first/` for the corrected policy. Do not substitute original results for corrected-policy results.
- Source evidence confirms the standard D4→D5→D6 *efficiency* chain but does not yet establish that these are the exact localized *Super Weapon Expertise I/II/III* labels for CB14. Treat that naming as provisional.
- No commits/pushes; unrelated working-tree files left untouched.

## Objective correction: D7, not D6 (2026-10-17)
- User clarified target is the final D7 Doctrine. Verified `tb_active_nodes` unlocks D7 after **D3 OR D6**, with both independent three-step branches.
- Simulator now tracks target D1–D7, D7 acquisition wave and route (`cost`, `efficiency`, `both`), and checkpoints for all seven nodes. Target-card and nested-draft scoring prioritizes an available D7, then the branch with the most progress (cost branch wins ties), while keeping unowned Amplifier-granting Doctrines first.
- The original `pilot/` and `pilot-amplifier-first/` outputs target D6 and must not be used as D7 success rates. New 24,000-run experiment is under `pilot-d7/`; no costs were modeled.
- Nine dedicated tests and 189 full-suite tests pass. No commits or pushes.

## Final D7 pilot checkpoint (2026-10-17)
- Completed 24,000 conditional runs in `pilot-d7/` (1,000 seeds × 6 policies × 2 commanders × 2 Blueprint modes). `REPORT.md` contains D7 acquisition rates, 95% Wilson sampling intervals, unlock-route counts, Amplifier/Attenuator observations and model limitations.
- Key isolated outcomes: guaranteed Blueprint 86.5% baseline / 80.9% Eleonor; modeled Blueprint 16.8% baseline / 60.6% Eleonor. These are **conditional simulator outputs**, not validated game odds.
- Amplifier-first selection, D7 OR-gate, and tie-breaking toward the cost branch are explicit experimental policies. The target's exact localized D7 label, ordinary Doctrine side effects, same-wave construction timing, and Eleanor special-draft sampling require additional fidelity checks.
- Earlier `pilot/` and `pilot-amplifier-first/` datasets are retained as historical D6-focused experiments and must not be reported as D7 acquisition.
