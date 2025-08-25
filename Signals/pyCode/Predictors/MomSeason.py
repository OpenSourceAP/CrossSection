# ABOUTME: Return Seasonality (years 2 to 5) predictor translation from Stata
# ABOUTME: Calculates seasonal momentum by averaging returns from lags 23-59 months

import pandas as pd
import numpy as np
import os
import sys
sys.path.append('.')
from utils.stata_replication import stata_multi_lag

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort data for processing
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 (equivalent to Stata: replace ret = 0 if mi(ret))
df['ret'] = df['ret'].fillna(0)

# Use stata_multi_lag for calendar-validated lag operations
# Create lags for 23, 35, 47, 59 months (equivalent to foreach n of numlist 23(12)59)
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [23, 35, 47, 59])

# Calculate row totals and counts like Stata using the lagged columns
lag_columns = ['ret_lag23', 'ret_lag35', 'ret_lag47', 'ret_lag59']

# egen retTemp1 = rowtotal(temp*), missing
df['retTemp1'] = df[lag_columns].sum(axis=1, skipna=True)

# egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[lag_columns].notna().sum(axis=1)

# Generate MomSeason = retTemp1/retTemp2
df['MomSeason'] = df['retTemp1'] / df['retTemp2']

# Set to NaN where retTemp2 is 0 to handle division by zero
df.loc[df['retTemp2'] == 0, 'MomSeason'] = np.nan

# SAVE
# Clean up - drop rows where MomSeason is missing (equivalent to Stata: drop if MomSeason == .)
df_output = df.dropna(subset=['MomSeason']).copy()

# Convert time_avail_m to yyyymm format (equivalent to Stata date conversion)
df_output['yyyymm'] = df_output['time_avail_m'].dt.year * 100 + df_output['time_avail_m'].dt.month

# Keep only required columns and ensure correct order
df_final = df_output[['permno', 'yyyymm', 'MomSeason']].copy()

# Save to CSV
output_path = '../pyData/Predictors/MomSeason.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_final.to_csv(output_path, index=False)

print(f"MomSeason predictor saved to {output_path}")
print(f"Output shape: {df_final.shape}")
print("First few rows:")
print(df_final.head())