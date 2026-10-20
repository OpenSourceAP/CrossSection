"""Exercise migrated A–M production predictors on explicit calendar-gap fixtures.

Run from the repository root:
    /opt/venv/projects/openap/bin/python3 -m unittest discover -s Signals/tests -p test_predictor_calendar_lags_am.py
Inputs: synthetic monthly accounting/market/options panels; production scripts.
Outputs: unittest results. Input reads and signal writes are mocked; no downloads.
"""

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


CODE = Path(__file__).resolve().parents[1] / "pyCode"
sys.path.insert(0, str(CODE))
import config


class PredictorCalendarLagTests(unittest.TestCase):
    def run_predictor(self, name, inputs):
        captures = []

        def read_input(path, columns=None, **kwargs):
            frame = inputs[Path(path).name].copy()
            return frame if columns is None else frame[list(columns)]

        def save_pd(frame, path_or_buf=None, *args, **kwargs):
            if "permno" in frame.index.names:
                frame = frame.reset_index()
            captures.append(frame.copy())

        def save_pl(frame, file=None, *args, **kwargs):
            captures.append(frame.to_pandas())

        with contextlib.redirect_stdout(io.StringIO()), \
                patch.object(pd, "read_parquet", side_effect=read_input), \
                patch.object(pd, "read_csv", side_effect=read_input), \
                patch.object(pl, "read_parquet", side_effect=lambda *a, **k: pl.from_pandas(read_input(*a, **k))), \
                patch.object(pd.DataFrame, "to_csv", save_pd), \
                patch.object(pl.DataFrame, "write_csv", save_pl), \
                patch.object(Path, "mkdir"), \
                patch.object(Path, "exists", return_value=True), \
                patch.object(config, "PATCH_OPTIONM_IV", False):
            namespace = runpy.run_path(str(CODE / "Predictors" / f"{name}.py"))
        self.assertEqual(len(captures), 1)
        result = captures[0]
        self.assertFalse(result.duplicated(["permno", "yyyymm"]).any())
        return namespace, result.set_index(["permno", "yyyymm"])[name]

    def accounting_panel(self):
        dates = pd.date_range("2010-01-01", periods=30, freq="MS")
        frames = []
        for permno in [1, 2]:
            t = np.arange(len(dates), dtype=float)
            frame = pd.DataFrame({
                "gvkey": str(permno), "permno": permno, "time_avail_m": dates,
                "at": 100.0 * permno + t, "act": 50 + 2 * t,
                "che": 5.0, "lct": 20 + t, "dlc": 2.0, "txp": 1.0,
                "dp": 3.0,
            })
            if permno == 1:
                frame = frame.drop(index=6)
                frame.loc[8, "at"] = np.nan
                frame.loc[0, "txp"] = np.nan
            frames.append(frame)
        return pd.concat(frames, ignore_index=True)

    def test_asset_growth_uses_exact_endpoints_across_gaps(self):
        panel = self.accounting_panel()
        namespace, output = self.run_predictor("AssetGrowth", {"m_aCompustat.parquet": panel})
        self.assertAlmostEqual(output.loc[1, 201101], 12 / 100)
        self.assertAlmostEqual(output.loc[2, 201101], 12 / 200)
        self.assertNotIn((1, 201107), output.index)  # Target July 2010 absent.
        self.assertNotIn((1, 201109), output.index)  # Target assets missing.
        self.assertEqual(len(namespace["df"]), len(panel))

    def test_multivariable_accruals_preserves_tax_imputation(self):
        panel = self.accounting_panel()
        _, output = self.run_predictor("Accruals", {"m_aCompustat.parquet": panel})
        # Delta act=24, delta che=0, delta lct=12, delta dlc=0,
        # delta filled taxes=1, depreciation=3, average assets=106.
        self.assertAlmostEqual(output.loc[1, 201101], (24 - (12 - 1) - 3) / 106)
        self.assertNotIn((1, 201107), output.index)

    def test_forecast_change_rejects_previous_observation_across_gap(self):
        panel = self.accounting_panel()
        # Enough firms for a well-defined monthly median accrual split.
        extras = []
        for permno in [3, 4]:
            frame = panel[panel.permno == 2].copy()
            frame["permno"] = permno
            frame["act"] *= permno
            extras.append(frame)
        panel = pd.concat([panel, *extras], ignore_index=True)
        # Remove February 2012 only for the firm with the largest accruals.
        panel = panel[~((panel.permno == 4) & (panel.time_avail_m == "2012-02-01"))].copy()
        master = panel[["permno", "time_avail_m"]].copy()
        master["tickerIBES"] = master.permno.astype(str)
        ibes = master[["tickerIBES", "time_avail_m"]].copy()
        ibes["fpi"] = "1"
        ibes["meanest"] = ibes.time_avail_m.dt.year * 12 + ibes.time_avail_m.dt.month
        namespace, output = self.run_predictor("ChForecastAccrual", {
            "m_aCompustat.parquet": panel, "SignalMasterTable.parquet": master,
            "IBES_EPS_Unadj.parquet": ibes,
        })
        self.assertNotIn((4, 201203), output.index)
        self.assertEqual(output.loc[4, 201204], 1)
        self.assertEqual(len(namespace["df"]), len(panel))

    def test_seasonal_signal_does_not_save_inserted_current_month(self):
        dates = pd.date_range("2010-01-01", periods=15, freq="MS")
        panel = pd.DataFrame({"permno": 1, "time_avail_m": dates, "ret": 0.1})
        panel = panel.drop(index=12)
        _, output = self.run_predictor("MomSeasonShort", {"SignalMasterTable.parquet": panel})
        self.assertNotIn((1, 201101), output.index)
        self.assertAlmostEqual(output.loc[1, 201102], 0.1)

    def test_offseason_average_excludes_absent_month_but_zeroes_observed_missing(self):
        dates = pd.date_range("2010-01-01", periods=15, freq="MS")
        panel = pd.DataFrame({"permno": 1, "time_avail_m": dates, "ret": np.arange(15) / 100.0})
        panel = panel.drop(index=4)
        panel.loc[5, "ret"] = np.nan
        _, output = self.run_predictor("Mom12mOffSeason", {"SignalMasterTable.parquet": panel})
        expected = np.mean([0.0 if i == 5 else i / 100.0 for i in range(2, 12) if i != 4])
        self.assertAlmostEqual(output.loc[1, 201101], expected)
        self.assertNotIn((1, 201005), output.index)

    def test_industry_mean_uses_only_observed_current_firms(self):
        dates = pd.date_range("2020-01-01", periods=8, freq="MS")
        panels = []
        for permno, ret, weight in [(1, 0.1, 100.0), (2, 0.2, 300.0)]:
            panel = pd.DataFrame({"permno": permno, "time_avail_m": dates,
                                  "ret": ret, "mve_c": weight, "sicCRSP": 2000})
            if permno == 1:
                panel = panel.drop(index=6)
            panels.append(panel)
        master = pd.concat(panels, ignore_index=True)
        _, output = self.run_predictor("IndMom", {"SignalMasterTable.parquet": master})
        expected = ((1.1 ** 5 - 1) * 100 + (1.2 ** 5 - 1) * 300) / 400
        self.assertAlmostEqual(output.loc[1, 202006], expected)
        self.assertNotIn((1, 202007), output.index)
        self.assertAlmostEqual(output.loc[2, 202007], 1.2 ** 5 - 1)

    def test_rolling_dividend_pipeline_keeps_original_output_keys(self):
        dates = pd.date_range("2020-01-01", periods=30, freq="MS")
        master = pd.DataFrame({"permno": 1, "time_avail_m": dates, "exchcd": 1, "shrcd": 10}).drop(index=20)
        distributions = pd.DataFrame({"permno": 1, "exdt": dates[::3], "divamt": 1.0, "cd2": 2})
        _, output = self.run_predictor("DivOmit", {
            "SignalMasterTable.parquet": master, "CRSPdistributions.parquet": distributions,
        })
        expected = {(1, d.year * 100 + d.month) for d in master.time_avail_m}
        self.assertEqual(set(output.index), expected)

    def test_option_volatility_changes_use_calendar_months_for_each_security(self):
        dates = pd.to_datetime(["2020-01-01", "2020-03-01", "2020-04-01"])
        rows = []
        for secid in [1, 2]:
            for date, call, put in zip(dates, [0.1, 0.4, 0.5], [0.2, 0.6, 0.9]):
                for flag, vol in [("C", call * secid), ("P", put * secid)]:
                    rows.append({"secid": secid, "time_avail_m": date, "days": 30,
                                 "delta": 50, "cp_flag": flag, "impl_vol": vol})
        options = pd.DataFrame(rows)
        master = options[["secid", "time_avail_m"]].drop_duplicates().copy()
        master["permno"] = master.secid
        for name, expected in [("dVolCall", 0.1), ("dVolPut", 0.3), ("dCPVolSpread", 0.2)]:
            with self.subTest(name=name):
                _, output = self.run_predictor(name, {
                    "OptionMetricsVolSurf.csv": options, "SignalMasterTable.parquet": master,
                })
                self.assertNotIn((1, 202003), output.index)
                self.assertAlmostEqual(output.loc[1, 202004], expected)
                self.assertAlmostEqual(output.loc[2, 202004], expected * 2)


if __name__ == "__main__":
    unittest.main()
