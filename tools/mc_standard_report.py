"""Generate a deterministic Markdown report from verified experiment results."""
import argparse
import json
from pathlib import Path
from mc_run_lifecycle import verify_completed


def fmt(value):
    return 'n/a' if value is None else ('%.3f' % value if isinstance(value, float) else str(value))


def table(headers, rows):
    def escape(x):
        return str(x).replace('|', '\\|').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(map(escape, headers)) + ' |',
                      '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                     ['| ' + ' | '.join(map(escape, row)) + ' |' for row in rows])


def build_report(data, manifest):
    resolved = data['resolved_configuration']
    spec = data['configuration']
    scenarios = resolved['scenarios']
    registry = data.get('metric_registry', {})
    metrics = list(registry) or list(next(iter(next(iter(data['summary'].values())).values()))['metrics'])
    lines = ['# Tower Dominion — Experiment Report', '', '## Question', '',
             spec.get('question', 'Compare the configured Mission Control acquisition scenarios.'), '',
             '## Methods and assumptions', '',
             'Seeded simulation of the configured faction, commander, Blueprint and Doctrine pools, construction rules, and selection policy. No combat survival, full economy, or building placement is simulated. Blueprint acquisition does not establish construction or readiness. Some commander mechanics are provisional. Identical seed identifiers may diverge in RNG consumption.', '',
             '## Run configuration', '',
             '- Model: `%s`; schema: `%s`' % (manifest['model_version'], resolved['schema_version']),
             '- Trials per scenario: %s; total planned runs: %s' % (resolved['trials'], resolved['total_runs']),
             '- Seed range: %s–%s' % (resolved['seed_start'], resolved['seed_start'] + resolved['trials'] - 1),
             '- Horizon: %s waves; checkpoints: %s' % (resolved['waves'], ', '.join(map(str, resolved['checkpoints']))), '',
             '### Resolved scenario matrix', '']
    keys = sorted({key for s in scenarios for key in s['config']})
    varying = [key for key in keys if len({json.dumps(s['config'].get(key), sort_keys=True) for s in scenarios}) > 1]
    lines += [table(['Scenario'] + varying, [[s['name']] + [json.dumps(s['config'].get(key)) for key in varying] for s in scenarios]), '',
              'Only varying parameters are shown. Full configurations are preserved in the run manifest.', '',
              '### Metrics', '', table(['Metric', 'Unit', 'Provenance'],
              [[m, registry.get(m, {}).get('unit', 'count'), registry.get(m, {}).get('provenance', 'checkpoint observation')] for m in metrics]), '',
              '## Checkpoint results', '']
    for wave in resolved['checkpoints']:
        lines += ['### Wave %s' % wave, '']
        for metric in metrics:
            rows = []
            for scenario in scenarios:
                result = data['summary'][scenario['name']][str(wave)]
                stat = result['metrics'].get(metric)
                rows.append([scenario['name'], result['observed'], fmt(stat['mean']) if stat else 'n/a', fmt(stat['sd']) if stat else 'n/a', fmt(stat['ci95_halfwidth']) if stat else 'n/a'])
            lines += ['**%s** (%s)' % (metric, registry.get(metric, {}).get('unit', 'count')), '',
                      table(['Scenario', 'Observed', 'Mean', 'SD', '95% CI half-width'], rows), '']
    lines += ['## Comparisons', '', 'Differences are scenario minus reference. Paired results use matching observed seeds; unpaired results use independent-sample mean differences.', '']
    for comparison in resolved['comparisons']:
        name = comparison['scenario'] + ' - ' + comparison['reference']
        mode = comparison.get('mode', 'paired')
        rows = []
        for wave in resolved['checkpoints']:
            entry = data['paired'][name][str(wave)]
            for metric in metrics:
                stat = entry['metrics'].get(metric)
                if stat:
                    n = entry['paired_seeds'] if mode == 'paired' else '%s / %s' % (entry['first_observed'], entry['reference_observed'])
                    rows.append([wave, metric, n, fmt(stat['mean']), fmt(stat['ci95_halfwidth'])])
        lines += ['### %s (%s)' % (name, mode), '', table(['Wave', 'Metric', 'Paired seeds / sample sizes', 'Mean difference', '95% CI half-width'], rows) if rows else 'No comparable observations.', '']
    lines += ['## Softlocks and censoring', '',
              table(['Scenario', 'Softlocks', 'Rate'], [[s['name'], len(data['softlocks'].get(s['name'], {})), fmt(data['softlock_rates'].get(s['name']))] for s in scenarios]), '',
              'Observed checkpoint counts are reported separately. Missing observations are not treated as zero; softlocked runs may have valid earlier observations.', '',
              '## Interpretation boundaries', '',
              'Results are conditional simulation estimates, not calibrated game probabilities or demonstrated combat survival. Confidence intervals use normal approximations without multiple-comparison correction. Policy comparisons can combine multiple changes.', '',
              '## Provenance', '',
              '- Revision: `%s`; dirty: `%s`' % (manifest['source_revision'], manifest['source_dirty']),
              '- Started: `%s`; finished: `%s`' % (manifest['started_at'], manifest['finished_at']),
              '- Python: `%s`; platform: `%s`' % (manifest['python_version'], manifest['platform']),
              '- raw.csv SHA-256: `%s`' % manifest['checksums']['raw.csv'],
              '- results.json SHA-256: `%s`' % manifest['checksums']['results.json'], '',
              '## Optional interpretation', '', 'No agent-authored interpretation included.', '']
    return '\n'.join(lines)


def render(output):
    output = Path(output)
    manifest = verify_completed(output)
    data = json.loads((output / 'results.json').read_text())
    markdown = build_report(data, manifest)
    destination = output / 'report.md'
    with destination.open('x') as f:
        f.write(markdown)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    print(render(parser.parse_args().output))

if __name__ == '__main__':
    main()
