# Tower Dominion — Mission Control Chain Analysis
## Revised editorial draft · 10 October 2026
**Status:** Assembled for editorial review; not final publication.  
**Principal checkpoint:** Wave 63. **Secondary:** Wave 83. **Diagnostic:** Wave 103.  
**Terminology:** Eleonor (correct spelling); Lions of Ravleski (Lions/Red); MC = Mission Control.

> Evidence rule: Results from historical immediate-construction experiments are not pooled with corrected Chain-policy results. Blueprint acquisitions do not establish construction, combat readiness, or survival. Values quoted below are scenario means, not guaranteed outcomes.

# 1. Introduction

## 1.1. What is a Mission Control chain?
A Mission Control (MC) chain is an acquisition strategy that uses Mission Control upgrades to improve access to further Blueprints, including additional Mission Controls. Its 1A upgrade adds two raw rarity-weight points to eligible Tier 2 and Tier 3 Blueprints; this affects competing buildings as well as MC. Its 3A upgrade creates two choose-one-of-five Blueprint drafts. When those drafts yield another MC, the new building can generate further opportunities once constructed and upgraded. This recursive mechanism is the chain.

## 1.2. Why pursue multiple Mission Controls?
The purpose is to generate useful offensive and support building opportunities beyond ordinary reinforcement. MC ownership is an intermediate measure, not the objective in itself. A chain must develop early enough for its acquisitions to contribute to the defense, and its actual value depends on resources, construction space, upgrade timing, and combat effectiveness.

## 1.3. Why Wave 63?
Enemy wave size increases substantially around Waves 63–64, making Wave 63 the principal pre-escalation acquisition checkpoint. Wave 83 tests later acquisition potential, and Wave 103 is a diagnostic extension. The model does not estimate survival at any checkpoint.

## 1.4. Research questions
How quickly does the chain establish? What changes when 3A becomes affordable at Wave 40? How do Natural, Saved Tier I, and Chain strategies compare? How do commanders and factions affect the result? How do Amplifiers and Tier 1 attenuation influence acquisition? How many individual offensive Blueprints, matched two-building sets, and supporting Blueprints are acquired by Waves 63 and 83? How do MC construction and inventory policies affect these outcomes?

# 2. How the simulation works

## 2.1. Monte Carlo approach
Simulated runs draw reinforcement and Blueprint rewards from modeled pools with dynamic rarity weights. The analysis compares repeated seeded runs under specified selection, construction, and upgrade policies. The newer experiments generally use 1,000 seeds per scenario. Results describe the modeled policy, not a random player's decisions or observed survival.

## 2.2. Blueprint acquisition and reinforcement
MC is a Tier 3 Blueprint. Ordinary reinforcement presents three cards of two rewards; Tander receives a fourth card. Selection favors MC and, when relevant, other targeted acquisition opportunities. MC's probability depends on its weight relative to all eligible alternatives. Controlled commander experiments use a common Lions roster; faction experiments use faction-filtered rosters and therefore test a different question.

## 2.3. Mission Control upgrades
Each constructed MC 1A contributes +2 raw rarity weight to eligible Tier 2 and Tier 3 Blueprints. Each 3A supplies two choose-one-of-five Blueprint drafts. The assumption that 3A upgrades can be afforded from Wave 40 isolates acquisition dynamics and is not a claim about real resources. Upgrade effects depend on what has actually been constructed under each policy.

## 2.4. Amplifiers
One Amplifier targeting MC adds +100% to its Blueprint rarity weight (2×); two add +200% total (3×). These are weight multipliers, not probability multipliers. Doctrines D1_45 (Tier I) and D2_42 (Tier II) grant the modeled Amplifiers. A preowned Tier I Doctrine is removed from later reward selection; it does not create a third Amplifier.

## 2.5. Acquisition and construction policies
The historical Natural model generally constructed MCs immediately. The newer Chain strategy uses continuous construction with a 40-MC build target, a three-MC inventory reserve, dynamic acquisition selectivity, and Tier 1-only attenuation. These strategies must not be described as interchangeable. MC owned, MC constructed, and MC held in inventory are separate concepts.

