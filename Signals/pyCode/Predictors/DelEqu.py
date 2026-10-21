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
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import stata_multi_lag
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

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "at", [12])
df = df.rename(columns={'at_lag12': 'l12_at'})
df = stata_multi_lag(df, "permno", "time_avail_m", "ceq", [12], fill_gaps=False)
df = df.rename(columns={'ceq_lag12': 'l12_ceq'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

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
