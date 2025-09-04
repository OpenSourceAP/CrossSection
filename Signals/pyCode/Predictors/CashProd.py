# ABOUTME: Cash Productivity following Chandrashekar and Rao 2009, Table 4A
# ABOUTME: calculates cash productivity ratio as (market value of equity - total assets) / cash

"""
CashProd.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/CashProd.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, at, che]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - CashProd.csv: CSV file with columns [permno, yyyymm, CashProd]
    - CashProd = (mve_permco - at)/che (Cash productivity ratio)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting CashProd.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with total assets and cash & equivalents
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['permno', 'time_avail_m', 'at', 'che']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# Remove duplicate observations for the same firm-month combination
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {df.shape[0]} rows")

# Merge with SignalMasterTable to get market value of equity data
print("Merging with SignalMasterTable...")

signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)
if 'mve_permco' not in signal_master.columns:
    raise ValueError("Missing required column 'mve_permco' in SignalMasterTable")

# Keep only required columns from SignalMasterTable
signal_master = signal_master[['permno', 'time_avail_m', 'mve_permco']].copy()

# Merge (equivalent to keep(match) - inner join)
df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='inner')

print(f"After merging with SignalMasterTable: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Generate (mve_permco - at)/che
print("Calculating CashProd...")
df['CashProd'] = (df['mve_permco'] - df['at']) / df['che']

print(f"Calculated CashProd for {df['CashProd'].notna().sum()} observations")

# SAVE
# Save the CashProd predictor to standardized CSV format
save_predictor(df, 'CashProd')

print("CashProd.py completed successfully")