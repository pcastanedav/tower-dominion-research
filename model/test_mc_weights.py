import unittest
from mc_weights import BlueprintEntry, blueprint_weights


class WeightTests(unittest.TestCase):
    def setUp(self):
        self.pool = [BlueprintEntry('T1', 1, 100, 0),
                     BlueprintEntry('MC', 2, -3, 1),
                     BlueprintEntry('T3', 3, -8, 1),
                     BlueprintEntry('LOCKED', 1, 100, 0, eligible=False)]

    def test_wave_one_and_eligibility(self):
        self.assertEqual(blueprint_weights(self.pool, 1), {'T1': 100, 'MC': 0, 'T3': 0})

    def test_mc_stack_before_amplifier(self):
        weights = blueprint_weights(self.pool, 5, mc_1a_active=2, amplified_types=('MC',))
        self.assertEqual(weights, {'T1': 100, 'MC': 10, 'T3': 0})

    def test_other_tier_currencies(self):
        weights = blueprint_weights(self.pool, 5, extra_tier_weights={2: 10, 3: 5})
        self.assertEqual(weights['MC'], 11)
        self.assertEqual(weights['T3'], 1)

    def test_same_type_percent_adds(self):
        weights = blueprint_weights(self.pool, 5, mc_1a_active=2,
                                    amplified_types=('MC',), type_bonus_percent={'MC': 50})
        self.assertEqual(weights['MC'], 12)

    def test_clamp_and_negative_modifier(self):
        entries = [BlueprintEntry('MC', 2, 99, 10)]
        self.assertEqual(blueprint_weights(entries, 10, amplified_types=('MC',))['MC'], 200)
        self.assertEqual(blueprint_weights(entries, 10, type_bonus_percent={'MC': -200})['MC'], 0)

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            blueprint_weights(self.pool, 0)
        with self.assertRaises(ValueError):
            blueprint_weights(self.pool + self.pool[:1], 1)


if __name__ == '__main__':
    unittest.main()
