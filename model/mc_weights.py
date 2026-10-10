"""MC-chain Blueprint weights with an explicitly supplied eligible roster.

No roster, tier or Eleanor value is inferred from asset names. The caller must
supply verified eligibility and any still-assumed effect magnitudes explicitly.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class BlueprintEntry:
    code: str
    tier: int
    base: int
    increment: int
    cap: int = 100
    eligible: bool = True


def blueprint_weights(entries, wave, mc_1a_active=0, amplified_types=(),
                      extra_tier_weights=None, type_bonus_percent=None):
    """Compute integer weights before weighted Blueprint selection.

    Higher-tier additive currencies are applied to raw tier rarity weights,
    while building-type percent modifiers multiply the resulting weights.
    The exact game's float-to-int rounding remains a verification boundary.
    """
    if wave < 1 or mc_1a_active < 0:
        raise ValueError('invalid wave or MC count')
    extra_tier_weights = extra_tier_weights or {}
    type_bonus_percent = type_bonus_percent or {}
    amplified_types = set(amplified_types)
    result = {}
    for entry in entries:
        if entry.code in result:
            raise ValueError('duplicate Blueprint code')
        if entry.tier not in (1, 2, 3) or entry.cap < 0:
            raise ValueError('invalid Blueprint tier or cap')
        if not entry.eligible:
            continue
        bonus = extra_tier_weights.get(entry.tier, 0)
        if entry.tier in (2, 3):
            bonus += 2 * mc_1a_active
        rarity = max(0, min(entry.cap, entry.base + (wave - 1) * entry.increment + int(bonus)))
        pct = type_bonus_percent.get(entry.code, 0) + (100 if entry.code in amplified_types else 0)
        result[entry.code] = max(0, int(rarity * max(0, 1 + pct / 100)))
    return result
