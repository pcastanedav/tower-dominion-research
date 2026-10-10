import unittest
from mc_choice import choose_card, apply_selected_card
from mc_state import MCState


class ChoiceTests(unittest.TestCase):
    def test_mc_priority_and_card_bundle(self):
        s = MCState()
        cards = [[('bp', 'Amplifier', 1)], [('bp', 'MC', 1), ('bp', 'Amplifier', 1)]]
        i = choose_card(cards, s)
        self.assertEqual(i, 1)
        apply_selected_card(cards, i, s)
        self.assertEqual((s.mc_in_hand, s.amplifier_in_hand), (1, 1))

    def test_conflict_policy(self):
        s = MCState()
        cards = [[('bp', 'MC', 1)], [('bp', 'Amplifier', 1)]]
        self.assertEqual(choose_card(cards, s), 0)
        self.assertEqual(choose_card(cards, s, conflict='amplifier_first'), 1)

    def test_red_quantity_not_extra_choices(self):
        s = MCState()
        cards = [[('bp', 'MC', 1)], [('bp', 'Amplifier', 1)]]
        apply_selected_card(cards, choose_card(cards, s), s, red=True)
        self.assertEqual(s.mc_in_hand, 2)
        self.assertEqual(s.amplifier_in_hand, 0)

    def test_first_amp_not_prioritized_twice(self):
        s = MCState()
        s.acquire('Amplifier')
        cards = [[('bp', 'Amplifier', 1)], [('bp', 'MC', 1)]]
        self.assertEqual(choose_card(cards, s, conflict='amplifier_first'), 1)

    def test_package_priority_order(self):
        from mc_doctrines import MCDocState
        state = MCState()
        options = [[('doctrine', 'D2_14', 1)],
                   [('bp', 'MC', 1)],
                   [('doctrine', 'D1_45', 1)],
                   [('doctrine', 'D1_44', 1)],
                   [('bp', 'BPCB21', 1)],
                   [('doctrine', 'D1_01', 1)]]
        def pick(cards, owned=0):
            return choose_card(cards, state, package='salamander', lions=True,
                               attenuators_owned=owned)
        self.assertEqual(pick(options), 0)  # SB beats everything
        self.assertEqual(pick(options[1:]), 0)  # first MC beats Amp
        state.acquire('MC')
        self.assertEqual(pick(options[1:]), 1)  # Amp beats more MCs
        state.acquire('Amplifier')
        self.assertEqual(pick(options[1:]), 0)  # more MCs beat Att
        self.assertEqual(pick(options[3:]), 0)  # Att beats strategy
        self.assertEqual(pick(options[4:]), 0)  # strategy beats other Doctrines
        self.assertEqual(pick(options[3:], owned=2), 1)  # Att no longer needed

    def test_empty_and_invalid(self):
        s = MCState()
        self.assertIsNone(choose_card([], s))
        with self.assertRaises(ValueError):
            choose_card([[('bp', 'MC', 1)]], s, conflict='unknown')
        with self.assertRaises(ValueError):
            choose_card([[('bp', 'MC', -1)]], s)


if __name__ == '__main__':
    unittest.main()
