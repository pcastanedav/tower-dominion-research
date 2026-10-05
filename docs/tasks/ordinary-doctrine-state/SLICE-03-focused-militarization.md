# Slice 03 — Focused Militarization exact behavior

Status: active

## Objective
Resolve D2_40 Focused Militarization's exact building-Doctrine multiplier delta and whether its immediate two-candidate Doctrine draft observes the updated multiplier.

## Starting evidence
Serialized D2_40 effect order is:
1. DroprateTBDoctrine4
2. SpecialRewardOnDemandDoctrineAmong2

The default global building-Doctrine multiplier is 3.

## Completion condition
Verify the +4 arithmetic and effect application order in current code sufficiently to determine the multiplier visible to the immediate draft, then update durable docs and checkpoint.

## Result
Complete.

Verified:
- DroprateTBDoctrine4 is GameEffectType 67.
- Its serialized math value is float 4.0.
- Default building-Doctrine multiplier 3 therefore becomes 7 after D2_40.
- D2_40 serializes DroprateTBDoctrine4 before SpecialRewardOnDemandDoctrineAmong2.
- Skill.ApplyEffects enumerates SkillData.effects in order and calls GameEffectsService.AddEffect for each before advancing.
- Special reward type 47 is handed to SpecialRewardService, which appends/queues SpecialRewardData and starts/uses its reward-processing coroutine.
- Consequently the +4 multiplier is live before D2_40's immediate Doctrine reward is processed. The two-candidate draft observes multiplier 7.

## Verification
Cross-checked D2_40 raw serialized effect order/value against current-build ISIL for Skill.ApplyEffects, GameEffectsService.AddEffect, and SpecialRewardService.ApplySpecialRewardEffect.

Status: complete.
Next: Slice 04 — model integration.
