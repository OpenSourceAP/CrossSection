# ABOUTME: Bid-ask spread following Amihud and Mendelson 1986 JFE, Table 2 Spread Mean
# ABOUTME: Effective bid ask spread based on Corwin-Schulz scaled by stock price

"""
BidAskSpread.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/BidAskSpread.py

Inputs:
    - corwin_schultz_spread.csv: Pre-computed bid-ask spreads from Corwin-Schultz methodology

Outputs:
    - BidAskSpread.csv: CSV file with columns [permno, yyyymm, BidAskSpread]
    - BidAskSpread data is pre-computed using SAS code (Corwin_Schultz_Edit.sas)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from config import MAX_ROWS_DL

print("Starting BidAskSpread.py...")

# DATA LOAD
print("Loading corwin_schultz_spread data...")

# Load preprocessed Corwin-Schultz spread data from CSV
input_file = "../pyData/Prep/corwin_schultz_spread.csv"

if not os.path.exists(input_file):
    raise FileNotFoundError(f"Input file not found: {input_file}")

df = pd.read_csv(input_file)
print(f"Loaded {len(df)} records from {input_file}")

# DATA TRANSFORMATION
# Convert month string (YYYYMM format) to time_avail_m period
df['month'] = df['month'].astype(str)
df['y'] = df['month'].str[:4].astype(int)
df['m'] = df['month'].str[4:6].astype(int)
df['time_avail_m'] = pd.PeriodIndex.from_fields(
    year=df['y'], month=df['m'], freq='M'
)
df = df.drop(['y', 'm', 'month'], axis=1)

# Clean and standardize data
df = df.dropna(subset=['PERMNO'])
print(f"After dropping missing PERMNO: {len(df)} records")

df = df.rename(columns={
    'PERMNO': 'permno',
    'hlspread': 'BidAskSpread'
})
df['permno'] = df['permno'].astype('int64')

# Convert period to timestamp for parquet compatibility
df['time_avail_m'] = df['time_avail_m'].dt.to_timestamp()

# Apply debugging row limit if configured
if MAX_ROWS_DL > 0:
    df = df.head(MAX_ROWS_DL)
    print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

print(f"Processed data: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# * Construction is done in SAS code (Corwin_Schultz_Edit.sas)
# The BidAskSpread variable should already exist in the data

if 'BidAskSpread' not in df.columns:
    raise ValueError("BidAskSpread column not found in input data")

print(f"BidAskSpread available for {df['BidAskSpread'].notna().sum()} observations")

# SAVE
# Save BidAskSpread predictor to standardized format
save_predictor(df, 'BidAskSpread')

print("BidAskSpread.py completed successfully")