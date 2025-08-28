# ABOUTME: Translates DivInit.do to create dividend initiation predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/DivInit.py

# Our signal balances users desire to have flexible data and 
# fidelity to OP's original test.

# Run from pyCode/ directory
# Inputs: CRSPdistributions.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/DivInit.csv

import pandas as pd
import numpy as np
import sys
import os
import sys

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.asrol import asrol_calendar_pd
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  DivInit.py")
print("Creating dividend initiation predictor")
print("=" * 80)

# PREP DISTRIBUTIONS DATA
print("📊 Loading distributions data...")
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
print(f"Loaded distributions: {len(dist_df):,} observations")

# Cash dividends only (cd2 == 2 | cd2 == 3)
dist_df = dist_df[(dist_df['cd2'] == 2) | (dist_df['cd2'] == 3)]

# Collapse by exdt: this date tends to come first
dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])

# Sum dividends by permno and time_avail_m
tempdivamt = dist_df.groupby(['permno', 'time_avail_m'])['divamt'].sum().reset_index()

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'exchcd', 'shrcd']].copy()

# Merge with dividend amounts
df = df.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
print("🧮 Computing dividend initiation signal...")
# Replace missing dividend amounts with 0
df['divamt'] = df['divamt'].fillna(0)

# Rolling 24-month sum of dividends using asrol_calendar_pd
df = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'divamt', stat='sum', window='24mo', min_obs=1)

# Sort by permno and time_avail_m for lag calculation
df = df.sort_values(['permno', 'time_avail_m'])

# Create dividend initiation indicator
#gen temp = divamt > 0 & l1.divsum == 0 & (exchcd == 1 | exchcd == 2) // OP does nyse/amex only, but we are more flexible
#gen temp = divamt > 0 & l1.divsum == 0
df['divsum_lag1'] = df.groupby('permno')['divamt_sum'].shift(1)
df['temp'] = (df['divamt'] > 0) & (df['divsum_lag1'] == 0)
df['temp'] = df['temp'].fillna(False).astype(int)  # Convert boolean to numeric

# Keep for 6 months using asrol_calendar_pd
df = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'temp', stat='sum', window='6mo', min_obs=1)

# Create final DivInit signal (initsum == 1)
df['DivInit'] = (df['temp_sum'] == 1).astype(int)

# save
print("💾 Saving DivInit predictor...")
save_predictor(df, 'DivInit')
print("✅ DivInit.csv saved successfully")

print("=" * 80)
print("✅ DivInit.py Complete")
print("Dividend initiation predictor generated successfully")
print("=" * 80)