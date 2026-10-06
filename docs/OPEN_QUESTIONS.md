# Open Questions and Model Caveats

## Highest priority


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

The D7 experiments have been refreshed against the stateful ordinary-Doctrine model at 5,000 trials per scenario. Their results are valid simulation outputs under the documented model assumptions, but they are not exact game probabilities while duplicate-card regeneration and some commander ordering/proposal details remain unresolved.

The qualitative result that unrelated doctrine-bearing families create persistent competition remains supported by both verified building-Doctrine eligibility/weight mechanics and the refreshed simulations.
