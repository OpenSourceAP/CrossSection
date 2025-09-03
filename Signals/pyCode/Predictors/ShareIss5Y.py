# ABOUTME: Share issuance (5 year) following Daniel and Titman 2006, Table 3 \iota(t-5,t)
# ABOUTME: calculates 5-year growth in number of shares adjusted for splits

"""
Usage:
    python3 Predictors/ShareIss5Y.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m]
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, shrout, cfacshr]

Outputs:
    - ShareIss5Y.csv: CSV file with columns [permno, yyyymm, ShareIss5Y]
    - ShareIss5Y = (shares 5mo ago - shares 65mo ago) / shares 65mo ago
    - Uses adjusted shares = shrout * cfacshr to handle stock splits (following Definition in OP)
"""

import pandas as pd
import numpy as np

print("Starting ShareIss5Y calculation...")

# DATA LOAD
# Load signal master table with permno and time_avail_m
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'time_avail_m'])

# Merge with monthly CRSP data to get shares outstanding and cumulative adjustment factor
monthly_crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', columns=['permno', 'time_avail_m', 'shrout', 'cfacshr'])
df = pd.merge(signal_master, monthly_crsp, on=['permno', 'time_avail_m'], how='inner', validate='1:1')

print(f"After merge: {len(df)} observations")

# SIGNAL CONSTRUCTION
# Calculate adjusted shares outstanding
df['temp'] = df['shrout'] * df['cfacshr']

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Create time-based lags for adjusted shares outstanding
# Get values from 5 months and 65 months ago
df['time_lag5'] = df['time_avail_m'] - pd.DateOffset(months=5)
df['time_lag65'] = df['time_avail_m'] - pd.DateOffset(months=65)

# Create lag data for merging
lag5_data = df[['permno', 'time_avail_m', 'temp']].copy()
lag5_data.columns = ['permno', 'time_lag5', 'l5_temp']

lag65_data = df[['permno', 'time_avail_m', 'temp']].copy()  
lag65_data.columns = ['permno', 'time_lag65', 'l65_temp']

# Merge to get lagged values
df = df.merge(lag5_data, on=['permno', 'time_lag5'], how='left')
df = df.merge(lag65_data, on=['permno', 'time_lag65'], how='left')

# Calculate 5-year share issuance: (shares 5mo ago - shares 65mo ago) / shares 65mo ago
df['ShareIss5Y'] = (df['l5_temp'] - df['l65_temp']) / df['l65_temp']

print(f"ShareIss5Y calculated for {df['ShareIss5Y'].notna().sum()} observations")

# SAVE
# Save ShareIss5Y predictor to CSV file
result = df[['permno', 'time_avail_m', 'ShareIss5Y']].copy()
result = result.dropna(subset=['ShareIss5Y'])

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month
result = result[['permno', 'yyyymm', 'ShareIss5Y']].copy()

# Convert to integers where appropriate
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv('../pyData/Predictors/ShareIss5Y.csv', index=False)
print("ShareIss5Y.csv saved successfully")