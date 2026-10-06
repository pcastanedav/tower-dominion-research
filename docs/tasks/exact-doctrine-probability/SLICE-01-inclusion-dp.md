# Slice 01 — Exact inclusion DP

Status: complete

## Objective
Compute exact probability that at least one target identity appears in k sequential weighted draws without replacement from a fixed Doctrine pool.

## Completion condition
Implementation matches brute-force enumeration on small weighted pools, handles k=0/empty targets, and is regression-tested.

## Result
Added exact_target_inclusion(pool, k, targets), an exact DP over target-free weighted-without-replacement paths.

## Verification
Regression coverage includes zero draws, empty targets, single-draw ratio, explicit two-draw weighted enumeration, multiple targets, and full-pool guarantee. Full discovered suite: 60/60 passing.
