# ABOUTME: Change in Net Working Capital following Soliman 2008, Table 7 Model 2 DeltaWC
# ABOUTME: calculates twelve-month change in net working capital scaled by total assets

"""
ChNWC.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ChNWC.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, act, che, lct, dlc, at]

Outputs:
    - ../pyData/Predictors/ChNWC.csv: CSV file with columns [permno, yyyymm, ChNWC]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting ChNWC predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "act", "che", "lct", "dlc", "at"],
)

print(f"Loaded {len(df):,} Compustat observations")

# Remove duplicate observations for same company-month
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing ChNWC signal...")

# Sort by company and time to enable lag calculations
df = df.sort_values(["permno", "time_avail_m"])

# Calculate net working capital ratio as proportion of total assets
df["nwc_numerator"] = (df["act"] - df["che"]) - (df["lct"] - df["dlc"])

# Calculate temp with domain-aware missing handling
df["temp"] = np.where(
    df["at"] == 0,
    np.nan,  # Division by zero = missing
    np.where(
        df["nwc_numerator"].isna() & df["at"].isna(),
        1.0,  # missing/missing = 1.0 (no change)
        df["nwc_numerator"] / df["at"],
    ),
)

# Create 12-month lag of working capital ratio
df["l12_temp"] = df.groupby("permno")["temp"].shift(12)

# Calculate 12-month change in net working capital
df["ChNWC"] = df["temp"] - df["l12_temp"]

print(f"Generated ChNWC values for {df['ChNWC'].notna().sum():,} observations")

# Clean up temporary columns
df = df.drop(columns=["nwc_numerator", "temp", "l12_temp"])

# SAVE
print("Saving predictor...")
save_predictor(df, "ChNWC")

print("ChNWC predictor completed successfully!")
