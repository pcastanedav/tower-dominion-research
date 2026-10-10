"""Weighted unique-Blueprint draft probability model.

Conditional model: one Blueprint per card, positive integer weights, five
unique offers. Game duplicate rejection/retry is established, but whether its
joint distribution equals sequential weighted sampling remains unverified.
"""
from functools import lru_cache


def target_offer_probability(weights, target, draws=5):
    """Exact probability target appears under sequential weighted unique draws.

    This is a conditional mathematical benchmark, not a verified game sampler.
    """
    if target not in weights:
        return 0.0
    if draws < 0:
        raise ValueError('draws must be nonnegative')
    pool = {key: int(value) for key, value in weights.items() if value > 0}
    if target not in pool or draws == 0:
        return 0.0
    if draws >= len(pool):
        return 1.0
    others = tuple((key, value) for key, value in pool.items() if key != target)
    target_weight = pool[target]

    @lru_cache(None)
    def miss(remaining, k):
        if k == 0:
            return 1.0
        total = target_weight + sum(others[i][1] for i in remaining)
        return sum((others[i][1] / total) * miss(tuple(j for j in remaining if j != i), k - 1)
                   for i in remaining)

    return 1.0 - miss(tuple(range(len(others))), draws)


def rejection_draft_target_probability(weights, target, draws=5):
    """Exact inclusion probability for iid weighted draws conditioned on uniqueness.

    This matches complete-screen rejection and retry if each Blueprint card is
    independently sampled and the entire screen is discarded on duplicates.
    Unlike sequential unique sampling, its distinct-set weight is proportional
    to the PRODUCT of constituent weights. Conditional model, not yet proven
    to match the game's partial regeneration algorithm.
    """
    if draws < 0:
        raise ValueError('draws must be nonnegative')
    pool = {k: int(v) for k, v in weights.items() if v > 0}
    if target not in pool or draws == 0:
        return 0.0
    if draws >= len(pool):
        return 1.0

    def elementary(values, n):
        coeff = [1] + [0] * n
        for weight in values:
            for j in range(n, 0, -1):
                coeff[j] += weight * coeff[j-1]
        return coeff[n]

    all_weight = elementary(pool.values(), draws)
    without_target = elementary((v for k, v in pool.items() if k != target), draws)
    return 1.0 - without_target / all_weight


def sample_rejection_draft(weights, rng, draws=5):
    """Sample the conditional full-screen rejection law without retry loops.

    Distinct subsets have probability proportional to their weight product.
    This efficient O(n*draws) sampler is conditional on the game using iid
    weighted cards and rejecting any complete screen containing duplicates.
    """
    if draws < 0:
        raise ValueError('draws must be nonnegative')
    items = [(key, int(value)) for key, value in weights.items() if value > 0]
    if draws > len(items):
        raise ValueError('not enough positive-weight Blueprints for unique draft')
    if draws == 0:
        return ()
    n = len(items)
    suffix = [[0] * (draws + 1) for _ in range(n + 1)]
    suffix[n][0] = 1
    for i in range(n - 1, -1, -1):
        suffix[i][0] = 1
        for k in range(1, draws + 1):
            suffix[i][k] = suffix[i + 1][k] + items[i][1] * suffix[i + 1][k - 1]
    result = []
    remaining = draws
    for i, (key, weight) in enumerate(items):
        if not remaining:
            break
        selected_mass = weight * suffix[i + 1][remaining - 1]
        total_mass = suffix[i][remaining]
        if rng.random() * total_mass < selected_mass:
            result.append(key)
            remaining -= 1
    return tuple(result)
