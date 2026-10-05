# Slice 01 — Ordinary-doctrine dependency graph

Status: active

## Objective
Reconstruct the complete ordinary D1/D2/D3 dependency graph from the current build, including prerequisite/successor chains, branches, OR dependencies, and inverted restrictions.

## Starting state
- Durable docs identify 118 ordinary D1/D2/D3 doctrines, but warn they are not independent terminal items.
- Existing evolving-run simulations use an incomplete independent-depletion approximation.
- Repository was clean on main tracking origin/main at slice start.
- Current direct execution of model/test_model.py runs 21 tests successfully; README separately records an earlier 50/50 baseline before linked-doctrine discoveries.

## Completion condition
Produce a reproducible dependency mapping from current-build evidence, classify dependency semantics, update durable mechanics/open-question documentation, and perform consistency checks sufficient to checkpoint the finding.

## Next action
Locate the current-build SkillData/dependency representation in ISIL and mapping artifacts, then reconstruct and cross-check all ordinary doctrine links.

## Result
Complete. Parsed all 118 ordinary D1/D2/D3 SkillData assets directly from the current build's resources.assets.

Findings:
- 0 ByOwnedSkillType restrictions.
- 0 reversed restrictions.
- Therefore 0 ordinary-to-ordinary prerequisite/successor edges.
- D1_43 is the sole non-faction placement dependency: AND requires CB19 placed.
- Faction OR restrictions exist as expected and account for faction-specific fresh pools.

This invalidates the prior provisional claim that ordinary doctrines form prerequisite/successor chains. Nonlinear ordinary-doctrine behavior instead comes from effects that alter reward weights or generate rewards.

## Verification
- Reproducible extractor added at tools/extract_ordinary_doctrines.py.
- Generated 118-row maps/ordinary-doctrines.json.
- Count matches the previously verified ordinary catalog total of 118.
- Serialized restriction semantics cross-checked against SkillData.IsAvailableAnd/IsAvailableOr and BundleRestrictionData.IsMatching ISIL.

Status: complete.
Next: Slice 02 — reward/weight-changing ordinary doctrines.
