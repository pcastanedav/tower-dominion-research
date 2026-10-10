import unittest
from mc_state import MCState
from mc_choice import choose_card
from mc_wave60 import WaveConfig, simulate_run

class ReservePolicyTests(unittest.TestCase):
    def test_draft_mc_stays_in_hand(self):
        s = MCState(wave=40, mc_built=20, mc_3a_processed=20, mc_reserve_target=6, mc_established=True)
        s.draft_queue.extend(['MC3A'] * 2)
        s.resolve_drafts(lambda _: True)
        self.assertEqual((s.mc_built, s.mc_in_hand), (20, 2))

    def test_priority_is_latched_for_wave(self):
        s = MCState(mc_built=20, mc_established=True, mc_reserve_target=6, mc_in_hand=5)
        cards = [[('bp', 'MC', 1)], [('bp', 'BPCB21', 1)]]
        self.assertEqual(choose_card(cards, s, package='salamander'), 0)
        s.mc_in_hand = 6
        self.assertEqual(choose_card(cards, s, package='salamander'), 0)
        s.mc_selective_this_wave = True
        self.assertEqual(choose_card(cards, s, package='salamander'), 1)
        s.mc_in_hand = 3
        self.assertEqual(choose_card(cards, s, package='salamander'), 1)

    def test_builds_beyond_threshold(self):
        _, history = simulate_run(None, None, waves=83, seed=1,
            config=WaveConfig(faction='Lions', red=True, package='salamander',
                attenuation_enabled=True, mc_build_target=20, mc_reserve_target=6))
        self.assertTrue(any(x['mc_built'] > 20 for x in history))
        self.assertTrue(all(x['mc_built'] - history[i-1]['mc_built'] <= 3
            for i, x in enumerate(history) if i > 0 and history[i-1]['mc_established']))

if __name__ == '__main__':
    unittest.main()
