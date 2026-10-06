# Slice 04 — Model integration

Status: complete

## Objective
Represent verified ordinary-doctrine eligibility and Doctrine-side reward/weight effects as executable evolving-run state transitions.

## Implemented
- Replaced anonymous ordinary T1/T2/T3 pool identities with real D1/D2/D3 IDs sourced from the verified serialized map.
- Preserved faction counts and Wave-1 denominators exactly: Iron 39/42/26 and 3900; Lions 38/37/24 and 3800; Pargan 34/38/19 and 3400.
- Enforced D1_43's CB19 placement gate.
- Replaced synthetic deployment targets with D1_44/D1_45 and D2_41/D2_42.
- Added DoctrineRunState with owned ordinary/TB doctrines, building-Doctrine multiplier, T2 weight bonus, placed families, and placed towers.
- D1_19 adds +6 to the T2 Doctrine rarity weight.
- D2_06 resolves two sequential choose-1-among-3 Doctrine drafts from current state.
- D2_40 applies +4 to building-Doctrine multiplier before resolving its choose-1-among-2 Doctrine draft.
- Recursive special-draft acquisitions immediately apply their own verified state transitions.
- Commander evolving-run simulation now uses the stateful pool and effect resolution.

## Test-harness correction
Direct execution previously stopped at an early unittest.main(), explaining the observed 21-test result while discovery contained 50 tests. The entry point is now at the end of the file.

## Verification
- Full direct suite: 55/55 passing.
- Historical faction pool counts and Wave-1 denominators preserved.
- D1_43 absent without CB19 and present with CB19.
- Military Academy regression verifies T2 weight 2 -> 8 at Wave 7.
- Focused Militarization regression verifies multiplier 3 -> 7 before its special draft.
- Strict Obedience regression verifies two three-candidate drafts.
- End-to-end commander run sample reaches Focused Militarization state transition (seed 1: multiplier 7).

Next: Slice 05 — refresh cleanup/D7 experiments against the corrected stateful model.
