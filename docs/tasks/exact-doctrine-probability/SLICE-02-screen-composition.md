# Slice 02 — Normal/Tander screen composition

Status: active

## Objective
Compute exact fixed-state probability that a normal reinforcement screen contains at least one target Doctrine by composing the binomial Doctrine-category count with exact weighted-without-replacement identity inclusion.

## Completion condition
Supports standard 6-candidate and Tander 8-candidate screens, agrees with simple analytical boundary cases, and is regression-tested.

## Blocker
The initial exact_target_inclusion DP is mathematically correct but tracks explicit non-target subsets. On a current-build Doctrine pool of roughly 100 identities, composing k up to 6/8 causes combinatorial state explosion and the full regression/snapshot command does not complete in an acceptable time. The attempted run was terminated.

## Evidence
- Slice-01 small-pool exact tests pass.
- Adding exact_screen_target_probability and invoking it on the Lions Wave-12 desired-family pool caused the test process to remain CPU-bound without output across repeated 10-second waits.
- No probability result from that stalled run is being accepted.

## Next diagnostic/action
Replace subset enumeration with a scalable exact formulation that aggregates equivalent weight classes / symmetric identities (or another polynomial-state recurrence) while preserving sequential PPS-without-replacement semantics. Cross-check the replacement against the existing small-pool brute-force DP before resuming screen composition.

Status remains active; do not advance to Slice 03.
