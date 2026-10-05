# Slice 02 — Reward/weight-changing ordinary doctrines

Status: active

## Objective
Map every ordinary D1/D2/D3 doctrine whose effects directly alter reinforcement/reward probability or generate additional reward drafts, and resolve exact current-build effect identities/counts.

## Starting evidence
The complete 118-asset extraction exposes each doctrine's referenced GameEffectData objects. Candidate reward-state doctrines are D1_15, D1_19, D2_01, D2_06, D2_10, D2_40, D2_43, and D3_11.

## Completion condition
Classify all candidate effects, verify exact multiplicity/target reward where possible from current assets/code, update durable mechanics/open questions, and checkpoint.

## Result
Complete. The exhaustive ordinary-doctrine effect-reference scan found exactly eight reward-state doctrines:
D1_15, D1_19, D2_01, D2_06, D2_10, D2_40, D2_43, D3_11.

Doctrine-side effects:
- D1_19 -> DoctrinesTier2Weight6.
- D2_06 -> SpecialRewardOnDemandDoctrine twice.
- D2_40 -> DroprateTBDoctrine4, then SpecialRewardOnDemandDoctrineAmong2.

Blueprint-side effects:
- D1_15 -> one Blueprint special reward.
- D2_01 -> BlueprintTier2Weight10.
- D2_10 -> two Blueprint special rewards.
- D2_43 -> three random-irregular-platform Blueprint rewards.
- D3_11 -> BlueprintTier3Weight5.

## Verification
All 118 ordinary assets were scanned through the reproducible extraction map. Candidate selection was derived from effect references for the complete set rather than from known doctrine IDs.

Status: complete.
Next: Slice 03 — Focused Militarization exact behavior.
