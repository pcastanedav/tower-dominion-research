import unittest
from mc_packages import evaluate_blueprint, choose_package_card, support_rank


class TestPackages(unittest.TestCase):
    def test_mc_dominates(self):
        self.assertGreater(evaluate_blueprint('MC', 'salamander'),
                           evaluate_blueprint('Omega Emitter', 'salamander'))

    def test_support_priorities(self):
        self.assertGreater(support_rank('salamander')['Omega Emitter'],
                           support_rank('salamander')['Air Command'])
        self.assertEqual(support_rank('howitzer')['Omega Emitter'],
                         support_rank('howitzer')['Air Command'])
        self.assertGreater(support_rank('salamander')['Ammo Depot'],
                           support_rank('salamander')['Division Relay'])

    def test_package_completion(self):
        before = evaluate_blueprint('Rampart Missile Silo', 'sphd_rampart')
        after = evaluate_blueprint('Rampart Missile Silo', 'sphd_rampart',
                                   {'Super Heavy Pulse Defense': 1})
        self.assertGreater(after, before)

    def test_platform_is_high_value_other(self):
        from mc_packages import BLUEPRINT_NAMES, SUPPORTS, PACKAGES
        self.assertEqual(BLUEPRINT_NAMES['BPSB06'], 'Platform')
        self.assertEqual(evaluate_blueprint('Platform', 'salamander')[0], 2)
        self.assertNotIn('Platform', SUPPORTS)
        self.assertNotIn('Platform', PACKAGES['salamander'])

    def test_lions_only(self):
        with self.assertRaises(ValueError):
            evaluate_blueprint('Fortress', 'sphd_fortress')

    def test_whole_card(self):
        cards = [[('bp', 'Omega Emitter', 1)], [('bp', 'MC', 1)]]
        self.assertEqual(choose_package_card(cards, 'salamander'), 1)


if __name__ == '__main__':
    unittest.main()