### Interpreting policy comparisons
Natural and Saved Tier I runs prioritize MC acquisition and generally build immediately; Chain runs use a different reward-selection and construction policy. Thus the differences between these conditions are *combined policy outcomes*, not isolated effects of holding inventory, attenuation, or Amplifiers. The all-HV offensive and support metrics below refer to the wider eligible acquisition categories and are not counts of constructed buildings.

## 2.6. Scope and limitations
The model does not resolve combat survival, full resource budgets, buildable space, or defensive placement. Some commander reward timing and mechanics remain provisional. Doctrine-pool exhaustion can produce genuine softlocks; these must be reported, not silently counted as completed runs. Offensive and support metrics track Blueprint acquisitions, not constructed or upgraded defensive assets.

# 3. Establishing a Mission Control chain

## 3.1. First acquisition
The first MC provides the opportunity to activate the 1A rarity effect and, later, 3A drafts. An Amplifier acquired before the first MC can become useful when a target is available. The timing of these early events creates variation between runs.

## 3.2. Before Wave 40
Before 3A availability, growth depends on reinforcement, additional commander opportunities, Doctrines, and already constructed 1A upgrades. Eleonor starts with the rarity-weight equivalent of ten MC 1A bonuses: +20 raw weight to eligible Tier 2 and Tier 3 Blueprints. This grants neither ten physical MCs nor free 3A drafts. Her additional choose-one-of-three Blueprint draft every two waves remains a provisional modeled mechanic.

## 3.3. The Wave 40 transition
At Wave 40, the model permits eligible constructed MCs to use 3A drafts. A draft yielding another MC may enable additional drafts after construction and upgrading, producing a recursive sequence. This is an acquisition-potential assumption, not proof that all buildings can be afforded or placed in a live run.

## 3.4. Recursive growth and inventory
The number of available 3A activations depends on constructed MCs, not simply all acquired MC Blueprints. The Chain policy's reserve and build target change how ownership translates into available upgrades. Consequently, historical immediate-construction growth curves cannot be used as if they describe the current Chain policy.

## 3.5. Amplifiers
Naturally obtained Amplifiers can accelerate MC acquisition by increasing its relative rarity weight. The Saved Tier I condition tests guaranteed early access to D1_45 while preserving natural availability of D2_42. The earlier artificial permanent Amplifier bonus is superseded.

## 3.6. From accumulation to productive acquisition
A productive chain generates opportunities for useful offensive and support Blueprints. The newer policy uses a 40-MC construction target, a three-MC reserve, continuous construction, dynamic selectivity, and Tier 1 attenuation. The effectiveness of this combined strategy should be evaluated by acquisition of target buildings, not solely MC totals. The independent causal contribution of each policy component requires an isolated comparison.

# 4. Faction and commander comparison

## 4.1. Controlled comparison
The controlled commander comparison holds the eligible Lions Blueprint roster constant to distinguish modeled commander acquisition effects. Baseline has no special acquisition bonus. Lions/Red doubles qualifying ordinary reinforcement Blueprint quantities. Eleonor receives the starting +20 raw Tier 2/3 rarity weight plus provisional periodic Blueprint drafts. Tander sees four reinforcement cards instead of three. Magel receives a choose-one-of-three Doctrine draft every other wave; the same-wave ordering remains provisional.

## 4.2. Corrected Chain outcomes
| Scenario | MC owned W63 | MC owned W83 |
|:--|--:|--:|
| Baseline | 13.49 | 29.00 |
| Lions / Red | 28.57 | 53.40 |
| Eleonor | 32.61 | 53.09 |
| Tander | 17.83 | 36.24 |
| Magel | 23.20 | 49.51 |

*Corrected Chain strategy; 1,000 seeds per scenario. Rounded means.*

