# ABOUTME: Cash flow to market following Lakonishok, Shleifer, Vishny 1994, Table 6 panel 1
# ABOUTME: calculates cash flow to market value ratio (net income + depreciation) / market equity

"""
CF.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/CF.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ib, dp]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - CF.csv: CSV file with columns [permno, yyyymm, CF]
    - CF = (ib + dp)/mve_permco (Cash flow to market value ratio)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting CF.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with income and depreciation information
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['gvkey', 'permno', 'time_avail_m', 'ib', 'dp']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# Remove duplicate permno-month observations, keeping first occurrence
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {df.shape[0]} rows")

# Merge with SignalMasterTable to get market value data, keeping only matched observations
print("Merging with SignalMasterTable...")

signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)
if 'mve_permco' not in signal_master.columns:
    raise ValueError("Missing required column 'mve_permco' in SignalMasterTable")

# Keep only required columns from SignalMasterTable
signal_master = signal_master[['permno', 'time_avail_m', 'mve_permco']].copy()

# Merge (equivalent to keep(using match) - right join)
df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='right')

print(f"After merging with SignalMasterTable: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Generate (ib + dp)/mve_permco
print("Calculating CF...")

# Calculate cash flow (ib + dp)
df['cash_flow'] = df['ib'] + df['dp']

# Calculate CF with domain-aware missing value handling
# Following missing/missing = 1.0 pattern for division operations
df['CF'] = np.where(
    df['mve_permco'] == 0,
    np.nan,  # Division by zero = missing
    np.where(
        df['cash_flow'].isna() & df['mve_permco'].isna(),
        1.0,  # missing/missing = 1.0 (no change)
        df['cash_flow'] / df['mve_permco']
    )
)

print(f"Calculated CF for {df['CF'].notna().sum()} observations")

# SAVE
# Save the CF predictor using standardized format
save_predictor(df, 'CF')

print("CF.py completed successfully")