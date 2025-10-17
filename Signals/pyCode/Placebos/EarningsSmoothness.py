# ABOUTME: Earnings smoothness placebo translated from Stata implementation
# ABOUTME: Computes 10-year earnings and cash-flow volatility ratio using annual Compustat data

"""
EarningsSmoothness.py

Inputs:
    - a_aCompustat.parquet: columns [gvkey, permno, time_avail_m, fyear, datadate, ib, at, act, lct, che, dlc, dp]

Outputs:
    - EarningsSmoothness.csv stored under ../pyData/Placebos/

How to run:
    cd Signals/pyCode
    python3 Placebos/EarningsSmoothness.py
    Example: python3 Placebos/EarningsSmoothness.py
"""

import os
import sys
import numpy as np
import pandas as pd

# Allow relative imports from utils
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.asrol import asrol
from utils.saveplacebo import save_placebo


def main() -> None:
    print("Starting EarningsSmoothness placebo...")

    # DATA LOAD
    compustat_cols = [
        "gvkey",
        "permno",
        "time_avail_m",
        "fyear",
        "datadate",
        "ib",
        "at",
        "act",
        "lct",
        "che",
        "dlc",
        "dp",
    ]

    print("Loading annual Compustat data...")
    df = pd.read_parquet(
        "../pyData/Intermediate/a_aCompustat.parquet",
        columns=compustat_cols,
    )
    print(f"Loaded {len(df):,} annual observations across {df['gvkey'].nunique():,} firms")

    # Ensure sorting equivalent to xtset gvkey fyear
    df = df.sort_values(["gvkey", "fyear", "datadate"])

    # SIGNAL CONSTRUCTION
    print("Computing lagged balance-sheet items...")
    lag_vars = ["at", "act", "lct", "che", "dlc"]
    grouped = df.groupby("gvkey", sort=False)
    for var in lag_vars:
        df[f"lag_{var}"] = grouped[var].shift(1)

    # Avoid zero or missing lagged assets causing divide-by-zero issues
    valid_assets = df["lag_at"]
    df.loc[(valid_assets.isna()) | (valid_assets == 0), "lag_at"] = np.nan

    print("Calculating earnings and cash-flow scaled by lagged assets...")
    df["tempEarnings"] = df["ib"] / df["lag_at"]

    accrual_component = (
        (df["act"] - df["lag_act"])  # change in current assets
        - (df["lct"] - df["lag_lct"])  # minus change in current liabilities
        - (df["che"] - df["lag_che"])  # minus change in cash and equivalents
        + (df["dlc"] - df["lag_dlc"])  # plus change in debt in current liabilities
        - df["dp"]  # minus depreciation and amortization
    )
    df["tempCF"] = (df["ib"] - accrual_component) / df["lag_at"]

    # Prepare annual date column for asrol (end of fiscal year)
    df["fyear_int"] = pd.to_numeric(df["fyear"], errors="coerce").astype("Int64")
    df["fyear_date"] = pd.to_datetime(
        df["fyear_int"].astype(str) + "-12-31", errors="coerce"
    )

    # Rolling standard deviations using asrol (10-year window, minimum 10 observations)
    print("Applying 10-year rolling standard deviations via asrol...")
    df = asrol(
        df,
        group_col="gvkey",
        time_col="fyear_date",
        freq="1y",
        window=10,
        value_col="tempEarnings",
        stat="std",
        new_col_name="sd10_tempEarnings",
        min_samples=10,
        fill_gaps=False,
    )
    df = asrol(
        df,
        group_col="gvkey",
        time_col="fyear_date",
        freq="1y",
        window=10,
        value_col="tempCF",
        stat="std",
        new_col_name="sd10_tempCF",
        min_samples=10,
        fill_gaps=False,
    )

    print("Forming earnings smoothness ratio...")
    df["EarningsSmoothness"] = df["sd10_tempEarnings"] / df["sd10_tempCF"]
    df.loc[df["sd10_tempCF"].isna() | (df["sd10_tempCF"] == 0), "EarningsSmoothness"] = np.nan

    # Keep relevant annual observations before monthly expansion
    annual_cols = [
        "gvkey",
        "permno",
        "time_avail_m",
        "datadate",
        "EarningsSmoothness",
    ]
    annual_df = df[annual_cols].dropna(subset=["time_avail_m", "permno"])
    annual_df = annual_df.dropna(subset=["EarningsSmoothness"])

    print("Expanding annual values to monthly availability dates...")
    expanded_frames = []
    for month_offset in range(12):
        month_df = annual_df.copy()
        month_df["time_avail_m"] = month_df["time_avail_m"] + pd.DateOffset(
            months=month_offset
        )
        expanded_frames.append(month_df)

    expanded_df = pd.concat(expanded_frames, ignore_index=True)

    # Mirror Stata deduplication logic
    expanded_df = expanded_df.sort_values(["gvkey", "time_avail_m", "datadate"])
    expanded_df = (
        expanded_df.groupby(["gvkey", "time_avail_m"], as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )
    expanded_df = (
        expanded_df.sort_values(["permno", "time_avail_m", "datadate"])
        .drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
        .reset_index(drop=True)
    )

    final_df = expanded_df[["permno", "time_avail_m", "EarningsSmoothness"]]

    print("Saving placebo output...")
    save_placebo(final_df, "EarningsSmoothness")

    print("EarningsSmoothness placebo completed successfully")


if __name__ == "__main__":
    main()
