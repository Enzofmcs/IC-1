import math
from pathlib import Path
import tempfile
import unittest

import pandas as pd
from ic1.analysis import (fit_calibration, consolidate_signals, signal_peak,
                          subtract_signals, parse_sample_name, read_signal)


class AnalysisTests(unittest.TestCase):
    def test_known_linear_calibration_and_inverse(self):
        fit = fit_calibration([0, 1, 2, 3], [2, 5, 8, 11])
        self.assertEqual(fit.slope, 3)
        self.assertEqual(fit.intercept, 2)
        self.assertEqual(fit.r_squared, 1)
        self.assertEqual(fit.rmse, 0)
        self.assertAlmostEqual(fit.estimate(6.5), 1.5)
        with self.assertRaises(ValueError):
            fit.estimate(100)

    def test_constant_or_nonfinite_data(self):
        with self.assertRaises(ValueError):
            fit_calibration([1, 1, 1], [1, 2, 3])
        with self.assertRaises(ValueError):
            fit_calibration([1, 2, 3], [1, math.nan, 3])
        fit = fit_calibration([1, 2, 3], [4, 4, 4])
        self.assertIsNone(fit.r_squared)
        with self.assertRaises(ValueError):
            fit.estimate(4)

    def test_pairs_are_never_independently_sorted(self):
        x, delta = subtract_signals([3, 1, 2], [30, 10, 20], [3, 1, 2], [36, 12, 24])
        self.assertEqual(x, [1, 2, 3])
        self.assertEqual(delta, [2, 4, 6])
        with self.assertRaises(ValueError):
            subtract_signals([1, 2], [10, 20], [2, 1], [24, 12])

    def test_peak_uses_only_requested_window(self):
        self.assertEqual(signal_peak([0, 1, 2], [100, 3, 4], 1, 2), (2, 4))
        with self.assertRaises(ValueError):
            signal_peak([0, 1], [2, 3], 4, 5)

    def test_consolidation_rejects_misaligned_grids(self):
        with tempfile.TemporaryDirectory() as folder:
            a, b = Path(folder)/'a.csv', Path(folder)/'b.csv'
            pd.DataFrame({'p':[0, 1], 'i':[2, 4]}).to_csv(a, index=False)
            pd.DataFrame({'p':[1, 0], 'i':[5, 3]}).to_csv(b, index=False)
            with self.assertRaises(ValueError):
                consolidate_signals([a, b], x_column='p', y_column='i')
            pd.DataFrame({'p':[0, 1], 'i':[3, 5]}).to_csv(b, index=False)
            combined = consolidate_signals([b, a], x_column='p', y_column='i')
            self.assertEqual(combined.columns.tolist(), ['x', 'a', 'b'])
            self.assertEqual(combined['b'].tolist(), [3, 5])

    def test_utf16_csv_and_xlsx(self):
        with tempfile.TemporaryDirectory() as folder:
            frame = pd.DataFrame({'wave':[190, 191], 'absorb':[0.1, 0.2]})
            csv, xlsx = Path(folder)/'s.csv', Path(folder)/'s.xlsx'
            frame.to_csv(csv, index=False, encoding='utf-16le')
            frame.to_excel(xlsx, index=False)
            for path, options in [(csv, {'encoding':'utf-16le'}), (xlsx, {})]:
                result = read_signal(path, 'wave', 'absorb', **options)
                self.assertEqual(result['signal'].tolist(), [0.1, 0.2])

    def test_sample_name_preserves_unit(self):
        self.assertEqual(parse_sample_name('MTX-2.5uM'), ('MTX', 2.5, 'uM'))
        with self.assertRaises(ValueError):
            parse_sample_name('sem-concentracao')


if __name__ == '__main__':
    unittest.main()