Eleonor leads the modeled MC ownership mean at Wave 63, while Lions/Red is narrowly ahead by Wave 83. The old conclusion that Lions leads every checkpoint is invalid for these corrected Chain runs. Ranking by MC ownership alone does not determine which commander acquires the most useful offensive and support Blueprints.

## 4.3. Actual faction configurations
The faction experiment uses each faction's eligible roster and its modeled acquisition rules. At Wave 83, Natural versus Chain mean MC ownership is: Iron Dragoons 20.78 versus 27.52; Lions of Ravleski 48.36 versus 53.40; Pargan Assault Group 21.88 versus 28.82. Corresponding offense-plus-support Blueprint acquisitions are Iron 14.65 versus 45.88; Lions 31.03 versus 94.55; Pargan 14.64 versus 46.80. This is **not** a roster-only causal test because Lions' Blueprint quantity bonus is also active.

## 4.4. Interpretation
Commander mechanisms affect different acquisition channels, and their relative value changes with the checkpoint and target metric. Magel's Doctrine drafting can also encounter genuine Doctrine-pool exhaustion. Comparisons must state the roster, policy, and metric being used.

# 5. Wave 63: acquisition and defensive readiness

## 5.1. Why this checkpoint matters
Wave 63 is the last principal measurement before the modeled strategic difficulty escalation around Waves 63–64. Late acquisition cannot retroactively help with this transition.

## 5.2. Chain establishment
Under the corrected Chain policy, mean MC ownership by Wave 63 is 13.49 Baseline, 28.57 Lions/Red, 32.61 Eleonor, 17.83 Tander, and 23.20 Magel. These counts do not specify how many buildings were constructed, upgraded, or combat-ready.

## 5.3. Acquisition thresholds
Thresholds of 5, 10, 20, and 40 MCs are descriptive markers, not established survival requirements. The historical threshold percentages are superseded. The corrected raw Chain experiment gives the following empirical shares (1,000 valid observations per scenario):

| Scenario | ≥5 MC | ≥10 MC | ≥20 MC | ≥40 MC |
|:--|--:|--:|--:|--:|
| Baseline | 83.2% | 57.8% | 21.3% | 3.4% |
| Lions / Red | 93.8% | 85.6% | 63.5% | 28.4% |
| Eleonor | 99.2% | 94.5% | 76.0% | 32.8% |
| Tander | 91.0% | 72.9% | 33.4% | 7.4% |
| Magel | 92.5% | 77.6% | 48.0% | 19.2% |

Eleonor leads all four MC thresholds at Wave 63 under the corrected Chain policy. These thresholds remain descriptive rather than survival requirements.

## 5.4. Offensive Blueprint acquisition
The package experiment separately tracks acquired copies of Slovek Howitzer, Sanction Cannon, Super Heavy Pulse Defense, Rampart Missile Silo, Retribution Position, and (for Lions/Red) Tactical Fortress, alongside the separate Salamander Position reference. These counts are acquisitions, not built defenses.

## 5.5. Matched offensive packages
For a two-building package, complete matched sets equal the smaller acquired count of its two required buildings. This distinguishes balanced combinations from duplicate-heavy totals.

| Package | Eleonor W63 matched sets | Lions/Red W63 matched sets |
|:--|--:|--:|
| Slovek Howitzer + Sanction Cannon | 12.30 | 10.59 |
| Super Heavy Pulse Defense + Rampart Missile Silo | 11.07 | 9.71 |
| Super Heavy Pulse Defense + Retribution Position | 12.29 | 10.48 |

*Package-establishment experiment; means across 1,000 seeds per scenario.* The separate indicator for having acquired at least one of each required building is already near saturation by Wave 83 and is less informative than matched-set counts. In the three paired-package Eleonor and Lions scenarios above, Wave 63 already ranges from 99.5% to 100.0% for this binary indicator; the matched-set measure retains more differentiation.

### Individual building acquisitions in the paired-package scenarios

