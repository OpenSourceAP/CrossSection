# ABOUTME: Change in net financial assets following Richardson et al. 2005, Table 8B DeltaFin
# ABOUTME: Change in net financial assets (financial assets minus liabilities) from prior 12 months divided by average total assets

"""
DelNetFin.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DelNetFin.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, pstk, dltt, dlc, ivst, ivao]

Outputs:
    - DelNetFin.csv: CSV file with columns [permno, yyyymm, DelNetFin]
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
    columns=[
        "gvkey",
        "permno",
        "time_avail_m",
        "at",
        "pstk",
        "dltt",
        "dlc",
        "ivst",
        "ivao",
    ],
)

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")

# Sort data for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lags using time-based approach

# Handle missing pstk values
df["tempPSTK"] = df["pstk"].fillna(0)

# Calculate net financial assets (financial assets minus liabilities)
df["temp"] = (df["ivst"] + df["ivao"]) - (df["dltt"] + df["dlc"] + df["tempPSTK"])

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "at", [12])
df = df.rename(columns={'at_lag12': 'l12_at'})
df = stata_multi_lag(df, "permno", "time_avail_m", "temp", [12], fill_gaps=False)
df = df.rename(columns={'temp_lag12': 'l12_temp'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate average total assets
df["tempAvAT"] = 0.5 * (df["at"] + df["l12_at"])

# Calculate change in net financial assets scaled by average assets
df["DelNetFin"] = (df["temp"] - df["l12_temp"]) / df["tempAvAT"]

# Drop missing values
df = df.dropna(subset=["DelNetFin"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "DelNetFin"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/DelNetFin.csv", index=False)
print(f"DelNetFin: Saved {len(df):,} observations")
