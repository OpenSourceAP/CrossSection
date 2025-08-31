# ABOUTME: Change in current operating liabilities following Richardson et al. 2005, Table 8C
# ABOUTME: Calculates year-over-year change in current operating liabilities scaled by average assets

"""
DelCOL.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/DelCOL.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, lct, dlc]

Outputs:
    - DelCOL.csv: CSV file with columns [permno, yyyymm, DelCOL]
    - Change in current operating liabilities normalized by average assets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting DelCOL.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with required fields
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['gvkey', 'permno', 'time_avail_m', 'at', 'lct', 'dlc']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate observations by permno-time_avail_m
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {df.shape[0]} rows")

# Sort data for panel operations
print("Setting up panel data structure...")
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month lag variables for year-over-year calculations
print("Creating lag variables...")
df['lag_at'] = df.groupby('permno')['at'].shift(12)
df['lag_lct'] = df.groupby('permno')['lct'].shift(12)
df['lag_dlc'] = df.groupby('permno')['dlc'].shift(12)

# Calculate average assets over two periods for normalization
print("Creating tempAvAT...")
df['tempAvAT'] = 0.5 * (df['at'] + df['lag_at'])

# Calculate change in current operating liabilities (current liabilities minus debt in current liabilities)
print("Calculating DelCOL...")
df['DelCOL'] = (df['lct'] - df['dlc']) - (df['lag_lct'] - df['lag_dlc'])

# Scale by average assets
df['DelCOL'] = df['DelCOL'] / df['tempAvAT']

# Clean up temporary variables
df = df.drop(columns=['lag_at', 'lag_lct', 'lag_dlc', 'tempAvAT'])

print(f"Calculated DelCOL for {df['DelCOL'].notna().sum()} observations")

# SAVE
# Save predictor using standardized format
save_predictor(df, 'DelCOL')

print("DelCOL.py completed successfully")