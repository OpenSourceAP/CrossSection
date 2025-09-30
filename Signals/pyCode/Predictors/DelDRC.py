# ABOUTME: Deferred Revenue following Prakash and Sinha 2013, Table 7
# ABOUTME: calculates annual change in deferred revenue scaled by average total assets

"""
DelDRC.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/DelDRC.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, drc, at, ceq, sale, sic]

Outputs:
    - DelDRC.csv: CSV file with columns [permno, yyyymm, DelDRC]
    - Change in deferred revenue normalized by average assets with filters applied
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("Starting DelDRC.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with required columns
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the required columns
required_cols = ["gvkey", "permno", "time_avail_m", "drc", "at", "ceq", "sale", "sic"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate observations for the same firm-month
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {df.shape[0]} rows")

# Sort data for panel operations
print("Setting up panel data structure...")
df = df.sort_values(["permno", "time_avail_m"])

# Ensure SIC code is numeric
print("Ensuring sic is numeric...")
df["sic"] = pd.to_numeric(df["sic"], errors="coerce")

# Create 12-month lag variables for deferred revenue and assets
print("Creating lag variables...")
df["lag_drc"] = df.groupby("permno")["drc"].shift(12)
df["lag_at"] = df.groupby("permno")["at"].shift(12)

# Calculate change in deferred revenue scaled by average total assets
print("Calculating DelDRC...")
df["DelDRC"] = (df["drc"] - df["lag_drc"]) / (0.5 * (df["at"] + df["lag_at"]))

# Apply exclusion filters: negative equity, zero deferred revenue with zero change, low sales, financial firms
print("Applying filters...")

# Create filter conditions
filter_condition = (
    (df["ceq"] <= 0)
    | ((df["drc"] == 0) & (df["DelDRC"] == 0))
    | (df["sale"] < 5)
    | ((df["sic"] >= 6000) & (df["sic"] < 7000))
)

# Apply the filter - set DelDRC to NaN where filter condition is true
df.loc[filter_condition, "DelDRC"] = np.nan

# Clean up temporary variables
df = df.drop(columns=["lag_drc", "lag_at"])

print(f"Calculated DelDRC for {df['DelDRC'].notna().sum()} observations")

# SAVE
# Save the predictor output
save_predictor(df, "DelDRC")

print("DelDRC.py completed successfully")
