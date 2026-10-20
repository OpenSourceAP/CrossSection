# ABOUTME: Payout Yield following Boudoukh et al. 2007, Table III B
# ABOUTME: calculates payout yield predictor scaled by market value of equity
"""
PayoutYield.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/PayoutYield.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, dvc, prstkc, pstkrv, sstk, sic, ceq, datadate]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - PayoutYield.csv: CSV file with columns [permno, yyyymm, PayoutYield]
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
    columns=[
        "permno",
        "time_avail_m",
        "dvc",
        "prstkc",
        "pstkrv",
        "sstk",
        "sic",
        "ceq",
        "datadate",
    ],
)

# Remove duplicate records within each permno-month combination
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")

# Merge market value data from SignalMasterTable
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_permco"],
)

df = df.merge(signal_master, on=["permno", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Fill calendar gaps once so the shared lag helper's shifts count months.
# Annual accounts are carried monthly, so preferred stock needs a 12-month lag.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
for column, months in [("mve_permco", 6), ("pstkrv", 12)]:
    df = stata_multi_lag(
        df, "permno", "time_avail_m", column, [months],
        prefix="l", fill_gaps=False,
    )

# Remove inserted calendar rows before eligibility filters and observation counts.
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Boudoukh et al. (2007), pp. 882-884: payout is dividends plus repurchases,
# including any annual reduction in preferred stock, not its outstanding level.
# If either preferred-stock value is unavailable, add no inferred reduction.
df["preferred_reduction"] = (df["l12_pstkrv"] - df["pstkrv"]).clip(lower=0).fillna(0)
df["PayoutYield"] = (
    df["dvc"] + df["prstkc"] + df["preferred_reduction"]
) / df["l6_mve_permco"]

# Set negative or zero payout yields to missing
df.loc[df["PayoutYield"] <= 0, "PayoutYield"] = np.nan

# FILTER
# Convert SIC codes to numeric format
df["sic"] = pd.to_numeric(df["sic"], errors="coerce")

# Filter out financial companies and require positive book equity
# Include missing book equity values (treated as valid)
df = df[
    ((df["sic"] < 6000) | (df["sic"] >= 7000)) & ((df["ceq"] > 0) | df["ceq"].isna())
]

# Sort data chronologically
df = df.sort_values(["permno", "time_avail_m"])

# Require at least 24 historical observations per company
df["obs_count"] = df.groupby("permno").cumcount() + 1
df = df[df["obs_count"] >= 24]

# Keep only observations with valid PayoutYield (not missing/infinite)
df = df.dropna(subset=["PayoutYield"])
df = df[np.isfinite(df["PayoutYield"])]

# Keep only required columns for final output
result = df[["permno", "time_avail_m", "PayoutYield"]].copy()

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Final format matching Stata output
result = result[["permno", "yyyymm", "PayoutYield"]]

# Convert permno and yyyymm to int
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

# SAVE
result.to_csv("../pyData/Predictors/PayoutYield.csv", index=False)

print(f"PayoutYield predictor created with {len(result)} observations")
