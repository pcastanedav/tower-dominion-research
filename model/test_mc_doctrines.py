import unittest
from mc_doctrines import MCDocState, apply_selected_doctrines
from mc_state import MCState
from mc_choice import choose_card
from mc_wave60 import simulate_run, WaveConfig
from mc_roster import load_blueprint_roster


class AmplifierDoctrineTests(unittest.TestCase):
    def test_grant_once_and_independent_tiers(self):
        doc, state = MCDocState(), MCState()
        self.assertTrue(doc.acquire('D1_45', state))
        self.assertFalse(doc.acquire('D1_45', state))
        self.assertTrue(doc.acquire('D2_42', state))
        self.assertEqual(state.amplifier_in_hand, 2)

    def test_selected_card_priority_and_grant(self):
        doc, state = MCDocState(), MCState()
        cards = [[('doctrine', 'D1_45', 1)], [('bp', 'OTHER', 1)]]
        idx = choose_card(cards, state, conflict='amplifier_first')
        self.assertEqual(idx, 0)
        self.assertEqual(apply_selected_doctrines(cards, idx, doc, state), ('D1_45',))
        self.assertEqual(state.amplifier_in_hand, 1)

    def test_pool_excludes_owned(self):
        doc, state = MCDocState(), MCState()
        doc.acquire('D1_45', state)
        self.assertNotIn('D1_45', dict(doc.pool(20)))

    def test_blueprint_tier_currency_and_doctrine_rarity(self):
        doc, state = MCDocState(), MCState()
        for code in ('D2_01', 'D3_11', 'D1_19', 'D2_40'):
            self.assertFalse(doc.acquire(code, state))
        self.assertEqual(doc.blueprint_tier_bonus, {2: 10, 3: 5})
        self.assertEqual(doc.t2_bonus, 6)
        self.assertEqual(doc.tb_mult, 7)
        doc.acquire('D2_01', state)
        self.assertEqual(doc.blueprint_tier_bonus[2], 10)

    def test_doctrine_draft_pool_removes_acquired_and_suppressed(self):
        from reinforcement_model import sample_doctrines
        import random
        doc, state = MCDocState(), MCState()
        doc.placed_families.add(0)
        initial = dict(doc.pool(30))
        self.assertIn('TB0D1', initial)
        self.assertIn('D2_14', initial)
        doc.acquire('D2_14', state)
        self.assertNotIn('D2_14', dict(doc.pool(30)))
        doc.suppressed_families.add(0)
        self.assertFalse(any(key.startswith('TB0D') for key in dict(doc.pool(30))))
        self.assertNotIn('D2_14', sample_doctrines(random.Random(7), doc.pool(30), 100))

    def test_tb_doctrine_progression_updates_next_draft(self):
        doc, state = MCDocState(), MCState()
        doc.placed_families.add(0)
        self.assertIn('TB0D1', dict(doc.pool(30)))
        doc.acquire('TB0D1', state)
        next_pool = dict(doc.pool(30))
        self.assertNotIn('TB0D1', next_pool)
        self.assertIn('TB0D2', next_pool)

    def test_wave_runner_uses_dynamic_pool(self):
        state, history = simulate_run(load_blueprint_roster(), None, waves=12,
                                      seed=8, config=WaveConfig())
        self.assertEqual(len(history), 12)
        self.assertEqual(state.wave, 12)


if __name__ == '__main__':
    unittest.main()