| Targeted package | Wave | Eleonor: building 1 / building 2 | Lions/Red: building 1 / building 2 |
|:--|--:|:--|:--|
| Slovek Howitzer + Sanction Cannon | 63 | 13.48 / 15.63 | 12.02 / 14.16 |
| Slovek Howitzer + Sanction Cannon | 83 | 20.64 / 23.78 | 21.64 / 24.54 |
| Super Heavy Pulse Defense + Rampart Missile Silo | 63 | 14.91 / 12.16 | 13.11 / 11.35 |
| Super Heavy Pulse Defense + Rampart Missile Silo | 83 | 23.22 / 18.71 | 23.99 / 20.00 |
| Super Heavy Pulse Defense + Retribution Position | 63 | 13.47 / 15.82 | 12.03 / 14.33 |
| Super Heavy Pulse Defense + Retribution Position | 83 | 20.88 / 24.06 | 21.58 / 25.00 |

*Mean Blueprint copies acquired for each specified building; building order matches the package name. Each package/scenario/wave has 1,000 observations. These are separate package-targeting simulations, not simultaneously available totals from one run.*

The Lions-only Super Heavy Pulse Defense + Tactical Fortress experiment produces 9.59 mean matched sets at Wave 63 and 18.27 at Wave 83 (1,000 observations each). For the single-building experiments, Wave 63 mean acquisitions are: Slovek Howitzer, Eleonor 15.08 and Lions 13.32; Sanction Cannon, Eleonor 15.74 and Lions 14.45. By Wave 83, the corresponding means are 23.16 / 24.09 and 23.93 / 24.98, respectively. The Salamander Position experiment is a separate corrected reference rather than one of the 26 package-batch scenarios.

## 5.6. Support acquisitions
Support Blueprint acquisitions should be reported alongside offensive targets because chain productivity is not exhausted by MC ownership. In the corrected Chain comparison, offense-plus-support acquisitions at Wave 63 average 59.07 for Eleonor and 55.35 for Lions/Red. These are aggregate acquisition counts, not a count of functioning defensive packages.

## 5.7. Saved Tier I comparison
The saved-D1_45 condition should be presented as an early-access sensitivity, not an extra Amplifier stacked beyond the two available Doctrines. The corrected Wave 63 mean MC ownership by condition is:

| Scenario | Natural | Saved Tier I | Chain |
|:--|--:|--:|--:|
| Baseline | 10.20 | 11.58 | 13.49 |
| Lions / Red | 23.99 | 27.72 | 28.57 |
| Eleonor | 29.33 | 35.99 | 32.61 |
| Tander | 15.16 | 16.38 | 17.83 |
| Magel | 19.34 | 19.60 | 23.20 |

These conditions are separate strategies. In particular, Saved Tier I exceeds Chain for Eleonor in mean MC ownership at this checkpoint, so the Chain policy must not be characterized as universally superior on MC count.

**Wave 63: acquisition versus construction (Eleonor example)**

| Metric | Natural | Saved Tier I | Chain |
|:--|--:|--:|--:|
| MC Blueprints owned | 29.33 | 35.99 | 32.61 |
| MCs constructed | 29.33 | 35.99 | 31.86 |
| MC Blueprints held | 0.00 | 0.00 | 0.75 |
| Offensive Blueprints acquired (all eligible) | 2.78 | 2.75 | 14.52 |
| Support Blueprints acquired (all eligible) | 13.56 | 14.14 | 44.55 |

*Corrected 1,000-run scenarios; means at Wave 63. Chain's acquisition priorities differ from Natural/Saved Tier I. These categories are not built defenses.*

## 5.8. Interpretation
The evidence supports statements about the availability of defensive-building Blueprints before the escalation, not about actual survival. Acquisition, construction, upgrading, placement, and combat readiness remain distinct stages.

# 6. Late-game growth: Waves 64–103

## 6.1. Wave 83 as the main later checkpoint
Wave 83 is the principal late-game comparison. Wave 103 is retained for diagnostic observation of longer-term accumulation and model behavior, not as a substitute for the Wave 63 objective.

