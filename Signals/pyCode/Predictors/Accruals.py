# ABOUTME: Accruals following Sloan 1996, Table 6, year t+1
# ABOUTME: calculates working capital accruals predictor scaled by average total assets

"""
Accruals.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/Accruals.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, txp, act, che, lct, dlc, at, dp]

Outputs:
    - Accruals.csv: CSV file with columns [permno, yyyymm, Accruals]
    - Implements Sloan 1996 equation 1 (page 6)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting Accruals.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with required balance sheet variables
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only required balance sheet variables
required_cols = ['gvkey', 'permno', 'time_avail_m', 'txp', 'act', 'che', 'lct', 'dlc', 'at', 'dp']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate observations per firm-month
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {df.shape[0]} rows")

# Sort by firm and time for lag operations
print("Setting up panel data structure...")
df = df.sort_values(['permno', 'time_avail_m'])

# Fill missing tax payable values with zero
df['tempTXP'] = df['txp'].fillna(0)

# Create 12-month lagged variables for each balance sheet item
print("Creating lag variables...")
df['lag_act'] = df.groupby('permno')['act'].shift(12)
df['lag_che'] = df.groupby('permno')['che'].shift(12)
df['lag_lct'] = df.groupby('permno')['lct'].shift(12)
df['lag_dlc'] = df.groupby('permno')['dlc'].shift(12)
df['lag_tempTXP'] = df.groupby('permno')['tempTXP'].shift(12)
df['lag_at'] = df.groupby('permno')['at'].shift(12)

# Calculate working capital accruals using Sloan 1996 formula:
# (Change in current assets - change in cash) minus (change in current liabilities
# - change in short-term debt - change in taxes payable) minus depreciation,
# all scaled by average total assets
print("Calculating Accruals...")

df['Accruals'] = (
    (df['act'] - df['lag_act']) - (df['che'] - df['lag_che']) -
    ((df['lct'] - df['lag_lct']) - (df['dlc'] - df['lag_dlc']) - (df['tempTXP'] - df['lag_tempTXP'])) -
    df['dp']
) / ((df['at'] + df['lag_at']) / 2)

# Remove temporary variables
df = df.drop(columns=['tempTXP', 'lag_act', 'lag_che', 'lag_lct', 'lag_dlc', 'lag_tempTXP', 'lag_at'])

print(f"Calculated Accruals for {df['Accruals'].notna().sum()} observations")

# Save predictor to CSV file
save_predictor(df, 'Accruals')

print("Accruals.py completed successfully")