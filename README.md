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

## Public and AI-assisted use

Start with [`AGENTS.md`](AGENTS.md) if you are using an AI assistant, or [`docs/AI_GUIDE.md`](docs/AI_GUIDE.md) for a guided chat workflow. [`docs/GAME_KNOWLEDGE_INDEX.md`](docs/GAME_KNOWLEDGE_INDEX.md) links the mechanics, strategy, datasets, experiments, and evidence gaps. The existing `maps/*.json` datasets can be read without extracting game assets; see [`docs/EXTRACTION_GUIDE.md`](docs/EXTRACTION_GUIDE.md) for optional local extraction.

A public GitHub link lets a chat assistant read accessible files, but does not automatically give it the ability to execute code or inspect a local game installation. All findings are scoped to inspected builds and their stated assumptions. The project is independent and unofficial.

To run a reusable experiment locally, use `python tools/mc_experiment.py presets` and follow [`docs/tasks/mission-control-chain/EXPERIMENT-SPECIFICATION.md`](docs/tasks/mission-control-chain/EXPERIMENT-SPECIFICATION.md).

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

Run the current test suite with `python -m unittest discover -s model -p "test_*.py" -q`. The suite evolves as research and experiment tools are added; avoid relying on historical test counts.

The evolving Doctrine model now uses real ordinary doctrine IDs and current-build faction/placement eligibility. Verified Doctrine-side state transitions are implemented for D1_19 Military Academy (+6 T2 weight), D2_06 Strict Obedience (two choose-1-among-3 drafts), and D2_40 Focused Militarization (+4 building-Doctrine multiplier before its choose-1-among-2 draft).

## Terminology

Internally, all reward weights remain exact integers. For player-facing explanations this project uses **tickets**, where **100 raw weight = 1.00 ticket**. Tickets are weighted-lottery entries, not percentage points.

The term **Frontier** is reserved for Tower Dominion's actual Frontier concept and is not used as a generic name for active/eligible progression nodes.
