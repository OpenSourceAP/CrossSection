# ABOUTME: Analyst earnings per share following Cen, Wei, and Zhang 2006, Table 2, Ret0:1
# ABOUTME: Calculates FEPS (Forecasted EPS) predictor using IBES analyst mean estimates (meanest)

"""
FEPS.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/FEPS.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES earnings per share data
    - SignalMasterTable.parquet: Monthly master table with permno, tickerIBES, time_avail_m

Outputs:
    - FEPS.csv: CSV file with columns [permno, yyyymm, FEPS]
    - FEPS = meanest (forecasted earnings per share)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("Starting FEPS.py...")

# Prep IBES data
print("Loading and preparing IBES data...")

# Load IBES data
ibes_path = Path("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
if not ibes_path.exists():
    raise FileNotFoundError(f"Required input file not found: {ibes_path}")

ibes_df = pd.read_parquet(ibes_path)

# Filter to primary forecasts only
ibes_df = ibes_df[ibes_df["fpi"] == "1"].copy()

# Select required columns: ticker identifier, time, and mean estimate
required_cols = ["tickerIBES", "time_avail_m", "meanest"]
missing_cols = [col for col in required_cols if col not in ibes_df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in IBES_EPS_Unadj: {missing_cols}")

ibes_df = ibes_df[required_cols].copy()
print(f"Prepared IBES data: {ibes_df.shape[0]} rows, {ibes_df.shape[1]} columns")

# DATA LOAD
print("Loading SignalMasterTable...")

# Load SignalMasterTable to get permno-tickerIBES mappings
signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)

# Keep only the columns we need
smt_required_cols = ["permno", "tickerIBES", "time_avail_m"]
smt_missing_cols = [
    col for col in smt_required_cols if col not in signal_master.columns
]
if smt_missing_cols:
    raise ValueError(
        f"Missing required columns in SignalMasterTable: {smt_missing_cols}"
    )

df = signal_master[smt_required_cols].copy()
print(f"Loaded SignalMasterTable: {df.shape[0]} rows, {df.shape[1]} columns")

# Merge with IBES data to add mean estimates
print("Merging with IBES data...")

# Left join to preserve all observations from master table
df = pd.merge(df, ibes_df, on=["tickerIBES", "time_avail_m"], how="left")

print(f"After merging with IBES data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Sort by permno and time for panel structure
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(["permno", "time_avail_m"])

# Create FEPS predictor from IBES mean estimates
print("Calculating FEPS...")
df["FEPS"] = df["meanest"]

print(f"Calculated FEPS for {df['FEPS'].notna().sum()} observations")

# SAVE
# Save FEPS predictor to standard format
save_predictor(df, "FEPS")

print("FEPS.py completed successfully")
