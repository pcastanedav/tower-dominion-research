# Guide for AI assistants and chat-based readers

## Start here
This is an independent, build-scoped research repository for Tower Dominion. Read `AGENTS.md` for operating rules and `docs/GAME_KNOWLEDGE_INDEX.md` for a map of sources. Read the relevant source file before answering; the README is an introduction, not a complete mechanics reference.

## Recommended question workflow
1. Identify the system: reinforcement, Blueprint, Doctrine, commander/faction, Mission Control, or experiment.
2. Navigate via `docs/GAME_KNOWLEDGE_INDEX.md` and inspect `docs/MECHANICS.md` for verified mechanics. For player decisions also consult `docs/STRATEGY.md`.
3. Check `docs/OPEN_QUESTIONS.md` for unresolved mechanics and model caveats.
4. Answer with explicit source paths/headings and the appropriate evidence label: **observed in inspected build**, **mathematically derived**, **conditional simulation**, or **unverified**.
5. If a user requests new results, do not imply that reading GitHub executed a simulation. Offer a reproducible spec/command or execute only when local tools are actually available.

## Data already available without game extraction
- `maps/blueprints.json`: extracted Blueprint records (serialized fields; not proof of all runtime eligibility).
- `maps/ordinary-doctrines.json`: extracted ordinary Doctrine records, restrictions and effect links (not complete runtime behavior).
- `maps/source-sha256.txt`: identity of inspected binaries/metadata.
- `docs/MECHANICS.md`, `docs/STRATEGY.md`: written discoveries and implications.
- `docs/tasks/mission-control-chain/`: specialized studies and reports. Different reports may represent different model versions or assumptions; do not merge estimates indiscriminately.

## Experiment workflow (requires Python and a local checkout)
```bash
python tools/mc_agent_interface.py capabilities
python tools/mc_experiment.py presets
python tools/mc_experiment.py init quick-comparison --config my-experiment.json
python tools/mc_experiment.py validate --config my-experiment.json
python tools/mc_experiment.py preview --config my-experiment.json
python tools/mc_experiment.py run --config my-experiment.json --output my-new-results
```
Review the JSON spec before running. `run` writes verified results, Markdown, PDF and chart data by default. Existing output directories are not overwritten. The detailed contract is `docs/tasks/mission-control-chain/EXPERIMENT-SPECIFICATION.md`.

## Good prompts for someone sharing a GitHub link
- "Read AGENTS.md and docs/GAME_KNOWLEDGE_INDEX.md in this repository. Explain the reinforcement reward system and cite the exact source files."
- "Using only verified findings from docs/MECHANICS.md, explain the difference between acquiring a Blueprint and constructing its building."
- "Compare the Mission Control strategies in the existing reports, noting assumptions and which comparisons are not equivalent."
- "Read the experiment specification guide and draft a new valid JSON experiment. Do not claim to run it."

## Limitations of GitHub-only chat
A chat assistant may be unable to retrieve every file, especially large datasets and PDFs, and may lack code execution. Link specific Markdown/JSON files or upload them when retrieval is incomplete. A public repository is a readable source, not automatically an installed connector or a remotely executable service.
