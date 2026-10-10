"""Binomial uncertainty and explicitly observed wave metrics for MC simulations."""
from math import sqrt


def wilson_interval(successes, trials, z=1.959963984540054):
    """Two-sided Wilson score interval (95% with default z)."""
    if trials < 1 or not 0 <= successes <= trials or z <= 0:
        raise ValueError('invalid binomial inputs')
    p = successes / trials
    denom = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denom
    half = z * sqrt((p * (1 - p) + z * z / (4 * trials)) / trials) / denom
    return max(0.0, center - half), min(1.0, center + half)


def first_mc_by(outcomes, wave):
    """First acquisition is observable even if a later chain is censored."""
    return sum(s.first_mc_wave is not None and s.first_mc_wave <= wave for s, _ in outcomes)


def wave_threshold(outcomes, wave, threshold):
    """Return (successes, observed) without counting early-censored runs as failures."""
    observed = [history[wave - 1]['mc_owned'] for _, history in outcomes if len(history) >= wave]
    return sum(value >= threshold for value in observed), len(observed)
