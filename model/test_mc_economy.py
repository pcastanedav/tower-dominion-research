import unittest
from mc_economy import MCEconomy, economy_history


class TestMCEconomy(unittest.TestCase):
    def test_reroll_milestones(self):
        self.assertEqual([MCEconomy(45, n).reroll_cost for n in (1, 2, 5, 11)], [25, 20, 5, 5])
        self.assertEqual([MCEconomy(46, n).reroll_cost for n in (1, 5, 10, 11)], [55, 35, 10, 5])

    def test_production_and_damage(self):
        self.assertEqual(MCEconomy(55, 1).supply_per_wave, 400)
        self.assertEqual(MCEconomy(56, 1).supply_per_wave, 0)
        self.assertEqual(MCEconomy(55, 1).recon_per_wave, 10)
        self.assertEqual(MCEconomy(63, 5).global_damage_bonus_percent, 200)

    def test_history(self):
        rows = economy_history([{'wave': 45, 'mc_built': 5}, {'wave': 46, 'mc_built': 5}], 2)
        self.assertEqual([x['reroll_cost'] for x in rows], [5, 35])
        self.assertEqual(rows[-1]['recon_produced'], 20)
        self.assertEqual(rows[-1]['reroll_recon_saved'], 80)
        self.assertEqual(rows[-1]['supply_produced'], 800)


if __name__ == '__main__':
    unittest.main()
