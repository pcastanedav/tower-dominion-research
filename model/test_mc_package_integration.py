import unittest
from mc_choice import choose_card
from mc_state import MCState
from mc_wave60 import WaveConfig, simulate_run
from mc_roster import load_blueprint_roster

class TestPackageIntegration(unittest.TestCase):
    def test_mc_remains_primary(self):
        cards = [[('bp','BPCB05',1)], [('bp','MC',1)]]
        self.assertEqual(choose_card(cards, MCState(), package='cannon',
                                    code_names={'BPCB05':'Sanction Cannon'}), 1)

    def test_support_and_offense_same_tier(self):
        cards = [[('bp','BPCB05',1)], [('bp','BPCB06',1)]]
        names = {'BPCB05':'Sanction Cannon','BPCB06':'Air Command'}
        self.assertEqual(choose_card(cards, MCState(), package='cannon',code_names=names),0)

    def test_fixed_reward_priority(self):
        s = MCState()
        names = {'BPCB05': 'Sanction Cannon'}
        cards = [[('doctrine','D1_01',1)], [('bp','BPCB05',1)],
                 [('doctrine','D1_44',1)], [('bp','MC',1)],
                 [('doctrine','D1_45',1)], [('doctrine','D2_14',1)]]
        def pick(options, state=s, attenuators=0):
            return options[choose_card(options,state,package='cannon',code_names=names,
                                       attenuators_owned=attenuators)]
        self.assertEqual(pick(cards), cards[5])
        self.assertEqual(pick(cards[:5]), cards[3])
        s.acquire('MC')
        self.assertEqual(pick(cards[:5]), cards[4])
        s.acquire('Amplifier')
        self.assertEqual(pick(cards[:4]), cards[3])
        self.assertEqual(pick(cards[:3]), cards[2])
        self.assertEqual(pick(cards[:3], attenuators=2), cards[1])
        self.assertEqual(pick(cards[:1]), cards[0])

    def test_existing_scenarios_still_run(self):
        roster = load_blueprint_roster()
        for flags in ({}, {'red':True}, {'eleanor':True}, {'tander':True}, {'magel':True}):
            _, history = simulate_run(roster, None, waves=5, seed=4,
                                      config=WaveConfig(**flags))
            self.assertEqual(len(history),5)
            self.assertIn('blueprint_acquisitions',history[-1])

if __name__ == '__main__':
    unittest.main()
