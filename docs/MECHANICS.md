# Verified Mechanics Snapshot

This document records mechanics verified from the installed build and current assets/code unless explicitly marked provisional.

## 1. Normal reinforcement generation

Default reinforcement presentation is **3 cards x 2 items = 6 candidate items**.

Base outer reward-category weights:

| Category | Raw weight | Probability per candidate |
|---|---:|---:|
| Supply | 10 | 10% |
| Recon | 4 | 4% |
| Blueprint | 57 | 57% |
| Doctrine | 29 | 29% |

For six independent category draws before validation/modifiers:
- expected Doctrine candidates: **1.74**;
- expected Blueprint candidates: **3.42**;
- P(at least one Doctrine): **87.18997%**;
- P(at least two Doctrines): **55.79638%**;
- P(at least one Blueprint): **99.37%** approximately;
- P(at least one Blueprint and at least one Doctrine): **86.56%** approximately.

Doctrine-count distribution over six candidate positions:
- 0: 12.8100%
- 1: 31.3936%
- 2: 32.0568%
- 3: 17.4582%
- 4: 5.3481%
- 5: 0.8738%
- 6: 0.0595%

Conditional resource amounts observed in the data/model:
- Supply mean: 139.
- Recon mean: 34.25.

## 2. Candidate identity and card validation

A reward category is selected first. Blueprint and Doctrine identities are then resolved during candidate generation, before the candidates are grouped into cards.

`BundleCardItem.IsEqual` compares reward type, quantity, concrete Blueprint, and concrete Doctrine. Exact duplicate cards are rejected by validation. Proposed Doctrines on a rejected card are removed from proposal state and replacement generation restores the required card count.

An initial Wave-1 Lions-like simulation measured exact duplicate cards at roughly **0.7%** (213/30,000). Exact duplicate-regeneration behavior is not yet fully reproduced in the probability model.

## 3. Blueprint selection

Blueprints are selected directly from a weighted eligible Blueprint pool; the game does not first choose a rarity and then choose within that rarity.

Blueprint rarity base progression:

| Wave | T1 | T2 | T3 |
|---:|---:|---:|---:|
| 1 | 100 | 0 | 0 |
| 10 | 100 | 6 | 1 |
| 20 | 100 | 16 | 11 |
| 35 | 100 | 31 | 26 |

Underlying settings:
- T1: start 100, increment 0/wave.
- T2: start -3, increment +1/wave.
- T3: start -8, increment +1/wave.
- clamp to 0..100 after applicable additions.

Therefore normal T2 Blueprint weight first becomes positive at Wave 5 and T3 at Wave 10 before commander/effect modifiers.

There are 71 Blueprint objects in the inspected data. Thirty-two are normal bundle Blueprints: 12 T1, 10 T2, 10 T3. Owning a normal Blueprint does **not** remove that Blueprint from future reward selection.

## 4. Doctrine selection

Doctrine identity is selected by `SkillService.GetRandomDoctrineData()` from the currently eligible weighted pool.

Eligibility includes skill type, availability restrictions, `availableInBundles`, copy limit, unlock state, and positive rarity weight.

A displayed Doctrine becomes proposed. For `copyAllowed=1`, proposal state prevents the same Doctrine from being selected repeatedly in the same reward construction. Unchosen/rejected proposals are removed; chosen Doctrines become owned/consumed.

### Doctrine rarity progression

| Wave | T1 | T2 | T3 |
|---:|---:|---:|---:|
| 1 | 100 | 0 | 0 |
| 10 | 100 | 8 | 0 |
| 20 | 100 | 28 | 18 |
| 35 | 100 | 58 | 48 |

Settings:
- T1: start 100, increment 0.
- T2: start -10, increment +2/wave.
- T3: start -20, increment +2/wave.

T2 first becomes positive at Wave 7; T3 at Wave 12 before other effects.

