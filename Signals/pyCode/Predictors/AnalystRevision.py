# ABOUTME: AnalystRevision.py - computes EPS forecast revision (Hawkins, Chamberlin, Daniel 1984 FAJ Table 10)
# ABOUTME: Calculates ratio of current month EPS forecast to previous month's forecast using IBES data

"""
AnalystRevision.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AnalystRevision.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES earnings per share data 
    - SignalMasterTable.parquet: Monthly master table with permno, tickerIBES, time_avail_m

Outputs:
    - AnalystRevision.csv: CSV file with columns [permno, yyyymm, AnalystRevision]
    - AnalystRevision = ratio of current to previous month's mean earnings estimate
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting AnalystRevision.py...")

# Prep IBES data
print("Loading and preparing IBES data...")

# Load IBES earnings per share data
ibes_path = Path("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
if not ibes_path.exists():
    raise FileNotFoundError(f"Required input file not found: {ibes_path}")

ibes_df = pd.read_parquet(ibes_path)

# Keep only 1-year ahead forecasts
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# Select required columns for analysis
required_cols = ['tickerIBES', 'time_avail_m', 'meanest']
missing_cols = [col for col in required_cols if col not in ibes_df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in IBES_EPS_Unadj: {missing_cols}")

ibes_df = ibes_df[required_cols].copy()
print(f"Prepared IBES data: {ibes_df.shape[0]} rows, {ibes_df.shape[1]} columns")

# DATA LOAD
print("Loading SignalMasterTable...")

# Load master table with security identifiers and timing
signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)

# Keep only the columns we need
smt_required_cols = ['permno', 'tickerIBES', 'time_avail_m']
smt_missing_cols = [col for col in smt_required_cols if col not in signal_master.columns]
if smt_missing_cols:
    raise ValueError(f"Missing required columns in SignalMasterTable: {smt_missing_cols}")

df = signal_master[smt_required_cols].copy()
print(f"Loaded SignalMasterTable: {df.shape[0]} rows, {df.shape[1]} columns")

# Merge IBES data with master table
print("Merging with IBES data...")

# Left join preserves all master table observations
df = pd.merge(df, ibes_df, on=['tickerIBES', 'time_avail_m'], how='left')

print(f"After merging with IBES data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Sort data by security and time for panel calculations
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate analyst revision as ratio of current to lagged forecast
print("Calculating 1-month lag and AnalystRevision...")

# Create 1-month lag of mean earnings estimate
df['l_meanest'] = df.groupby('permno')['meanest'].shift(1)

# Compute forecast revision ratio
df['AnalystRevision'] = df['meanest'] / df['l_meanest']

print(f"Calculated AnalystRevision for {df['AnalystRevision'].notna().sum()} observations")

# SAVE
# Save predictor to standardized output format
save_predictor(df, 'AnalystRevision')

print("AnalystRevision.py completed successfully")