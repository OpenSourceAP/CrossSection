# ABOUTME: Translates ShareIss1Y.do - calculates 1-year share issuance signal
# ABOUTME: Run from pyCode/ directory: python3 Predictors/ShareIss1Y.py

# Inputs: 
#   - ../pyData/Intermediate/SignalMasterTable.parquet 
#   - ../pyData/Intermediate/monthlyCRSP.parquet
# Outputs:
#   - ../pyData/Predictors/ShareIss1Y.csv

import pandas as pd
import numpy as np

print("Starting ShareIss1Y calculation...")

# DATA LOAD
# use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'time_avail_m'])

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(shrout cfacshr) nogenerate keep(match)
monthly_crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', columns=['permno', 'time_avail_m', 'shrout', 'cfacshr'])
df = pd.merge(signal_master, monthly_crsp, on=['permno', 'time_avail_m'], how='inner', validate='1:1')

print(f"After merge: {len(df)} observations")

# SIGNAL CONSTRUCTION
# gen temp = shrout*cfacshr
df['temp'] = df['shrout'] * df['cfacshr']

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Create time-based lags (not position-based)
# l6.temp means 6 months ago, l18.temp means 18 months ago
df['time_lag6'] = df['time_avail_m'] - pd.DateOffset(months=6)
df['time_lag18'] = df['time_avail_m'] - pd.DateOffset(months=18)

# Create lag data for merging
lag6_data = df[['permno', 'time_avail_m', 'temp']].copy()
lag6_data.columns = ['permno', 'time_lag6', 'l6_temp']

lag18_data = df[['permno', 'time_avail_m', 'temp']].copy()  
lag18_data.columns = ['permno', 'time_lag18', 'l18_temp']

# Merge to get lagged values
df = df.merge(lag6_data, on=['permno', 'time_lag6'], how='left')
df = df.merge(lag18_data, on=['permno', 'time_lag18'], how='left')

# gen ShareIss1Y = (l6.temp - l18.temp)/l18.temp
df['ShareIss1Y'] = (df['l6_temp'] - df['l18_temp']) / df['l18_temp']

print(f"ShareIss1Y calculated for {df['ShareIss1Y'].notna().sum()} observations")

# SAVE
# do "$pathCode/savepredictor" ShareIss1Y
result = df[['permno', 'time_avail_m', 'ShareIss1Y']].copy()
result = result.dropna(subset=['ShareIss1Y'])

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month
result = result[['permno', 'yyyymm', 'ShareIss1Y']].copy()

# Convert to integers where appropriate
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv('../pyData/Predictors/ShareIss1Y.csv', index=False)
print("ShareIss1Y.csv saved successfully")