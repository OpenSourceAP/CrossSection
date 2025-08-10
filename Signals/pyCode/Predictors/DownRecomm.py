# ABOUTME: Translates DownRecomm.do to calculate recommendation downgrades indicator
# ABOUTME: Run with: python3 Predictors/DownRecomm.py

# Calculates binary indicator for analyst recommendation downgrades using IBES data
# Input: ../pyData/Intermediate/IBES_Recommendations.parquet, ../pyData/Intermediate/SignalMasterTable.parquet  
# Output: ../pyData/Predictors/DownRecomm.csv

import pandas as pd
import numpy as np

# PREP IBES DATA
# Load IBES_Recommendations with specific columns
df = pd.read_parquet('../pyData/Intermediate/IBES_Recommendations.parquet', 
                     columns=['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd'])

# collapse down to firm-month
# First collapse: gcollapse (lastnm) ireccd by (tickerIBES, amaskcd, time_avail_m)
# lastnm = last non-missing value
def last_non_missing(series):
    non_missing = series.dropna()
    return non_missing.iloc[-1] if len(non_missing) > 0 else np.nan

df = df.groupby(['tickerIBES', 'amaskcd', 'time_avail_m'])['ireccd'].apply(last_non_missing).reset_index()

# Second collapse: gcollapse (mean) ireccd by (tickerIBES, time_avail_m)
df = df.groupby(['tickerIBES', 'time_avail_m'], as_index=False)['ireccd'].mean()

# bys tickerIBES (time_avail_m): gen DownRecomm = ireccd > ireccd[_n-1] & ireccd[_n-1] != .
# Sort by ticker and time within groups
df = df.sort_values(['tickerIBES', 'time_avail_m'])

# Create lag of ireccd
df['ireccd_lag'] = df.groupby('tickerIBES')['ireccd'].shift(1)

# Calculate DownRecomm: current > previous AND previous is not missing
df['DownRecomm'] = ((df['ireccd'] > df['ireccd_lag']) & (df['ireccd_lag'].notna())).astype(int)

# add permno
# Merge with SignalMasterTable to get permno
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                columns=['permno', 'tickerIBES', 'time_avail_m'])

# Merge 1:m tickerIBES time_avail_m, keep only matches
df = df.merge(signal_master, on=['tickerIBES', 'time_avail_m'], how='inner')

# Keep only observations where DownRecomm calculation was valid (had a lag)
df = df[df['ireccd_lag'].notna()]

# Keep only required columns for final output
result = df[['permno', 'time_avail_m', 'DownRecomm']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final format matching Stata output
result = result[['permno', 'yyyymm', 'DownRecomm']]

# Convert permno and yyyymm to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/DownRecomm.csv', index=False)

print(f"DownRecomm predictor created with {len(result)} observations")