"""Composable wave progression for MC-chain experiments.

This is a conditional simulator: callers supply verified eligible Blueprint and
Doctrine pools. Eleanor's draft cadence/phase and MC 3A draft sampling are
explicit assumptions until game asset validation is complete.
"""
import random
from collections import Counter
from dataclasses import dataclass
from mc_state import MCState
from mc_family_policy import FamilyIntroduction
from mc_weights import blueprint_weights
from mc_reinforcement import reinforcement_step
from mc_draft import sample_rejection_draft
from mc_roster import blueprint_identity
from mc_packages import evaluate_blueprint, BLUEPRINT_NAMES, attenuation_candidates, SUPPORTS, PACKAGES
from mc_doctrines import MCDocState, apply_selected_doctrines, acquire_with_drafts, AMPLIFIER_DOCTRINES, SPECIAL_BUDGETS_DOCTRINE
from reinforcement_model import sample_doctrines


@dataclass(frozen=True)
class WaveConfig:
    faction: str = 'Lions'
    tier3_wave: int = 40
    max_drafts_per_wave: int = 10000
    tander: bool = False
    red: bool = False
    magel: bool = False
    tier1_amplifier_doctrine_from_wave1: bool = False
    eleanor: bool = False
    eleanor_starting_mc_1a_equivalent: int = 10  # +2 Tier 2/3 rarity per equivalent MC 1A
    eleanor_initial_tier23_dampening: bool = False  # explicit: no initial dampening
    eleanor_first_wave: int = 2
    eleanor_cadence: int = 2
    conflict: str = 'mc_first'
    amplifier_effect_enabled: bool = True
    amplifier_always_on: bool = False  # Counterfactual: one saved Amplifier active from outset
    early_3a_interval: int | None = None  # None = original Wave-40-only baseline
    package: str | None = None
    blueprint_names: dict | None = None
    mc_1a_effect_enabled: bool = True
    mc_3a_effect_enabled: bool = True
    attenuation_enabled: bool = False
    attenuation_start_wave: int = 1
    attenuation_switch_wave: int = 40
    attenuation_policy: str = 'tier1_only'  # baseline; alternatives: wave40_switch, highest_weight
    mc_build_target: int | None = None
    mc_reserve_target: int = 0
    mc_batch_size: int = 3
    mc_replenish_source: str = 'both'  # both, draft_only, reinforcement_only
    mc_dynamic_selectivity: bool = False  # Counterfactual: recompute after inventory changes
    mc_construction_policy: str = 'threshold'  # threshold, draft_replenish, preserve, continuous
    third_tier1_family: str | None = None  # verified tower ID, e.g. CBxx
    immediate_3a: bool = False  # Counterfactual: unlimited 3A upgrades from Wave 1


