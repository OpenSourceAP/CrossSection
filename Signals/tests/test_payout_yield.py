"""Check annual preferred-stock reductions using synthetic monthly inputs.

Run from the repository root:
    /opt/venv/projects/openap/bin/python3 -m unittest discover -s Signals/tests -p test_payout_yield.py
Inputs: synthetic Compustat and market-value panels; the production predictor.
Outputs: unittest results; no signal files are written.
"""

from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd


PREDICTOR = Path(__file__).resolve().parents[1] / "pyCode/Predictors/PayoutYield.py"


class PayoutYieldTests(unittest.TestCase):
    def setUp(self):
        dates = pd.date_range("2018-01-01", periods=48, freq="MS")
        panels = []
        for permno in range(1, 11):
            preferred = np.repeat([20.0, 12.0, 5.0, 5.0], 12)
            if permno == 2:
                preferred[:] = 10  # Outstanding stock is not a payout.
            elif permno == 3:
                preferred = np.repeat([5.0, 12.0, 20.0, 20.0], 12)
            elif permno == 4:
                preferred[12] = np.nan
            elif permno == 5:
                preferred[24] = np.nan
            panel = pd.DataFrame({
                "permno": permno, "time_avail_m": dates,
                "datadate": np.repeat(pd.date_range("2017-06-30", periods=4, freq="YE-JUN"), 12),
                "dvc": 2.0, "prstkc": 3.0, "pstkrv": preferred,
                "sstk": 0.0, "sic": "2000", "ceq": 10.0,
            })
            if permno == 6:
                panel = panel.drop(index=12)  # Do not use the 12th previous row.
            elif permno == 7:
                panel[["dvc", "prstkc"]] = 0.0
            elif permno == 8:
                panel["dvc"] = np.nan
            elif permno == 9:
                panel["sic"] = "6000"
            elif permno == 10:
                panel["ceq"] = 0.0
            panels.append(panel)
        self.compustat = pd.concat(panels, ignore_index=True)
        self.master = self.compustat[["permno", "time_avail_m"]].copy()
        self.master["mve_permco"] = 100 + self.master.time_avail_m.dt.month

    def run_predictor(self):
        with patch.object(pd, "read_parquet", side_effect=[self.compustat, self.master]), \
                patch.object(pd.DataFrame, "to_csv") as save:
            result = runpy.run_path(str(PREDICTOR))["result"]
        save.assert_called_once()
        self.assertFalse(result.duplicated(["permno", "yyyymm"]).any())
        return result.set_index(["permno", "yyyymm"]).PayoutYield

    def test_annual_reduction_persists_and_uses_six_month_denominator(self):
        result = self.run_predictor()
        self.assertAlmostEqual(result.loc[1, 202001], (2 + 3 + 7) / 107)
        self.assertAlmostEqual(result.loc[1, 202002], (2 + 3 + 7) / 108)
        self.assertAlmostEqual(result.loc[2, 202001], (2 + 3) / 107)
        self.assertAlmostEqual(result.loc[3, 202001], (2 + 3) / 107)

    def test_unavailable_difference_adds_zero_without_inventing_redemptions(self):
        result = self.run_predictor()
        for permno in [4, 5, 6]:
            with self.subTest(permno=permno):
                self.assertAlmostEqual(result.loc[permno, 202001], 5 / 107)
        # The gap affects only its matching month, not the next month's lag.
        self.assertAlmostEqual(result.loc[6, 202002], 12 / 108)

    def test_payout_and_universe_filters_remain_in_effect(self):
        result = self.run_predictor()
        self.assertAlmostEqual(result.loc[7, 202001], 7 / 107)
        self.assertNotIn((7, 202101), result.index)  # No flow despite stock > 0.
        self.assertFalse(result.index.get_level_values("permno").isin([8, 9, 10]).any())
        self.assertTrue((result > 0).all())
        self.assertNotIn((1, 201911), result.index)  # Fewer than 24 months.


if __name__ == "__main__":
    unittest.main()
