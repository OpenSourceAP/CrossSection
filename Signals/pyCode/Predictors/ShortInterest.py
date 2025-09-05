# ABOUTME: Short Interest following Dechow et al. 2001, Table 1A
# ABOUTME: calculates short interest predictor scaled by shares outstanding
"""
Usage:
    python3 Predictors/ShortInterest.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with company identifiers
    - monthlyCRSP.parquet: Monthly CRSP data with shares outstanding
    - monthlyShortInterest.parquet: Monthly short interest data

Outputs:
    - ShortInterest.csv: CSV file with columns [permno, yyyymm, ShortInterest]
    - ShortInterest = shortint/shrout, short interest scaled by shares outstanding
"""

import pandas as pd
import numpy as np

print("Starting ShortInterest calculation...")

# DATA LOAD
# Load base universe of stocks with company identifiers
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'time_avail_m'])

# Add shares outstanding data from monthly CRSP
monthly_crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', columns=['permno', 'time_avail_m', 'shrout'])
df = pd.merge(signal_master, monthly_crsp, on=['permno', 'time_avail_m'], how='inner', validate='1:1')
print(f"After merge with monthlyCRSP: {len(df)} observations")

# Add short interest data
monthly_short = pd.read_parquet('../pyData/Intermediate/monthlyShortInterest.parquet', columns=['permno', 'time_avail_m', 'shortint'])
df = pd.merge(df, monthly_short, on=['permno', 'time_avail_m'], how='inner', validate='1:1')
print(f"After merge with monthlyShortInterest: {len(df)} observations")

# SIGNAL CONSTRUCTION
# Calculate short interest as ratio of shares short to shares outstanding
df['ShortInterest'] = df['shortint'] / df['shrout']

print(f"ShortInterest calculated for {df['ShortInterest'].notna().sum()} observations")

# SAVE
# Prepare final output dataset
result = df[['permno', 'time_avail_m', 'ShortInterest']].copy()
result = result.dropna(subset=['ShortInterest'])

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month
result = result[['permno', 'yyyymm', 'ShortInterest']].copy()

# Convert to integers where appropriate
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv('../pyData/Predictors/ShortInterest.csv', index=False)
print("ShortInterest.csv saved successfully")