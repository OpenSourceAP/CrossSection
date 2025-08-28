# ABOUTME: ChNWC predictor - calculates change in net working capital
# ABOUTME: Run: python3 pyCode/Predictors/ChNWC.py

"""
ChNWC Predictor

Change in net working capital calculation.

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, act, che, lct, dlc, at)

Outputs:
- ChNWC.csv (permno, yyyymm, ChNWC)

This predictor calculates:
1. Net working capital ratio = ((act - che) - (lct - dlc))/at
2. Change in NWC = current ratio - 12-month lag ratio
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting ChNWC predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                    columns=['gvkey', 'permno', 'time_avail_m', 'act', 'che', 'lct', 'dlc', 'at'])

print(f"Loaded {len(df):,} Compustat observations")

# Deduplicate by permno time_avail_m (equivalent to bysort permno time_avail_m: keep if _n == 1)
df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing ChNWC signal...")

# Sort by permno and time_avail_m (equivalent to xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate net working capital ratio: temp = ((act - che) - (lct - dlc))/at
df['nwc_numerator'] = (df['act'] - df['che']) - (df['lct'] - df['dlc'])

# Calculate temp with domain-aware missing handling
df['temp'] = np.where(
    df['at'] == 0,
    np.nan,  # Division by zero = missing
    np.where(
        df['nwc_numerator'].isna() & df['at'].isna(),
        1.0,  # missing/missing = 1.0 (no change)
        df['nwc_numerator'] / df['at']
    )
)

# Create 12-month lag of temp
df['l12_temp'] = df.groupby('permno')['temp'].shift(12)

# Calculate change in NWC: ChNWC = temp - l12.temp
df['ChNWC'] = df['temp'] - df['l12_temp']

print(f"Generated ChNWC values for {df['ChNWC'].notna().sum():,} observations")

# Clean up temporary columns
df = df.drop(columns=['nwc_numerator', 'temp', 'l12_temp'])

# SAVE
print("Saving predictor...")
save_predictor(df, 'ChNWC')

print("ChNWC predictor completed successfully!")