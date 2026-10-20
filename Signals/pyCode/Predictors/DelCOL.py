# ABOUTME: Change in current operating liabilities following Richardson et al. 2005, Table 8C
# ABOUTME: Calculates year-over-year change in current operating liabilities scaled by average assets

"""
DelCOL.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DelCOL.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, lct, dlc]

Outputs:
    - DelCOL.csv: CSV file with columns [permno, yyyymm, DelCOL]
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag, fill_date_gaps


print("Starting DelCOL.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with required fields
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ["gvkey", "permno", "time_avail_m", "at", "lct", "dlc"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate observations by permno-time_avail_m
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {df.shape[0]} rows")

# Sort data for panel operations
print("Setting up panel data structure...")
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lag variables for year-over-year calculations
print("Creating lag variables...")
# Fill calendar gaps for lags, then restore the observed rows.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
lag_vars = ['at', 'lct', 'dlc']
for var in lag_vars:
    df = stata_multi_lag(df, "permno", "time_avail_m", var, [12], fill_gaps=False)
df = df.rename(columns={f"{var}_lag12": f"lag_{var}" for var in lag_vars})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate average assets over two periods for normalization
print("Creating tempAvAT...")
df["tempAvAT"] = 0.5 * (df["at"] + df["lag_at"])

# Calculate change in current operating liabilities (current liabilities minus debt in current liabilities)
print("Calculating DelCOL...")
df["DelCOL"] = (df["lct"] - df["dlc"]) - (df["lag_lct"] - df["lag_dlc"])

# Scale by average assets
df["DelCOL"] = df["DelCOL"] / df["tempAvAT"]

# Clean up temporary variables
df = df.drop(columns=["lag_at", "lag_lct", "lag_dlc", "tempAvAT"])

print(f"Calculated DelCOL for {df['DelCOL'].notna().sum()} observations")

# SAVE
# Save predictor using standardized format
save_predictor(df, "DelCOL")

print("DelCOL.py completed successfully")
