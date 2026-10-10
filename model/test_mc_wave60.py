import unittest
from mc_wave60 import WaveConfig, simulate_run
from mc_weights import BlueprintEntry


POOL = ([BlueprintEntry('MC', 1, 100, 0),
         BlueprintEntry('Amplifier', 1, 100, 0)] +
        [BlueprintEntry(f'OTHER{i}', 1, 100, 0) for i in range(8)])
DOCTRINES = [(f'D{i}', 100) for i in range(25)]


class WaveIntegrationTests(unittest.TestCase):
    def test_reproducible_horizon_and_monotonic_inventory(self):
        a, ah = simulate_run(POOL, DOCTRINES, waves=12, seed=19)
        b, bh = simulate_run(POOL, DOCTRINES, waves=12, seed=19)
        self.assertEqual(ah, bh)
        self.assertEqual(len(ah), 12)
        self.assertTrue(all(x['mc_owned'] <= y['mc_owned'] for x, y in zip(ah, ah[1:])))
        self.assertEqual(a.mc_1a_active, a.mc_built)

    def test_tander_and_red_scenarios(self):
        for config in (WaveConfig(tander=True), WaveConfig(red=True)):
            state, history = simulate_run(POOL, DOCTRINES, waves=8, seed=7, config=config)
            self.assertEqual(len(history), 8)
            self.assertEqual(state.wave, 8)

    def test_wave_threshold_and_censoring(self):
        state, history = simulate_run(POOL, DOCTRINES, waves=10, seed=3,
            config=WaveConfig(tier3_wave=1, max_drafts_per_wave=0))
        self.assertTrue(state.censored)
        self.assertTrue(history[-1]['draft_queue'] > 0)

    def test_eleanor_optional_draft(self):
        state, history = simulate_run(POOL, DOCTRINES, waves=6, seed=8,
                                     config=WaveConfig(eleanor=True))
        self.assertEqual(len(history), 6)
        self.assertGreaterEqual(state.mc_owned, 0)

    def test_attenuation_retargets_at_wave_40(self):
        from unittest.mock import patch
        from mc_doctrines import MCDocState
        from mc_state import MCState
        doc = MCDocState()
        doc.acquire('D1_44', MCState())
        entries = [BlueprintEntry('BPCB01', 1, 100, 0),
                   BlueprintEntry('BPCB02', 2, -3, 1),
                   BlueprintEntry('BPCB03', 3, -8, 1)]
        config = WaveConfig(package='salamander', attenuation_enabled=True,
                            attenuation_policy='wave40_switch')
        with patch('mc_wave60.MCDocState', return_value=doc), \
             patch('mc_wave60.reinforcement_step', return_value=([], None)):
            _, history = simulate_run(entries, None, waves=41, config=config)
        self.assertEqual(history[0]['attenuated'], ('BPCB01',))
        self.assertEqual(history[38]['attenuated'], ('BPCB01',))
        self.assertEqual(history[39]['attenuated'], ('BPCB02',))
        self.assertEqual(history[40]['attenuated'], ('BPCB02',))

    def test_default_attenuation_policy_is_tier1(self):
        self.assertEqual(WaveConfig().attenuation_policy, 'tier1_only')

    def test_invalid_horizon(self):
        with self.assertRaises(ValueError):
            simulate_run(POOL, DOCTRINES, waves=0)


if __name__ == '__main__':
    unittest.main()
