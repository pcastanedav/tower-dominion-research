import unittest
from mc_state import MCState


class MCStateTests(unittest.TestCase):
    def test_red_doubles_only_ordinary(self):
        s = MCState()
        s.acquire('MC', ordinary=True, red=True)
        s.acquire('MC', red=True)
        self.assertEqual(s.mc_in_hand, 3)

    def test_inventory_and_amplifier_activation(self):
        s = MCState(wave=10)
        s.acquire('Amplifier')
        s.build()
        self.assertEqual(s.amplifier_mc_targeted, 0)
        s.acquire('MC')
        s.build()
        self.assertEqual(s.amplifier_mc_targeted, 1)
        self.assertEqual(s.mc_1a_active, 1)
        self.assertEqual((s.first_mc_wave, s.first_mc_built_wave), (10, 10))
        self.assertEqual(len(s.draft_queue), 0)

    def test_two_drafts_and_one_time_trigger(self):
        s = MCState(wave=40)
        s.acquire('MC')
        s.build()
        self.assertEqual(len(s.draft_queue), 2)
        s.build()
        self.assertEqual(len(s.draft_queue), 2)
        self.assertEqual(s.resolve_drafts(lambda _: False), 2)
        self.assertEqual(s.mc_3a_processed, 1)

    def test_same_wave_recursion_and_censor(self):
        s = MCState(wave=40)
        s.acquire('MC')
        s.build()
        self.assertEqual(s.resolve_drafts(lambda _: True, max_drafts=7), 7)
        self.assertTrue(s.censored)
        self.assertEqual(s.mc_built, 8)
        self.assertEqual(len(s.draft_queue), 9)

    def test_old_mc_upgrade_on_wave40(self):
        s = MCState(wave=12)
        s.acquire('MC')
        s.build()
        s.wave = 40
        s.build(mc_count=0, amplifier_count=0)
        self.assertEqual(len(s.draft_queue), 2)

    def test_reject_overbuild(self):
        s = MCState()
        with self.assertRaises(ValueError):
            s.build(mc_count=1)


if __name__ == '__main__':
    unittest.main()
