# Agent entry point — Tower Dominion Research

This repository studies Tower Dominion using extracted game data, inspected game behavior, independent probability models, and simulations. It is not an official game project. **Read `docs/AI_GUIDE.md` before making claims or running experiments.**

## Routing
- Mechanics and exact weights: `docs/MECHANICS.md`
- Player-facing strategy: `docs/STRATEGY.md`
- Research status and limitations: `docs/OPEN_QUESTIONS.md`
- Topic and file map: `docs/GAME_KNOWLEDGE_INDEX.md`
- Data extraction and local setup: `docs/EXTRACTION_GUIDE.md`
- Experiment specification and execution: `docs/tasks/mission-control-chain/EXPERIMENT-SPECIFICATION.md`
- Work and change protocol: `docs/WORK_PROCEDURE.md`

## Evidence rules
1. Distinguish game-code/asset observations, exact mathematics, conditional simulations, and hypotheses. Cite repository paths and, where practical, headings.
2. State source-build scope using `maps/source-sha256.txt`; do not claim findings apply to every patch.
3. Never call modeled frequencies calibrated in-game odds, or treat Blueprint ownership as constructed buildings or combat survival.
4. Do not invent missing Blueprint/Doctrine eligibility, extraction results, or game rules. Consult `docs/OPEN_QUESTIONS.md` when uncertain.
5. For simulation work, discover supported parameters through `python tools/mc_agent_interface.py capabilities`, then validate and preview before executing. Use a fresh output directory. No changes to published results.
6. Do not commit, push, publish, or modify unrelated files without the user's authorization.

## Remote chat vs local clone
Public GitHub readers can answer documented questions using Markdown and `maps/*.json`; running models or extracting assets requires an execution environment and, for extraction, user-supplied installed game files. A GitHub URL alone does not grant a chat assistant terminal access.