Player-facing ticket examples:
- Wave 10: T1 1.00, T2 0.08, T3 0.00 tickets.
- Wave 20: 1.00 / 0.28 / 0.18.
- Wave 35: 1.00 / 0.58 / 0.48.

## 5. Building/TB doctrines

The default global building-doctrine multiplier is **3**. Thus a T1 building Doctrine with rarity weight 100 normally carries raw weight 300 = **3.00 tickets**.

Twenty-one building families have the standard seven-node building-Doctrine structure. A freshly placed eligible family normally exposes two opening nodes, D1 and D4, so at T1/default multiplier it introduces **6.00 tickets** to the Doctrine lottery.

Standard progression:
- D1 -> D2 -> D3
- D4 -> D5 -> D6
- D7 becomes available through completion of D3 **or** D6.

All 147 standard building-Doctrine SkillData entries (21 x 7) use rarity index 1, `copyAllowed=1`, and are bundle-available.

### Placement and removal

Building placement and Doctrine ownership are independent availability mechanisms.

Fresh placed family: D1 + D4 eligible.

If a branch has begun, its successor can remain eligible even after all copies of the building are removed because the successor is gated by the owned predecessor. An untouched opening node, however, disappears when the last qualifying building is removed.

Examples:
- place then remove before taking D1/D4 -> no nodes remain;
- own D1 then remove building -> D2 remains, untouched D4 disappears;
- own D3 then remove -> D7 remains, untouched opposite branch disappears;
- if both branches have started, both successor paths can persist.

Thus selling a building is not guaranteed to erase all of its Doctrine competition.

## 6. Bundle Blueprint families without standard building doctrines

Among the 32 normal bundle Blueprint types, 21 admit a standard building-Doctrine family and 11 do not:

`CB12, F102, F201, F202, F301, F302, SB01, SB02, SB04, SB06, SB07`

Tier distribution among these doctrine-free normal bundle buildings:
- T1: 2
- T2: 3
- T3: 6

These can broaden the combat toolkit without admitting a standard building-Doctrine progression.

## 7. Fresh ordinary-Doctrine pools

There are **118 ordinary D1/D2/D3 doctrines** in the current catalog:
- T1: 46
- T2: 43
- T3: 29

Initial faction-eligible ordinary pools previously reconstructed:
- Iron Dragoons: 39 T1 / 42 T2 / 26 T3 = 107.
- Lions of Ravleski: 38 / 37 / 24 = 99.
- Pargan Assault Group: 34 / 38 / 19 = 91.

These are **fresh-state eligibility snapshots**. They must not be interpreted as 118 independent terminal items: some ordinary doctrines are linked to other ordinary doctrines, and some modify/generate future rewards.

Fresh Lions ordinary ticket totals:
- W1: 38.00
- W7: 38.74
- W10: 40.96
- W20: 52.68
- W35: 70.98

## 8. Weight-modification layers

The reconstructed selection pipeline supports several distinct probability controls and they must not be conflated.

### Building-specific Blueprint/Doctrine weighting

Known targeted modifiers include:
- -500% Blueprint / building-Doctrine effects (Attenuator behavior);
- +100% Blueprint / building-Doctrine effects (Amplifier behavior);
- +10% targeted effects used by Reactive-style mechanics.

The final building-Doctrine weight is conceptually:

`rarity weight x global TB multiplier x item/building-specific modifier`

Percentage modifiers on the item-specific `GameEffectValue` add before the final multiplication. Consequently multiple +10% contributions and a +100% Amplifier combine additively at that layer. For N qualifying +10% contributions:
- without Amplifier: `1 + 0.10N`;
- with Amplifier: `2 + 0.10N`, not `2 * (1 + 0.10N)`.

### Global building-Doctrine multiplier

`GameEffectType 67` changes the global building-Doctrine multiplier. Current assets contain raw +4 and +9 effects. Starting from default 3, reachable arithmetic includes 7, 12, and 16 if both stack. D2_40 Focused Militarization owns the +4 effect and therefore changes the multiplier from 3 to 7 when taken.

