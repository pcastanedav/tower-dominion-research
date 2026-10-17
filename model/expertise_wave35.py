"""Conditional Wave-35 expertise experiment; not calibrated to live game odds."""
import random
from dataclasses import dataclass, field
from mc_roster import load_blueprint_roster
from mc_weights import blueprint_weights
from mc_reinforcement import generate_mc_cards
from reinforcement_model import dynamic_doctrine_pool_fast, TB_FAMILIES, pick_weighted, sample_doctrines
from mc_doctrines import AMPLIFIER_DOCTRINES, ATTENUATOR_DOCTRINES

POLICIES = {
    'isolated': (),
    'minimal': (1,),
    'moderate': (1, 1, 1),
    'broad': (1, 1, 1, 1, 1),
    'delayed': (1, 20, 20),
    'late': (1, 25, 25, 25, 25),
}
CHECKPOINTS = (10, 15, 20, 25, 30, 35)

@dataclass
class ExpertiseResult:
    target: str
    eleanor: bool
    policy: str
    blueprint_wave: int | None = None
    construction_wave: int | None = None
    expertise_waves: dict = field(default_factory=dict)
    d7_wave: int | None = None
    d7_route: str | None = None
    amplifier_offer_count: int = 0
    amplifier_acquired: int = 0
    amplifier_assignment_wave: int | None = None
    amplifier_active_waves: int = 0
    attenuator_offer_count: int = 0
    attenuator_acquired: int = 0
    checkpoints: dict = field(default_factory=dict)
    nested_drafts: int = 0
    eleanor_drafts: int = 0
    amplifier_saved_before_build: bool = False


def construction_wave(acquired_wave, floor=10):
    return max(floor, acquired_wave) if acquired_wave is not None else None


def target_doctrine_weights(faction, wave, target_family, owned, placed, amplifiers=0,
                            ordinary_owned=(), other_families=(), tb_multiplier=3, t2_bonus=0):
    """Apply additive +100% per assigned Amplifier to target family only."""
    if amplifiers not in (0, 1, 2):
        raise ValueError('supported Amplifier count is 0..2')
    families = set(other_families)
    if placed:
        families.add(target_family)
    pool = dynamic_doctrine_pool_fast(
        faction, wave, removed=set(ordinary_owned), tb_owned=set(owned),
        placed_families=families, tb_mult=tb_multiplier, t2_bonus=t2_bonus)
    prefix = f'TB{target_family}D'
    return [(name, weight * (1 + amplifiers) if name.startswith(prefix) else weight)
            for name, weight in pool]


