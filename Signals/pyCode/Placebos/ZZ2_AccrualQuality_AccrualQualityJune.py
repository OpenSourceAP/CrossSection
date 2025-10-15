# ABOUTME: ZZ2_AccrualQuality_AccrualQualityJune.py - calculates accrual quality placebos
# ABOUTME: Python equivalent of ZZ2_AccrualQuality_AccrualQualityJune.do, mirrors Stata logic

"""
ZZ2_AccrualQuality_AccrualQualityJune.py

Inputs:
    - a_aCompustat.parquet: columns [gvkey, permno, time_avail_m, datadate, fyear, ib, act, che, lct, dlc, dp, at, sale, sic, ppegt]

Outputs:
    - AccrualQuality.csv: [permno, yyyymm, AccrualQuality]
    - AccrualQualityJune.csv: [permno, yyyymm, AccrualQualityJune]

Usage:
    cd Signals/pyCode
    python3 Placebos/ZZ2_AccrualQuality_AccrualQualityJune.py

Notes:
    - Stata’s industry-by-year regressions rely on its `regress` machinery with
      collinearity checks, so this script uses `statsmodels` via `utils.stata_regress.regress`
      instead of `polars` rolling OLS to reproduce the exact sample filtering and
      dropped-column behavior.
    - Fiscal-year gaps must break lags/leads the way Stata’s `l.` operator does, so
      custom lag helpers enforce the "only when years are consecutive" rule; the
      generic `stata_multi_lag` helper is avoided because it cannot detect these
      gaps when operating without calendar backfilling.
"""

from __future__ import annotations

import os
import sys
from typing import Iterable

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_placebo
from utils.sicff import sicff
from utils.stata_regress import regress


def _lag_with_gap(df: pd.DataFrame, column: str, periods: int = 1) -> pd.Series:
    """Stata-like lag that respects annual gaps within each gvkey."""

    grouped = df.groupby("gvkey", group_keys=False)
    shifted = grouped[column].shift(periods)
    prev_year = grouped["fyear"].shift(periods)
    valid = (df["fyear"] - prev_year) == periods
    return shifted.where(valid, np.nan)


def _lead_with_gap(df: pd.DataFrame, column: str, periods: int = 1) -> pd.Series:
    """Stata-like lead that respects annual gaps within each gvkey."""

    grouped = df.groupby("gvkey", group_keys=False)
    shifted = grouped[column].shift(-periods)
    next_year = grouped["fyear"].shift(-periods)
    valid = (next_year - df["fyear"]) == periods
    return shifted.where(valid, np.nan)


def _row_std(values: np.ndarray) -> float:
    """Sample standard deviation with NaNs ignored; returns NaN if <2 valid obs."""

    finite_vals = values[np.isfinite(values)]
    if finite_vals.size <= 1:
        return np.nan
    return float(finite_vals.std(ddof=1))


def _prepare_annual_data(df: pd.DataFrame) -> pd.DataFrame:
    """Reproduce the annual panel transformations from the Stata .do file."""

    df = df.sort_values(["gvkey", "fyear"]).copy()

    # Lags needed for accrual components
    for col in ["act", "che", "lct", "dlc", "at"]:
        df[f"l_{col}"] = _lag_with_gap(df, col, periods=1)

    avg_at = (df["at"] + df["l_at"]) / 2.0
    avg_at = avg_at.replace(0, np.nan)
    df["avg_at"] = avg_at

    df["tempAccruals"] = (
        (df["act"] - df["l_act"])
        - (df["che"] - df["l_che"])
        - ((df["lct"] - df["l_lct"]) - (df["dlc"] - df["l_dlc"]))
        - df["dp"]
    ) / df["avg_at"]

    df["tempCAcc"] = df["tempAccruals"] + df["dp"] / df["avg_at"]
    df["tempRev"] = df["sale"] / df["avg_at"]
    df["tempPPE"] = df["ppegt"] / df["avg_at"]
    df["tempCFO"] = df["ib"] / df["avg_at"] - df["tempAccruals"]

    df["l1_tempRev"] = _lag_with_gap(df, "tempRev", periods=1)
    df["tempDelRev"] = df["tempRev"] - df["l1_tempRev"]

    df["f1_tempCFO"] = _lead_with_gap(df, "tempCFO", periods=1)
    df["l1_tempCFO"] = _lag_with_gap(df, "tempCFO", periods=1)

    return df


