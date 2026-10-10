# Generalized Experiment Platform — Implementation Plan

Status: approved for incremental implementation; baseline 2026-10-10.

## Objective
Allow an agent first, and later a standalone program, to specify, validate, execute, analyze, and report reproducible Tower Dominion experiments **without experiment-specific Python**. Retain the existing `simulate_run` model and `tools/run_mc_experiment.py` interface. Do not conflate conditional model outputs with calibrated game probabilities or combat outcomes.

## Current baseline
- JSON runner: trials, seed range, horizon, checkpoints, defaults, scenarios with `WaveConfig` overrides, pairwise comparisons.
- Outputs: per-seed checkpoint `raw.csv`, aggregated `results.json` with observed denominators, paired statistics, softlock data.
- Supported packages are hardcoded in `model/mc_packages.py`; metrics are fixed in the runner. Existing PDF renderer reads a hand-edited report rather than experiment results.
- Config validation is partial; some combinations alter multiple behaviors (e.g. `mc_reserve_target=0`), and statistical comparisons can have divergent RNG paths.
- Existing experiments and published report must remain reproducible and untouched during migration.

## Architecture
Experiment intent (versioned declarative spec) → validation and scenario expansion → existing simulator adapter → canonical observations and statistics → standard report model → Markdown/PDF renderer. Agent and standalone interfaces consume the same contract; neither owns simulation rules or statistical interpretation.

## Implementation slices and gates

### Slice 1 — Formal specification and validation
- Introduce a versioned experiment specification with explicit required fields, supported parameters, enumerations, names, comparison references, and actionable diagnostics.
- Resolve defaults and overrides into an inspectable scenario matrix before execution. Distinguish structural validation from simulation-domain constraints and warn about known confounders/assumptions.
- Preserve existing JSON inputs and CLI behavior; migration should be additive, with explicit compatibility tests against Experiment A and A8.
- **Gate:** dry-run resolution of existing experiment configurations matches current effective `WaveConfig` values; invalid configurations fail before any output is written.

### Slice 2 — Declarative parameter sweeps
- Add bounded Cartesian grids and one-factor-at-a-time variations with stable scenario names, deterministic expansion, explicit comparison baselines, and scenario-count previews.
- Define collision/override semantics and a safety limit for accidental large runs.
- **Gate:** recreate Experiment A scenario matrix using a declarative spec, without experiment-specific Python, and verify resolved scenarios.

### Slice 3 — Metric and comparison registry
- Give metrics stable identifiers, units, descriptions, provenance, applicability, and aggregation rules; distinguish acquired copies, constructed buildings, rates, and censoring.
- Support selected metrics and derived metrics through a safe, constrained expression vocabulary (no arbitrary executable code); paired and unpaired comparison policies must be explicit.
- Preserve historical metrics and results structure or version changes deliberately.
- **Gate:** reproduce Experiment A numerical outputs and denominators to defined tolerance.

### Slice 4 — Run lifecycle and provenance
- Record fully resolved spec, source revision, model/schema version, seeds, execution environment, timestamps, success/failure status, and output checksums.
- Handle interrupted/partial runs safely; never mistake partial `raw.csv` for a finished result.
- **Gate:** reproducibility and interruption tests, with no silent overwrite of published data.

### Slice 5 — Standard Markdown report
- Build a report model directly from results: question, methods, assumptions, scenario matrix, sample sizes, metrics, results, uncertainty, softlocks/censoring, interpretation boundaries, provenance.
- Separate mechanically generated findings from optional agent-authored commentary.
- **Gate:** render Experiment A as a useful complete report without hand-editing or bespoke experiment scripts.

### Slice 6 — Charts and PDF
- Render consistent figures and an accessible PDF from the same report model; preserve chart source data and label denominators and units.
- **Gate:** Markdown/PDF numerical agreement and legible multi-page output.

### Slice 7 — Agent-facing interface
- Expose capabilities, schema, validation, previews, execution, and reports through a stable machine-readable interface; no agent dependency in core logic.
- **Gate:** an agent can author and run a new supported experiment without reading simulator internals.

### Slice 8 — Standalone interface
- Provide CLI/API workflow for human or programmatic use, with presets and reusable reports, on the same validated specification.
- **Gate:** complete experiment lifecycle without an agent or custom Python.

## Cross-cutting constraints
- Prefer small, testable slices; verify existing unit tests after each slice.
- Never silently change game assumptions or retroactively rewrite published report findings.
- Keep model limitations visible: uncalibrated probabilities, no combat-survival model, conditional eligibility, RNG divergence between paired seeds, genuine Doctrine-exhaustion softlocks.
- New arbitrary package composition and configurable Amplifier counts are **model capability extensions**, not automatically implied by generalizing the runner; track as separate requirements with explicit validation.
- Before each implementation slice, inspect the current repository version. Commit and push only on user request.

## Immediate next action
Implement Slice 1 in a compatibility-preserving manner: schema/validator, scenario resolution, dry-run preview, and tests. Do not start Slice 2 until Slice 1 gate passes.
