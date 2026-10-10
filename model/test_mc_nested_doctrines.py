import random
import unittest
from mc_doctrines import MCDocState, acquire_with_drafts, apply_selected_doctrines
from mc_state import MCState


class NestedDoctrineTests(unittest.TestCase):
    def test_d2_40_draft_and_multiplier(self):
        doc, state = MCDocState(), MCState()
        result = acquire_with_drafts(doc, 'D2_40', state, random.Random(2), 30)
        self.assertIn('D2_40', doc.ordinary_owned)
        self.assertEqual(doc.tb_mult, 7)
        self.assertEqual(len(doc.draft_events), 1)
        self.assertEqual(len(doc.draft_events[0][1]), 2)
        self.assertTrue(set(result).issubset(doc.ordinary_owned))

    def test_d2_06_two_drafts_and_idempotence(self):
        doc, state = MCDocState(), MCState()
        acquire_with_drafts(doc, 'D2_06', state, random.Random(3), 30)
        self.assertEqual(len(doc.draft_events), 2)
        self.assertEqual(acquire_with_drafts(doc, 'D2_06', state, random.Random(3), 30), ())
        self.assertEqual(len(doc.draft_events), 2)

    def test_nested_amplifier_and_tier_effect(self):
        doc, state = MCDocState(), MCState()
        doc.pool = lambda wave: [('D1_45', 100), ('D3_11', 100)]
        acquire_with_drafts(doc, 'D2_06', state, random.Random(1), 30)
        self.assertEqual(state.amplifier_in_hand, 1)
        self.assertIsNone(doc.blueprint_tier_bonus.get(3))
        acquire_with_drafts(doc, 'D3_11', state, random.Random(1), 30)
        self.assertEqual(doc.blueprint_tier_bonus.get(3), 5)

    def test_second_draft_observes_first_acquisition(self):
        doc, state = MCDocState(), MCState()
        pools = []
        def pool(wave):
            available = [('D1_45', 100), ('D3_11', 100)]
            current = [(code, weight) for code, weight in available
                       if code not in doc.ordinary_owned]
            pools.append(tuple(code for code, _ in current))
            return current
        doc.pool = pool
        acquire_with_drafts(doc, 'D2_06', state, random.Random(1), 30)
        self.assertEqual(len(doc.draft_events), 2)
        self.assertEqual(len(pools), 2)
        self.assertNotIn(doc.draft_events[0][2], pools[1])
        self.assertEqual(state.amplifier_in_hand, 1)
        self.assertEqual(doc.blueprint_tier_bonus.get(3), 5)

    def test_selected_card_uses_nested_resolution(self):
        doc, state = MCDocState(), MCState()
        doc.pool = lambda wave: [('D1_45', 100)]
        cards = [[('doctrine', 'D2_40', 1)]]
        grants = apply_selected_doctrines(cards, 0, doc, state, rng=random.Random(1), wave=30)
        self.assertEqual(grants, ('D1_45',))
        self.assertEqual(state.amplifier_in_hand, 1)


if __name__ == '__main__':
    unittest.main()
