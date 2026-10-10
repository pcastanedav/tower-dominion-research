"""Strategy-specific Blueprint preference model.

MC/Amplifier remain dominant. Supports and offensive package targets occupy
one comparable priority tier; no fixed offensive-versus-support preference.
This module does not assume Blueprint codes until verified against game assets.
"""
from collections import Counter

BLUEPRINT_NAMES = {
    'BPCB05': 'Sanction Cannon', 'BPCB06': 'Slovek Howitzer',
    'BPCB09': 'Retribution Position', 'BPCB10': 'Omega Emitter',
    'BPCB11': 'Super Heavy Pulse Defense', 'BPCB12': 'Air Command',
    'BPCB14': 'Rampart Missile Silo', 'BPCB21': 'Salamander Position',
    'BPF202': 'Tactical Fortress', 'BPSB01': 'Ammo Depot',
    'BPSB02': 'Division Relay', 'BPSB06': 'Platform', 'BPSB07': 'MC',
}

SUPPORTS = ('Air Command', 'Omega Emitter', 'Ammo Depot', 'Division Relay')
PERMANENTLY_PROTECTED = frozenset(SUPPORTS + ('MC', 'Super Heavy Pulse Defense', 'Rampart Missile Silo'))

PACKAGES = {
    'sphd_rampart': ('Super Heavy Pulse Defense', 'Rampart Missile Silo'),
    'sphd_retribution': ('Super Heavy Pulse Defense', 'Retribution Position'),
    'sphd_fortress': ('Super Heavy Pulse Defense', 'Tactical Fortress'),
    'salamander': ('Salamander Position',),
    'howitzer_cannon': ('Slovek Howitzer', 'Sanction Cannon'),
    'howitzer': ('Slovek Howitzer',),
    'cannon': ('Sanction Cannon',),
}


def attenuation_candidates(weights, package, names=None):
    """Deterministic roster-order nonessential Blueprint targets."""
    if package not in PACKAGES:
        raise ValueError('unknown offensive package')
    labels = dict(BLUEPRINT_NAMES)
    labels.update(names or {})
    protected = PERMANENTLY_PROTECTED.union(PACKAGES[package])
    return [code for code, weight in weights.items()
            if weight > 0 and not code.startswith('BPSB')
            and labels.get(code, code) not in protected]


def support_rank(package):
    if package == 'salamander':
        return {'Omega Emitter': 4, 'Air Command': 3,
                'Ammo Depot': 2, 'Division Relay': 1}
    if package in ('howitzer', 'howitzer_cannon', 'cannon'):
        return {'Omega Emitter': 4, 'Air Command': 4,
                'Ammo Depot': 2, 'Division Relay': 1}
    return {'Air Command': 4, 'Omega Emitter': 3,
            'Ammo Depot': 2, 'Division Relay': 1}


def evaluate_blueprint(name, package, acquired=None, lions=False):
    """Return comparable (tier, preference) values, not invented utility points."""
    if package not in PACKAGES:
        raise ValueError('unknown offensive package')
    if package == 'sphd_fortress' and not lions:
        raise ValueError('Fortress package is Lions-only')
    acquired = Counter(acquired or {})
    if name in ('MC', 'Amplifier'):
        return (3, 0)
    if name in SUPPORTS:
        return (2, support_rank(package)[name])
    if name in PACKAGES[package]:
        # Package completion gets a tie-break within the same priority tier.
        missing_others = sum(not acquired[x] for x in PACKAGES[package] if x != name)
        return (2, 4 if missing_others == 0 else 3)
    if name in ('Rampart Missile Silo', 'Platform'):
        # Utility selections outside the current offensive/support categories.
        return (2, 2)
    return (1, 0)


def choose_package_card(cards, package, acquired=None, lions=False):
    """Score complete reward cards; do not cherry-pick items within a card."""
    if not cards:
        return None
    def score(card):
        values = [evaluate_blueprint(name, package, acquired, lions)
                  for kind, name, qty in card if kind == 'bp' and qty > 0]
        return max(values, default=(0, 0)), sum(qty for kind, name, qty in card
                                                if kind == 'bp' and qty > 0)
    return max(range(len(cards)), key=lambda index: score(cards[index]))
