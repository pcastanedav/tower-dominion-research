# Strategy Conclusions to Date

These are mechanics-derived conclusions, not a claim that every run should be played identically.

## Pool engineering is a real strategic layer

A Blueprint and its placed building are separate decisions. Acquiring a Blueprint broadens what can be built; **placing** a doctrine-bearing building can admit its building-Doctrine progression into future Doctrine lotteries.

A fresh default T1 building family normally introduces two 3.00-ticket opening doctrines = **6.00 tickets** of competition. Therefore:

> Every additional doctrine-bearing building family should justify entering your reward pool.

Combat diversity and Doctrine-family diversity are not identical. Doctrine-free buildings can add capabilities without opening a standard building-Doctrine family.

## Concentrate, progress, diversify

When deliberately hunting a particular building D7, unrelated building families compete against every progression step required to reach that D7. Their effect therefore compounds across the sequence rather than merely reducing one isolated roll.

The emerging advanced pattern is:

**Concentrate -> progress -> diversify.**

If another doctrine-bearing family is not needed yet, delaying its placement until after the desired Doctrine progression has advanced can materially improve the hunt.

Stateful 5,000-run Lions simulations reinforce this effect. With only the desired family active, the modeled D7 completion rate is 29.00% by Wave 20 and 69.38% by Wave 35. With five unrelated families active from the start, it falls to 7.38% and 30.10%. In the timing experiment, introducing three unrelated families early (Waves 1/4/9) produced 14.86% / 45.32%, while delaying them to Waves 10/15/20 produced 24.54% / 57.92%. These are simulation results, not exact closed-form probabilities.

## Cleanup is useful but more complicated than simple depletion

For a truly independent `copyAllowed=1` ordinary T1 doctrine, taking it removes 1.00 ticket from subsequent pools. This creates a cumulative advantage. However, the newly identified ordinary-doctrine links and reward-generating effects mean this rule cannot be applied indiscriminately.

A selected doctrine may instead:
- expose a linked successor;
- increase future T2 Doctrine weights;
- increase building-Doctrine weights;
- immediately create one or more additional Doctrine drafts.

Therefore the correct general rule is:

> Evaluate a Doctrine by both its immediate effect and the state transition it causes in the future reward pool.

## Building removal is conditional cleanup

Selling every copy of a building can remove untouched building-gated opening doctrines. Once a progression branch has started, owned-doctrine prerequisites can keep successors alive even after the building is gone.

Thus early removal can clean a family more completely than late removal, but it sacrifices resources and combat infrastructure.

## Tander, Magel, and Eleanor change different dimensions

- **Tander** increases normal card count: more samples of all normal reward categories.
- **Magel** creates recurring Doctrine-only drafts: many more samples from the Doctrine lottery without inherently improving its composition.
- **Eleanor** creates recurring Blueprint-only drafts and also increases T2/T3 Blueprint likelihood.

For Magel in particular, a clean Doctrine pool extracts more value from the increased number of Doctrine samples. “More Doctrine drafts” is not the same thing as “better Doctrine odds within each draft.”

In the refreshed stateful 5,000-run desired-family-only experiment, modeled W20/W35 D7 completion was 29.00%/69.38% for the standard six-candidate case, 50.92%/88.92% for Tander, and 84.82%/98.94% for Magel. Magel's absolute figures remain provisional because same-wave ordering and exact special-draft proposal cleanup are unresolved; the comparison is retained as simulation evidence rather than verified game odds.

## Focused Militarization is a nonlinear ordinary doctrine

Focused Militarization is strategically unusual because it combines an immediate Doctrine draft with a persistent increase to building-Doctrine likelihood. Its value therefore depends strongly on what building-Doctrine families are already active when it is taken.

If the active families are deliberately concentrated around a desired progression, increased building-Doctrine weight can be beneficial. If many unrelated families are active, the same global shift can amplify their competition as well.

## Ticket framing

Useful player-facing baseline:
- ordinary T1 doctrine: **1.00 ticket**;
- default eligible T1 building doctrine: **3.00 tickets**;
- fresh building family with two opening nodes: **6.00 tickets**.

Tickets are lottery weights, not percentages. The probability of a target is its tickets divided by the total currently eligible tickets.

Fractional later-tier weights matter exactly: for example a Wave-35 T2 doctrine has 0.58 base ticket before other modifiers.
