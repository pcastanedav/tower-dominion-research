import unittest
from mc_sensitivity import sensitivity_grid


class SensitivityTests(unittest.TestCase):
    def test_paired_seed_grid(self):
        a = sensitivity_grid(trials=2, seed_start=13)
        b = sensitivity_grid(trials=2, seed_start=13)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 5)
        self.assertEqual(a['threshold_35']['config']['tier3_wave'], 35)
        self.assertEqual(a['threshold_45']['config']['tier3_wave'], 45)
        self.assertFalse(a['amplifier_weight_disabled']['config']['amplifier_effect_enabled'])


if __name__ == '__main__':
    unittest.main()
