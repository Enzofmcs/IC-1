from pathlib import Path
import unittest
import pandas as pd
from ic1.reproduce import analyze_vincristine

ROOT=Path(__file__).resolve().parents[1]


class SuppliedDataTests(unittest.TestCase):
    def test_raw_series_reproduces_stored_consolidation_and_peak_table(self):
        signals,peaks,report=analyze_vincristine(ROOT/'data/source_tables/vincristine')
        reference=pd.read_csv(ROOT/'data/reference/vincristine_consolidated.csv')
        expected_peaks=pd.read_csv(ROOT/'data/reference/vincristine_peaks.csv')
        self.assertEqual(len(signals),69)
        self.assertEqual(report['source_rows_per_signal'],74)
        self.assertEqual(signals.columns.tolist(),reference.columns.tolist())
        for column in signals:
            for a,b in zip(signals[column],reference[column]):
                self.assertAlmostEqual(a,b,delta=1e-14)
        for field in ('amount_label_nmol','peak_current_A'):
            for a,b in zip(peaks[field],expected_peaks[field]):
                self.assertAlmostEqual(a,b,delta=1e-14)

    def test_recovered_regression_agrees_with_recorded_result(self):
        _,_,report=analyze_vincristine(ROOT/'data/source_tables/vincristine')
        self.assertEqual(report['fit']['n'],6)
        self.assertAlmostEqual(report['fit']['slope'],3.1991141183035744e-9,delta=1e-20)
        self.assertAlmostEqual(report['fit']['r_squared'],0.9849660357643235,places=10)
        self.assertTrue(report['matches_recorded_R2_at_three_decimals'])
        self.assertEqual(report['x_variable'],'amount_label_nmol')
        self.assertNotIn('concentration_min',report['fit'])

    def test_spectra_reproduce_existing_190_to_400_consolidation(self):
        reference=pd.read_csv(ROOT/'data/reference/spectra_190_400.csv')
        self.assertEqual(len(reference),211)
        for name in ('0','2','3','4','5','6'):
            frame=pd.read_csv(ROOT/f'data/source_tables/spectra/{name}.csv')
            self.assertEqual(len(frame),911)
            selected=frame.loc[frame['Wavelength (nm)']<=400]
            for a,b in zip(selected['Absorbance (AU)'],reference[f'{name}.CSV']):
                self.assertAlmostEqual(a,b,delta=1e-12)
            self.assertIn('Std.Dev.',frame)


if __name__=='__main__':
    unittest.main()
