import unittest
from unittest.mock import patch
from mc_wave60 import WaveConfig, simulate_run


class SoftlockTests(unittest.TestCase):
    def test_doctrine_exhaustion_is_recorded_as_softlock(self):
        with patch('mc_wave60.reinforcement_step', side_effect=ValueError('no eligible Doctrines')):
            state, history = simulate_run(None, None, waves=3, seed=1, config=WaveConfig())
        self.assertEqual(state.softlock_wave, 1)
        self.assertEqual(history, [])
        self.assertFalse(state.censored)

    def test_unrelated_value_error_propagates(self):
        with patch('mc_wave60.reinforcement_step', side_effect=ValueError('no eligible Blueprints')):
            with self.assertRaisesRegex(ValueError, 'no eligible Blueprints'):
                simulate_run(None, None, waves=3, seed=1, config=WaveConfig())


if __name__ == '__main__':
    unittest.main()
