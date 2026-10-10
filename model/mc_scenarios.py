"""Reproducible conditional MC-chain scenario summaries, not calibrated game odds."""
from dataclasses import dataclass
from statistics import mean
from mc_roster import load_blueprint_roster
from mc_wave60 import WaveConfig, simulate_run
from mc_statistics import first_mc_by, wave_threshold, wilson_interval

SNAPSHOTS = (10, 20, 35, 40, 45, 50, 60)


def summarize_scenario(trials=100, seed_start=1, config=None, waves=60):
    if trials < 1:
        raise ValueError('trials must be positive')
    config = config or WaveConfig()
    faction_id = {'Iron': 'Faction1', 'Lions': 'Faction2', 'Pargan': 'Faction3'}.get(config.faction)
    if faction_id is None:
        raise ValueError('unknown faction for Blueprint eligibility')
    roster = load_blueprint_roster(faction=faction_id)
    outcomes = []
    for seed in range(seed_start, seed_start + trials):
        state, history = simulate_run(roster, None, waves=waves, seed=seed, config=config)
        outcomes.append((state, history))
    def fraction(predicate):
        return sum(bool(predicate(state, history)) for state, history in outcomes) / trials
    result = {
        'trials': trials, 'config': config.__dict__,
        'censored': fraction(lambda s, h: s.censored),
        'first_mc_by_10': fraction(lambda s, h: s.first_mc_wave is not None and s.first_mc_wave <= 10),
        'first_mc_by_20': fraction(lambda s, h: s.first_mc_wave is not None and s.first_mc_wave <= 20),
        'first_mc_by_40': fraction(lambda s, h: s.first_mc_wave is not None and s.first_mc_wave <= 40),
        'amplifier_by_40': fraction(lambda s, h: s.first_amplifier_wave is not None and s.first_amplifier_wave <= 40),
        'mc_ge_3_by_60': fraction(lambda s, h: not s.censored and s.mc_owned >= 3),
        'mc_ge_5_by_60': fraction(lambda s, h: not s.censored and s.mc_owned >= 5),
        'mc_mean_uncensored_60': None,
        'snapshots': {},
    }
    complete = [s.mc_owned for s, h in outcomes if not s.censored and len(h) == waves]
    if complete:
        result['mc_mean_uncensored_60'] = mean(complete)
    # Preserve observation denominators: early-censored chains are not failures.
    result['first_mc_probabilities'] = {
        wave: {'successes': first_mc_by(outcomes, wave), 'trials': trials,
               'probability': first_mc_by(outcomes, wave) / trials,
               'wilson95': wilson_interval(first_mc_by(outcomes, wave), trials)}
        for wave in (5, 10, 15, 20, 40) if wave <= waves
    }
    result['threshold_probabilities'] = {}
    for wave in (40, 45, 50, 60):
        if wave > waves:
            continue
        result['threshold_probabilities'][wave] = {}
        for threshold in (2, 3, 4, 5):
            successes, observed = wave_threshold(outcomes, wave, threshold)
            result['threshold_probabilities'][wave][threshold] = {
                'successes': successes, 'observed': observed,
                'probability': successes / observed if observed else None,
                'wilson95': wilson_interval(successes, observed) if observed else None,
            }
    for wave in SNAPSHOTS:
        if wave > waves:
            continue
        available = [h[wave - 1]['mc_owned'] for s, h in outcomes if len(h) >= wave]
        result['snapshots'][wave] = {
            'observed': len(available),
            'mc_mean_observed': mean(available) if available else None,
            'mc_ge_3_observed': sum(v >= 3 for v in available) / len(available) if available else None,
        }
    return result


if __name__ == '__main__':
    import json
    for name, config in (
        ('mc_first', WaveConfig()),
        ('amplifier_first', WaveConfig(conflict='amplifier_first')),
        ('red', WaveConfig(red=True)),
        ('tander', WaveConfig(tander=True)),
        ('eleanor', WaveConfig(eleanor=True)),
    ):
        print(json.dumps({'scenario': name, **summarize_scenario(trials=100, config=config)}, sort_keys=True), flush=True)