def simulate_run(entries, doctrine_pool, waves=60, seed=1, config=None,
                 extra_tier_weights=None, type_bonus_percent=None):
    """Run one scenario and return (state, wave snapshots).

    Wave 40 assumption: all built MCs receive 3A immediately, and every newly
    acquired MC can be built/upgraded in the same wave. Censored runs stop.
    """
    config = config or WaveConfig()
    if entries is None:
        from mc_roster import load_blueprint_roster
        faction_code = {'Iron': 'Faction1', 'Lions': 'Faction2', 'Pargan': 'Faction3'}[config.faction]
        entries = load_blueprint_roster(faction=faction_code)
    if waves < 1 or config.tier3_wave < 1 or config.max_drafts_per_wave < 0:
        raise ValueError('invalid simulation horizon or draft cap')
    if config.eleanor_starting_mc_1a_equivalent < 0:
        raise ValueError('invalid Eleanor starting rarity bonus')
    if config.eleanor and config.eleanor_initial_tier23_dampening:
        raise ValueError('Eleanor initial Tier 2/3 dampening is not modeled or supported')
    if config.eleanor and (config.eleanor_cadence < 1 or config.eleanor_first_wave < 1):
        raise ValueError('invalid Eleanor cadence')
    if config.early_3a_interval is not None and config.early_3a_interval < 1:
        raise ValueError('invalid early 3A interval')
    rng = random.Random(seed)
    state = MCState()
    state.mc_build_target = config.mc_build_target
    state.mc_reserve_target = config.mc_reserve_target
    state.mc_batch_size = config.mc_batch_size
    if config.mc_construction_policy not in ('threshold', 'draft_replenish', 'preserve', 'continuous'):
        raise ValueError('unknown MC construction policy')
    if config.mc_replenish_source not in ('both', 'draft_only', 'reinforcement_only'):
        raise ValueError('unknown MC replenishment source')
    if config.mc_reserve_target and (config.mc_build_target is None or config.mc_build_target < 1 or config.mc_batch_size < 1):
        raise ValueError('reserve policy requires positive establishment target and batch size')
    doc_state = MCDocState(faction=config.faction) if doctrine_pool is None else None
    family_policy = FamilyIntroduction(third_tower=config.third_tier1_family)
    if config.tier1_amplifier_doctrine_from_wave1:
        if doc_state is None:
            raise ValueError("saved Doctrine requires dynamic Doctrine pool")
        doc_state.acquire("D1_45", state)
    history = []
    blueprint_acquisitions = Counter()
    mc_draft_outcomes = Counter()
    early_3a_credits = 0
    attenuated = []
    blueprint_tiers = {blueprint_identity(entry.code): entry.tier for entry in entries}

    def apply_attenuation():
        if not (config.attenuation_enabled and config.package and doc_state
                and state.wave >= config.attenuation_start_wave):
            return
        available = min(2, doc_state.attenuators_owned)
        # Retarget existing Attenuators at the Wave-40 transition.
        # A fresh unattenuated pool is used to compare candidate weights.
        if not available:
            attenuated.clear()
            return
        attenuated.clear()
        weights = current_weights()
        candidates = attenuation_candidates(weights, config.package, config.blueprint_names)
        if config.attenuation_policy == 'tier1_only' or (config.attenuation_policy == 'wave40_switch' and state.wave < config.attenuation_switch_wave):
            candidates = [code for code in candidates if blueprint_tiers.get(code) == 1]
        elif config.attenuation_policy == 'wave40_switch':
            higher = [code for code in candidates if blueprint_tiers.get(code) in (2, 3)]
            candidates = higher or candidates
        elif config.attenuation_policy != 'highest_weight':
            raise ValueError('unknown attenuation policy')
        candidates.sort(key=lambda code: (-weights[code], code))
        attenuated.extend(candidates[:available])

    def current_weights():
        amp_count = (state.amplifier_mc_targeted + int(config.amplifier_always_on)) if config.amplifier_effect_enabled else 0
        bonuses = dict(type_bonus_percent or {})
        if amp_count:
            bonuses['BPSB07'] = bonuses.get('BPSB07', 0) + 100 * amp_count
        raw = blueprint_weights(
            entries, state.wave, state.mc_1a_active if config.mc_1a_effect_enabled else 0,
            amplified_types=(),
            extra_tier_weights={tier: (extra_tier_weights or {}).get(tier, 0) +
                                (2 * config.eleanor_starting_mc_1a_equivalent if config.eleanor and tier in (2, 3) else 0) +
                                (doc_state.blueprint_tier_bonus.get(tier, 0) if doc_state else 0)
                                for tier in (1, 2, 3)},
            type_bonus_percent=bonuses)
        return {blueprint_identity(key): value for key, value in raw.items()
                if key not in attenuated}

    def acquired_names():
        names = config.blueprint_names or BLUEPRINT_NAMES
        counts = Counter()
        for code, quantity in blueprint_acquisitions.items():
            counts[names.get(code, code)] += quantity
        return counts

    def refresh_selectivity():
        reserve_full = (state.mc_established and config.mc_reserve_target > 0
                        and state.mc_in_hand >= config.mc_reserve_target)
        state.mc_selective_this_wave = reserve_full or (state.mc_established and config.mc_replenish_source == 'draft_only')
        state.mc_draft_selective_this_wave = reserve_full or (state.mc_established and config.mc_replenish_source == 'reinforcement_only')
        return reserve_full

    def choose_draft(choices):
        if config.mc_dynamic_selectivity:
            refresh_selectivity()
        if not choices:
            return None
        if config.package is None:
            need_amp = not (state.amplifier_built or state.amplifier_in_hand)
            if config.conflict == 'amplifier_first' and need_amp and 'Amplifier' in choices:
                return 'Amplifier'
            if 'MC' in choices:
                return 'MC'
            if need_amp and 'Amplifier' in choices:
                return 'Amplifier'
            return choices[0]
        names = config.blueprint_names or BLUEPRINT_NAMES
        acquired = acquired_names()
        def priority(identity):
            name = names.get(identity, identity)
            if name == 'Amplifier' and (state.amplifier_built or state.amplifier_in_hand):
                return (1, 0)
            established = state.mc_draft_selective_this_wave
            if established and name == 'MC':
                return (1, 0)
            return evaluate_blueprint(name, config.package, acquired, config.red)
        return max(choices, key=priority)

    def select_special_mc(_state):
        selected = choose_draft(sample_rejection_draft(current_weights(), rng, draws=5))
        if selected is None:
            mc_draft_outcomes['empty'] += 1
        elif selected == 'MC':
            mc_draft_outcomes['mc_reinvestment'] += 1
        else:
            name = (config.blueprint_names or BLUEPRINT_NAMES).get(selected, selected)
            tier = evaluate_blueprint(name, config.package, acquired_names(), config.red)[0] if config.package else 0
            if tier >= 2 and name in SUPPORTS:
                mc_draft_outcomes['hv_support'] += 1
            elif tier >= 2 and config.package and name in PACKAGES[config.package]:
                mc_draft_outcomes['hv_offense'] += 1
            elif tier >= 2:
                mc_draft_outcomes['hv_other'] += 1
            else:
                mc_draft_outcomes['low_value'] += 1
        if selected is not None and selected != 'MC':
            blueprint_acquisitions[selected] += 1
            if selected == 'Amplifier':
                state.acquire('Amplifier')
                state.build(mc_count=0, tier3_wave=effective_tier3_wave)
        return selected == 'MC'

    def build_mc_policy():
        if not config.mc_reserve_target:
            state.build(tier3_wave=effective_tier3_wave)
        elif not state.mc_established:
            remaining = max(0, config.mc_build_target - state.mc_built)
            state.build(mc_count=min(state.mc_in_hand, remaining), tier3_wave=effective_tier3_wave)
            if state.mc_built >= config.mc_build_target:
                state.mc_established = True
        else:
            state.build(mc_count=0, tier3_wave=effective_tier3_wave)

    effective_tier3_wave = 1 if config.immediate_3a else config.tier3_wave

    for wave in range(1, waves + 1):
        state.wave = wave
        reserve_full = refresh_selectivity()
        if doc_state is not None:
            acquired_towers = {entry.code[2:] for entry in entries
                               if blueprint_acquisitions.get(blueprint_identity(entry.code), 0) > 0}
            doc_state.placed_families = family_policy.advance(wave, acquired_towers, rng)
        # Existing MCs receive their assumed affordable 3A at the threshold.
        state.build(mc_count=0, amplifier_count=0, tier3_wave=effective_tier3_wave)
        apply_attenuation()
        if state.mc_established and config.mc_reserve_target:
            if config.mc_construction_policy == 'threshold':
                construction_count = min(config.mc_batch_size, state.mc_in_hand) if reserve_full else 0
            elif config.mc_construction_policy == 'draft_replenish':
                construction_count = min(config.mc_batch_size, state.mc_in_hand) if not reserve_full else 0
            elif config.mc_construction_policy == 'continuous':
                construction_count = min(config.mc_batch_size, state.mc_in_hand)
            else:
                construction_count = min(config.mc_batch_size, max(0, state.mc_in_hand - config.mc_reserve_target))
            if construction_count:
                state.build(mc_count=construction_count, amplifier_count=0,
                            tier3_wave=effective_tier3_wave)
        if config.mc_dynamic_selectivity:
            refresh_selectivity()  # Construction has spent the reserve.
        weights = current_weights()
        current_doctrines = doc_state.pool(wave) if doc_state is not None else (doctrine_pool(wave, state) if callable(doctrine_pool) else doctrine_pool)
        try:
            cards, selected = reinforcement_step(
                rng, state, weights, current_doctrines,
            tander=(config.tander or (doc_state is not None and SPECIAL_BUDGETS_DOCTRINE in doc_state.ordinary_owned)),
            red=config.red, conflict=config.conflict,
            package=config.package, code_names=config.blueprint_names,
            acquired=acquired_names(),
            lions=config.red,
            attenuators_owned=doc_state.attenuators_owned if doc_state else 0)
        except ValueError as exc:
            if str(exc) != 'no eligible Doctrines':
                raise
            state.softlock_wave = wave
            break
        if selected is not None:
            for kind, identity, quantity in cards[selected]:
                if kind == 'bp':
                    blueprint_acquisitions[identity] += quantity * (2 if config.red else 1)
        if doc_state is not None:
            apply_selected_doctrines(cards, selected, doc_state, state, rng=rng, wave=wave)
        build_mc_policy()
        apply_attenuation()

        # Magel: normal reinforcement precedes every-even-wave Doctrine draft.
        if config.magel and wave % 2 == 0:
            if doc_state is None:
                raise ValueError("Magel requires dynamic Doctrine pool")
            pool = doc_state.pool(wave)
            if pool:
                offered = sample_doctrines(rng, pool, min(3, len(pool)))
                chosen = next((x for x in offered if x == SPECIAL_BUDGETS_DOCTRINE),
                              next((x for x in offered if x in AMPLIFIER_DOCTRINES), offered[0]))
                acquire_with_drafts(doc_state, chosen, state, rng, wave)
                build_mc_policy()
                apply_attenuation()

        # Optional separate Eleanor choose-one-of-three Blueprint draft.
        # Cadence phase is parameterized; its exact game sampling is unresolved.
        if (config.eleanor and wave >= config.eleanor_first_wave
                and (wave - config.eleanor_first_wave) % config.eleanor_cadence == 0):
            draft = sample_rejection_draft(current_weights(), rng, draws=3)
            selected_draft = choose_draft(draft)
            if selected_draft is not None:
                blueprint_acquisitions[selected_draft] += 1
                if selected_draft in ('MC', 'Amplifier'):
                    state.acquire(selected_draft)
            build_mc_policy()

        # Early 3A opportunities accrue at fixed intervals and carry forward.
        # Wave 40 remains an unlimited upgrade catch-up point.
        if wave < config.tier3_wave and config.early_3a_interval is not None:
            if wave % config.early_3a_interval == 0:
                early_3a_credits += 1
            affordable = min(early_3a_credits, state.mc_built - state.mc_3a_processed)
            state.upgrade_3a(affordable)
            early_3a_credits -= affordable
        mc_before_drafts = state.mc_owned
        if not config.mc_3a_effect_enabled:
            state.draft_queue.clear()
        state.resolve_drafts(select_special_mc,
                             max_drafts=config.max_drafts_per_wave,
                             tier3_wave=effective_tier3_wave)
        mc_from_3a = state.mc_owned - mc_before_drafts
        blueprint_acquisitions['MC'] += mc_from_3a
        history.append({
            'wave': wave, 'mc_owned': state.mc_owned, 'mc_built': state.mc_built,
            'mc_in_hand': state.mc_in_hand,
            'mc_established': state.mc_established,
            'mc_selective_this_wave': state.mc_selective_this_wave,
            'mc_draft_selective_this_wave': state.mc_draft_selective_this_wave,
            'mc_1a_active': state.mc_1a_active,
            'amplifier_built': state.amplifier_built,
            'amplifier_mc_targeted': state.amplifier_mc_targeted,
            'drafts_resolved': state.drafts_resolved,
            'draft_queue': len(state.draft_queue), 'censored': state.censored,
            'selected_card': selected,
            'blueprint_acquisitions': dict(blueprint_acquisitions),
            'attenuated': tuple(attenuated),
            'attenuators_owned': doc_state.attenuators_owned if doc_state else 0,
            'doctrine_families': tuple(sorted(doc_state.placed_families)) if doc_state else (),
            'mc_from_3a_this_wave': mc_from_3a,
            'mc_draft_outcomes': dict(mc_draft_outcomes),
        })
        if state.censored:
            break
    return state, history
