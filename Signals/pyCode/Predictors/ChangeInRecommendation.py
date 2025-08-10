# ABOUTME: Translates ChangeInRecommendation.do to calculate change in analyst recommendations
# ABOUTME: Run with: python3 Predictors/ChangeInRecommendation.py

# Calculates change in analyst recommendations using IBES data
# Input: ../pyData/Intermediate/IBES_Recommendations.parquet, ../pyData/Intermediate/SignalMasterTable.parquet  
# Output: ../pyData/Predictors/ChangeInRecommendation.csv

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

# Second collapse: take mean ireccd by (tickerIBES, time_avail_m) 
df = df.groupby(['tickerIBES', 'time_avail_m'], as_index=False)['ireccd'].mean()

# reverse score following OP
df['opscore'] = 6 - df['ireccd']

# Sort for lag operation
df = df.sort_values(['tickerIBES', 'time_avail_m'])

# Calculate ChangeInRecommendation = opscore - opscore[_n-1] if opscore[_n-1] != .
df['opscore_lag'] = df.groupby('tickerIBES')['opscore'].shift(1)
df['ChangeInRecommendation'] = np.where(df['opscore_lag'].notna(), 
                                        df['opscore'] - df['opscore_lag'], 
                                        np.nan)

# add permno
# Merge with SignalMasterTable to get permno
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                columns=['permno', 'tickerIBES', 'time_avail_m'])

# Merge 1:m tickerIBES time_avail_m, keep only matches
df = df.merge(signal_master, on=['tickerIBES', 'time_avail_m'], how='inner')

# Keep only observations with valid ChangeInRecommendation (following Stata if condition)
df = df.dropna(subset=['ChangeInRecommendation'])

# Keep only required columns for final output
result = df[['permno', 'time_avail_m', 'ChangeInRecommendation']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final format matching Stata output
result = result[['permno', 'yyyymm', 'ChangeInRecommendation']]

# Convert permno and yyyymm to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/ChangeInRecommendation.csv', index=False)

print(f"ChangeInRecommendation predictor created with {len(result)} observations")