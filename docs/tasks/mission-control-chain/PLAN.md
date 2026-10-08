# Mission Control Chain — Comparative Analysis

## Outcome
Measure how quickly and reliably valid Tower Dominion commander/faction categories establish and develop a Mission Control (MC) chain through Wave 60, distinguishing Blueprint access, inventory, construction, amplifier decisions, doctrine pollution, and chain propagation. Additional strategic value of chains is deliberately deferred.

## Slices
1. **Mechanics and eligibility inventory — active.** Verify Mission Control IDs, blueprint availability, 1A behavior, chain draft triggers and limits, Red reward duplication, Tander cards, Eleanor modifiers, and Amplifier mechanics; document unknowns.
2. **State and policy specification — pending.** Define MC in-hand/built state, first mandatory Amplifier, conditional second, doctrine pollution, finite cascading chain, threshold sensitivity, and valid faction/commander combinations.
3. **Fixed-state probabilities and tests — pending.** Validate weighted Blueprint selector and special drafts against inspected game behavior.
4. **Wave-60 simulator and tests — pending.** Implement acquisition/chain transitions and baseline comparisons, explicitly separating assumptions from verified rules.
5. **Experiments and interpretation — pending.** Report first MC timing, chain threshold rates, inventory distributions and sensitivity through Wave 60; defer unmodeled chain benefits.

## Constraints
- Do not treat Red as additional candidate positions: selected reinforcement Blueprints give two copies.
- Tander adds one normal reinforcement card (3 to 4 cards).
- Eleanor receives a periodic choose-1-among-3 Blueprint draft and additive T2/T3 Blueprint rarity adjustment; the localized +20% is approximate wording, not an exact probability.
- The first Amplifier targets Mission Control; the second depends on whether the chain is established.
- User working assumption: 1A acquired/applied same wave; after Wave 40, qualifying MC acquisition generates two immediate choose-1-among-5 drafts, with MC chosen when offered. Confirm trigger/finite limits before numeric claims.
- MC inventory in hand plus built is a chain maturity indicator, not proof of infinite propagation. Threshold is configurable.
- Respect existing active exact-doctrine-probability Slice 2 blocker; this is a separate task, not a claim that blocker is resolved.
- Do not push without explicit request.
