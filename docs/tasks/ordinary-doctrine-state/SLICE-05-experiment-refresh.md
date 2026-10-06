# Slice 05 — Experiment refresh

Status: complete

## Objective
Re-run the cleanup/D7 experiments against the corrected stateful ordinary-Doctrine model and replace provisional absolute probabilities.

## Completion condition
The experiment runners apply verified ordinary state transitions on acquisition; refreshed results are reproducible and documented; strategy conclusions are updated without overstating unresolved Magel ordering.

## Starting caveats
- Magel same-wave normal-vs-special ordering remains provisional.
- Duplicate-card regeneration remains approximate in the broader model.
- This slice refreshes simulation evidence; it does not convert those unresolved mechanics into verified behavior.

## Results (5,000 trials per scenario)
Baseline, no cleanup: desired-only 29.00%/69.38% W20/W35; +1 21.44%/60.58%; +2 16.74%/50.62%; +3 12.74%/42.28%; +4 9.48%/35.54%; +5 7.38%/30.10%.

Cleanup policy: desired-only 34.78%/81.34%; five competitors 8.88%/35.62%.

Commander comparison, no cleanup, desired-only: standard 29.00%/69.38%; Tander 50.92%/88.92%; Magel 84.82%/98.94%. Magel retains its ordering/proposal caveat.

Timing, no cleanup: one early 21.40%/59.06% vs late 26.22%/64.06%; two early 18.00%/52.28% vs late 24.94%/59.56%; three early 14.86%/45.32% vs late 24.54%/57.92%.

## Verification
The runner uses DoctrineRunState/acquire_doctrine so verified ordinary effects mutate same-run state. Full suite: 55/55 passing.