### Doctrine reward/rank weighting

There are separate effects for Doctrine reward/rank weighting. Current investigation has confirmed at least:
- a Doctrine reinforcement-item rarity-weight modifier (`GameEffectType 66`);
- T2 Doctrine weighting (`GameEffectType 56`).

Do not treat these as the same operation as the global building-Doctrine multiplier.

## 9. Amplifier and Attenuator

Sanctioned Attenuator and Certified Amplifier are special Blueprints granted by ordinary doctrines rather than ordinary Blueprint bundle rolls.

Ordinary doctrines:
- D1_44: Attenuator Deployment I.
- D1_45: Amplifier Deployment I.
- D2_41: Attenuator Deployment II.
- D2_42: Amplifier Deployment II.

The Tier-II versions are not simple successors of the Tier-I versions; they are independently eligible when their rarity weight permits them. Owning the special Blueprint does not itself suppress the later doctrine.

Attenuator makes the targeted building type's Blueprint and building doctrines unable to appear in rewards. Amplifier doubles the targeted building type's Blueprint and building-Doctrine chances.

## 10. Commander reinforcement exceptions

### Marshal Tander

Tander grants +1 normal reinforcement card:
- standard: 3 cards x 2 = 6 candidates;
- Tander: 4 cards x 2 = 8 candidates.

This changes the number of samples from the same underlying lotteries, not the composition of the Doctrine pool.

For eight category positions with p(Doctrine)=0.29:
- expected Doctrine candidates: **2.32**;
- P(at least one): **93.54246%**;
- P(at least two): **72.44179%**.

### Magel

Current F1H06S01 localization: **“Gain 1 Doctrine among 3 every other wave.”**

The live effect has event-count trigger 2, and the special reward is the three-Doctrine variant. Code tracing shows special Doctrine rewards use the same Doctrine selector machinery, so this is best modeled as a separate all-Doctrine draft from the currently eligible weighted Doctrine pool.

Working rule:
**Every other wave, choose 1 Doctrine among 3 from the same currently eligible weighted Doctrine pool.**

The exact ordering between the normal reinforcement and Magel's special draft on the same wave remains to be conclusively traced. Current model assumes normal reinforcement first, then the special draft.

### Eleanor / F3H08

Current localization identifies:
- **F3H08S01 — Grande Ecole:** “Gain 1 blueprint among 3, every other wave.”
- **F3H08S02 — Meticulous preparations:** “Tier 2 and 3 blueprints are +20% more likely to appear.”

Thus Eleanor has two distinct Blueprint-side effects:
1. a periodic Blueprint-only choose-1-among-3 draft every other wave;
2. increased T2/T3 Blueprint appearance weighting.

**Later research correction (2026-10-10):** The current corrected model represents this as ten MC-1A rarity-weight equivalents, or **+20 raw Tier 2 and +20 raw Tier 3 Blueprint weight** from Wave 1, additive rather than a +20% probability multiplier. This is a model/source-derived correction, not a claim of measured in-game odds. See `docs/tasks/mission-control-chain/CHAIN-ESTABLISHMENT-2026-10-10.md` (Eleanor commander modeling). The extra Blueprint draft timing and sampling still require game-asset verification.

## 11. Newly verified ordinary-Doctrine exceptions

Current English localization/shared-table mapping confirms:

### D1_19 — Military academy
“Tier 2 Doctrines are 6% more likely to appear.”

This is an ordinary T1 doctrine and changes future T2 Doctrine probability.

### D2_06 — Strict obedience
“Gain 1 Doctrine among 3, twice.”

This ordinary T2 doctrine generates **two separate Doctrine drafts**, each choose 1 among 3.

### D2_40 — Focused militarization
“Building doctrines are more likely to appear\nGain 1 Doctrine among 2.”

