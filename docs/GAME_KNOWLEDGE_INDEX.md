# Tower Dominion knowledge and evidence index

This is a navigation index, not a claim that every mechanic is completely understood. Use the linked documents for exact statements, conditions, and caveats.

| Topic | Start with | Supporting sources |
|---|---|---|
| Reinforcement screens, category weights, weighted selection | `docs/MECHANICS.md` | `model/reinforcement_model.py`, `model/test_model.py` |
| Blueprint rarity, availability and faction roster | `docs/MECHANICS.md` | `maps/blueprints.json`, `tools/extract_blueprint_roster.py` |
| Ordinary Doctrine eligibility, progression and pool competition | `docs/MECHANICS.md` | `maps/ordinary-doctrines.json`, `tools/extract_ordinary_doctrines.py`, `docs/tasks/ordinary-doctrine-state/` |
| Commander-specific modifiers and uncertain ordering | `docs/MECHANICS.md` | `docs/OPEN_QUESTIONS.md`, `model/` |
| Strategic heuristics and pool engineering | `docs/STRATEGY.md` | `docs/MECHANICS.md` |
| Mission Control acquisition, construction and policies | `docs/tasks/mission-control-chain/ANALYSIS-REPORT.md` | `docs/tasks/mission-control-chain/EXPERIMENT-RUNNER.md`, `docs/tasks/mission-control-chain/EXPERIMENT-SPECIFICATION.md` |
| Exact Doctrine probability research | `docs/tasks/exact-doctrine-probability/PLAN.md` | `docs/tasks/exact-doctrine-probability/` |
| Outstanding evidence gaps | `docs/OPEN_QUESTIONS.md` | individual task plans |
| Source build identity | `maps/source-sha256.txt` | `README.md` |
| How to run or extend research | `docs/AI_GUIDE.md` | `docs/EXTRACTION_GUIDE.md`, `docs/WORK_PROCEDURE.md` |

## Evidence categories
- **Inspected-build observation:** directly traced from inspected game code/assets; subject to build and runtime caveats.
- **Mathematical result:** calculated from stated mechanics/assumptions; distinguish idealized independent draws from full game selection.
- **Conditional model:** output of the repository's independent simulator; not a calibrated gameplay probability, combat or economy simulator.
- **Provisional/unresolved:** a working hypothesis or explicitly incomplete investigation; consult `docs/OPEN_QUESTIONS.md`.

## How to use extracted datasets
`maps/blueprints.json` and `maps/ordinary-doctrines.json` contain machine-readable serialized observations. They are useful for filtering and lookups, but field names and references do not by themselves establish full runtime eligibility, effective weights, or timing. When interpreting a field, inspect the extraction script and corroborating mechanics document. Do not treat a missing record as proof that an object never exists in another game build.

## Research provenance
The repository does not bundle the game's installed binaries or `resources.assets`. Extraction requires a lawful local installation and compatible source files. The inspected-build hashes are recorded in `maps/source-sha256.txt`. Historical experiments can use different assumptions; check the associated experiment config and report before comparing numerical findings.
