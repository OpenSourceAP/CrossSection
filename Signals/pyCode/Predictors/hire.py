# ABOUTME: Employment growth following Bazdresch, Belo and Lin 2014, Table 1A
# ABOUTME: Change in number of employees scaled by average employment, set to 0 if emp data missing

"""
hire.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/hire.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, emp]

Outputs:
    - hire.csv: CSV file with columns [permno, yyyymm, hire]
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
    columns=["permno", "time_avail_m", "emp"],
)

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")

# Sort data for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lags using time-based approach

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "emp", [12])
df = df.rename(columns={'emp_lag12': 'l12_emp'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate hire rate
df["hire"] = (df["emp"] - df["l12_emp"]) / (0.5 * (df["emp"] + df["l12_emp"]))

# Replace with 0 if either emp or l12_emp is missing
df.loc[(df["emp"].isna()) | (df["l12_emp"].isna()), "hire"] = 0

# Set to missing if year < 1965
df.loc[df["time_avail_m"].dt.year < 1965, "hire"] = np.nan

# Drop missing values
df = df.dropna(subset=["hire"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "hire"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/hire.csv", index=False)
print(f"hire: Saved {len(df):,} observations")
