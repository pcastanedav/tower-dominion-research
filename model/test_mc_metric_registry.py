"""Regression checks for MC metric selection, safe expressions, and paired semantics."""
import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from mc_metric_registry import METRICS, aggregate, compile_metrics, evaluate_metric, paired_aggregate, summarize

class MetricRegistryTests(unittest.TestCase):
    def test_legacy_summary_equivalence(self):
        rows = [tuple(i + offset for i in range(len(METRICS))) for offset in range(1, 5)]
        names, derived = compile_metrics({})
        actual = aggregate(rows, names, derived)
        self.assertEqual(list(actual), list(METRICS))
        for i, metric in enumerate(METRICS):
            self.assertEqual(actual[metric], summarize([r[i] for r in rows]))
        matches = [(rows[0], rows[1]), (rows[2], rows[3])]
        paired = paired_aggregate(matches, names, derived)
        for i, metric in enumerate(METRICS):
            self.assertEqual(paired[metric], summarize([a[i] - b[i] for a, b in matches]))

    def test_derived_and_missing_denominator(self):
        names, derived = compile_metrics({'metrics': ['mc_owned', 'build_fraction'],
                                           'derived_metrics': {'build_fraction': 'mc_built / mc_owned'}})
        first = (4, 2) + (0,) * (len(METRICS)-2)
        zero = (0,) * len(METRICS)
        self.assertEqual(evaluate_metric('build_fraction', first, derived), .5)
        self.assertIsNone(evaluate_metric('build_fraction', zero, derived))
        self.assertEqual(aggregate([first, zero], names, derived)['build_fraction']['mean'], .5)
        self.assertEqual(paired_aggregate([(first, zero)], names, derived)['mc_owned']['mean'], 4)
        self.assertNotIn('build_fraction', paired_aggregate([(first, zero)], names, derived))

    def test_invalid_expressions_and_metrics(self):
        for expr in ('__import__("os")', 'mc_owned.__class__', 'unknown + 1', '[1,2]', 'mc_owned ** 2'):
            with self.subTest(expr=expr), self.assertRaises(ValueError):
                compile_metrics({'derived_metrics': {'unsafe': expr}})
        with self.assertRaises(ValueError):
            compile_metrics({'metrics': ['missing']})
        with self.assertRaises(ValueError):
            compile_metrics({'derived_metrics': {'mc_owned': '1'}})

if __name__ == '__main__':
    unittest.main()
