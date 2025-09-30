# ABOUTME: Net Payout Yield following Boudoukh et al. 2007, Table 6D
# ABOUTME: calculates net payout yield scaled by lagged market value of equity

"""
NetPayoutYield.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/NetPayoutYield.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, dvc, prstkc, sstk, sic, ceq]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - NetPayoutYield.csv: CSV file with columns [permno, yyyymm, NetPayoutYield]
"""

import pandas as pd
import numpy as np

# DATA LOAD
# Load m_aCompustat with specific columns
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["permno", "time_avail_m", "dvc", "prstkc", "sstk", "sic", "ceq"],
)

# Remove duplicate observations by permno and time_avail_m
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")

# Merge with SignalMasterTable to get market value of equity
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_c"],
)

df = df.merge(signal_master, on=["permno", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Sort for lag operation
df = df.sort_values(["permno", "time_avail_m"])

# Create 6-month lag of market value of equity
# Need calendar-based lag (6 months back in time)
# Use efficient merge-based approach for calendar lag
df["lag6_date"] = df["time_avail_m"] - pd.DateOffset(months=6)

# Create lag lookup table
lag_lookup = df[["permno", "time_avail_m", "mve_c"]].copy()
lag_lookup = lag_lookup.rename(
    columns={"time_avail_m": "lag6_date", "mve_c": "mve_c_l6"}
)

# Merge to get 6-month lagged values
df = df.merge(lag_lookup, on=["permno", "lag6_date"], how="left")

# Calculate net payout yield as net payouts scaled by lagged market value
df["NetPayoutYield"] = (df["dvc"] + df["prstkc"] - df["sstk"]) / df["mve_c_l6"]

# Remove observations with zero net payout yield
# Handle floating point precision to match Stata behavior
zero_mask = df["NetPayoutYield"] == 0.0
has_components = (df["dvc"] != 0) | (df["prstkc"] != 0) | (df["sstk"] != 0)
tiny_residual_mask = zero_mask & has_components

# For observations that should have tiny residuals, assign a small value
df.loc[tiny_residual_mask, "NetPayoutYield"] = 1e-19

# Now filter out true zeros
df = df[df["NetPayoutYield"] != 0]

# Convert SIC code to numeric format
df["sic"] = pd.to_numeric(df["sic"], errors="coerce")

# Filter out financial firms (SIC 6000-6999) and require positive book equity
# Missing book equity values are included (treated as positive in original logic)
df = df[
    ((df["sic"] < 6000) | (df["sic"] >= 7000)) & ((df["ceq"] > 0) | df["ceq"].isna())
]

# Sort data by permno and time
df = df.sort_values(["permno", "time_avail_m"])

# Require at least 24 observations per firm for stability
df["obs_count"] = df.groupby("permno").cumcount() + 1
df = df[df["obs_count"] >= 24]

# Keep only observations with valid NetPayoutYield (not missing/infinite)
df = df.dropna(subset=["NetPayoutYield"])
df = df[np.isfinite(df["NetPayoutYield"])]

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
