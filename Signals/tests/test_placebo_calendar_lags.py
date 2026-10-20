"""Exercise production placebo calendar endpoints and observed-row preservation.

Run from the repository root:
  /opt/venv/projects/openap/bin/python3 -m unittest discover -s Signals/tests -p test_placebo_calendar_lags.py
Inputs: synthetic monthly accounting panels with explicit missing targets/values.
Outputs: unittest results; parquet reads and signal saves are mocked in memory.
"""
import ast
import contextlib
import io
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import polars as pl

CODE = Path(__file__).resolve().parents[1] / 'pyCode'
sys.path.insert(0, str(CODE))
from utils import saveplacebo, save_standardized


class PlaceboCalendarLagTests(unittest.TestCase):
    def setUp(self):
        frames = []
        for permno in [1, 2, 3]:
            n = np.arange(40, dtype=float)
            frame = pd.DataFrame({
                'permno': permno, 'gvkey': str(permno),
                'time_avail_m': pd.date_range('2018-01-01', periods=40, freq='MS'),
                'at': 100 + n, 'atq': 100 + n, 'sale': 200 + 3*n,
                'saleq': 200 + 3*n, 'cogs': 20 + n, 'rect': 30 + n,
                'invt': 10 + n, 'che': 5 + n, 'act': 50 + 2*n,
                'gdwl': 2., 'intan': 3., 'ap': 4., 'sic': '2000', 'sicCRSP': 2000,
                'ib': 5., 'dp': 2., 'dvpsx_c': 0., 'dltt': 10.,
                'lct': 10 + n, 'mve_permco': 1000., 'prcc_f': 10., 'am': 0., 'txt': 1 + n,
                'pi': 10 + n, 'epspx': 2 + n, 'ajex': 1.,
            })
            if permno == 1:
                frame = frame.drop(index=25)  # Intervening gap, valid 12-month endpoints.
            elif permno == 2:
                frame = frame.drop(index=12)  # Missing target, never previous observation.
            else:
                frame.loc[12, ['at', 'atq']] = np.nan  # Existing missing target stays missing.
            frames.append(frame)
        self.panel = pd.concat(frames, ignore_index=True)

    def run_signal(self, filename):
        captured = {}
        def read(path, columns=None, **kwargs):
            frame = self.panel.copy()
            return pl.from_pandas(frame if columns is None else frame[columns])
        def save(frame, name):
            captured[name] = frame.to_pandas() if isinstance(frame, pl.DataFrame) else frame.copy()
        with contextlib.redirect_stdout(io.StringIO()), \
             patch.object(pl, 'read_parquet', side_effect=read), \
             patch.object(saveplacebo, 'save_placebo', side_effect=save), \
             patch.object(save_standardized, 'save_placebo', side_effect=save):
            runpy.run_path(str(CODE / 'Placebos' / filename), run_name='__main__')
        return captured

    def assert_observed_keys(self, frame):
        actual = frame.set_index(['permno', 'time_avail_m']).index
        expected = self.panel.set_index(['permno', 'time_avail_m']).index
        self.assertTrue(actual.is_unique)
        self.assertEqual(set(actual), set(expected))

    def test_monthly_lag_formulas_use_explicit_calendar_targets(self):
        # These scripts cover raw shifts, local joins, and existing helper callers.
        specs = {
            'AssetLiquidityBook.py': ('AssetLiquidityBook', 1, lambda r: r.che + .75*(r.act-r.che) + .5*(r['at']-r.act-r.gdwl-r.intan)),
            'GPlag.py': ('GPlag', 12, lambda r: r.sale-r.cogs),
            'GPlag_q.py': ('GPlag_q', 3, None),
            'AssetGrowth_q.py': ('AssetGrowth_q', 12, None),
        }
        # Quarterly input names still use monthly availability-date lags.
        self.panel['revtq'] = self.panel.sale
        self.panel['cogsq'] = self.panel.cogs
        keyed = self.panel.set_index(['permno', 'time_avail_m'])
        for filename, (signal, months, numerator) in specs.items():
            with self.subTest(filename=filename):
                result = self.run_signal(filename)[signal]
                self.assert_observed_keys(result)
                for row in result.itertuples():
                    source = keyed.loc[(row.permno, row.time_avail_m)]
                    target = (row.permno, row.time_avail_m-pd.DateOffset(months=months))
                    denominator = keyed.loc[target, 'at'] if target in keyed.index else np.nan
                    if signal == 'AssetGrowth_q':
                        expected = (source.atq-denominator)/denominator
                    elif signal == 'GPlag_q':
                        q = self.panel.sort_values(['permno','time_avail_m']).copy()
                        q['atq'] = q.groupby('permno').atq.ffill()
                        q = q.set_index(['permno','time_avail_m'])
                        denominator = q.loc[target, 'atq'] if target in q.index else np.nan
                        expected = (source.revtq-source.cogsq)/denominator
                    else:
                        expected = numerator(source)/denominator
                    actual = getattr(row, signal)
                    if pd.isna(expected): self.assertTrue(pd.isna(actual))
                    else: self.assertAlmostEqual(actual, expected)

    def test_current_ratio_nan_normalization_preserves_missing_value_rule(self):
        month = pd.Timestamp('2019-01-01')
        mask = (self.panel.permno == 3) & (self.panel.time_avail_m == month)
        self.panel.loc[mask, ['act', 'lct']] = 0.0
        result = self.run_signal('ZZ1_currat_pchcurrat.py')
        for frame in result.values(): self.assert_observed_keys(frame)
        current = result['currat'].set_index(['permno','time_avail_m']).currat
        change = result['pchcurrat'].set_index(['permno','time_avail_m']).pchcurrat
        self.assertTrue(pd.isna(current.loc[(3, month)]))
        self.assertEqual(change.loc[(3, month)], 0.0)
        self.assertEqual(change.loc[(3, pd.Timestamp('2020-01-01'))], 0.0)

    def test_monthly_return_leads_keep_actual_time_column_and_join_dtype(self):
        path = CODE / 'Placebos/ZZ1_EarningsValueRelevance_EarningsTimeliness_EarningsConservatism.py'
        # Execute the complete production CRSP stage; the remaining stages are
        # annual regressions unrelated to calendar-return alignment.
        source = path.read_text()
        nodes = ast.parse(source).body
        stop = next(node.lineno for node in nodes
                    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'compustat_annual' for t in node.targets))
        self.panel['ret'] = np.arange(len(self.panel))/1000
        self.panel['prc'] = 10.
        self.panel['shrout'] = 100.
        namespace = {'__file__': str(path)}
        with contextlib.redirect_stdout(io.StringIO()), patch.object(pl, 'read_parquet', return_value=pl.from_pandas(self.panel)):
            exec(compile('\n'.join(source.splitlines()[:stop-1]), str(path), 'exec'), namespace)
        result = namespace['crsp']
        self.assertEqual(result.schema['time_m'], pl.from_pandas(self.panel).schema['time_avail_m'])
        keyed = self.panel.set_index(['permno','time_avail_m'])
        self.assertEqual(result.height, len(self.panel))
        for row in result.to_dicts():
            for lag, name in [(-2, 'f2_ret'), (-1, 'f_ret'), (1, 'l_ret'), (11, 'l11_ret')]:
                target = (row['permno'], pd.Timestamp(row['time_m'])-pd.DateOffset(months=lag))
                expected = keyed.loc[target, 'ret'] if target in keyed.index else np.nan
                if pd.isna(expected): self.assertIsNone(row[name])
                else: self.assertAlmostEqual(row[name], expected)

    def test_delay_accounting_stage_uses_monthly_endpoints(self):
        path = CODE / 'Placebos/ZZ3_DelayAcct_DelayNonAcct.py'
        source = path.read_text()
        stage = source[source.index('# Sort for lag operations'):source.index('# Compute rolling standard deviation')]
        panel = self.panel.assign(spi=2., meanest=np.arange(len(self.panel)), fy0a=1.)
        from utils.stata_replication import stata_multi_lag
        namespace = {'df': pl.from_pandas(panel), 'pl': pl, 'stata_multi_lag': stata_multi_lag}
        exec(compile(stage, str(path), 'exec'), namespace)
        result = namespace['df'].to_pandas()
        self.assert_observed_keys(result)
        keyed = panel.set_index(['permno', 'time_avail_m'])
        for row in result.itertuples():
            for months in [12, 24, 36, 48]:
                target = (row.permno, row.time_avail_m-pd.DateOffset(months=months))
                expected = keyed.loc[target, 'meanest']-1 if target in keyed.index else np.nan
                actual = getattr(row, f'tempSurprise{months}')
                if pd.isna(expected): self.assertTrue(pd.isna(actual))
                else: self.assertAlmostEqual(actual, expected)
            target = (row.permno, row.time_avail_m-pd.DateOffset(months=12))
            prior_at = keyed.loc[target, 'at'] if target in keyed.index else np.nan
            expected = 2 / ((row.at + prior_at) / 2)
            if pd.isna(expected): self.assertTrue(pd.isna(row.tempSI))
            else: self.assertAlmostEqual(row.tempSI, expected)

    def test_beta_market_regressions_keep_calendar_grid_without_exporting_gap_coefficients(self):
        from polars_ols import compute_rolling_least_squares, RollingKwargs
        from utils.stata_replication import fill_date_gaps, stata_multi_lag
        path = CODE / 'Placebos/ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.py'
        source = path.read_text()
        stage = source[source.index('# Market filtering ONLY'):source.index('# Compute stock-level innovation')]
        t = np.arange(90)
        panel = pd.DataFrame({
            'permno': 1, 'time_avail_m': pd.date_range('2000-01-01', periods=90, freq='MS'),
            'prc': 10., 'exchcd': 1, 'shrout': 100., 'MarketCapitalization': 1+t/100,
            'ill': .2+np.sin(t)/10, 'vwretd': np.cos(t*.7)/100,
        })
        # Stocks exist, but the market eligibility filter removes these months.
        panel.loc[[60, 61], 'prc'] = 3.
        namespace = {'df': panel, 'pd': pd, 'pl': pl, 'np': np,
                     'fill_date_gaps': fill_date_gaps, 'stata_multi_lag': stata_multi_lag,
                     'compute_rolling_least_squares': compute_rolling_least_squares,
                     'RollingKwargs': RollingKwargs}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(stage, str(path), 'exec'), namespace)
        # Sixty-row regressions must still count calendar months.
        regression_dates = namespace['market_pl']['time_avail_m'].to_list()
        self.assertEqual(pd.DatetimeIndex(regression_dates).tolist(), panel.time_avail_m.tolist())
        exported = namespace['temp_placebo'].set_index('time_avail_m')
        gap_dates = panel.loc[[60, 61], 'time_avail_m']
        self.assertFalse(exported.index.isin(gap_dates).any())
        merged = namespace['df'].set_index('time_avail_m')
        self.assertTrue(merged.loc[gap_dates, 'APa0'].isna().all())
        self.assertTrue(pd.notna(merged.loc[panel.time_avail_m.iloc[-1], 'APa0']))

    def test_multi_column_growth_fallback_and_industry_growth_use_calendar_months(self):
        growth = self.run_signal('GrSaleToGrReceivables.py')['GrSaleToGrReceivables']
        ww = self.run_signal('WW.py')['WW']
        keyed = self.panel.set_index(['permno', 'time_avail_m'])
        industry = self.panel.groupby('time_avail_m').sale.sum()
        for frame, signal in [(growth, 'GrSaleToGrReceivables'), (ww, 'WW')]:
            self.assert_observed_keys(frame)
            for row in frame.itertuples():
                source = keyed.loc[(row.permno, row.time_avail_m)]
                t12 = (row.permno, row.time_avail_m-pd.DateOffset(months=12))
                t24 = (row.permno, row.time_avail_m-pd.DateOffset(months=24))
                t1 = (row.permno, row.time_avail_m-pd.DateOffset(months=1))
                expected = np.nan
                if signal == 'GrSaleToGrReceivables' and t12 in keyed.index:
                    prev = keyed.loc[t12]
                    if t24 in keyed.index:
                        old = keyed.loc[t24]
                        sale_avg, rect_avg = (prev.sale+old.sale)/2, (prev.rect+old.rect)/2
                        expected = (source.sale-sale_avg)/sale_avg-(source.rect-rect_avg)/rect_avg
                    else:
                        expected = (source.sale-prev.sale)/prev.sale-(source.rect-prev.rect)/prev.rect
                elif signal == 'WW' and t12 in keyed.index and t1 in keyed.index:
                    expected = (-.091*(source.ib+source.dp)/(4*source['at'])
                                + .021*source.dltt/source['at']-.044*np.log(source['at'])
                                + .102*(industry.loc[row.time_avail_m]/industry.loc[t12[1]]-1)/4
                                - .035*(source.sale/keyed.loc[t1, 'sale']-1)/4)
                actual = getattr(row, signal)
                if pd.isna(expected): self.assertTrue(pd.isna(actual))
                else: self.assertAlmostEqual(actual, expected)

    def test_two_distinct_calendar_endpoints_survive_intervening_gap(self):
        result = self.run_signal('CapTurnover.py')['CapTurnover']
        self.assert_observed_keys(result)
        keyed = result.set_index(['permno', 'time_avail_m']).CapTurnover
        # April 2021 uses April 2020 sales and April 2019 assets despite February 2020 gap.
        self.assertAlmostEqual(keyed.loc[(1, pd.Timestamp('2021-04-01'))], (200+3*27)/(100+15))
        self.assertTrue(pd.isna(keyed.loc[(2, pd.Timestamp('2021-01-01'))]))

    def test_multi_column_helper_and_iterative_missing_rule_preserve_observed_rows(self):
        for filename, signal in [('ETR.py', 'ETR'), ('pchquick.py', 'pchquick')]:
            with self.subTest(filename=filename):
                result = self.run_signal(filename)[signal]
                self.assert_observed_keys(result)
        result = self.run_signal('pchquick.py')['pchquick'].set_index(['permno','time_avail_m']).pchquick
        # The source's explicit missing-value rule supplies zero at an observed
        # month with no calendar target, but must not create the missing month itself.
        self.assertEqual(result.loc[(2, pd.Timestamp('2020-01-01'))], 0.0)
        self.assertNotIn((2, pd.Timestamp('2019-01-01')), result.index)


if __name__ == '__main__':
    unittest.main()
