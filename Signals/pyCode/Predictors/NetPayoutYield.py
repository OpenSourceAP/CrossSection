# ABOUTME: Net Payout Yield following Boudoukh et al. 2007, Table VI B
# ABOUTME: calculates net payout yield scaled by lagged market value of equity

"""
NetPayoutYield.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/NetPayoutYield.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, dvc, prstkc, pstkrv, sstk, sic, ceq]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - NetPayoutYield.csv: CSV file with columns [permno, yyyymm, NetPayoutYield]
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import fill_date_gaps, stata_multi_lag

# DATA LOAD
# Load m_aCompustat with specific columns
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["permno", "time_avail_m", "dvc", "prstkc", "pstkrv", "sstk", "sic", "ceq"],
)

# Remove duplicate observations by permno and time_avail_m
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")

# Merge with SignalMasterTable to get market value of equity
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_permco"],
)

df = df.merge(signal_master, on=["permno", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Complete the calendar once; shifts must count months rather than observations.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
for column, months in [("mve_permco", 6), ("pstkrv", 12)]:
    df = stata_multi_lag(
        df, "permno", "time_avail_m", column, [months],
        prefix="l", fill_gaps=False,
    )
# Inserted months must not contribute to the existing age filter.
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Both preferred adjustments are positive magnitudes. Missing differences
# contribute zero; missing dividends, purchases, and sales remain missing.
df["preferred_reduction"] = (df["l12_pstkrv"] - df["pstkrv"]).clip(lower=0).fillna(0)
df["preferred_increase"] = (df["pstkrv"] - df["l12_pstkrv"]).clip(lower=0).fillna(0)
df["gross_payout"] = df["dvc"] + df["prstkc"] + df["preferred_reduction"]
df["equity_issuance"] = df["sstk"] - df["preferred_increase"]
df["NetPayoutYield"] = (df["gross_payout"] - df["equity_issuance"]) / df["l6_mve_permco"]

# Exclude exact zeros without inventing residuals or rounding small values.
df = df[df["NetPayoutYield"] != 0]

# Convert SIC code to numeric format
df["sic"] = pd.to_numeric(df["sic"], errors="coerce")

# Filter out financial firms (SIC 6000-6999) and require positive book equity
# Missing, zero, and negative book equity values are excluded.
df = df[
    ((df["sic"] < 6000) | (df["sic"] >= 7000)) & (df["ceq"] > 0)
]

# Sort data by permno and time
df = df.sort_values(["permno", "time_avail_m"])

# Require at least 24 observations per firm for stability
df["obs_count"] = df.groupby("permno").cumcount() + 1
df = df[df["obs_count"] >= 24]

# Keep only observations with valid NetPayoutYield (not missing/infinite)
df = df.dropna(subset=["NetPayoutYield"])
df = df[
    np.isfinite(df["NetPayoutYield"])
    & np.isfinite(df["l6_mve_permco"])
    & (df["l6_mve_permco"] > 0)
]

# Keep only required columns for final output
result = df[["permno", "time_avail_m", "NetPayoutYield"]].copy()

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Final format matching Stata output
result = result[["permno", "yyyymm", "NetPayoutYield"]]

# Convert permno and yyyymm to int
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

# SAVE
result.to_csv("../pyData/Predictors/NetPayoutYield.csv", index=False)

print(f"NetPayoutYield predictor created with {len(result)} observations")
