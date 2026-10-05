# Open Questions and Model Caveats

## Highest priority

1. Reconstruct the complete **ordinary-doctrine dependency graph** from the current build. Identify every prerequisite/successor chain, branch, OR dependency, and inverted restriction.
2. Map all ordinary doctrines that change reward probability or generate rewards, including exact live effects for:
   - D1_19 Military academy;
   - D2_06 Strict obedience;
   - D2_40 Focused militarization;
   - any additional T2/T3 Doctrine-weight modifiers.
3. Resolve Focused Militarization's exact building-Doctrine multiplier delta and whether its immediate draft observes the new multiplier before drawing.
4. Integrate linked ordinary doctrines and draft-generating doctrines into the evolving-run model and add regression tests without breaking the existing 50-test baseline.
5. Re-run cleanup and D7 experiments. Existing absolute probabilities that assume independent ordinary-doctrine depletion are provisional.

## Eleanor

- Trace F3H08S02 live effect arithmetic. Determine whether “T2 and T3 blueprints are +20% more likely” is raw addition, percentage modification, or another rarity-weight operation.
- Compute exact Wave-2 and later T2/T3 Blueprint weights/odds.
- Confirm that Grande Ecole's Blueprint-only drafts use the same weighted Blueprint selector and therefore inherit Meticulous Preparations.
- Confirm same-wave ordering if both a normal reinforcement and special Blueprint draft occur.

## Magel

- Prove exact ordering of normal reinforcement vs special Doctrine draft on the same wave.
- Confirm event target 2 mapping/activation timing sufficiently to state exact wave schedule without caveat.
- Finish exact proposal cleanup behavior for unchosen special-draft doctrines.

## Probability engine

- Implement exact weighted-without-replacement target-inclusion DP for Doctrine screens (normal 6-candidate, Tander 8-candidate, and special drafts).
- Reproduce duplicate-card rejection/regeneration exactly rather than approximating it.

## Reactive Pit / targeted modifiers

- Prove caller loop applies one +10% contribution per adjacent qualifying BuildingEntity and no downstream deduplication occurs.
- Determine exact geometry/max adjacency and removal/reversion behavior.
- Confirm Attenuator interactions with positive targeted modifiers.

## Deferred special cases

- Denshikova / The Stars Call exact current first-upgrade effect ownership/timing.
- Xeno Extractor pseudo-reinforcement rewards.
- Blueprint-only special drafts beyond those needed for Eleanor/general classification.

## Important simulation caveat

Temporary D7 experiments currently in `model/*_tmp.py` established strong directional effects for family concentration, delayed diversification, Tander, and Magel. Their **absolute completion probabilities are not authoritative** until ordinary linked doctrines and reward-generating doctrines are represented.

The qualitative result that unrelated doctrine-bearing families create persistent competition remains supported by the verified building-Doctrine eligibility/weight mechanics.
