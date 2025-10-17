# ABOUTME: Advertising Expense following Chan, Lakonishok and Sougiannis 2001, Table 7, first year
# ABOUTME: calculates advertising expense predictor scaled by market value of equity

"""
AdExp.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/AdExp.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, xad]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - AdExp.csv: CSV file with columns [permno, yyyymm, AdExp]
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("Starting AdExp.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load advertising expense data from monthly Compustat
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ["permno", "time_avail_m", "xad"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# Merge with SignalMasterTable to get market value of equity
print("Merging with SignalMasterTable...")

signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
if "mve_permco" not in signal_master.columns:
    raise ValueError("Missing required column 'mve_permco' in SignalMasterTable")

# Keep only required columns from SignalMasterTable
signal_master = signal_master[["permno", "time_avail_m", "mve_permco"]].copy()

# Use right join to keep only observations present in SignalMasterTable
df = pd.merge(df, signal_master, on=["permno", "time_avail_m"], how="right")

print(f"After merging with SignalMasterTable: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Calculate advertising expense scaled by market value of equity
print("Calculating AdExp...")
df["AdExp"] = df["xad"] / df["mve_permco"]

# Set to missing for non-positive advertising expense values
df.loc[df["xad"] <= 0, "AdExp"] = np.nan

print(f"Calculated AdExp for {df['AdExp'].notna().sum()} observations")

# SAVE
# Save the AdExp predictor to CSV file
save_predictor(df, "AdExp")

print("AdExp.py completed successfully")
