"""Resolve and validate Mission Control experiment specifications without executing runs."""
from dataclasses import asdict, fields
from itertools import product
from mc_wave60 import WaveConfig
from mc_packages import PACKAGES

CONFIG_FIELDS = {field.name for field in fields(WaveConfig)}
CHOICES = {
    'faction': {'Iron', 'Lions', 'Pargan'},
    'package': set(PACKAGES) | {None},
    'attenuation_policy': {'tier1_only', 'wave40_switch', 'highest_weight'},
    'mc_construction_policy': {'threshold', 'draft_replenish', 'preserve', 'continuous'},
    'mc_replenish_source': {'both', 'draft_only', 'reinforcement_only'},
    'conflict': {'mc_first', 'amplifier_first'},
}


MAX_SCENARIOS = 256


def expand_scenarios(spec):
    """Expand declarative grid/one-factor variants into legacy scenario entries.

    `sweeps` entries have name, base config, mode (grid|one_factor), parameters,
    and optional reference. Generated names are deterministic and human-readable.
    A reference is a named explicit scenario or the sweep's own generated base
    when include_base=true. No silent collisions or override precedence.
    """
    scenarios = list(spec.get('scenarios', []))
    comparisons = spec.get('comparisons', [])
    if not isinstance(comparisons, list):
        raise ValueError('comparisons must be a list')
    comparisons = list(comparisons)
    sweeps = spec.get('sweeps', [])
    if not isinstance(sweeps, list):
        raise ValueError('sweeps must be a list')
    for sweep in sweeps:
        if not isinstance(sweep, dict) or not isinstance(sweep.get('name'), str) or not sweep['name'].strip():
            raise ValueError('sweep requires a nonempty name')
        name = sweep['name']
        mode = sweep.get('mode')
        if mode not in ('grid', 'one_factor'):
            raise ValueError('sweep %s mode must be grid or one_factor' % name)
        base = sweep.get('base', {})
        params = sweep.get('parameters')
        if not isinstance(base, dict) or not isinstance(params, dict) or not params:
            raise ValueError('sweep %s requires base object and nonempty parameters object' % name)
        if set(params) - CONFIG_FIELDS:
            raise ValueError('sweep %s unknown parameter: %s' % (name, ', '.join(sorted(set(params)-CONFIG_FIELDS))))
        for key, values in params.items():
            if not isinstance(values, list) or not values:
                raise ValueError('sweep %s parameter %s requires nonempty values list' % (name, key))
        include_base = sweep.get('include_base', False)
        if type(include_base) is not bool:
            raise ValueError('sweep %s include_base must be boolean' % name)
        baseline = name + ' / base' if include_base else sweep.get('reference')
        if include_base:
            scenarios.append({'name': baseline, 'config': dict(base)})
        keys = list(params)
        if mode == 'grid':
            variants = (dict(zip(keys, values)) for values in product(*(params[k] for k in keys)))
        else:
            variants = ({key: value} for key in keys for value in params[key])
        for changes in variants:
            label = ', '.join('%s=%s' % (key, json_value(changes[key])) for key in changes)
            scenario_name = name + ' / ' + label
            scenarios.append({'name': scenario_name, 'config': {**base, **changes}})
            if baseline is not None:
                comparisons.append({'scenario': scenario_name, 'reference': baseline})
            if len(scenarios) > MAX_SCENARIOS:
                raise ValueError('scenario count exceeds safety limit %s' % MAX_SCENARIOS)
    return scenarios, comparisons


def json_value(value):
    import json
    return json.dumps(value, separators=(',', ':'), sort_keys=True)


