# ABOUTME: DelCOA.py - calculates DelCOA predictor (Change in current operating assets)
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/DelCOA.do

"""
DelCOA.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/DelCOA.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, act, che]

Outputs:
    - DelCOA.csv: CSV file with columns [permno, yyyymm, DelCOA]
    - Change in current operating assets normalized by average assets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting DelCOA.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load m_aCompustat with required fields for current operating assets calculation
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)
##Print query of df == 23033 (bad permno), tell claude to add similiar feedback for debugging
# Keep only the columns we need for the calculation
required_cols = ['gvkey', 'permno', 'time_avail_m', 'at', 'act', 'che']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate observations by permno and time_avail_m
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {df.shape[0]} rows")

# Sort data for panel lag operations
print("Setting up panel data structure...")
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month lagged variables for year-over-year changes
print("Creating lag variables...")
df['lag_at'] = df.groupby('permno')['at'].shift(12)
df['lag_act'] = df.groupby('permno')['act'].shift(12)
df['lag_che'] = df.groupby('permno')['che'].shift(12)

# Calculate average assets over current and lagged periods
print("Creating tempAvAT...")
df['tempAvAT'] = 0.5 * (df['at'] + df['lag_at'])

# Calculate change in current operating assets (current assets minus cash)
print("Calculating DelCOA...")
df['DelCOA'] = (df['act'] - df['che']) - (df['lag_act'] - df['lag_che'])

# Scale by average assets
df['DelCOA'] = df['DelCOA'] / df['tempAvAT']

# Clean up temporary variables
df = df.drop(columns=['lag_at', 'lag_act', 'lag_che', 'tempAvAT'])

print(f"Calculated DelCOA for {df['DelCOA'].notna().sum()} observations")

# SAVE
# Save the standardized predictor output
save_predictor(df, 'DelCOA')

print("DelCOA.py completed successfully")