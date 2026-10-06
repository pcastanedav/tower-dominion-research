# Tower Dominion Reinforcement Analysis

Independent reverse-engineering and probability model for **Tower Dominion**, focused on reinforcement generation, Blueprint and Doctrine selection, building-doctrine progression, and the strategic consequences of changing the reward pool during a run.

This repository deliberately reconstructs the game mechanics from the installed build before comparing against prior player models. Generated decompilation output and local Python environments are kept outside Git.

## Current source build

Source hashes are recorded in `maps/source-sha256.txt`.

Observed installed build characteristics during this analysis:
- Unity 2022.3.62.
- Current IL2CPP metadata version 31.
- `GameAssembly.dll`: `8d231ba6042414bdb050b8f13ea5e0fe3c6efd46add0e912381ab42a1dc5711a`.
- `global-metadata.dat`: `884ba0045d3734daa64ce15f60bbe4d25494c2eeda2c3ba95540c4d40c18e2e1`.

## Repository layout

- `docs/MECHANICS.md` — verified mechanics and exact values.
- `docs/STRATEGY.md` — conclusions and player-facing heuristics supported by the mechanics.
- `docs/OPEN_QUESTIONS.md` — unresolved work and important model caveats.
- `docs/WORK_PROCEDURE.md` — required task/slice workflow, resumability, `progress <n>` semantics, and checkpoint procedure.
- `model/reinforcement_model.py` — independent executable model.
- `model/test_model.py` — model tests.
- `model/*_tmp.py` — exploratory simulations retained for reproducibility; results using the old independent-ordinary-doctrine approximation are explicitly provisional.
- `maps/` — compact mapping/source identity data.

## Model status

The current executable test suite passes **55/55 tests**. A misplaced early unittest.main() previously made direct execution report only 21 tests even though discovery contained 50; the harness now runs the complete suite directly.

The evolving Doctrine model now uses real ordinary doctrine IDs and current-build faction/placement eligibility. Verified Doctrine-side state transitions are implemented for D1_19 Military Academy (+6 T2 weight), D2_06 Strict Obedience (two choose-1-among-3 drafts), and D2_40 Focused Militarization (+4 building-Doctrine multiplier before its choose-1-among-2 draft).

## Terminology

Internally, all reward weights remain exact integers. For player-facing explanations this project uses **tickets**, where **100 raw weight = 1.00 ticket**. Tickets are weighted-lottery entries, not percentage points.

The term **Frontier** is reserved for Tower Dominion's actual Frontier concept and is not used as a generic name for active/eligible progression nodes.