def run(seed, target='CB14', faction='Lions', eleanor=False, policy='isolated',
        guaranteed_blueprint=False, floor=10):
    if target not in TB_FAMILIES:
        raise ValueError('target has no standard building-Doctrine family')
    if policy not in POLICIES:
        raise ValueError('unknown family policy')
    roster = load_blueprint_roster(faction={'Lions':'Faction2','Iron':'Faction1','Pargan':'Faction3'}[faction])
    bp_code = 'BP' + target
    entry = next((x for x in roster if x.code == bp_code), None)
    if entry is None or entry.tier != 3:
        raise ValueError('target must be eligible tier-3 bundle Blueprint')
    rng = random.Random(seed)
    result = ExpertiseResult(target, eleanor, policy)
    if guaranteed_blueprint:
        result.blueprint_wave = 1
    ordinary_owned, tb_owned = set(), set()
    tb_multiplier, t2_bonus = 3, 0
    tier_bonus = {2:0, 3:0}
    other_ids = sorted(TB_FAMILIES - {target})[:len(POLICIES[policy])]
    target_family = target
    other_families = [(name, wave) for name, wave in zip(other_ids, POLICIES[policy])]
    for wave in range(1, 36):
        built = result.blueprint_wave is not None and wave >= construction_wave(result.blueprint_wave, floor)
        if built and result.construction_wave is None:
            result.construction_wave = wave
        if result.amplifier_acquired and not built:
            result.amplifier_saved_before_build = True
        assigned = min(2, result.amplifier_acquired) if built else 0
        if assigned and result.amplifier_assignment_wave is None:
            result.amplifier_assignment_wave = wave
        if assigned:
            result.amplifier_active_waves += 1
        pool = target_doctrine_weights(faction, wave, target_family, tb_owned, built,
            assigned, ordinary_owned, (f for f, first in other_families if wave >= first), tb_multiplier, t2_bonus)
        bp_weights = blueprint_weights(roster, wave,
            extra_tier_weights={tier:tier_bonus[tier] + (20 if eleanor else 0) for tier in (2,3)},
            type_bonus_percent={bp_code:100*assigned} if assigned else None)
        cards = generate_mc_cards(rng, bp_weights, pool)
        for card in cards:
            result.amplifier_offer_count += sum(kind == 'doctrine' and name in AMPLIFIER_DOCTRINES for kind,name,_ in card)
            result.attenuator_offer_count += sum(kind == 'doctrine' and name in ATTENUATOR_DOCTRINES for kind,name,_ in card)
        def target_priority(name):
            prefix = f'TB{target_family}D'
            if not name.startswith(prefix) or name in tb_owned:
                return 0
            level = name[len(prefix):]
            if level == '7':
                return 100
            if level not in ('1','2','3','4','5','6'):
                return 0
            # Either branch can unlock D7. Prefer the branch already further
            # along; at a tie prefer cost D1-D3 as a declared policy choice.
            cost_progress = sum(prefix+str(i) in tb_owned for i in (1,2,3))
            efficiency_progress = sum(prefix+str(i) in tb_owned for i in (4,5,6))
            if cost_progress == 3 or efficiency_progress == 3:
                return 0
            route = 'cost' if cost_progress >= efficiency_progress else 'efficiency'
            return 10 + int(level) if ((route == 'cost' and level in ('1','2','3')) or (route == 'efficiency' and level in ('4','5','6'))) else 1

        def score(card):
            expertise = max((target_priority(name) for kind,name,_ in card if kind == 'doctrine'),default=0)
            amplifier = sum(kind == 'doctrine' and name in AMPLIFIER_DOCTRINES and name not in ordinary_owned
                            for kind,name,_ in card)
            target_bp = sum(kind == 'bp' and name == bp_code for kind,name,_ in card)
            return (amplifier if result.amplifier_acquired < 2 else 0,
                    expertise, target_bp if result.blueprint_wave is None else 0,
                    sum(kind == 'doctrine' for kind,_,_ in card))
        chosen = max(cards, key=score)
        def record_doctrine_offers(names):
            result.amplifier_offer_count += sum(n in AMPLIFIER_DOCTRINES for n in names)
            result.attenuator_offer_count += sum(n in ATTENUATOR_DOCTRINES for n in names)

        def acquire_doctrine(name, depth=0):
            nonlocal tb_multiplier, t2_bonus
            if depth >= 50:
                raise RuntimeError('nested Doctrine depth exceeded')
            if name.startswith('TB'):
                if name in tb_owned:
                    return
                tb_owned.add(name)
                for level in range(1,8):
                    if name == f'TB{target_family}D{level}':
                        result.expertise_waves.setdefault(level, wave)
                        if level == 7:
                            result.d7_wave = wave
                            result.d7_route = ('both' if f'TB{target_family}D3' in tb_owned and f'TB{target_family}D6' in tb_owned
                                               else 'cost' if f'TB{target_family}D3' in tb_owned else 'efficiency')
            else:
                if name in ordinary_owned:
                    return
                ordinary_owned.add(name)
                if name in AMPLIFIER_DOCTRINES:
                    result.amplifier_acquired += 1
                if name in ATTENUATOR_DOCTRINES:
                    result.attenuator_acquired += 1
                if name == 'D1_19':
                    t2_bonus += 6
                elif name == 'D2_40':
                    tb_multiplier += 4
                elif name == 'D2_01':
                    tier_bonus[2] += 10
                elif name == 'D3_11':
                    tier_bonus[3] += 5
            if name in ('D2_40','D2_06'):
                for size in ((2,) if name == 'D2_40' else (3,3)):
                    fresh = target_doctrine_weights(faction, wave, target_family,
                        tb_owned, built, assigned, ordinary_owned,
                        (f for f, first in other_families if wave >= first),
                        tb_multiplier, t2_bonus)
                    if not fresh:
                        continue
                    offered = sample_doctrines(rng, fresh, min(size,len(fresh)))
                    record_doctrine_offers(offered)
                    result.nested_drafts += 1
                    def draft_priority(n):
                        return (n in AMPLIFIER_DOCTRINES and result.amplifier_acquired < 2,
                                target_priority(n),
                                n == 'D2_40', n == 'D2_06')
                    acquire_doctrine(max(offered,key=draft_priority),depth+1)

        for kind, name, _ in chosen:
            if kind == 'bp' and name == bp_code and result.blueprint_wave is None:
                result.blueprint_wave = wave
            elif kind == 'doctrine':
                acquire_doctrine(name)
        if eleanor and wave % 2 == 0:
            result.eleanor_drafts += 1
            bp_pool = [(k,v) for k,v in blueprint_weights(roster,wave,
                extra_tier_weights={tier:tier_bonus[tier]+20 for tier in (2,3)},
                type_bonus_percent={bp_code:100*assigned} if assigned else None).items() if v>0]
            if bp_pool:
                # Three distinct Blueprint offers, selected from one weighted pool.
                offers = []
                for _ in range(min(3,len(bp_pool))):
                    chosen_bp = pick_weighted(bp_pool,rng)
                    offers.append(chosen_bp)
                    bp_pool = [(k,v) for k,v in bp_pool if k != chosen_bp]
                if bp_code in offers and result.blueprint_wave is None:
                    result.blueprint_wave = wave
        if wave in CHECKPOINTS:
            result.checkpoints[wave] = {level:level in result.expertise_waves for level in range(1,8)}
    return result


