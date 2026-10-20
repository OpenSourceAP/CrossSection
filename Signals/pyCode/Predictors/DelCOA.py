# ABOUTME: Change in current operating assets following Richardson et al. 2005, Table 8C
# ABOUTME: calculates DelCOA predictor, difference in current operating assets scaled by average total assets

"""
DelCOA.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DelCOA.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, act, che]

Outputs:
    - DelCOA.csv: CSV file with columns [permno, yyyymm, DelCOA]
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


print("Starting DelCOA.py...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "at", "act", "che"],
)
print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate observations by permno and time_avail_m
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {df.shape[0]} rows")

# Sort data for panel lag operations
print("Setting up panel data structure...")
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lagged variables for year-over-year changes
print("Creating lag variables...")
# Fill calendar gaps for lags, then restore the observed rows.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
lag_vars = ['at', 'act', 'che']
for var in lag_vars:
    df = stata_multi_lag(df, "permno", "time_avail_m", var, [12], fill_gaps=False)
df = df.rename(columns={f"{var}_lag12": f"lag_{var}" for var in lag_vars})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate average assets over current and lagged periods
print("Creating tempAvAT...")
df["tempAvAT"] = 0.5 * (df["at"] + df["lag_at"])

# Calculate change in current operating assets (current assets minus cash)
print("Calculating DelCOA...")
df["DelCOA"] = (df["act"] - df["che"]) - (df["lag_act"] - df["lag_che"])

# Scale by average assets
df["DelCOA"] = df["DelCOA"] / df["tempAvAT"]

# Clean up temporary variables
df = df.drop(columns=["lag_at", "lag_act", "lag_che", "tempAvAT"])

print(f"Calculated DelCOA for {df['DelCOA'].notna().sum()} observations")

# SAVE
# Save the standardized predictor output
save_predictor(df, "DelCOA")

print("DelCOA.py completed successfully")
