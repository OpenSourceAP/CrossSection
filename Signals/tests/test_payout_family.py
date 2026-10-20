"""Check payout-family formulas and eligibility with small monthly panels.

Run from the repository root:
    /opt/venv/projects/openap/bin/python3 -m unittest discover -s Signals/tests -p 'test_payout*.py'
Inputs: synthetic accounting/master panels and the three production scripts.
Outputs: unittest results; CSV writes are mocked.
"""

from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd


CODE = Path(__file__).resolve().parents[1] / "pyCode"


class PayoutFamilyTests(unittest.TestCase):
    def run_signal(self, name):
        annual = name == "NetPayoutYield"
        lag = 12 if annual else 3
        dates = pd.date_range("2018-01-01", periods=48, freq="MS")
        panels = []
        masters = []
        for permno in range(1, 22):
            panel = pd.DataFrame({
                "permno": permno, "gvkey": permno, "time_avail_m": dates,
                "dvc": 2.0, "dvpsxq": 2.0, "cshoq": 1.0, "ajexq": 1.0,
                "prstkc": 3.0, "prstkcyq": 3.0, "sstk": 1.0, "sstkyq": 1.0,
                "pstkrv": 10.0, "pstkq": 10.0, "sic": "2000", "ceq": 10.0,
            })
            if permno in (2, 3):
                panel.loc[24:, ["pstkrv", "pstkq"]] = 2.0 if permno == 2 else 18.0
            elif permno == 4:
                panel.loc[24, ["pstkrv", "pstkq"]] = np.nan
            elif permno == 5:
                panel.loc[24 - lag, ["pstkrv", "pstkq"]] = np.nan
            elif permno == 6:
                panel = panel.drop(index=24 - lag)
            elif permno == 7:
                panel[["dvc", "dvpsxq", "prstkc", "prstkcyq", "sstk", "sstkyq"]] = 0.0
            elif permno == 8:
                panel[["sstk", "sstkyq"]] = 9.0
            elif permno == 9:
                panel[["sstk", "sstkyq"]] = 5.0  # Exact cancellation of nonzero flows.
            elif permno == 10:
                panel[["dvc", "dvpsxq"]] = np.nan
            elif permno == 11:
                panel[["dvc", "dvpsxq"]] = 1e-19
                panel[["prstkc", "prstkcyq", "sstk", "sstkyq"]] = 0.0
            elif permno == 12:
                panel[["dvc", "dvpsxq"]] = 0.0
                panel[["cshoq", "ajexq"]] = np.nan
            elif permno == 13:
                panel[["prstkc", "prstkcyq"]] = np.nan
            elif permno == 18:
                panel["sic"] = "6000"
            elif permno == 20:
                panel["cshoq"] = np.nan  # Nonzero dividends require shares.
            elif permno == 21:
                panel[["sstk", "sstkyq"]] = np.nan
            master = panel[["permno", "gvkey", "time_avail_m"]].copy()
            master["mve_permco"] = 100.0 + master.time_avail_m.dt.month
            if permno in (14, 15, 16, 17):
                master["mve_permco"] = {14: 0.0, 15: -100.0, 16: np.inf, 17: np.nan}[permno]
            if permno == 19:
                panel = panel.drop(index=24)  # A master row without accounting data.
            panels.append(panel)
            masters.append(master)
        accounting = pd.concat(panels, ignore_index=True)
        master = pd.concat(masters, ignore_index=True)
        reads = [accounting, master] if annual else [master, accounting.drop(columns="permno")]
        script = CODE / ("Predictors" if annual else "Placebos") / f"{name}.py"
        with patch.object(pd, "read_parquet", side_effect=reads), \
                patch.object(pd.DataFrame, "to_csv") as save, patch("os.makedirs"):
            result = runpy.run_path(str(script))["result"]
        save.assert_called_once()
        self.assertFalse(result.duplicated(["permno", "yyyymm"]).any())
        return result.set_index(["permno", "yyyymm"])[name]

    def test_preferred_adjustments_and_denominator_dates(self):
        for name in ("NetPayoutYield", "PayoutYield_q", "NetPayoutYield_q"):
            with self.subTest(signal=name):
                result = self.run_signal(name)
                gross = name == "PayoutYield_q"
                denominator = 101 if name == "NetPayoutYield_q" else 107
                expected = {1: 5 if gross else 4, 2: 13 if gross else 12, 3: 5 if gross else 12}
                for permno, numerator in expected.items():
                    self.assertAlmostEqual(result.loc[permno, 202001], numerator / denominator)
                # Unavailable current/lagged balance or calendar month adds zero.
                for permno in (4, 5, 6):
                    self.assertAlmostEqual(result.loc[permno, 202001], (5 if gross else 4) / denominator)
                self.assertNotIn((19, 202001), result.index)
                if name == "NetPayoutYield":
                    self.assertNotIn((6, 201912), result.index)  # Inserted month does not count toward age.
                else:
                    self.assertAlmostEqual(result.loc[2, 202004], (5 if gross else 4) / (104 if not gross else 110))

    def test_zero_negative_missing_and_small_yields(self):
        for name in ("NetPayoutYield", "PayoutYield_q", "NetPayoutYield_q"):
            with self.subTest(signal=name):
                result = self.run_signal(name)
                gross = name == "PayoutYield_q"
                denominator = 101 if name == "NetPayoutYield_q" else 107
                self.assertNotIn((7, 202001), result.index)
                if gross:
                    self.assertTrue((result > 0).all())
                else:
                    self.assertAlmostEqual(result.loc[8, 202001], -4 / denominator)
                    self.assertNotIn((9, 202001), result.index)
                    self.assertTrue((result != 0).all())
                self.assertTrue(np.isfinite(result).all())
                self.assertEqual(result.loc[11, 202001], 1e-19 / denominator)
                self.assertAlmostEqual(result.loc[12, 202001], (3 if gross else 2) / denominator)
                for permno in (10, 13, 14, 15, 16, 17):
                    self.assertNotIn((permno, 202001), result.index)
                if not gross:
                    self.assertNotIn((21, 202001), result.index)
                if name == "NetPayoutYield":
                    self.assertNotIn((18, 202001), result.index)
                else:
                    self.assertIn((18, 202001), result.index)
                    self.assertNotIn((20, 202001), result.index)


if __name__ == "__main__":
    unittest.main()
