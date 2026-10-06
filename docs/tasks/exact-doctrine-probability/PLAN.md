# Exact Doctrine Probability Engine

## Outcome
Add an exact weighted-without-replacement probability engine for Doctrine identity inclusion and use it to replace Monte Carlo where the Doctrine candidate count/pool state is fixed.

## Slices
1. **Exact inclusion DP** — active
   Implement and test exact target-inclusion probability for weighted draws without replacement.
2. **Normal/Tander screen composition** — pending
   Combine exact identity inclusion with the binomial Doctrine-slot count for 6- and 8-candidate normal screens.
3. **Special-draft integration and documentation** — pending
   Apply exact calculations to fixed-state choose-1-among-N Doctrine drafts and update mechanics/strategy tooling.

## Constraints
- Preserve integer weights internally.
- Sampling is sequential weighted without replacement.
- This task computes fixed-state probabilities; evolving-run state transitions remain simulation territory.
- Duplicate-card regeneration is separate and remains unresolved.