def _run_cross_sectional_ols(df: pd.DataFrame) -> pd.DataFrame:
    """Run year-industry regressions and keep Stata-style residuals."""

    df = df.copy()
    df["tempResid"] = np.nan

    dependent = "tempCAcc"
    regressors: Iterable[str] = [
        "l1_tempCFO",
        "tempCFO",
        "f1_tempCFO",
        "tempDelRev",
        "tempPPE",
    ]

    grouped = df.groupby(["fyear", "FF48"])
    for (year, ind), group in grouped:
        if len(group) < 20:
            continue

        X = group[list(regressors)]
        y = group[dependent]

        valid_mask = y.notna()
        for col in regressors:
            valid_mask &= X[col].notna()

        if valid_mask.sum() == 0:
            continue

        X_valid = X.loc[valid_mask]
        y_valid = y.loc[valid_mask]

        try:
            model, keep_cols, *_ = regress(
                X_valid,
                y_valid,
                add_constant=True,
                omit_collinear=True,
                return_full_coefs=True,
            )
        except Exception:
            continue

        X_design = sm.add_constant(X_valid[keep_cols], has_constant="add")
        preds = model.predict(X_design)
        resid = y_valid - preds

        df.loc[resid.index, "tempResid"] = resid

    # Ensure groups with <20 total observations remain missing
    counts = df.groupby(["fyear", "FF48"])["tempResid"].transform("size")
    df.loc[counts < 20, "tempResid"] = np.nan

    return df


def _compute_accrual_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Generate AQ and lagged AccrualQuality following the .do file."""

    df = df.sort_values(["gvkey", "fyear"]).copy()

    for n in range(1, 5):
        df[f"tempResid{n}"] = _lag_with_gap(df, "tempResid", periods=n)

    resid_cols = ["tempResid"] + [f"tempResid{n}" for n in range(1, 5)]
    df["tempN"] = df[resid_cols].isna().sum(axis=1)

    values = df[resid_cols].to_numpy(dtype=float)
    df["AQ"] = np.apply_along_axis(_row_std, 1, values)
    df.loc[df["tempN"] > 1, "AQ"] = np.nan

    df["AccrualQuality"] = _lag_with_gap(df, "AQ", periods=1)

    return df


def _expand_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Replicate Stata's expand-12 monthly mapping and June carry-forward."""

    monthly_cols = ["permno", "time_avail_m", "datadate", "AccrualQuality"]
    monthly = df[monthly_cols].dropna(subset=["permno", "time_avail_m"]).copy()

    monthly["time_avail_m"] = pd.to_datetime(monthly["time_avail_m"])
    monthly["datadate"] = pd.to_datetime(monthly["datadate"])

    expanded = monthly.loc[monthly.index.repeat(12)].copy()
    expanded["month_offset"] = expanded.groupby(level=0).cumcount().astype(int)
    period_base = expanded["time_avail_m"].dt.to_period("M")
    expanded["time_avail_m"] = (
        (period_base + expanded["month_offset"]).dt.to_timestamp()
    )
    expanded = expanded.drop(columns="month_offset")

    expanded = expanded.sort_values(["permno", "time_avail_m", "datadate"])
    expanded = expanded.groupby(["permno", "time_avail_m"]).tail(1)
    expanded = expanded.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

    expanded["AccrualQualityJune"] = np.where(
        expanded["time_avail_m"].dt.month == 6,
        expanded["AccrualQuality"],
        np.nan,
    )
    expanded["AccrualQualityJune"] = expanded.groupby("permno")[
        "AccrualQualityJune"
    ].ffill()

    return expanded


def main() -> None:
    print("=" * 80)
    print("ZZ2_AccrualQuality_AccrualQualityJune.py")
    print("Replicating accrual quality placebos (Stata parity)")
    print("=" * 80)

    data = pd.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
    data = data[
        [
            "gvkey",
            "permno",
            "time_avail_m",
            "datadate",
            "fyear",
            "ib",
            "act",
            "che",
            "lct",
            "dlc",
            "dp",
            "at",
            "sale",
            "sic",
            "ppegt",
        ]
    ].copy()
    print(f"Loaded a_aCompustat: {len(data):,} rows")

    annual = _prepare_annual_data(data)

    sic_numeric = pd.to_numeric(annual["sic"], errors="coerce")
    annual = annual.assign(sic_numeric=sic_numeric)
    annual = annual.dropna(subset=["sic_numeric"]).copy()
    annual["sic_numeric"] = annual["sic_numeric"].astype(int)
    annual["FF48"] = sicff(annual["sic_numeric"])
    annual = annual.dropna(subset=["FF48"]).copy()
    annual["FF48"] = annual["FF48"].astype(int)

    annual = _run_cross_sectional_ols(annual)
    print("Cross-sectional regressions complete")

    annual = _compute_accrual_quality(annual)
    print("Computed annual AccrualQuality")

    monthly = _expand_to_monthly(annual)
    print(f"Monthly panel size before saving: {len(monthly):,} rows")

    save_placebo(monthly[["permno", "time_avail_m", "AccrualQuality"]], "AccrualQuality")
    save_placebo(
        monthly[["permno", "time_avail_m", "AccrualQualityJune"]],
        "AccrualQualityJune",
    )

    print("=" * 80)
    print("Accrual quality placebos generated and saved")
    print("=" * 80)


if __name__ == "__main__":
    main()
