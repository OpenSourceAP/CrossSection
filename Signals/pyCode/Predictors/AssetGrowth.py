# ABOUTME: AssetGrowth.py - calculates annual asset growth rate for each firm
# ABOUTME: Computes percentage change in total assets over a 12-month period

"""
AssetGrowth.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AssetGrowth.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at]

Outputs:
    - AssetGrowth.csv: CSV file with columns [permno, yyyymm, AssetGrowth]
    - AssetGrowth = (at - l12.at)/l12.at (12-month asset growth)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting AssetGrowth.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data containing total assets
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['gvkey', 'permno', 'time_avail_m', 'at']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Sort data by firm and time to enable panel calculations
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate asset growth as percentage change from 12 months ago
print("Calculating 12-month lag and AssetGrowth...")

# Create 12-month lag of total assets for growth calculation
df['l12_at'] = df.groupby('permno')['at'].shift(12)

# Calculate asset growth with proper handling of missing values and zero denominators
df['AssetGrowth'] = np.where(
    df['l12_at'] == 0,
    np.nan,  # Division by zero = missing
    np.where(
        df['at'].isna() & df['l12_at'].isna(),
        1.0,  # missing/missing = 1.0 (no change)
        (df['at'] - df['l12_at']) / df['l12_at']
    )
)

print(f"Calculated AssetGrowth for {df['AssetGrowth'].notna().sum()} observations")

# SAVE
# Save predictor to standardized CSV format
save_predictor(df, 'AssetGrowth')

print("AssetGrowth.py completed successfully")