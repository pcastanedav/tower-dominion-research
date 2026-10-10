import unittest
from mc_draft import target_offer_probability


class DraftTests(unittest.TestCase):
    def test_equal_weights(self):
        self.assertAlmostEqual(target_offer_probability({'MC': 1, 'A': 1, 'B': 1, 'C': 1}, 'MC', 2), 0.5)

    def test_one_draw(self):
        self.assertAlmostEqual(target_offer_probability({'MC': 2, 'A': 3}, 'MC', 1), 0.4)

    def test_full_draft(self):
        self.assertEqual(target_offer_probability({'MC': 1, 'A': 3}, 'MC', 2), 1.0)

    def test_missing_or_zero(self):
        self.assertEqual(target_offer_probability({'A': 1}, 'MC'), 0.0)
        self.assertEqual(target_offer_probability({'MC': 0, 'A': 1}, 'MC'), 0.0)

    def test_no_draws(self):
        self.assertEqual(target_offer_probability({'MC': 1, 'A': 1}, 'MC', 0), 0.0)

    def test_negative_draws(self):
        with self.assertRaises(ValueError):
            target_offer_probability({'MC': 1}, 'MC', -1)


if __name__ == '__main__':
    unittest.main()


class RejectionDraftTests(unittest.TestCase):
    def test_equal_weights(self):
        from mc_draft import rejection_draft_target_probability as p
        self.assertAlmostEqual(p({'MC': 1, 'A': 1, 'B': 1, 'C': 1}, 'MC', 2), .5)

    def test_weighted_two_of_three(self):
        from mc_draft import rejection_draft_target_probability as p
        # Distinct pairs weighted by products: MC-A=2, MC-B=6, A-B=3.
        self.assertAlmostEqual(p({'MC': 2, 'A': 1, 'B': 3}, 'MC', 2), 8/11)

    def test_differs_from_sequential_unique(self):
        from mc_draft import rejection_draft_target_probability as p
        weights = {'MC': 2, 'A': 1, 'B': 3}
        self.assertNotAlmostEqual(p(weights, 'MC', 2), target_offer_probability(weights, 'MC', 2))

    def test_edge_cases(self):
        from mc_draft import rejection_draft_target_probability as p
        self.assertEqual(p({'MC': 2, 'A': 1}, 'MC', 2), 1.0)
        self.assertEqual(p({'MC': 0, 'A': 1}, 'MC', 1), 0.0)
        with self.assertRaises(ValueError):
            p({'MC': 1}, 'MC', -1)


class RejectionSamplerTests(unittest.TestCase):
    def test_full_and_zero_draws(self):
        import random
        from mc_draft import sample_rejection_draft
        self.assertEqual(set(sample_rejection_draft({'MC': 2, 'A': 1}, random.Random(1), 2)), {'MC', 'A'})
        self.assertEqual(sample_rejection_draft({'MC': 2}, random.Random(1), 0), ())

    def test_impossible_draft(self):
        import random
        from mc_draft import sample_rejection_draft
        with self.assertRaises(ValueError):
            sample_rejection_draft({'MC': 1}, random.Random(1), 2)

    def test_sample_matches_exact_inclusion(self):
        import random
        from mc_draft import sample_rejection_draft, rejection_draft_target_probability
        weights = {'MC': 2, 'A': 1, 'B': 3, 'C': 4, 'D': 1, 'E': 2}
        rng = random.Random(9182)
        trials = 12000
        observed = sum('MC' in sample_rejection_draft(weights, rng, 3) for _ in range(trials)) / trials
        self.assertAlmostEqual(observed, rejection_draft_target_probability(weights, 'MC', 3), delta=.018)
