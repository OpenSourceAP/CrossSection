# ABOUTME: Change in financial liabilities following Richardson et al. 2005, Table 8C
# ABOUTME: calculates change in financial liabilities scaled by average total assets

"""
DelFINL.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DelFINL.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, pstk, dltt, dlc]

Outputs:
    - DelFINL.csv: CSV file with columns [permno, yyyymm, DelFINL]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "at", "pstk", "dltt", "dlc"],
)

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")

# Sort data for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lags using time-based approach
df["time_lag12"] = df["time_avail_m"] - pd.DateOffset(months=12)

# Handle missing pstk values
df["tempPSTK"] = df["pstk"].fillna(0)

# Create lag data for merge
lag_data = df[["permno", "time_avail_m", "at", "dltt", "dlc", "tempPSTK"]].copy()
lag_data.columns = [
    "permno",
    "time_lag12",
    "l12_at",
    "l12_dltt",
    "l12_dlc",
    "l12_tempPSTK",
]

# Merge to get lagged values
df = df.merge(lag_data, on=["permno", "time_lag12"], how="left")

# Calculate average total assets
df["tempAvAT"] = 0.5 * (df["at"] + df["l12_at"])

# Calculate change in financial liabilities
df["DelFINL"] = (
    (df["dltt"] + df["dlc"] + df["tempPSTK"])
    - (df["l12_dltt"] + df["l12_dlc"] + df["l12_tempPSTK"])
) / df["tempAvAT"]

# Drop missing values
df = df.dropna(subset=["DelFINL"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "DelFINL"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/DelFINL.csv", index=False)
print(f"DelFINL: Saved {len(df):,} observations")
