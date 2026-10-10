"""Provisional complete reinforcement cards using existing reward-category weights.

Blueprint roster and doctrine eligibility must be supplied by the caller.
Exact game duplicate-card validation is still a separate verification task.
"""
from reinforcement_model import OUTER, Q, pick_weighted, sample_doctrines
from mc_choice import choose_card, apply_selected_card


def _generate_screen(rng, blueprint_weights, doctrine_weights=(), card_count=3):
    """Return cards of two (kind, identity, quantity) items each.

    Doctrine identities are sampled without replacement within a screen.
    Blueprint identities are sampled with replacement across slots, as in
    the game's ordinary weighted Blueprint selector.
    """
    if card_count < 1:
        raise ValueError('card_count must be positive')
    bp_pool = [(key, weight) for key, weight in blueprint_weights.items() if weight > 0]
    doctrine_pool = [(key, weight) for key, weight in doctrine_weights if weight > 0]
    items = []
    for _ in range(card_count * 2):
        category = pick_weighted(OUTER, rng)
        if category == 'bp' and not bp_pool:
            raise ValueError('no eligible Blueprints')
        if category == 'doctrine' and not doctrine_pool:
            raise ValueError('no eligible Doctrines')
        if category == 'bp':
            items.append(('bp', pick_weighted(bp_pool, rng), 1))
        elif category == 'doctrine':
            identity = sample_doctrines(rng, doctrine_pool, 1)[0]
            doctrine_pool = [(key, weight) for key, weight in doctrine_pool if key != identity]
            items.append(('doctrine', identity, 1))
        else:
            items.append((category, category, pick_weighted(Q[category], rng)))
    rng.shuffle(items)
    return [items[i:i + 2] for i in range(0, len(items), 2)]


def generate_mc_cards(rng, blueprint_weights, doctrine_weights=(), card_count=3,
                      max_screen_retries=100):
    """Reject exact duplicate two-item cards and regenerate the entire screen.

    Finite retry cap is a simulation safety boundary, not a game limit.
    """
    if max_screen_retries < 1:
        raise ValueError('max_screen_retries must be positive')
    for _ in range(max_screen_retries):
        cards = _generate_screen(rng, blueprint_weights, doctrine_weights, card_count)
        identities = [tuple(sorted(card)) for card in cards]
        if len(set(identities)) == len(identities):
            return cards
    raise RuntimeError('duplicate-card screen retry limit reached')


def reinforcement_step(rng, state, blueprint_weights, doctrine_weights=(),
                       tander=False, red=False, conflict='mc_first',
                       package=None, code_names=None, acquired=None, lions=False,
                       attenuators_owned=0):
    cards = generate_mc_cards(rng, blueprint_weights, doctrine_weights, 4 if tander else 3)
    index = choose_card(cards, state, conflict=conflict, package=package,
                        code_names=code_names, acquired=acquired, lions=lions,
                        attenuators_owned=attenuators_owned)
    apply_selected_card(cards, index, state, red=red)
    return cards, index