This ordinary T2 doctrine is a hybrid: it increases the global building-Doctrine multiplier by exactly +4 (default 3 -> 7) and creates an immediate choose-1-among-2 Doctrine draft. Its serialized effect order is the +4 multiplier first, then the special reward. Skill.ApplyEffects applies effects sequentially, while SpecialRewardService queues the reward for processing, so the immediate draft observes the updated multiplier of 7. It is available across factions according to the current investigation.

### TBCB05D7 — Sanction cannon expertise
“Gain 1 Doctrine among 3, 3 times.”

This is a building D7, not an ordinary doctrine. It demonstrates that building-Doctrine progression itself can create further Doctrine drafts.

### FH_05 — Early propaganda
“Gain 1 Doctrine among 2.”

This is not part of the ordinary D1/D2/D3 pool and must be modeled according to its own acquisition path rather than counted as an ordinary doctrine.

These findings invalidate the simplifying assumption that taking every ordinary doctrine simply subtracts its current weight from all subsequent pools.

## 12. Reactive-style targeted weighting

Inspection of adjacency collection shows actual `BuildingEntity` instances are collected, with no obvious family-level deduplication in the inspected path. This is strong evidence that multiple qualifying adjacent buildings can each contribute a +10% modifier even when they belong to the same family. Exact caller-loop proof and geometry limits remain open.

## 13. Selling economics

Removing a doctrine-bearing family can clean untouched opening nodes from the pool, but this has a real cost. Selling returns 80% of the **current building cost**, which can be less than 80% of total Supply invested after upgrades, and destroys combat infrastructure. Therefore “never place it” and “place then sell it” are strategically different operations.

## 14. Ordinary-doctrine availability graph correction

A complete serialized scan of all 118 current-build ordinary `D1_*` / `D2_*` / `D3_*` SkillData assets found **no `ByOwnedSkillType` restrictions** and **no reversed restrictions**. Therefore there is no ordinary-to-ordinary prerequisite/successor dependency graph in the inspected build.

The only non-faction placement dependency among the 118 ordinary doctrines is:
- `D1_43`: AND restriction requiring tower type `CB19` to be placed.

Faction restrictions remain part of ordinary-doctrine eligibility, but they do not create in-run doctrine successor chains.

This corrects the earlier provisional assumption that some ordinary doctrines expose linked ordinary successors. Ordinary doctrines can still cause nonlinear state transitions through reward-generating and weight-changing effects; those effects are separate from availability dependencies.

The reproducible serialized extraction is retained in `tools/extract_ordinary_doctrines.py` and `maps/ordinary-doctrines.json`.

## 15. Ordinary doctrines that change reward state

The complete 118-asset effect-reference scan identifies eight ordinary doctrines with direct reward-generation or reward-weight effects:

- `D1_15` — `SpecialRewardOnDemandBlueprint`: one immediate Blueprint special reward.
- `D1_19` — `DoctrinesTier2Weight6`: +6 to the T2 Doctrine rarity-weight layer.
- `D2_01` — `BlueprintTier2Weight10`: +10 to the T2 Blueprint rarity-weight layer.
- `D2_06` — two references to `SpecialRewardOnDemandDoctrine`: two immediate Doctrine special rewards.
- `D2_10` — two references to `SpecialRewardOnDemandBlueprint`: two immediate Blueprint special rewards.
- `D2_40` — `DroprateTBDoctrine4` followed by `SpecialRewardOnDemandDoctrineAmong2`: +4 to the global building-Doctrine multiplier and one immediate two-candidate Doctrine draft.
- `D2_43` — three references to `SpecialRewardOnDemandBlueprintRandomIrregularPlatform`: three immediate random-irregular-platform Blueprint rewards.
- `D3_11` — `BlueprintTier3Weight5`: +5 to the T3 Blueprint rarity-weight layer.

No other ordinary D1/D2/D3 SkillData asset references a GameEffectData whose identity changes reward weights or creates a special reward. This classification is based on the complete serialized ordinary-doctrine asset set, not a name-selected subset.
