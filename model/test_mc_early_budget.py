import unittest
from mc_state import MCState
from mc_wave60 import WaveConfig, simulate_run
from mc_roster import load_blueprint_roster


class EarlyBudgetTests(unittest.TestCase):
    def test_upgrade_spends_one_opportunity_and_queues_two_drafts(self):
        state = MCState(wave=20)
        state.acquire('MC', copies=2)
        state.build(tier3_wave=40)
        state.upgrade_3a(1)
        self.assertEqual(state.mc_3a_processed, 1)
        self.assertEqual(len(state.draft_queue), 2)
        state.wave = 40
        state.build(mc_count=0, amplifier_count=0, tier3_wave=40)
        self.assertEqual(state.mc_3a_processed, 2)
        self.assertEqual(len(state.draft_queue), 4)

    def test_cannot_upgrade_unbuilt_or_twice(self):
        state = MCState()
        with self.assertRaises(ValueError):
            state.upgrade_3a(1)
        state.acquire('MC')
        state.build(tier3_wave=40)
        state.upgrade_3a(1)
        with self.assertRaises(ValueError):
            state.upgrade_3a(1)

    def test_immediate_3a_works_before_wave_40(self):
        roster = load_blueprint_roster()
        immediate, history = simulate_run(roster, None, waves=35, seed=2,
                                          config=WaveConfig(immediate_3a=True))
        self.assertEqual(len(history), 35)
        self.assertEqual(immediate.mc_3a_processed, immediate.mc_built)
        self.assertEqual(immediate.drafts_resolved, 2 * immediate.mc_3a_processed)

    def test_invalid_interval_rejected(self):
        with self.assertRaises(ValueError):
            simulate_run([], [], config=WaveConfig(early_3a_interval=0))


if __name__ == '__main__':
    unittest.main()