## 6.2. Additional MC ownership
| Scenario | MC W63 | MC W83 | Increase |
|:--|--:|--:|--:|
| Baseline | 13.49 | 29.00 | 15.51 |
| Lions / Red | 28.57 | 53.40 | 24.83 |
| Eleonor | 32.61 | 53.09 | 20.48 |
| Tander | 17.83 | 36.24 | 18.41 |
| Magel | 23.20 | 49.51 | 26.31 |

*Corrected Chain strategy; means across 1,000 runs per scenario.*

## 6.3. Acquisition beyond MC
At Wave 83, corrected Chain offense-plus-support acquisitions average 47.54 Baseline, 94.55 Lions/Red, 89.22 Eleonor, 56.10 Tander, and 62.81 Magel. Thus the ordering for total useful Blueprint acquisitions is not identical to MC ownership.

## 6.4. Matched sets at Wave 83
| Package | Eleonor | Lions / Red |
|:--|--:|--:|
| Slovek Howitzer + Sanction Cannon | 19.27 | 19.72 |
| Super Heavy Pulse Defense + Rampart Missile Silo | 17.61 | 18.39 |
| Super Heavy Pulse Defense + Retribution Position | 19.59 | 19.65 |

*Mean complete matched sets; 1,000 seeds per scenario.*

## 6.5. Reliability and longer-run limits
The corrected Chain experiment gives these Wave 83 empirical shares:

| Scenario | ≥10 MC | ≥20 MC | ≥40 MC |
|:--|--:|--:|--:|
| Baseline | 92.5% | 66.7% | 23.1% |
| Lions / Red | 98.1% | 93.1% | 75.5% |
| Eleonor | 99.9% | 96.1% | 75.2% |
| Tander | 97.4% | 81.4% | 37.8% |
| Magel | 98.5% | 91.5% | 66.3% |

All five scenarios have 1,000 Wave 83 observations. At Wave 103, Chain / Magel has only 996 recorded checkpoint rows from the 1,000 starting seeds, consistent with four runs ending before that checkpoint. Its Wave 103 denominator must therefore be shown as 996, not 1,000. Other Chain scenarios retain 1,000 Wave 103 observations. The package batch has 1,000 observations per scenario at Waves 63 and 83. At Wave 103, Magel has 995 for single Howitzer, 992 for single Cannon, 1,000 for Howitzer + Cannon, 994 for SPHD + Rampart, and 997 for SPHD + Retribution. The corresponding documented Doctrine-pool softlock counts are 5, 8, 0, 6, and 3; their recorded stop waves can include Wave 103, so the number of softlocks and number of missing Wave 103 rows need not be identical. No modeled run should be described as an actual survivor merely because the simulation reached a later checkpoint.

# 7. Amplifier analysis

## 7.1. Weight mechanics
Each MC-targeted Amplifier adds +100% to MC's rarity weight: 1× without Amplifiers, 2× with one, and 3× with two. This is additive stacking of weight modifiers, not multiplication of acquisition probabilities.

## 7.2. Natural versus preowned Tier I
Natural acquisition obtains D1_45 and D2_42 through the modeled reward process. The Saved Tier I condition starts with D1_45 owned, excludes it from future draws, and still permits D2_42. The timing of the first Amplifier affects how many later drafts benefit.

## 7.3. Commander interactions
Magel's additional Doctrine drafts create more opportunities to encounter Amplifier-granting Doctrines. Any claim about the magnitude of this specific mechanism should be distinguished from the aggregate commander comparison; the older 500-run no-Amplifier ablation is historical evidence, not a matched corrected experiment.

## 7.4. Attenuation
Tier 1-only attenuation changes relative Blueprint selection weights without directly multiplying MC's own rarity weight. Amplification and attenuation therefore act through different mechanisms. The Chain policy combines them; an isolated ablation is required to attribute a measured fraction of its advantage to attenuation alone.

## 7.5. Evidence limits
The current report must not reuse the obsolete permanent saved-Amplifier comparison. Controlled zero/one/two-Amplifier and timing experiments would be required to establish their independent causal effects in the corrected model.

