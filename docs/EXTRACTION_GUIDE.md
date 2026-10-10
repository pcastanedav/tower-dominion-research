# Extracting game data from a local Tower Dominion installation

## Scope
The repository provides two asset extraction utilities for inspected Unity serialized data. Extraction is optional for reading the existing JSON datasets and is **not** necessary for running the independent simulation. It is required when you want to inspect a different installed build or re-extract raw asset records.

## Prerequisites
- A local, legally obtained Tower Dominion installation containing the relevant Unity `resources.assets` file.
- Python 3 and the `UnityPy` package in an isolated environment.
- Enough free disk space for your own extracted outputs.
- The installed game version may differ from the source build identified by `maps/source-sha256.txt`; parsers assume layouts discovered in that build.

The game assets are not bundled here. Locate the `resources.assets` in your own installation; the exact location varies by operating system and installation layout. Do not upload copyrighted game binaries or private local paths into the public repository.

## Setup and commands
From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install UnityPy
python tools/extract_blueprint_roster.py /path/to/resources.assets -o /tmp/tower-blueprints.json
python tools/extract_ordinary_doctrines.py /path/to/resources.assets -o /tmp/tower-doctrines.json
```

On Windows activate the virtual environment with the platform-specific command. `UnityPy` is a third-party dependency; the commands above are a basic starting point, not a pinned reproducible environment. Review extraction output before comparing or replacing tracked datasets.

## Output and interpretation
- Blueprint extraction (`tools/extract_blueprint_roster.py`) emits records including code, asset path ID, GUID, tower, faction, cost, rarity index, and `available_in_bundles`.
- Ordinary Doctrine extraction (`tools/extract_ordinary_doctrines.py`) emits codes, GUIDs, rarity indices, effects and serialized AND/OR restrictions.
- These are serialized fields. Neither script proves full runtime eligibility, reward probabilities, or game state transitions. Refer to `docs/MECHANICS.md` for inspected behavior and `docs/OPEN_QUESTIONS.md` for unresolved interactions.
- The scripts depend on binary layout offsets and can return incomplete or misleading output if the game updates. Empty output is not evidence that the game contains no records.

## Reproducibility and safety
Record the build identity and SHA-256 hashes of inspected inputs. Compare them to `maps/source-sha256.txt` before interpreting differences. Keep generated game assets, decompilation output, and local virtual environments out of Git. Avoid modifying published `maps/*.json` until changes have been reviewed, explained, and tested. `isil/` is intentionally excluded from version control; its local contents are not part of the public clone.

## What this does not cover yet
This guide does not reproduce the complete IL2CPP disassembly/decompilation and runtime call-chain investigation workflow used to verify every game mechanic. That deeper reverse-engineering workflow requires separate documentation, compatible tools, and validation against the exact inspected build. Do not describe these two asset scripts as a complete extraction or game-analysis pipeline.
