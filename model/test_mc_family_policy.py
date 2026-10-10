import unittest
from mc_family_policy import FamilyIntroduction
from mc_wave60 import WaveConfig, simulate_run
from mc_weights import BlueprintEntry


class FamilyPolicyTests(unittest.TestCase):
    def test_introduction_schedule(self):
        policy = FamilyIntroduction(third_tower='CB01')
        self.assertEqual(policy.advance(1), set())
        self.assertEqual(policy.advance(2), {0})
        self.assertEqual(policy.advance(11), {0, 1})
        self.assertEqual(policy.advance(21), {0, 1})
        self.assertEqual(policy.advance(22, {'CB01'}), {0, 1, 2})
        self.assertEqual(policy.advance(40, {'CB01'}), {0, 1, 2})

    def test_doctrine_free_third_family_rejected(self):
        policy = FamilyIntroduction(third_tower='CB12')
        self.assertEqual(policy.advance(21, {'CB12'}), {0, 1})

    def test_wave_integration(self):
        entries = [BlueprintEntry('BPCB01', 1, 100, 0)]
        _, history = simulate_run(entries, None, waves=22, seed=7)
        self.assertEqual(history[0]['doctrine_families'], ())
        self.assertEqual(history[1]['doctrine_families'], (0,))
        self.assertEqual(history[10]['doctrine_families'], (0, 1))


if __name__ == '__main__':
    unittest.main()
