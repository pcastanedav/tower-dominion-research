"""Paired-seed sensitivity experiments for conditional Mission Control simulations."""
import json
from mc_scenarios import summarize_scenario
from mc_wave60 import WaveConfig


def sensitivity_grid(trials=500, seed_start=1):
    cases = (
        ('threshold_35', WaveConfig(tier3_wave=35)),
        ('baseline_40', WaveConfig(tier3_wave=40)),
        ('threshold_45', WaveConfig(tier3_wave=45)),
        ('amplifier_weight_disabled', WaveConfig(tier3_wave=40, amplifier_effect_enabled=False)),
        ('amplifier_first', WaveConfig(tier3_wave=40, conflict='amplifier_first')),
    )
    return {name: summarize_scenario(trials=trials, seed_start=seed_start, config=config)
            for name, config in cases}


if __name__ == '__main__':
    for name, result in sensitivity_grid().items():
        print(json.dumps({'scenario': name, **result}, sort_keys=True), flush=True)
