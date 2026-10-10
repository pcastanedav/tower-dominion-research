# MC Experiment Specification — Version 1

The runner accepts existing named-scenario JSON files unchanged, and optionally supports declarative `sweeps`. Validate/preview without running:

```bash
python tools/run_mc_experiment.py --config PATH.json --dry-run
```

Execute with `--config PATH.json --output OUTPUT_DIRECTORY`. A dry run writes nothing. A normal run emits `raw.csv` and `results.json`, including `resolved_configuration` for generated scenarios. The original `configuration` is retained. Simulation outputs are conditional model results, not calibrated gameplay probabilities.

## Experiment fields
- `schema_version`: optional, currently `1` (also the default for legacy files).
- `trials`, `waves`: positive integers; `seed_start`: optional integer (default 1).
- `checkpoints`: unique wave integers in the simulation horizon.
- `defaults`: common `WaveConfig` overrides; `scenarios`: optional explicit `{name, config}` entries when sweeps exist.
- `comparisons`: optional `{scenario, reference}` pairs referencing resolved names.
- `sweeps`: optional array of `{name, mode, base, parameters, reference, include_base}`.

`mode: grid` forms a Cartesian product of all parameter values; `mode: one_factor` changes one listed parameter at a time relative to `base`. `base` is a `WaveConfig` override object applied to each generated scenario. `parameters` maps existing `WaveConfig` fields to nonempty arrays. `include_base: true` creates `<name> / base` and automatically compares variants against it; alternatively `reference` names an explicit scenario. Generated scenario labels include each changed parameter and its JSON value. Existing explicit scenarios are kept first; generated scenarios follow sweep and parameter order. The current limit is 256 scenarios. Unknown parameters and duplicate scenario names fail validation.

## Example

```json
{
  "schema_version": 1,
  "description": "Compare attenuation policy under fixed chain conditions",
  "trials": 1000,
  "seed_start": 1,
  "waves": 103,
  "checkpoints": [40, 63, 83, 103],
  "defaults": {"faction": "Lions", "package": "howitzer_cannon"},
  "sweeps": [{
    "name": "attenuation",
    "mode": "one_factor",
    "base": {"attenuation_enabled": true, "attenuation_policy": "tier1_only"},
    "parameters": {
      "attenuation_enabled": [false],
      "attenuation_policy": ["highest_weight", "wave40_switch"]
    },
    "include_base": true
  }]
}
```

## Interpretation and constraints
- The runner uses matched seed identifiers for comparisons; different policies may consume RNG differently, so this does not guarantee identical random events.
- Softlocks remove subsequent checkpoints from observed denominators. Do not interpret absent observations as zeros.
- A zero reserve can select a different construction branch, not merely change a numeric reserve level.
- This specification varies existing simulator capabilities only. Custom building packages, arbitrary active Amplifier counts, and custom metrics still require separate extensions.
- Generated variants may duplicate their base configuration if a parameter list includes the baseline value; names are distinct but the experimental treatment may not be.

## Metrics and comparisons (Slice 3)

- `metrics`: optional list of metric IDs to aggregate; omitted means all 16 historical metrics. The canonical `raw.csv` retains all historical metric columns.
- `derived_metrics`: optional object mapping new metric IDs to arithmetic expressions using existing built-in metric IDs and numeric constants. Allowed operators are `+`, `-`, `*`, `/`, unary signs, and parentheses. No functions, attribute access, or Python execution. Division by zero excludes that metric observation; it does not remove the underlying checkpoint from other metrics.
- `comparisons`: each `{scenario, reference}` may additionally set `mode` to `paired` (default) or `unpaired`. Paired comparisons summarize within-seed differences; unpaired comparisons estimate the difference of sample means with an independent-samples standard-error confidence half-width. Unpaired median, quantiles, and standard deviation of differences are intentionally null. Different seed identifiers do not imply identical random events.
- `metric_registry` in `results.json` describes units, provenance and aggregation. `observed` counts checkpoints present; derived metrics may have fewer valid observations due to undefined ratios.

## Run lifecycle (Slice 4, initial implementation)

- A nonempty output directory is rejected rather than overwritten. Use a new directory per execution.
- `run_manifest.json` is written at the start with a `running` status, resolved configuration, source revision, environment, seed range, and planned run count.
- Progress is updated after each scenario. `completed` is written only after both `raw.csv` and `results.json` exist, with SHA-256 checksums.
- A manifest left in `running` status means the run was interrupted or failed before completion; its CSV must not be interpreted as complete. Resume and explicit failure recovery are not implemented yet.

