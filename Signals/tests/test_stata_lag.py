"""Check calendar lag values, grid expansion, and the existing backend API.

Run from the repository root:
    /opt/venv/projects/openap/bin/python3 -m unittest discover -s Signals/tests -p test_stata_lag.py
Inputs: synthetic Pandas/Polars panels and the shared lag utility.
Outputs: unittest results; no data files are read or written.
"""

from pathlib import Path
import sys
import unittest

import pandas as pd
import polars as pl


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pyCode"))
from utils.stata_replication import (  # noqa: E402
    stata_multi_lag,
    stata_multi_lag_pd,
    stata_multi_lag_pl,
)


class StataLagTests(unittest.TestCase):
    def panel(self, backend, rows):
        df = pd.DataFrame(rows, columns=["entity", "date", "value"])
        df["date"] = pd.to_datetime(df["date"])
        df["_observed"] = True
        return df if backend == "pandas" else pl.from_pandas(df)

    def indexed(self, result):
        if isinstance(result, pl.DataFrame):
            result = result.to_pandas()
        result["date"] = pd.to_datetime(result["date"])
        return result.set_index(["entity", "date"])

    def assert_value(self, result, entity, date, column, expected):
        actual = result.loc[(entity, pd.Timestamp(date)), column]
        if expected is None:
            self.assertTrue(pd.isna(actual), (entity, date, column, actual))
        else:
            self.assertEqual(actual, expected)

    def test_monthly_gaps_missing_values_and_observed_rows(self):
        # Deliberately unsorted and interleaved: the helper sorts within entity.
        rows = [
            (2, "2020-02-01", 200.0), (1, "2020-05-01", 50.0),
            (1, "2020-01-01", 10.0), (1, "2020-04-01", 40.0),
            (2, "2020-01-01", 100.0), (1, "2020-03-01", None),
        ]
        for backend in ("pandas", "polars"):
            with self.subTest(backend=backend):
                result = self.indexed(stata_multi_lag(
                    self.panel(backend, rows), "entity", "date", "value", [1, 3]
                ))
                expected_keys = [
                    (1, pd.Timestamp(date)) for date in pd.date_range("2020-01-01", periods=5, freq="MS")
                ] + [(2, pd.Timestamp("2020-01-01")), (2, pd.Timestamp("2020-02-01"))]
                self.assertEqual(result.index.tolist(), expected_keys)
                for date, lag1, lag3 in [
                    ("2020-01-01", None, None),
                    ("2020-02-01", 10.0, None),
                    ("2020-03-01", None, None),  # Missing target month.
                    ("2020-04-01", None, 10.0),  # Existing missing value; valid 3-month endpoint.
                    ("2020-05-01", 40.0, None),
                ]:
                    self.assert_value(result, 1, date, "value_lag1", lag1)
                    self.assert_value(result, 1, date, "value_lag3", lag3)
                self.assert_value(result, 2, "2020-01-01", "value_lag1", None)
                self.assert_value(result, 2, "2020-02-01", "value_lag1", 100.0)
                self.assert_value(result, 1, "2020-02-01", "value", None)
                self.assert_value(result, 1, "2020-02-01", "_observed", None)
                observed = result.loc[result["_observed"].eq(True)]
                self.assertEqual(set(observed.index), {(entity, pd.Timestamp(date)) for entity, date, _ in rows})
                self.assert_value(observed, 1, "2020-03-01", "value", None)

    def test_annual_grid_and_multiyear_endpoint(self):
        rows = [(1, "2018-01-01", 8.0), (1, "2020-01-01", 20.0),
                (1, "2021-01-01", None), (1, "2022-01-01", 22.0)]
        for backend in ("pandas", "polars"):
            with self.subTest(backend=backend):
                result = self.indexed(stata_multi_lag(
                    self.panel(backend, rows), "entity", "date", "value", [1, 2], freq="Y", prefix="l"
                ))
                self.assertEqual(result.index.tolist(), [(1, pd.Timestamp(year, 1, 1)) for year in range(2018, 2023)])
                for year, lag1, lag2 in [(2018, None, None), (2019, 8.0, None),
                                        (2020, None, 8.0), (2021, 20.0, None),
                                        (2022, None, 20.0)]:
                    self.assert_value(result, 1, f"{year}-01-01", "l1_value", lag1)
                    self.assert_value(result, 1, f"{year}-01-01", "l2_value", lag2)
                self.assert_value(result, 1, "2019-01-01", "_observed", None)
                self.assertEqual(result["_observed"].eq(True).sum(), len(rows))

    def test_daily_and_quarterly_frequency_forwarding(self):
        for backend in ("pandas", "polars"):
            for freq, dates in [("D", ["2020-01-01", "2020-01-02", "2020-01-03"]),
                                ("Q", ["2020-01-01", "2020-04-01", "2020-07-01"])]:
                with self.subTest(backend=backend, freq=freq):
                    rows = [(1, dates[0], 1.0), (1, dates[2], 3.0)]
                    result = self.indexed(stata_multi_lag(
                        self.panel(backend, rows), "entity", "date", "value", [1, 2], freq=freq
                    ))
                    self.assertEqual(result.index.tolist(), [(1, pd.Timestamp(date)) for date in dates])
                    self.assert_value(result, 1, dates[2], "value_lag1", None)
                    self.assert_value(result, 1, dates[2], "value_lag2", 1.0)

    def test_complete_grid_without_filling(self):
        rows = [(1, "2020-01-01", 1.0), (1, "2021-01-01", None),
                (1, "2022-01-01", 3.0)]
        for backend in ("pandas", "polars"):
            with self.subTest(backend=backend):
                result = self.indexed(stata_multi_lag(
                    self.panel(backend, rows), "entity", "date", "value", [1, 2], freq="Y", fill_gaps=False
                ))
                self.assertEqual(len(result), 3)
                self.assertTrue(result["_observed"].eq(True).all())
                self.assert_value(result, 1, "2021-01-01", "value_lag1", 1.0)
                self.assert_value(result, 1, "2022-01-01", "value_lag1", None)
                self.assert_value(result, 1, "2022-01-01", "value_lag2", 1.0)

    def test_column_api_and_return_type(self):
        rows = [(1, "2020-01-01", 10.0), (1, "2020-02-01", 20.0)]
        pandas_panel = self.panel("pandas", rows)
        result = stata_multi_lag(pandas_panel, "entity", "date", ["value"], [1])
        self.assertIsInstance(result, pd.DataFrame)
        self.assert_value(self.indexed(result), 1, "2020-02-01", "value_lag1", 10.0)
        with self.assertRaisesRegex(ValueError, "only supports single value_col"):
            stata_multi_lag(pandas_panel, "entity", "date", ["value", "other"], [1])
        polars_panel = self.panel("polars", rows).with_columns((pl.col("value") * 2).alias("other"))
        result = stata_multi_lag(polars_panel, "entity", "date", ["value", "other"], [1])
        self.assertIsInstance(result, pl.DataFrame)
        result = self.indexed(result)
        self.assert_value(result, 1, "2020-02-01", "value_lag1", 10.0)
        self.assert_value(result, 1, "2020-02-01", "other_lag1", 20.0)

    def test_invalid_frequency_rejected_by_wrapper_and_both_backends(self):
        rows = [(1, "2020-01-01", 10.0)]
        for backend, direct in [("pandas", stata_multi_lag_pd), ("polars", stata_multi_lag_pl)]:
            for function in (stata_multi_lag, direct):
                for fill_gaps in (True, False):
                    with self.subTest(backend=backend, function=function.__name__, fill_gaps=fill_gaps):
                        value_col = ["value"] if function is stata_multi_lag_pl else "value"
                        with self.assertRaisesRegex(ValueError, "Unsupported lag frequency.*Expected M, D, Q, or Y"):
                            function(self.panel(backend, rows), "entity", "date", value_col, [1],
                                     freq="invalid", fill_gaps=fill_gaps)


if __name__ == "__main__":
    unittest.main()
