"""Stable MC experiment metrics, safe derived expressions, and comparison statistics."""
import ast
import math
from statistics import mean, median, stdev

METRICS = ('mc_owned', 'mc_built', 'mc_in_hand', 'hv_offense', 'hv_support', 'hv_other', 'hv_total', 'drafts_resolved', 'all_hv_offense', 'all_hv_support', 'all_hv_total', 'offense_building_1', 'offense_building_2', 'complete_sets', 'has_all_required', 'has_only_one_required')

METRIC_REGISTRY = {
    name: {'id': name, 'unit': 'indicator' if name.startswith('has_') else 'blueprint copies' if name.startswith(('all_hv_', 'offense_building_', 'complete_sets')) else 'count',
           'provenance': 'checkpoint observation', 'aggregation': 'sample distribution',
           'description': name.replace('_', ' '), 'censoring': 'observed checkpoints only'}
    for name in METRICS
}
METRIC_REGISTRY['mc_built']['unit'] = 'constructed buildings'
METRIC_REGISTRY['mc_in_hand']['unit'] = 'unbuilt blueprint copies'
METRIC_REGISTRY['mc_owned']['unit'] = 'owned blueprint copies'
for name in ('hv_offense', 'hv_support', 'hv_other', 'hv_total', 'drafts_resolved'):
    METRIC_REGISTRY[name]['unit'] = 'draft outcomes' if name.startswith('hv_') else 'drafts'


def summarize(values):
    values = sorted(values)
    n = len(values)
    sd = stdev(values) if n > 1 else 0.0
    return {'mean': mean(values), 'sd': sd, 'median': median(values),
            'p10': values[int(.1*(n-1))], 'p90': values[int(.9*(n-1))],
            'ci95_halfwidth': 1.96*sd/math.sqrt(n)}


def _eval(node, values):
    if isinstance(node, ast.Expression):
        return _eval(node.body, values)
    if isinstance(node, ast.Name) and node.id in values:
        return values[node.id]
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _eval(node.operand, values)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div):
        a, b = _eval(node.left, values), _eval(node.right, values)
        if isinstance(node.op, ast.Add): return a + b
        if isinstance(node.op, ast.Sub): return a - b
        if isinstance(node.op, ast.Mult): return a * b
        return a / b
    raise ValueError('unsupported derived metric expression')


def compile_metrics(spec):
    """Return selected metric IDs, compiled safe derived expressions, and metadata."""
    selected = spec.get('metrics', list(METRICS))
    if not isinstance(selected, list) or not selected or any(not isinstance(m, str) for m in selected):
        raise ValueError('metrics must be a nonempty list of metric IDs')
    derived = spec.get('derived_metrics', {})
    if not isinstance(derived, dict):
        raise ValueError('derived_metrics must be an object')
    if set(derived) & set(METRICS):
        raise ValueError('derived metric cannot override a built-in metric')
    compiled = {}
    for name, expression in derived.items():
        if not isinstance(name, str) or not name.isidentifier() or not isinstance(expression, str) or len(expression) > 200:
            raise ValueError('invalid derived metric name or expression')
        try:
            tree = ast.parse(expression, mode='eval')
            # Only existing built-in metrics can be referenced; no chaining, calls or attribute access.
            _eval(tree, {m: 1 for m in METRICS})
        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as exc:
            if isinstance(exc, ZeroDivisionError):
                pass  # Valid expressions can divide by a metric that happens to be zero.
            else:
                raise ValueError('invalid derived metric %s: %s' % (name, exc)) from exc
        compiled[name] = tree
    if len(selected) != len(set(selected)) or set(selected) - (set(METRICS) | set(compiled)):
        raise ValueError('duplicate or unknown selected metric')
    return selected, compiled


def evaluate_metric(name, row, compiled):
    values = dict(zip(METRICS, row))
    if name in values:
        return values[name]
    try:
        result = _eval(compiled[name], values)
    except ZeroDivisionError:
        return None
    if not math.isfinite(result):
        return None
    return result


def aggregate(rows, metrics, compiled):
    return {metric: summarize(values) for metric in metrics
            if (values := [v for row in rows if (v := evaluate_metric(metric, row, compiled)) is not None])}


def paired_aggregate(matches, metrics, compiled):
    result = {}
    for metric in metrics:
        differences = []
        for first, reference in matches:
            a = evaluate_metric(metric, first, compiled)
            b = evaluate_metric(metric, reference, compiled)
            if a is not None and b is not None:
                differences.append(a - b)
        if differences:
            result[metric] = summarize(differences)
    return result


def unpaired_aggregate(first_rows, reference_rows, metrics, compiled):
    """Difference of independent sample means; standard error uses both samples."""
    result = {}
    for metric in metrics:
        first = [v for row in first_rows if (v := evaluate_metric(metric, row, compiled)) is not None]
        reference = [v for row in reference_rows if (v := evaluate_metric(metric, row, compiled)) is not None]
        if not first or not reference:
            continue
        a, b = summarize(first), summarize(reference)
        se = math.sqrt(a['sd'] ** 2 / len(first) + b['sd'] ** 2 / len(reference))
        result[metric] = {'mean': a['mean'] - b['mean'], 'sd': None, 'median': None,
                          'p10': None, 'p90': None, 'ci95_halfwidth': 1.96 * se,
                          'first_observed': len(first), 'reference_observed': len(reference)}
    return result
