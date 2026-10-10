"""Card-level MC/Amplifier choice policy for already generated rewards.

Candidate generation and Blueprint eligibility are separate responsibilities.
A selected card grants every item on it, not a cherry-picked Blueprint slot.
"""
from collections import Counter


def choose_card(cards, state, conflict='mc_first', package=None, code_names=None, acquired=None, lions=False,
                attenuators_owned=0):
    """Return index of best card, or None if no cards.

    Cards are sequences of (kind, identity, quantity). 'bp' identity must be
    normalized by the caller to 'MC' or 'Amplifier' where appropriate.
    This deterministic baseline scores all Blueprint copies in a card, but
    favors first access to either strategic building over other Blueprints.
    """
    if conflict not in ('mc_first', 'amplifier_first'):
        raise ValueError('unknown conflict policy')
    if not cards:
        return None
    if package is not None:
        from mc_doctrines import AMPLIFIER_DOCTRINES, ATTENUATOR_DOCTRINES, SPECIAL_BUDGETS_DOCTRINE
        from mc_packages import evaluate_blueprint, BLUEPRINT_NAMES
        from collections import Counter as _Counter
        counts = _Counter(acquired or {})
        def package_score(card):
            mapped = [(code_names or BLUEPRINT_NAMES).get(identity, identity) for kind, identity, qty in card if kind == 'bp' and qty > 0]
            values = [evaluate_blueprint(name, package, counts, lions) for name in mapped]
            doctrines = {identity for kind, identity, qty in card if kind == 'doctrine' and qty > 0}
            mc = sum(qty for kind, identity, qty in card if kind == 'bp' and identity == 'MC')
            need_amp = not (state.amplifier_built or state.amplifier_in_hand)
            special = SPECIAL_BUDGETS_DOCTRINE in doctrines
            first_mc = bool(mc and not state.mc_owned)
            amplifier = bool(need_amp and doctrines.intersection(AMPLIFIER_DOCTRINES))
            extra_mc = bool(mc and state.mc_owned)
            attenuator = bool(attenuators_owned < 2 and doctrines.intersection(ATTENUATOR_DOCTRINES))
            ordinary = max(values, default=(0, 0))
            established = state.mc_selective_this_wave
            if established:
                strategic = max((evaluate_blueprint(name, package, counts, lions)
                                 for name in mapped if name != 'MC'), default=(0, 0))
                return (special, first_mc, amplifier, attenuator,
                        strategic, extra_mc, bool(doctrines), len(doctrines), mc,
                        sum(qty for kind, name, qty in card if kind == 'bp'))
            return (special, first_mc, amplifier, extra_mc, attenuator,
                    ordinary, bool(doctrines), len(doctrines), mc,
                    sum(qty for kind, identity, qty in card if kind == 'bp'))
        return max(range(len(cards)), key=lambda i: package_score(cards[i]))
    need_amp = state.amplifier_built + state.amplifier_in_hand == 0
    def score(card):
        amp_doctrine = any(kind == 'doctrine' and identity in ('D1_45', 'D2_42') for kind, identity, qty in card)
        bp = Counter()
        for kind, identity, qty in card:
            if qty < 0:
                raise ValueError('negative reward quantity')
            if kind == 'bp':
                bp[identity] += qty
        mc = bp['MC']
        amp = bp['Amplifier']
        if conflict == 'mc_first':
            priority = (bool(mc), bool((amp or amp_doctrine) and need_amp))
        else:
            priority = (bool((amp or amp_doctrine) and need_amp), bool(mc))
        return (*priority, mc, amp if need_amp else 0, sum(bp.values()))
    return max(range(len(cards)), key=lambda i: score(cards[i]))


def apply_selected_card(cards, index, state, red=False):
    """Grant selected Blueprint contents; Red duplication is ordinary-only."""
    if index is None:
        return
    for kind, identity, qty in cards[index]:
        if kind == 'bp' and identity in ('MC', 'Amplifier'):
            state.acquire(identity, copies=qty, ordinary=True, red=red)
