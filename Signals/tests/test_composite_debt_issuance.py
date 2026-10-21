"""Check calendar debt lags through the production predictor and CSV formatter.

Run from the repository root:
    /opt/venv/projects/openap/bin/python3 -m unittest discover -s Signals/tests -p test_composite_debt_issuance.py
Inputs: synthetic monthly Compustat panels and the production predictor.
Outputs: unittest results; parquet reads and CSV writes are mocked.
"""

from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import polars as pl


PREDICTOR = Path(__file__).resolve().parents[1] / "pyCode/Predictors/CompositeDebtIssuance.py"
SIGNAL = "CompositeDebtIssuance"


class CompositeDebtIssuanceTests(unittest.TestCase):
    def setUp(self):
        dates = pd.date_range("2010-01-01", periods=75, freq="MS")
        panels = []
        for permno in [1, 2]:
            panel = pd.DataFrame({
                "gvkey": str(permno), "permno": permno, "time_avail_m": dates,
                "dltt": 100.0 * permno + np.arange(len(dates)), "dlc": 10.0,
            })
            if permno == 1:
                panel = panel.drop(index=6)  # July 2010 is an absent target.
                panel.loc[8, "dltt"] = np.nan  # September exists but debt is missing.
                panel.loc[[11, 70], ["dltt", "dlc"]] = 0.0
            panels.append(panel)
        short = panels[1].iloc[:12].copy()
        short["permno"] = 3
        short["gvkey"] = "3"
        panels.append(short)
        # Existing keep-first deduplication must precede lagging.
        duplicate = panels[0].loc[[60]].copy()
        duplicate["dltt"] = 9999.0
        self.compustat = pd.concat([*panels, duplicate], ignore_index=True)

    def run_predictor(self):
        with patch.object(pd, "read_parquet", return_value=self.compustat.copy()), \
                patch.object(Path, "mkdir"), \
                patch.object(pl.DataFrame, "write_csv", autospec=True) as save:
            namespace = runpy.run_path(str(PREDICTOR))
        save.assert_called_once()
        output = save.call_args.args[0].to_pandas()
        self.assertEqual(output.columns.tolist(), ["permno", "yyyymm", SIGNAL])
        self.assertFalse(output.duplicated(["permno", "yyyymm"]).any())
        self.assertTrue(np.isfinite(output[SIGNAL]).all())
        return namespace["df"], output.set_index(["permno", "yyyymm"])[SIGNAL]

    def test_missing_calendar_target_and_missing_debt_stay_missing(self):
        observed, output = self.run_predictor()
        for month in [201507, 201509]:
            with self.subTest(month=month):
                self.assertNotIn((1, month), output.index)
        indexed = observed.set_index(["permno", "time_avail_m"])[SIGNAL]
        self.assertTrue(pd.isna(indexed.loc[1, pd.Timestamp("2015-07-01")]))
        self.assertTrue(pd.isna(indexed.loc[1, pd.Timestamp("2015-09-01")]))

    def test_valid_endpoints_survive_intermediate_gap_and_keep_first_duplicate(self):
        _, output = self.run_predictor()
        self.assertAlmostEqual(output.loc[1, 201501], np.log(170.0 / 110.0))
        self.assertAlmostEqual(output.loc[1, 201508], np.log(177.0 / 117.0))

    def test_entities_history_and_zero_debt(self):
        _, output = self.run_predictor()
        self.assertAlmostEqual(output.loc[2, 201501], np.log(270.0 / 210.0))
        self.assertFalse(output.index.get_level_values("permno").isin([3]).any())
        self.assertFalse((output.index.get_level_values("yyyymm") < 201501).any())
        self.assertNotIn((1, 201511), output.index)  # Current debt is zero.
        self.assertNotIn((1, 201512), output.index)  # Lagged debt is zero.

    def test_inserted_calendar_months_do_not_reach_output(self):
        observed, output = self.run_predictor()
        expected = pd.MultiIndex.from_frame(
            self.compustat[["permno", "time_avail_m"]].drop_duplicates()
        )
        actual = pd.MultiIndex.from_frame(observed[["permno", "time_avail_m"]])
        self.assertEqual(set(actual), set(expected))
        self.assertEqual(len(actual), len(expected))
        self.assertNotIn((1, 201007), output.index)


if __name__ == "__main__":
    unittest.main()
