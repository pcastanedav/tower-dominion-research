import unittest
from mc_run import run_mc_waves
from mc_weights import BlueprintEntry


class WaveRunnerTests(unittest.TestCase):
    def setUp(self):
        self.entries = [BlueprintEntry('MC', 1, 100, 0)] + [
            BlueprintEntry(f'OTHER{i}', 1, 100, 0) for i in range(8)]
        self.doctrines = [(f'D{i}', 100) for i in range(20)]

    def test_deterministic_horizon(self):
        a, history_a = run_mc_waves(self.entries, self.doctrines, waves=12, seed=45)
        b, history_b = run_mc_waves(self.entries, self.doctrines, waves=12, seed=45)
        self.assertEqual(history_a, history_b)
        self.assertEqual(len(history_a), 12)
        self.assertEqual(a.mc_built, b.mc_built)

    def test_early_tier3_triggers_drafts(self):
        self.entries[0] = BlueprintEntry("MC", 1, 100000, 0, cap=100000)
        state, history = run_mc_waves(self.entries, self.doctrines,
                                      waves=6, seed=45, tier3_wave=1)
        self.assertGreater(state.mc_built, 0)
        self.assertGreater(state.drafts_resolved, 0)
        self.assertTrue(state.censored)

    def test_eleanor_requires_explicit_cadence(self):
        with self.assertRaises(ValueError):
            run_mc_waves(self.entries, self.doctrines, eleanor=True)
        state, history = run_mc_waves(self.entries, self.doctrines, waves=4,
                                      eleanor=True, eleanor_due=lambda wave: wave % 2 == 0)
        self.assertEqual(len(history), 4)

    def test_dynamic_doctrine_callback(self):
        seen = []
        def pool(wave, state):
            seen.append(wave)
            return self.doctrines
        _, history = run_mc_waves(self.entries, pool, waves=3)
        self.assertEqual(seen, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
