# ABOUTME: Change in long-term investment following Richardson et al. 2005, Table 8C
# ABOUTME: calculates difference in investment and advances (ivao) scaled by average total assets

"""
DelLTI predictor calculation

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/DelLTI.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (gvkey, permno, time_avail_m, at, ivao)

Outputs:
    - ../pyData/Predictors/DelLTI.csv (permno, yyyymm, DelLTI)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "at", "ivao"],
)

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")

# Sort data for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lags using time-based approach
df["time_lag12"] = df["time_avail_m"] - pd.DateOffset(months=12)

# Create lag data for merge
lag_data = df[["permno", "time_avail_m", "at", "ivao"]].copy()
lag_data.columns = ["permno", "time_lag12", "l12_at", "l12_ivao"]

# Merge to get lagged values
df = df.merge(lag_data, on=["permno", "time_lag12"], how="left")

# Calculate average total assets
df["tempAvAT"] = 0.5 * (df["at"] + df["l12_at"])

# Calculate change in long-term investments scaled by average assets
df["DelLTI"] = (df["ivao"] - df["l12_ivao"]) / df["tempAvAT"]

# Drop missing values
df = df.dropna(subset=["DelLTI"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "DelLTI"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/DelLTI.csv", index=False)
print(f"DelLTI: Saved {len(df):,} observations")
