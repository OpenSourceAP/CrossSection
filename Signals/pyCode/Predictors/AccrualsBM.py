# ABOUTME: AccrualsBM predictor following Bartov and Kim 2004, Table 3, mean difference 1-2
# ABOUTME: Binary signal combining book-to-market and accruals to identify value vs growth with extreme accruals

"""
AccrualsBM.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AccrualsBM.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ceq, act, che, lct, dlc, txp, at]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - AccrualsBM.csv: CSV file with columns [permno, yyyymm, AccrualsBM]
    - Binary signal: 1 if high BM + low accruals, 0 if low BM + high accruals
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile

print("Starting AccrualsBM.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load m_aCompustat with required financial statement variables
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['gvkey', 'permno', 'time_avail_m', 'ceq', 'act', 'che', 'lct', 'dlc', 'txp', 'at']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# Remove duplicate observations by keeping first occurrence per permno-month
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {df.shape[0]} rows")

# Merge with SignalMasterTable to get market value of equity
print("Merging with SignalMasterTable...")

signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)
if 'mve_permco' not in signal_master.columns:
    raise ValueError("Missing required column 'mve_permco' in SignalMasterTable")

# Keep only required columns from SignalMasterTable
signal_master = signal_master[['permno', 'time_avail_m', 'mve_permco']].copy()

# Merge (equivalent to keep(using match) - right join to keep all SignalMasterTable obs)
df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='right')

print(f"After merging with SignalMasterTable: {df.shape[0]} rows")

# Sort data by firm and time for lag calculations
print("Setting up panel data structure...")
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION

# Calculate log book-to-market ratio
print("Calculating BM...")
df['BM'] = np.log(df['ceq'] / df['mve_permco'])

# Create lag variables for accruals calculation
print("Creating lag variables for accruals...")
df['lag_act'] = df.groupby('permno')['act'].shift(12)
df['lag_che'] = df.groupby('permno')['che'].shift(12)
df['lag_lct'] = df.groupby('permno')['lct'].shift(12)
df['lag_dlc'] = df.groupby('permno')['dlc'].shift(12)
df['lag_txp'] = df.groupby('permno')['txp'].shift(12)
df['lag_at'] = df.groupby('permno')['at'].shift(12)

# Calculate working capital accruals: change in working capital divided by average total assets
print("Calculating tempacc...")
df['tempacc'] = (
    (df['act'] - df['lag_act']) - (df['che'] - df['lag_che']) -
    ((df['lct'] - df['lag_lct']) - (df['dlc'] - df['lag_dlc']) - (df['txp'] - df['lag_txp']))
) / ((df['at'] + df['lag_at']) / 2)

# Rank firms into book-to-market quintiles within each month
print("Creating BM quintiles...")
df['tempqBM'] = fastxtile(df, 'BM', by='time_avail_m', n=5)

# Rank firms into accruals quintiles within each month
print("Creating accruals quintiles...")
df['tempqAcc'] = fastxtile(df, 'tempacc', by='time_avail_m', n=5)

# Create binary signal: 1 for high BM + low accruals, 0 for low BM + high accruals
print("Generating AccrualsBM signal...")
df['AccrualsBM'] = np.nan

# High book-to-market (quintile 5) and low accruals (quintile 1) = 1
df.loc[(df['tempqBM'] == 5) & (df['tempqAcc'] == 1), 'AccrualsBM'] = 1

# Low book-to-market (quintile 1) and high accruals (quintile 5) = 0
df.loc[(df['tempqBM'] == 1) & (df['tempqAcc'] == 5), 'AccrualsBM'] = 0

# Set missing if negative book equity
df.loc[df['ceq'] < 0, 'AccrualsBM'] = np.nan

# Remove temporary and lag variables
temp_cols = [col for col in df.columns if col.startswith('temp')]
lag_cols = [col for col in df.columns if col.startswith('lag_')]
drop_cols = temp_cols + lag_cols
df = df.drop(columns=drop_cols)

print(f"Calculated AccrualsBM for {df['AccrualsBM'].notna().sum()} observations")

# Save predictor to standardized format
save_predictor(df, 'AccrualsBM')

print("AccrualsBM.py completed successfully")


