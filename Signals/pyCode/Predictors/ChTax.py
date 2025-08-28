# ABOUTME: ChTax predictor - calculates change in taxes
# ABOUTME: Run: python3 pyCode/Predictors/ChTax.py

"""
ChTax Predictor

Change in taxes calculation: (txtq - l12.txtq)/l12.at

Inputs:
- m_aCompustat.parquet (permno, gvkey, time_avail_m, at)
- m_QCompustat.parquet (gvkey, time_avail_m, txtq)

Outputs:
- ChTax.csv (permno, yyyymm, ChTax)

This predictor calculates the change in quarterly taxes scaled by lagged assets.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting ChTax predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                                columns=['permno', 'gvkey', 'time_avail_m', 'at'])

print(f"Loaded {len(compustat_df):,} Compustat observations")

print("Loading m_QCompustat data...")
qcompustat_df = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', 
                                columns=['gvkey', 'time_avail_m', 'txtq'])

print(f"Loaded {len(qcompustat_df):,} quarterly Compustat observations")

# Merge data (equivalent to merge 1:1 gvkey time_avail_m using m_QCompustat, keepusing(txtq) nogenerate keep(match))
print("Merging Compustat and quarterly data...")
df = pd.merge(compustat_df, qcompustat_df, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing ChTax signal...")

# Sort by gvkey and time_avail_m (equivalent to xtset gvkey time_avail_m)
df = df.sort_values(['gvkey', 'time_avail_m'])

# Create 12-month lags using calendar-based method (not position-based shift)
# Create lag time column
df['lag_time'] = df['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for txtq
txtq_lag_data = df[['gvkey', 'time_avail_m', 'txtq']].copy()
txtq_lag_data = txtq_lag_data.rename(columns={'time_avail_m': 'lag_time', 'txtq': 'l12_txtq'})
df = pd.merge(df, txtq_lag_data, on=['gvkey', 'lag_time'], how='left')

# Create lag data for at
at_lag_data = df[['gvkey', 'time_avail_m', 'at']].copy()
at_lag_data = at_lag_data.rename(columns={'time_avail_m': 'lag_time', 'at': 'l12_at'})
df = pd.merge(df, at_lag_data, on=['gvkey', 'lag_time'], how='left')

# Sort data
df = df.sort_values(['gvkey', 'time_avail_m'])

# Clean up
df = df.drop('lag_time', axis=1)    

# Calculate ChTax = (txtq - l12.txtq)/l12.at 
df['ChTax'] = (df['txtq'] - df['l12_txtq']) / df['l12_at']

print(f"Generated ChTax values for {df['ChTax'].notna().sum():,} observations")

# SAVE
print("Saving predictor...")
save_predictor(df, 'ChTax')

print("ChTax predictor completed successfully!")
