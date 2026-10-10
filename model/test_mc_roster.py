import unittest
from collections import Counter
from mc_roster import load_blueprint_roster, blueprint_identity
from mc_weights import blueprint_weights
from mc_wave60 import simulate_run


class AssetRosterTests(unittest.TestCase):
    def test_verified_roster_counts(self):
        entries = load_blueprint_roster()
        self.assertEqual(len(entries), 32)
        self.assertEqual(Counter(e.tier for e in entries), {1: 12, 2: 10, 3: 10})

    def test_mc_tier_and_wave_eligibility(self):
        entries = load_blueprint_roster()
        mc = next(e for e in entries if e.code == 'BPSB07')
        self.assertEqual(mc.tier, 3)
        self.assertEqual(blueprint_weights(entries, 9)['BPSB07'], 0)
        self.assertEqual(blueprint_weights(entries, 10)['BPSB07'], 1)
        self.assertEqual(blueprint_identity(mc.code), 'MC')

    def test_asset_roster_short_run(self):
        state, history = simulate_run(load_blueprint_roster(),
            [(f'D{i}', 100) for i in range(30)], waves=12, seed=4)
        self.assertEqual(len(history), 12)
        self.assertEqual(state.wave, 12)


if __name__ == '__main__':
    unittest.main()
