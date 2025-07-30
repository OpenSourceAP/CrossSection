# ABOUTME: Translates REV6.do to create 6-month earnings forecast revision measure  
# ABOUTME: Run from pyCode/ directory: python3 Predictors/REV6.py

# Run from pyCode/ directory
# Inputs: IBES_EPS_Unadj.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/REV6.csv

import pandas as pd
import numpy as np

print("Loading and processing REV6...")

# Prep IBES data (simplified)
ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# Simple filter: keep data where fpedats > statpers + 30 days
valid_forecasts = ((ibes_df['fpedats'].notna()) & 
                   (ibes_df['fpedats'] > ibes_df['statpers'] + pd.Timedelta(days=30)))
ibes_df = ibes_df[valid_forecasts].copy()

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'tickerIBES', 'time_avail_m', 'prc']].copy()

# Merge with IBES data
df = df.merge(ibes_df[['tickerIBES', 'time_avail_m', 'meanest']], 
              on=['tickerIBES', 'time_avail_m'], 
              how='left')

# SIGNAL CONSTRUCTION
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate tempRev (earnings forecast revision)
df['meanest_lag1'] = df.groupby('permno')['meanest'].shift(1)
df['prc_lag1'] = df.groupby('permno')['prc'].shift(1)
df['tempRev'] = (df['meanest'] - df['meanest_lag1']) / np.abs(df['prc_lag1'])

# Calculate REV6 as sum of current and 6 lagged tempRev values
rev6_sum = df['tempRev'].copy()
for lag in range(1, 7):
    tempRev_lag = df.groupby('permno')['tempRev'].shift(lag)
    rev6_sum = rev6_sum + tempRev_lag

df['REV6'] = rev6_sum

# Convert to output format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
df['permno'] = df['permno'].astype('int64')
df['yyyymm'] = df['yyyymm'].astype('int64')

df_final = df[['permno', 'yyyymm', 'REV6']].copy()
df_final = df_final.dropna(subset=['REV6'])
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/REV6.csv')
print("REV6 predictor saved successfully")