# 8. Conclusions

## 8.1. Main findings
The MC chain can generate substantially more Blueprint opportunities, especially once 3A becomes available at Wave 40. Its strategic value is the acquisition of useful offensive and support buildings early enough to matter, rather than the largest possible eventual MC count.

## 8.2. Wave 63 priority
Wave 63 remains the key checkpoint. Corrected Chain results show Eleonor leading mean MC ownership at that wave, while package metrics reveal how the chain translates into acquisition of paired offensive buildings. Neither statistic alone establishes survival.

## 8.3. Strategy effectiveness
Natural, Saved Tier I, and Chain strategies represent different interventions. Their results should be compared under clearly labeled policies and datasets. The newer Chain policy incorporates continuous construction, an inventory reserve, dynamic selectivity, and Tier 1 attenuation; its combined effect must not be attributed to a single component without a controlled test.

## 8.4. Commander and faction implications
Lions/Red narrowly leads Eleonor in Wave 83 MC ownership and produces more offense-plus-support acquisitions at that checkpoint. Eleonor leads Wave 63 MC ownership in the corrected Chain runs. Actual-faction comparisons also incorporate faction-specific Blueprint rosters, so they answer a different question from controlled commander comparisons.

## 8.5. Limitations and future work
The model does not establish combat survival, economic feasibility, buildable placement, or upgrade completion. Provisional reward sequencing, Doctrine exhaustion, and absent mechanics require explicit treatment. Future research should prioritize in-game validation and controlled component ablations rather than tuning results to match anecdotal outcomes.

## 8.6. Final conclusion
A Mission Control chain is best evaluated by **how early it becomes a productive Blueprint-acquisition engine and how effectively it supplies the offensive and support buildings required by the player's strategy**, not simply by the number of Mission Controls accumulated.

# Appendix — Evidence and reproducibility

**Primary corrected datasets:** `commander-salamander-eleanor-corrected-2026-10-10/{raw.csv,results.json}`; `package-establishment-results-2026-10-10/{raw.csv,results.json}`; `faction-establishment-results/{raw.csv,results.json}`; `chain-establishment-results/{raw.csv,results.json}`.

**Experimental references:** `CHAIN-ESTABLISHMENT-2026-10-10.md`, `PACKAGE-ESTABLISHMENT-2026-10-10.md`, `FACTION-ESTABLISHMENT-2026-10-10.md`, `package-establishment-experiment.json`. The package batch contains 26,000 runs across 26 scenarios; the corrected Salamander reference adds 5,000 runs. These are separate experiments, not 31,000 interchangeable observations.

**Historical source:** `SIMULATION-1000-RUNS.json` and the earlier 500-run sensitivity batch. Their results are preserved for provenance but not used as corrected Chain findings.

**Model:** `model/mc_wave60.py` and supporting roster/Doctrine modules. Results depend on the source revision, input rosters, policies, and seed configuration.

**Metrics:** MC owned is not necessarily MC constructed. Offensive and support values count acquired Blueprint copies. Two-building matched sets are `min(required_building_1_count, required_building_2_count)`. The binary “has all required” indicator only records whether at least one of each type has been acquired. Softlocks must be distinguished from completed runs.

**Presentation conventions:** Eleonor is the correct display spelling, including when historical dataset keys use `Eleanor`. Scenario chart colors: Baseline #777777; Lions #D64545; Eleonor #36965C; Tander #3478D4; Magel #9B59B6. Main design: navy #172331, ivory #F4F2EC, gold #D5A34B, slate #26394C, steel gray #6B7885. A4 portrait; searchable text, navigable headings, and carefully reviewed page breaks.

**Verified raw-data checks:** Wave 63 and Wave 83 MC thresholds, Wave 63 Natural/Saved Tier I/Chain means, Wave 103 Chain checkpoint denominators, individual package-building acquisitions, matched-set averages, and package-specific softlock/observation counts were checked against corrected raw.csv and results.json. Final editorial consistency and presentation review remain before PDF publication.
