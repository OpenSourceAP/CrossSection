"""Check migrated N–Z predictors against explicit calendar endpoints.

Run from the repository root:
    /opt/venv/projects/openap/bin/python3 -m unittest discover -s Signals/tests -p test_predictor_calendar_lags_nz.py
Inputs: synthetic monthly/accounting/daily panels and production predictor scripts.
Outputs: unittest results; input reads and all signal writes are mocked.
"""

from contextlib import redirect_stdout
import io
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import polars as pl


CODE = Path(__file__).resolve().parents[1] / "pyCode"
sys.path.insert(0, str(CODE))


class PredictorCalendarLagTests(unittest.TestCase):
    def run_predictor(self, name, panels, csv=None, polars=False):
        def read(path, columns=None, **kwargs):
            panel = panels[Path(path).stem].copy()
            if columns is not None:
                panel = panel[columns]
            return pl.from_pandas(panel) if polars else panel

        with redirect_stdout(io.StringIO()), \
                patch.object(pl if polars else pd, "read_parquet", side_effect=read), \
                patch.object(pd, "read_csv", return_value=csv), \
                patch.object(pd.DataFrame, "to_csv"), \
                patch("utils.save_standardized.save_predictor"), \
                patch("utils.save_standardized.save_placebo"), \
                patch.object(Path, "exists", return_value=True):
            return runpy.run_path(str(CODE / "Predictors" / f"{name}.py"))

    def accounting(self):
        dates = pd.date_range("2018-01-01", periods=60, freq="MS")
        idx = np.arange(len(dates))
        at = 100.0 + idx
        df = pd.DataFrame({
            "permno": 1, "gvkey": 1, "time_avail_m": dates, "at": at,
            "act": .5 * at, "che": .1 * at, "lct": .2 * at,
            "dlc": .04 * at, "txp": .02 * at, "dltt": 10.0,
            "mib": 1.0, "dc": 2.0, "ceq": 30.0, "dlcch": 2.0,
            "dltis": 3.0, "dltr": 1.0, "sstk": 3.0, "prstkc": 1.0,
            "dv": 1.0, "ob": 5.0, "ib": 10.0, "ni": 20.0,
            "oancf": 3.0, "ivncf": 1.0, "fincf": 1.0, "dp": 2.0,
            "ivao": 1.0, "ivst": 1.0, "pstk": 1.0, "lt": .6 * at,
            "xrd": 1.0 + .1 * idx, "revt": 50.0,
            "capx": 5.0 + .2 * idx, "ppent": 30.0 + idx, "exchcd": 1,
        })
        df = df.loc[df.time_avail_m.ne(pd.Timestamp("2019-01-01"))].copy()
        df.loc[df.time_avail_m.eq(pd.Timestamp("2019-03-01")),
               ["at", "act", "che", "lct", "dlc", "txp", "xrd"]] = np.nan
        return df

    def indexed(self, df):
        if isinstance(df, pl.DataFrame):
            df = df.to_pandas()
        return df.set_index("time_avail_m")

    def test_accounting_formulas_use_exact_twelve_month_endpoints(self):
        # February 2020 has a valid February 2019 endpoint despite January's gap.
        # January's absent target and March's observed missing target stay missing.
        expected = {
            "NOA": 30.5 / 113,
            "NetDebtFinance": 4 / 119,
            "NetEquityFinance": 1 / 119,
            "OrderBacklog": 5 / 119,
            "OrderBacklogChg": 5 / 119 - 5 / 107,
            "PctAcc": 5.12 / 10,
            "SurpriseRD": 1,
            "TotalAccruals": 16 / 113,
        }
        for name, value in expected.items():
            with self.subTest(signal=name):
                panel = self.accounting()
                if name == "PctAcc":
                    panel["oancf"] = np.nan  # Exercise balance-sheet fallback.
                result = self.run_predictor(name, {"m_aCompustat": panel})
                frame = self.indexed(result["df"])
                self.assertEqual(set(frame.index), set(panel.time_avail_m))
                self.assertAlmostEqual(frame.loc["2020-02-01", name], value)
                self.assertTrue(pd.isna(frame.loc["2020-01-01", name]))
                self.assertTrue(pd.isna(frame.loc["2020-03-01", name]))

    def test_capex_lags_follow_imputation_without_counting_inserted_months(self):
        panel = self.accounting()
        panel.loc[panel.time_avail_m.eq(pd.Timestamp("2020-01-01")), "capx"] = np.nan
        result = self.run_predictor("ZZ1_grcapx_grcapx1y_grcapx3y", {
            "m_aCompustat": panel, "SignalMasterTable": panel,
        })
        frame = self.indexed(result["df"])
        # Missing January 2019 ppent cannot supply January 2020 replacement capx.
        self.assertTrue(pd.isna(frame.loc["2020-01-01", "capx"]))
        self.assertAlmostEqual(frame.loc["2021-02-01", "grcapx"], (12.4 - 7.6) / 7.6)
        self.assertAlmostEqual(frame.loc["2021-02-01", "grcapx1y"], (10 - 7.6) / 7.6)
        self.assertAlmostEqual(frame.loc["2021-02-01", "grcapx3y"], 3 * 12.4 / (10 + 7.6 + 5.2))
        self.assertEqual(frame.loc["2020-02-01", "FirmAge"], 25)
        self.assertEqual(set(frame.index), set(panel.time_avail_m))

    def test_rd_capital_distinguishes_absent_month_from_observed_missing_xrd(self):
        dates = pd.date_range("2013-01-01", periods=108, freq="MS")
        panel = pd.concat([pd.DataFrame({
            "permno": entity, "time_avail_m": dates, "at": 100.0,
            "xrd": 10.0, "mve_c": 10.0 * entity,
        }) for entity in (1, 2, 3)], ignore_index=True)
        panel = panel.loc[panel.time_avail_m.ne(pd.Timestamp("2018-01-01"))].copy()
        panel.loc[panel.time_avail_m.eq(pd.Timestamp("2018-02-01")), "xrd"] = np.nan
        result = self.run_predictor("RDcap", {"m_aCompustat": panel, "SignalMasterTable": panel})
        frame = self.indexed(result["df"].query("permno == 1"))
        self.assertTrue(pd.isna(frame.loc["2019-01-01", "RDcap"]))
        self.assertAlmostEqual(frame.loc["2019-02-01", "RDcap"], .22)
        self.assertEqual(set(frame.index), set(panel.time_avail_m))

    def test_revision_window_requires_all_calendar_revisions(self):
        dates = pd.date_range("2018-01-01", periods=36, freq="MS")
        panel = pd.DataFrame({"permno": 1, "tickerIBES": "A", "time_avail_m": dates,
                              "prc": 10.0, "meanest": np.arange(36, dtype=float),
                              "fpi": "1", "statpers": dates, "fpedats": dates + pd.Timedelta(days=300)})
        panel = panel.loc[panel.time_avail_m.ne(pd.Timestamp("2019-01-01"))].copy()
        result = self.run_predictor("REV6", {"IBES_EPS_Unadj": panel, "SignalMasterTable": panel})
        frame = self.indexed(result["df"])
        self.assertTrue(pd.isna(frame.loc["2019-08-01", "REV6"]))
        self.assertAlmostEqual(frame.loc["2019-09-01", "REV6"], .7)
        self.assertEqual(set(frame.index), set(panel.time_avail_m))

    def test_option_lags_keep_missing_prior_month_and_partial_calendar_mean(self):
        dates = pd.to_datetime(["2020-01-01", "2020-02-01", "2020-04-01", "2020-05-01",
                                "2020-06-01", "2020-07-01", "2020-08-01"])
        panel = pd.DataFrame({"permno": 1, "secid": 1, "time_avail_m": dates,
                              "prc": 10.0, "shrcd": 10, "vol": 100.0})
        options = pd.DataFrame({"secid": 1, "date": dates, "optvolume_js12": dates.month * 10.0})
        result = self.run_predictor("ZZ1_OptionVolume1_OptionVolume2", {
            "SignalMasterTable": panel, "monthlyCRSP": panel,
        }, csv=options)
        frame = self.indexed(result["df"])
        self.assertTrue(pd.isna(frame.loc["2020-04-01", "OptionVolume1"]))
        self.assertAlmostEqual(frame.loc["2020-08-01", "OptionVolume2"], 1.6)
        self.assertEqual(set(frame.index), set(dates))

    def test_zero_trading_aggregates_lag_calendar_months_after_daily_collapse(self):
        dates = pd.date_range("2018-01-01", periods=36, freq="MS")
        daily = pd.DataFrame({"permno": 1, "time_d": dates, "vol": 10.0, "shrout": 100.0})
        daily = daily.loc[daily.time_d.ne(pd.Timestamp("2019-01-01"))].copy()
        result = self.run_predictor("ZZ1_zerotrade_zerotradeAlt1_zerotradeAlt12", {"dailyCRSP": daily})
        frame = result["collapsed"].set_index("time_avail_m")
        self.assertTrue(pd.isna(frame.loc[201902, "zerotrade1M"]))
        self.assertAlmostEqual(frame.loc[201903, "zerotrade1M"], 21 / (.1 * 480000))
        self.assertTrue(pd.isna(frame.loc[201907, "zerotrade6M"]))
        self.assertAlmostEqual(frame.loc[201908, "zerotrade6M"], 21 / (.6 * 11000))
        self.assertTrue(pd.isna(frame.loc[202001, "zerotrade12M"]))
        self.assertAlmostEqual(frame.loc[202002, "zerotrade12M"], 21 / (1.2 * 11000))
        self.assertNotIn(201901, frame.index)

    def test_share_volume_keeps_original_first_observation_rules(self):
        dates = pd.to_datetime(["2020-01-01", "2020-03-01", "2020-04-01", "2020-05-01"])
        panel = pd.DataFrame({"permno": 1, "time_avail_m": dates, "sicCRSP": 2000,
                              "exchcd": 1, "vol": 1.0, "shrout": 100.0})
        result = self.run_predictor("ShareVol", {"SignalMasterTable": panel, "monthlyCRSP": panel}, polars=True)
        frame = self.indexed(result["df"])
        self.assertEqual(frame.loc["2020-03-01", "_n"], 1)
        self.assertTrue(pd.isna(frame.loc["2020-03-01", "l1_vol"]))
        self.assertEqual(frame.loc["2020-05-01", "ShareVol"], 0)
        self.assertEqual(set(frame.index), set(dates))

    def test_patent_june_lags_use_year_endpoints_across_missing_junes(self):
        dates = pd.date_range("1975-01-01", "1984-12-01", freq="MS")
        panel = pd.concat([pd.DataFrame({
            "permno": entity, "gvkey": entity, "time_avail_m": dates,
            "xrd": dates.year.astype(float) - 1970, "sich": 2000,
            "sicCRSP": 2000, "datadate": dates, "ceq": 10.0,
            "mve_c": entity * 100.0, "exchcd": 1,
        }) for entity in (1, 2, 3)], ignore_index=True)
        panel = panel.loc[panel.time_avail_m.ne(pd.Timestamp("1979-06-01"))].copy()
        patents = pd.DataFrame([(entity, year, float(year - 1970))
                                for entity in (1, 2, 3) for year in range(1975, 1985)],
                               columns=["gvkey", "year", "npat"])
        result = self.run_predictor("PatentsRD", {"SignalMasterTable": panel, "m_aCompustat": panel,
                                                 "PatentDataProcessed": patents})
        frame = result["df"].query("permno == 1").set_index("time_avail_m")
        self.assertEqual(frame.loc[198006, "comp1"], 8.0)
        self.assertEqual(frame.loc[198106, "comp1"], 0.0)
        self.assertAlmostEqual(frame.loc[198106, "RDcap"], 14.0)
        self.assertNotIn(197906, frame.index)


if __name__ == "__main__":
    unittest.main()
