# ABOUTME: Change in equity to assets following Richardson et al. 2005, Table 9A
# ABOUTME: calculates change in common equity scaled by average total assets

"""
DelEqu.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DelEqu.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, ceq]

Outputs:
    - DelEqu.csv: CSV file with columns [permno, yyyymm, DelEqu]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "at", "ceq"],
)

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")

# Sort data for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Calculate 12-month look-back period for comparison
df["time_lag12"] = df["time_avail_m"] - pd.DateOffset(months=12)

# Prepare historical data for comparison with current values
lag_data = df[["permno", "time_avail_m", "at", "ceq"]].copy()
lag_data.columns = ["permno", "time_lag12", "l12_at", "l12_ceq"]

# Join current data with historical values from 12 months prior
df = df.merge(lag_data, on=["permno", "time_lag12"], how="left")

# Use average of current and prior period total assets as scaling denominator
df["tempAvAT"] = 0.5 * (df["at"] + df["l12_at"])

# Scale the change in common equity by average firm size
df["DelEqu"] = (df["ceq"] - df["l12_ceq"]) / df["tempAvAT"]

# Drop missing values
df = df.dropna(subset=["DelEqu"])

# Create monthly date identifier for output
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "DelEqu"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/DelEqu.csv", index=False)
print(f"DelEqu: Saved {len(df):,} observations")
