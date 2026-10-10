import random
import unittest
from mc_reinforcement import generate_mc_cards, reinforcement_step
from mc_state import MCState


class ReinforcementIntegrationTests(unittest.TestCase):
    def test_card_counts_and_structure(self):
        for count in (3, 4):
            cards = generate_mc_cards(random.Random(2), {'MC': 100, 'OTHER': 100},
                                      [(f'D{i}', 100) for i in range(8)], count)
            self.assertEqual(len(cards), count)
            self.assertTrue(all(len(card) == 2 for card in cards))

    def test_red_grants_two_without_extra_cards(self):
        state = MCState()
        cards, index = reinforcement_step(random.Random(1), state, {'MC': 100},
                                         [(f'D{i}', 100) for i in range(8)], red=True)
        self.assertEqual(len(cards), 3)
        mc_count = sum(item[2] for item in cards[index] if item[0] == 'bp' and item[1] == 'MC')
        self.assertEqual(state.mc_in_hand, 2 * mc_count)

    def test_generated_cards_are_distinct(self):
        cards = generate_mc_cards(random.Random(11), {'MC': 100, 'OTHER': 100},
                                  [(f'D{i}', 100) for i in range(20)])
        self.assertEqual(len({tuple(sorted(card)) for card in cards}), len(cards))

    def test_retry_limit_validation(self):
        with self.assertRaises(ValueError):
            generate_mc_cards(random.Random(1), {'MC': 100},
                              [(f'D{i}', 100) for i in range(20)],
                              max_screen_retries=0)

    def test_no_blueprint_pool_rejected_when_needed(self):
        with self.assertRaises(ValueError):
            generate_mc_cards(random.Random(1), {}, [(f'D{i}', 100) for i in range(8)])


if __name__ == '__main__':
    unittest.main()
