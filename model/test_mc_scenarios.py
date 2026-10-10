import unittest
from mc_scenarios import summarize_scenario
from mc_wave60 import WaveConfig


class ScenarioSummaryTests(unittest.TestCase):
    def test_deterministic_summary(self):
        a = summarize_scenario(trials=3, seed_start=1, waves=12)
        b = summarize_scenario(trials=3, seed_start=1, waves=12)
        self.assertEqual(a, b)
        self.assertEqual(a['trials'], 3)
        self.assertIn(10, a['snapshots'])
        self.assertNotIn(20, a['snapshots'])

    def test_invalid_trials(self):
        with self.assertRaises(ValueError):
            summarize_scenario(trials=0)

    def test_scenario_parameters(self):
        result = summarize_scenario(trials=2, waves=10,
                                    config=WaveConfig(tander=True, red=True))
        self.assertTrue(result['config']['tander'])
        self.assertTrue(result['config']['red'])
        self.assertEqual(result['snapshots'][10]['observed'], 2)


if __name__ == '__main__':
    unittest.main()
