import unittest
from mc_roster import load_blueprint_roster
from mc_wave60 import WaveConfig, simulate_run
from mc_scenarios import summarize_scenario


class CounterfactualTests(unittest.TestCase):
    def test_faction_eligibility(self):
        for faction, own in [('Faction1', 'BPF101'), ('Faction2', 'BPF202'), ('Faction3', 'BPF301')]:
            codes = {e.code for e in load_blueprint_roster(faction=faction)}
            self.assertEqual(len(codes), 28)
            self.assertIn(own, codes)
            self.assertEqual(len([c for c in codes if c.startswith('BPF')]), 2)

    def test_no_3a_drafts(self):
        roster = load_blueprint_roster(faction='Faction2')
        state, history = simulate_run(roster, None, waves=63, seed=3,
                                      config=WaveConfig(mc_3a_effect_enabled=False))
        self.assertEqual(state.drafts_resolved, 0)
        self.assertTrue(all(row['mc_from_3a_this_wave'] == 0 for row in history))

    def test_no_1a_bonus_is_deterministic(self):
        roster = load_blueprint_roster(faction='Faction2')
        cfg = WaveConfig(mc_1a_effect_enabled=False)
        a, ah = simulate_run(roster, None, waves=45, seed=9, config=cfg)
        b, bh = simulate_run(roster, None, waves=45, seed=9, config=cfg)
        self.assertEqual(ah, bh)

    def test_scenario_rejects_unknown_faction(self):
        with self.assertRaises(ValueError):
            summarize_scenario(trials=1, config=WaveConfig(faction='Unknown'))


if __name__ == '__main__':
    unittest.main()
