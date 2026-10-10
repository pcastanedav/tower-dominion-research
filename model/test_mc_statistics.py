import unittest
from mc_statistics import wilson_interval, first_mc_by, wave_threshold


class StatisticsTests(unittest.TestCase):
    def test_wilson_extremes_are_not_certain(self):
        low, high = wilson_interval(0, 100)
        self.assertAlmostEqual(low, 0)
        self.assertGreater(high, 0)
        low, high = wilson_interval(100, 100)
        self.assertLess(low, 1)
        self.assertEqual(high, 1)

    def test_wilson_invalid(self):
        for successes, trials in ((0, 0), (-1, 10), (11, 10)):
            with self.assertRaises(ValueError):
                wilson_interval(successes, trials)

    def test_censored_wave_not_failure(self):
        class State:
            first_mc_wave = 2
        outcomes = [(State(), [{'mc_owned': 1}, {'mc_owned': 2}]),
                    (State(), [{'mc_owned': 0}])]
        self.assertEqual(first_mc_by(outcomes, 2), 2)
        self.assertEqual(wave_threshold(outcomes, 2, 2), (1, 1))


if __name__ == '__main__':
    unittest.main()
