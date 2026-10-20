# ABOUTME: Change in long-term investment following Richardson et al. 2005, Table 8C
# ABOUTME: calculates difference in investment and advances (ivao) scaled by average total assets

"""
DelLTI.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DelLTI.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, ivao]

Outputs:
    - DelLTI.csv: CSV file with columns [permno, yyyymm, DelLTI]
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
    columns=["gvkey", "permno", "time_avail_m", "at", "ivao"],
)

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")

# Sort data for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lags using time-based approach

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "at", [12])
df = df.rename(columns={'at_lag12': 'l12_at'})
df = stata_multi_lag(df, "permno", "time_avail_m", "ivao", [12], fill_gaps=False)
df = df.rename(columns={'ivao_lag12': 'l12_ivao'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

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
