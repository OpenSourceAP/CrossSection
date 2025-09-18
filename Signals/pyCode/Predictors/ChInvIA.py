# ABOUTME: Change in capital investment (industry adjusted) following Abarbanell and Bushee 1998, Table 2b RCAPX
# ABOUTME: Calculates growth in capital expenditure minus average growth in same industry (two-digit SIC)

"""
ChInvIA.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ChInvIA.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (columns: gvkey, permno, time_avail_m, capx, ppent, at)
    - ../pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, sicCRSP)

Outputs:
    - ../pyData/Predictors/ChInvIA.csv (columns: permno, yyyymm, ChInvIA)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOAD
# Load Compustat data with capital expenditures, PP&E, and total assets
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "capx", "ppent", "at"],
)

# Merge with signal master table to get industry classification (SIC codes)
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "sicCRSP"],
)
df = pd.merge(signal_master, df, on=["permno", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Sort by permno and time for lag operations
df = df.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

# Convert SIC codes to string for industry classification
df["sicCRSP"] = df["sicCRSP"].astype(str)

# Extract 2-digit SIC code for industry grouping
df["sic2D"] = df["sicCRSP"].str[:2]

# Fill missing capital expenditures using change in PP&E when capx is missing
# Use calendar-based lag (12 months back) instead of positional lag
df["ppent_l12_date"] = df["time_avail_m"] - pd.DateOffset(months=12)
ppent_lag = df[["permno", "time_avail_m", "ppent"]].rename(
    columns={"time_avail_m": "ppent_l12_date", "ppent": "ppent_l12"}
)
df = df.merge(ppent_lag, on=["permno", "ppent_l12_date"], how="left")
df = df.drop(columns=["ppent_l12_date"])

df["capx"] = df["capx"].fillna(df["ppent"] - df["ppent_l12"])

# Calculate percentage change in capx relative to average of 12 and 24 month lags
# Use calendar-based lags for capx
df["capx_l12_date"] = df["time_avail_m"] - pd.DateOffset(months=12)
capx_lag12 = df[["permno", "time_avail_m", "capx"]].rename(
    columns={"time_avail_m": "capx_l12_date", "capx": "capx_l12"}
)
df = df.merge(capx_lag12, on=["permno", "capx_l12_date"], how="left")
df = df.drop(columns=["capx_l12_date"])

df["capx_l24_date"] = df["time_avail_m"] - pd.DateOffset(months=24)
capx_lag24 = df[["permno", "time_avail_m", "capx"]].rename(
    columns={"time_avail_m": "capx_l24_date", "capx": "capx_l24"}
)
df = df.merge(capx_lag24, on=["permno", "capx_l24_date"], how="left")
df = df.drop(columns=["capx_l24_date"])
df["avg_lag_capx"] = 0.5 * (df["capx_l12"] + df["capx_l24"])

# Handle division by zero - in Stata, division by zero results in missing
df["pchcapx"] = np.where(
    df["avg_lag_capx"] == 0,
    np.nan,
    (df["capx"] - df["avg_lag_capx"]) / df["avg_lag_capx"],
)

# For missing values, use simple percentage change from 12 months ago
mask_missing = df["pchcapx"].isna()
df.loc[mask_missing, "pchcapx"] = np.where(
    df.loc[mask_missing, "capx_l12"] == 0,
    np.nan,
    (df.loc[mask_missing, "capx"] - df.loc[mask_missing, "capx_l12"])
    / df.loc[mask_missing, "capx_l12"],
)

# Calculate industry average percentage change in capx by 2-digit SIC and time
df["temp"] = df.groupby(["sic2D", "time_avail_m"])["pchcapx"].transform("mean")

# Industry-adjusted capital investment change (firm minus industry average)
df["ChInvIA"] = df["pchcapx"] - df["temp"]

# Remove temporary variable
df = df.drop(columns=["temp"])

# Keep only needed columns and non-missing values
result = df[["permno", "time_avail_m", "ChInvIA"]].copy()
result = result.dropna(subset=["ChInvIA"]).copy()

# Convert time_avail_m to yyyymm
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Prepare final output
final_result = result[["permno", "yyyymm", "ChInvIA"]].copy()

# SAVE
Path("../pyData/Predictors").mkdir(parents=True, exist_ok=True)
final_result.to_csv("../pyData/Predictors/ChInvIA.csv", index=False)

print(f"ChInvIA predictor saved: {len(final_result)} observations")