def summarize(trials=1000, target='CB14', faction='Lions', guaranteed_blueprint=False):
    output = {}
    for policy in POLICIES:
        for eleanor in (False,True):
            runs = [run(seed,target,faction,eleanor,policy,guaranteed_blueprint) for seed in range(1,trials+1)]
            output[f'{policy}/{"eleanor" if eleanor else "baseline"}'] = {
                'trials':trials,
                'expertise': {str(level):sum(level in r.expertise_waves for r in runs)/trials for level in range(1,8)},
                'd7_completed':sum(r.d7_wave is not None for r in runs)/trials,
                'd7_routes':{route:sum(r.d7_route == route for r in runs) for route in ('cost','efficiency','both')},
                'checkpoints': {str(w):{str(level):sum(r.checkpoints[w][level] for r in runs)/trials for level in range(1,8)} for w in CHECKPOINTS},
                'blueprint_acquired':sum(r.blueprint_wave is not None for r in runs)/trials,
                'constructed':sum(r.construction_wave is not None for r in runs)/trials,
                'amplifier_offers':sum(r.amplifier_offer_count for r in runs),
                'amplifier_acquired':sum(r.amplifier_acquired for r in runs),
                'amplifier_active_waves':sum(r.amplifier_active_waves for r in runs),
                'attenuator_offers':sum(r.attenuator_offer_count for r in runs),
                'attenuator_acquired':sum(r.attenuator_acquired for r in runs),
                'attenuator_zero_offer_runs':sum(r.attenuator_offer_count == 0 for r in runs),
                'amplifier_saved_runs':sum(r.amplifier_saved_before_build for r in runs),
                'amplifier_assigned_runs':sum(r.amplifier_assignment_wave is not None for r in runs),
                'nested_drafts':sum(r.nested_drafts for r in runs),
                'eleanor_drafts':sum(r.eleanor_drafts for r in runs),
            }
    return output
