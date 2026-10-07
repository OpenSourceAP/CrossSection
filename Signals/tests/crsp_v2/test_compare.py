"""Run: /opt/venv/projects/openap/bin/python -m unittest discover -s Signals/tests/crsp_v2 -p 'test_*.py'.
Inputs: tiny synthetic parquet files created in temporary directories.
Outputs: unittest results; temporary comparison artifacts are removed afterward.
No WRDS or production/frozen datasets are accessed.
"""

import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

SPEC = importlib.util.spec_from_file_location('crsp_compare', Path(__file__).with_name('compare.py'))
comparison = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(comparison)


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.baseline, self.candidate, self.out = root/'baseline', root/'candidate', root/'reports'
        for directory in (self.baseline, self.candidate):
            (directory/'Intermediate').mkdir(parents=True)

    def run_comparison(self, name, old, new):
        old.to_parquet(self.baseline/'Intermediate'/f'{name}.parquet', index=False)
        new.to_parquet(self.candidate/'Intermediate'/f'{name}.parquet', index=False)
        return comparison.compare(name, self.baseline, self.candidate, self.out)

    @staticmethod
    def panel(permnos, dates, **columns):
        return pd.DataFrame({'permno': permnos, 'time_avail_m': pd.to_datetime(dates), **columns})

    def test_outer_union_exposes_lost_and_added_keys_after_independent_windows(self):
        old = self.panel([1, 2, 4], ['1981-01-01', '1981-01-01', '1980-12-01'], ret=[0., .1, .2])
        new = self.panel([1, 3, 5], ['1981-01-01', '1981-01-01', '1982-01-01'], ret=[0., .1, .2])
        result = self.run_comparison('monthlyCRSP', old, new)
        self.assertEqual(result['coverage'], {'left_only': 1, 'right_only': 1, 'both': 1})
        unmatched = pd.read_parquet(self.out/'monthlyCRSP_unmatched_keys.parquet')
        self.assertEqual(set(unmatched.permno), {2, 3})
        self.assertEqual(len(pd.read_parquet(self.out/'monthlyCRSP_baseline_keys.parquet')), 2)

    def test_null_event_key_components_match_explicitly(self):
        old = pd.DataFrame({'permno': [1], 'rcrddt': [pd.NaT], 'exdt': [pd.Timestamp('1981-03-01')],
                            'paydt': [pd.NaT], 'distcd': [1232], 'divamt': [.5]})
        result = self.run_comparison('CRSPdistributions', old, old.copy())
        self.assertEqual(result['coverage']['both'], 1)
        self.assertEqual(result['columns']['divamt']['mismatches'], 0)
        keys = pd.read_parquet(self.out/'CRSPdistributions_baseline_keys.parquet')
        self.assertTrue(keys.rcrddt.isna().all())
        self.assertTrue(keys.paydt.isna().all())

    def test_duplicate_keys_rejected_before_comparison_join(self):
        old = self.panel([1], ['1981-01-01'], ret=[.1])
        new = pd.concat([old, old.assign(ret=.2)], ignore_index=True)
        with self.assertRaisesRegex(ValueError, 'duplicate candidate keys'):
            self.run_comparison('monthlyCRSP', old, new)
        duplicates = pd.read_parquet(self.out/'monthlyCRSP_candidate_duplicate_keys.parquet')
        self.assertEqual(len(duplicates), 2)
        self.assertFalse((self.out/'monthlyCRSP_comparison.json').exists())

    def test_return_missingness_transitions_are_separate_from_values(self):
        dates = ['1981-01-01', '1981-02-01', '1981-03-01', '1981-04-01']
        old = self.panel([1]*4, dates, ret=[np.nan, .1, np.nan, .2])
        new = self.panel([1]*4, dates, ret=[.1, np.nan, np.nan, .2])
        details = self.run_comparison('monthlyCRSP', old, new)['columns']['ret']
        self.assertEqual((details['missing_to_present'], details['present_to_missing'], details['both_missing']), (1, 1, 1))
        self.assertEqual(details['mismatches'], 2)
        self.assertEqual(details['maximum_absolute_difference'], 0.)

    def test_factor_vintage_scaling_leaves_raw_diagnostics_and_missingness(self):
        # Shuffled dates ensure the anchor is chronological, not input order.
        dates = ['1981-03-01', '1981-01-01', '1981-02-01', '1981-04-01', '1981-05-01']
        old = self.panel([1]*5, dates, cfacshr=[4., 2., 3., np.nan, 5.], cfacpr=[8., 4., 6., np.nan, 10.])
        new = self.panel([1]*5, dates, cfacshr=[40., 20., 30., 7., np.nan], cfacpr=[4., 2., 3., 7., np.nan])
        columns = self.run_comparison('monthlyCRSP', old, new)['columns']
        for column in ('cfacshr', 'cfacpr'):
            raw = columns[column]
            normalized = raw['within_permno_normalization']
            self.assertEqual(raw['mismatches'], 5)
            self.assertIn('Diagnostic', raw['raw_comparison_role'])
            self.assertEqual(raw['tolerance'], {'absolute': 1e-7, 'relative': 1e-8})
            self.assertEqual(normalized['raw_value_mismatches_consistent_with_normalization'], 3)
            self.assertEqual(normalized['remaining_rebased_value_mismatches'], 0)
            self.assertEqual(normalized['ratio_changes_relative_to_anchor'], 0)
            self.assertEqual((normalized['missing_to_present'], normalized['present_to_missing']), (1, 1))
            anchors = pd.read_parquet(self.out/f'monthlyCRSP_{column}_normalization_anchors.parquet')
            self.assertEqual(anchors.time_avail_m.iloc[0], pd.Timestamp('1981-01-01'))

    def test_factor_trajectory_change_survives_rebasing_per_permno(self):
        old = self.panel([1, 1, 2, 2], ['1981-01-01', '1981-02-01']*2, cfacshr=[1., 2., 3., 6.])
        new = old.copy()
        new['cfacshr'] = [10., 30., 1.5, 3.]
        normalized = self.run_comparison('monthlyCRSP', old, new)['columns']['cfacshr']['within_permno_normalization']
        self.assertEqual(normalized['anchor_permnos'], 2)
        self.assertEqual(normalized['raw_value_mismatches_consistent_with_normalization'], 3)
        self.assertEqual(normalized['remaining_rebased_value_mismatches'], 1)
        self.assertEqual(normalized['ratio_changes_relative_to_anchor'], 1)
        examples = pd.read_csv(self.out/'monthlyCRSP_cfacshr_rebased_examples.csv')
        self.assertEqual(examples.permno.tolist(), [1])

    def test_nonpositive_factors_are_not_normalized(self):
        old = self.panel([1, 1, 2], ['1981-01-01', '1981-02-01', '1981-01-01'], cfacshr=[0., -1., 2.])
        new = old.assign(cfacshr=[0., -2., 4.])
        normalized = self.run_comparison('monthlyCRSP', old, new)['columns']['cfacshr']['within_permno_normalization']
        self.assertEqual(normalized['present_rows_not_normalized'], 2)
        self.assertEqual(normalized['raw_mismatches_not_normalized'], 1)
        self.assertEqual(normalized['permnos_with_only_one_comparable_date'], 1)


if __name__ == '__main__':
    unittest.main()
