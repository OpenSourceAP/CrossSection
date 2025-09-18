# ABOUTME: Composite debt issuance following Lyandres, Sun and Zhang 2008, Table 5B
# ABOUTME: calculates log of total debt minus log of total debt 5 years ago

"""
CompositeDebtIssuance.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/CompositeDebtIssuance.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, dltt, dlc]

Outputs:
    - CompositeDebtIssuance.csv: CSV file with columns [permno, yyyymm, CompositeDebtIssuance]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting CompositeDebtIssuance predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "dltt", "dlc"],
)

print(f"Loaded {len(df):,} Compustat observations")

# SIGNAL CONSTRUCTION
print("Constructing CompositeDebtIssuance signal...")

# Deduplicate by permno time_avail_m
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(df):,} observations")

# Sort by permno and time_avail_m
df = df.sort_values(["permno", "time_avail_m"])

# Calculate total debt
df["tempBD"] = df["dltt"] + df["dlc"]

# Create 60-month lag using calendar-based calculation
print("Calculating 60-month calendar-based lag...")

# Create target date column and merge with self for exact date matching
df["target_lag_date"] = df["time_avail_m"] - pd.DateOffset(months=60)

# Create lookup table for lag values
lag_lookup = df[["permno", "time_avail_m", "tempBD"]].copy()
lag_lookup.columns = ["permno", "lag_date", "l60_tempBD"]

# Merge to get exact matches first
df = df.merge(
    lag_lookup,
    left_on=["permno", "target_lag_date"],
    right_on=["permno", "lag_date"],
    how="left",
)

# For cases without exact matches, use position-based approximation
shift_lag = df.groupby("permno")["tempBD"].shift(60)
df["l60_tempBD"] = df["l60_tempBD"].fillna(shift_lag)

# Clean up temporary columns
df = df.drop(columns=["target_lag_date", "lag_date"])

# Calculate composite debt issuance as log growth in total debt over 60 months
df["CompositeDebtIssuance"] = np.log(df["tempBD"] / df["l60_tempBD"])

print(
    f"Generated CompositeDebtIssuance values for {df['CompositeDebtIssuance'].notna().sum():,} observations"
)

# Clean up temporary columns
df = df.drop(columns=["tempBD", "l60_tempBD"])

# SAVE
print("Saving predictor...")
save_predictor(df, "CompositeDebtIssuance")

print("CompositeDebtIssuance predictor completed successfully!")
