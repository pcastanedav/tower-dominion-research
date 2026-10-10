"""Conditional MC wave runner; caller supplies verified Blueprint/doctrine pools.

This is not a calibrated game probability simulator. Special draft law assumes
five iid weighted Blueprint cards conditioned on unique identities.
"""
import random
from dataclasses import dataclass
from mc_state import MCState
from mc_weights import blueprint_weights
from mc_reinforcement import reinforcement_step
from mc_draft import sample_rejection_draft


@dataclass(frozen=True)
class WaveSnapshot:
    wave: int
    mc_owned: int
    mc_built: int
    amplifier_built: int
    mc_1a_active: int
    drafts_resolved: int
    censored: bool


def run_mc_waves(entries, doctrine_pool, waves=60, seed=1, tander=False,
                 red=False, eleanor=False, tier3_wave=40, max_drafts=10000,
                 extra_tier_weights=None, conflict='mc_first',
                 eleanor_due=None, special_draft_size=5):
    """Run a reproducible conditional scenario with caller-supplied pools.

    eleanor_due(wave) must be explicitly supplied for Eleanor; cadence is not
    guessed. Amplifier is modeled as an acquired Doctrine-granted Blueprint,
    NOT an ordinary Blueprint candidate. Its acquisition must be injected by
    an external doctrine-acquisition policy (not yet integrated).
    """
    if waves < 1 or max_drafts < 0:
        raise ValueError('invalid simulation horizon or draft limit')
    if eleanor and eleanor_due is None:
        raise ValueError('Eleanor cadence must be explicitly supplied')
    rng = random.Random(seed)
    state = MCState()
    history = []
    for wave in range(1, waves + 1):
        state.wave = wave
        weights = blueprint_weights(entries, wave, state.mc_1a_active,
                                    amplified_types=('MC',) if state.amplifier_mc_targeted else (),
                                    extra_tier_weights=extra_tier_weights)
        doctrines = doctrine_pool(wave, state) if callable(doctrine_pool) else doctrine_pool
        reinforcement_step(rng, state, weights, doctrines, tander=tander,
                           red=red, conflict=conflict)
        if eleanor and eleanor_due(wave):
            # Provisional Eleanor choose-1-of-3 Blueprint draft, no Red duplication.
            candidates = sample_rejection_draft(weights, rng, 3)
            if 'MC' in candidates:
                state.acquire('MC')
        state.build(tier3_wave=tier3_wave)
        if state.draft_queue:
            def special_offer(current):
                current_weights = blueprint_weights(
                    entries, wave, current.mc_1a_active,
                    amplified_types=('MC',) if current.amplifier_mc_targeted else (),
                    extra_tier_weights=extra_tier_weights)
                return 'MC' in sample_rejection_draft(current_weights, rng, special_draft_size)
            state.resolve_drafts(special_offer, max_drafts=max_drafts,
                                 tier3_wave=tier3_wave)
        history.append(WaveSnapshot(wave, state.mc_owned, state.mc_built,
                                    state.amplifier_built, state.mc_1a_active,
                                    state.drafts_resolved, state.censored))
        if state.censored:
            break
    return state, history