## Run lifecycle (Slice 4)

A non-dry-run requires a new or empty output directory. Existing nonempty directories
are rejected rather than overwritten. `run_manifest.json` is created with status
`running`, UTC start time, fully resolved scenario matrix, source Git revision and
dirty flag, Python/platform versions, model and spec identifiers, seed range, and
planned run count. The manifest's `completed_runs` advances after each completed
simulation. A failure or interruption marks the manifest `failed`; partial raw CSV
is **not** a valid finished result. Completion records UTC finish time and SHA-256
checksums for `raw.csv` and `results.json`. Consumers must call
`mc_run_lifecycle.verify_completed(output_directory)` before using a result;
this checks the completion state, run count, and output checksums. There is no
automatic resume in this slice; reruns require a fresh output directory.

The Git revision is not sufficient to identify uncommitted source changes; a
`source_dirty` flag is recorded. A reproducible release should use a clean revision.

## Standard Markdown report (Slice 5)

After a completed run, invoke:

```bash
python tools/mc_standard_report.py --output /path/to/finished-run
```

The generator requires a verified `run_manifest.json`, `raw.csv`, and
`results.json`. It writes a new `report.md` and refuses to overwrite an
existing report. It includes the optional specification `question`, resolved
scenario differences, metrics and units, per-checkpoint observed sample sizes,
summary uncertainty, paired/unpaired comparisons, softlocks, model limitations,
and run provenance. The full resolved matrix remains in machine-readable files.
No hand-authored findings are inserted. The report is a deterministic rendering
of the completed run, not an independent re-analysis of raw data.

## PDF and vector checkpoint charts (Slice 6)

After successful simulation, generate a PDF and reusable chart data:

```bash
python tools/mc_report_pdf.py --output /path/to/finished-run
```

The command validates the run manifest and SHA-256 output checksums, then writes
`report.pdf` and `charts.json` without overwriting existing outputs. The PDF
uses the standard Markdown report model for its textual findings and draws
checkpoint means with normal-approximation 95% confidence whiskers. Every
plotted mean, uncertainty interval, unit, scenario and observation denominator
is preserved in `charts.json`, taken directly from `results.json`.
Charts represent conditional simulation results, not survival probabilities.

## Agent-facing JSON contract (Slice 7)

`tools/mc_agent_interface.py` is the stable version-1, agent-neutral command
boundary. Each command writes exactly one JSON response on stdout, with
`ok: true` and `data` on success, or `ok: false` and a typed `error` on failure.
A nonzero exit status indicates failure. It never evaluates arbitrary agent code.

```bash
python tools/mc_agent_interface.py capabilities
python tools/mc_agent_interface.py validate --config experiment.json
python tools/mc_agent_interface.py preview --config experiment.json
python tools/mc_agent_interface.py run --config experiment.json --output new-results
python tools/mc_agent_interface.py report --output new-results --format both
```

Capabilities expose all WaveConfig fields and defaults, allowed enum values,
metric identifiers and definitions, safe derived operators, sweep and comparison
modes, required fields, output artifacts, and model limitations. `preview`
returns the fully resolved matrix and run count without executing anything.
`run` and `report` delegate to the same tested core entrypoints used by humans.
Existing outputs are never overwritten. Agents should use this contract rather
than importing simulator internals or inventing game mechanics.

## Standalone CLI and presets (Slice 8)

Human and programmatic users share the same validation, execution, and reporting
logic through `tools/mc_experiment.py`. A complete example:

```bash
python tools/mc_experiment.py presets
python tools/mc_experiment.py init quick-comparison --config my-experiment.json
python tools/mc_experiment.py validate --config my-experiment.json
python tools/mc_experiment.py preview --config my-experiment.json
python tools/mc_experiment.py run --config my-experiment.json --output my-results
```

`run` generates Markdown and PDF reports by default; use `--report none` to
skip them or `--report markdown` to omit PDF. To generate reports separately,
use `report --output my-results --format both`. All output paths are exclusive;
existing experiment runs, reports, and preset destination files are not
silently overwritten. Bundled presets live in `presets/mc/`, are ordinary JSON
specifications, and should be edited before long runs. The bundled
`quick-comparison` example is a small attenuation-policy comparison, not a
replacement for published Experiment A results.
