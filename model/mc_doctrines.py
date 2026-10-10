"""Bridge selected ordinary Doctrine rewards to MC-chain Amplifier acquisition.

Uses the existing dynamic ordinary Doctrine pool. D1_45 and D2_42 are
independent grant sources; their Blueprint reward quantities are provisionally
one each until the effect payload is verified.
"""
from dataclasses import dataclass, field
from reinforcement_model import dynamic_doctrine_pool_fast, sample_doctrines

AMPLIFIER_DOCTRINES = frozenset(('D1_45', 'D2_42'))
ATTENUATOR_DOCTRINES = frozenset(('D1_44', 'D2_41'))
SPECIAL_BUDGETS_DOCTRINE = 'D2_14'  # ReinformentChoiceIncreaseBy1


@dataclass
class MCDocState:
    faction: str = 'Lions'
    ordinary_owned: set = field(default_factory=set)
    tb_owned: set = field(default_factory=set)
    placed_families: set = field(default_factory=set)
    placed_towers: set = field(default_factory=set)
    tb_mult: int = 3
    t2_bonus: int = 0
    blueprint_tier_bonus: dict = field(default_factory=dict)
    draft_events: list = field(default_factory=list)
    attenuators_owned: int = 0
    suppressed_families: set = field(default_factory=set)
    amplified_families: set = field(default_factory=set)

    def pool(self, wave):
        return dynamic_doctrine_pool_fast(
            self.faction, wave, removed=self.ordinary_owned,
            tb_owned=self.tb_owned, tb_mult=self.tb_mult,
            placed_families=self.placed_families, t2_bonus=self.t2_bonus,
            placed_towers=self.placed_towers,
            suppressed_families=self.suppressed_families,
            amplified_families=self.amplified_families)

    def acquire(self, name, mc_state):
        """Return True only if this was a new Amplifier-granting Doctrine."""
        if name.startswith('TB'):
            if name in self.tb_owned:
                return False
            self.tb_owned.add(name)
            return False
        if name in self.ordinary_owned:
            return False
        self.ordinary_owned.add(name)
        if name in ATTENUATOR_DOCTRINES:
            self.attenuators_owned = min(2, self.attenuators_owned + 1)
        if name == 'D2_01':
            self.blueprint_tier_bonus[2] = self.blueprint_tier_bonus.get(2, 0) + 10
        elif name == 'D3_11':
            self.blueprint_tier_bonus[3] = self.blueprint_tier_bonus.get(3, 0) + 5
        elif name == 'D1_19':
            self.t2_bonus += 6
        elif name == 'D2_40':
            self.tb_mult += 4
        if name in AMPLIFIER_DOCTRINES:
            mc_state.acquire('Amplifier')
            return True
        return False


def acquire_with_drafts(doctrine_state, name, mc_state, rng, wave,
                        policy='amplifier_first', max_depth=100):
    """Resolve immediate Doctrine drafts recursively, with a bounded depth."""
    if max_depth < 1:
        raise ValueError('max_depth must be positive')
    if name in (doctrine_state.tb_owned if name.startswith('TB') else doctrine_state.ordinary_owned):
        return ()
    granted = []
    steps = 0

    def resolve(current):
        nonlocal steps
        if current in (doctrine_state.tb_owned if current.startswith('TB') else doctrine_state.ordinary_owned):
            return
        if steps >= max_depth:
            raise RuntimeError('nested Doctrine acquisition limit reached')
        steps += 1
        if doctrine_state.acquire(current, mc_state):
            granted.append(current)
        if current not in ('D2_40', 'D2_06'):
            return
        sizes = (2,) if current == 'D2_40' else (3, 3)
        for size in sizes:
            # Recompute after each selection and its nested effects.
            pool = doctrine_state.pool(wave)
            if not pool:
                continue
            offered = sample_doctrines(rng, pool, min(size, len(pool)))
            if policy == 'amplifier_first':
                chosen = next((x for x in offered if x == SPECIAL_BUDGETS_DOCTRINE),
                              next((x for x in offered if x in AMPLIFIER_DOCTRINES), offered[0]))
            elif policy == 'first':
                chosen = offered[0]
            else:
                raise ValueError('unknown nested Doctrine policy')
            doctrine_state.draft_events.append((current, tuple(offered), chosen))
            resolve(chosen)

    resolve(name)
    return tuple(granted)


def apply_selected_doctrines(cards, index, doctrine_state, mc_state, rng=None, wave=None):
    if index is None:
        return ()
    grants = []
    for kind, identity, quantity in cards[index]:
        if kind != 'doctrine':
            continue
        if quantity != 1:
            raise ValueError('Doctrine item quantity must be one')
        if rng is not None and wave is not None:
            grants.extend(acquire_with_drafts(doctrine_state, identity, mc_state, rng, wave))
        elif doctrine_state.acquire(identity, mc_state):
            grants.append(identity)
    return tuple(grants)