def resolve_spec(spec):
    """Return fully resolved, validated scenarios; accept legacy unversioned JSON."""
    if not isinstance(spec, dict):
        raise ValueError('experiment specification must be an object')
    version = spec.get('schema_version', 1)
    if type(version) is not int or version != 1:
        raise ValueError('unsupported experiment schema_version: %r' % version)
    trials, waves = spec.get('trials'), spec.get('waves')
    if type(trials) is not int or trials < 1 or type(waves) is not int or waves < 1:
        raise ValueError('trials and waves must be positive integers')
    checkpoints = spec.get('checkpoints')
    if not isinstance(checkpoints, list) or not checkpoints or any(type(w) is not int or not 1 <= w <= waves for w in checkpoints):
        raise ValueError('checkpoints must be nonempty integers within simulation horizon')
    if len(set(checkpoints)) != len(checkpoints):
        raise ValueError('checkpoints must be unique')
    seed_start = spec.get('seed_start', 1)
    if type(seed_start) is not int:
        raise ValueError('seed_start must be an integer')
    defaults = spec.get('defaults', {})
    if not isinstance(defaults, dict) or not isinstance(spec.get('scenarios', []), list):
        raise ValueError('defaults and scenarios must be objects/list')
    cases, comparisons = expand_scenarios(spec)
    if not cases:
        raise ValueError('scenarios must be nonempty')
    if len(cases) > MAX_SCENARIOS:
        raise ValueError('scenario count exceeds safety limit %s' % MAX_SCENARIOS)
    resolved, names = [], set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get('name'), str) or not case['name'].strip():
            raise ValueError('scenario %s requires a nonempty name' % index)
        name = case['name']
        if name in names:
            raise ValueError('duplicate scenario name: %s' % name)
        names.add(name)
        overrides = case.get('config', {})
        if not isinstance(overrides, dict):
            raise ValueError('scenario %s config must be an object' % name)
        merged = {**defaults, **overrides}
        unknown = set(merged) - CONFIG_FIELDS
        if unknown:
            raise ValueError('scenario %s unknown WaveConfig options: %s' % (name, ', '.join(sorted(unknown))))
        for key, options in CHOICES.items():
            if key in merged and merged[key] not in options:
                raise ValueError('scenario %s invalid %s: %r' % (name, key, merged[key]))
        try:
            config = WaveConfig(**merged)
        except TypeError as exc:
            raise ValueError('scenario %s invalid configuration: %s' % (name, exc)) from exc
        if config.tier3_wave < 1 or config.max_drafts_per_wave < 0:
            raise ValueError('scenario %s invalid tier3_wave or draft cap' % name)
        if config.eleanor_starting_mc_1a_equivalent < 0 or (config.eleanor and config.eleanor_initial_tier23_dampening):
            raise ValueError('scenario %s invalid Eleonor assumptions' % name)
        if config.eleanor and (config.eleanor_cadence < 1 or config.eleanor_first_wave < 1):
            raise ValueError('scenario %s invalid Eleonor draft cadence' % name)
        if config.early_3a_interval is not None and config.early_3a_interval < 1:
            raise ValueError('scenario %s invalid early_3a_interval' % name)
        if config.mc_reserve_target and (config.mc_build_target is None or config.mc_build_target < 1 or config.mc_batch_size < 1):
            raise ValueError('scenario %s reserve requires establishment target and batch size' % name)
        if config.package == 'sphd_fortress' and config.faction != 'Lions':
            raise ValueError('scenario %s Fortress package requires Lions roster' % name)
        resolved.append({'name': name, 'config': asdict(config)})
    if not isinstance(comparisons, list):
        raise ValueError('comparisons must be a list')
    for pair in comparisons:
        if not isinstance(pair, dict) or pair.get('scenario') not in names or pair.get('reference') not in names:
            raise ValueError('comparison references unknown scenario')
        if pair.get('mode', 'paired') not in ('paired', 'unpaired'):
            raise ValueError('comparison mode must be paired or unpaired')
    return {'schema_version': version, 'trials': trials, 'waves': waves, 'seed_start': seed_start,
            'checkpoints': checkpoints, 'scenarios': resolved, 'comparisons': comparisons,
            'total_runs': len(resolved)*trials}
