# ABOUTME: Return Seasonality (16-20 years) predictor translation from Stata
# ABOUTME: Calculates seasonal momentum by averaging returns from lags 191, 203, 215, 227, 239 months

import pandas as pd
import numpy as np
import os

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 (equivalent to Stata: replace ret = 0 if mi(ret))
df['ret'] = df['ret'].fillna(0)

# Create time-based lags for months 191(12)240 (191, 203, 215, 227, 239)
# This matches Stata's numlist pattern 191(12)240 which generates 191, 191+12=203, 191+24=215, 191+36=227, 191+48=239
# Use time-based lags instead of position-based to handle gaps in data correctly
for n in [191, 203, 215, 227, 239]:
    temp_col = f'temp{n}'
    
    # Create time-based lag by merging with shifted time periods
    df['time_lag'] = pd.to_datetime(df['time_avail_m']) - pd.DateOffset(months=n)
    
    # Create lag data to merge
    lag_data = df[['permno', 'time_avail_m', 'ret']].copy()
    lag_data.columns = ['permno', 'time_lag', temp_col]
    lag_data['time_lag'] = pd.to_datetime(lag_data['time_lag'])
    
    # Merge to get lagged values
    df['time_avail_m_dt'] = pd.to_datetime(df['time_avail_m'])
    df = df.merge(lag_data[['permno', 'time_lag', temp_col]], 
                  left_on=['permno', 'time_lag'], 
                  right_on=['permno', 'time_lag'], 
                  how='left')
    
    # Clean up temporary columns
    df = df.drop(['time_lag'], axis=1)

# Clean up the datetime column
df = df.drop(['time_avail_m_dt'], axis=1)

# Get list of temp columns
temp_cols = [f'temp{n}' for n in [191, 203, 215, 227, 239]]

# Calculate row total and row non-missing count (equivalent to Stata egen commands)
# egen retTemp1 = rowtotal(temp*), missing
df['retTemp1'] = df[temp_cols].sum(axis=1, skipna=True)

# egen retTemp2 = rownonmiss(temp*)  
df['retTemp2'] = df[temp_cols].notna().sum(axis=1)

# Generate MomSeason16YrPlus = retTemp1/retTemp2
df['MomSeason16YrPlus'] = df['retTemp1'] / df['retTemp2']

# Set to NaN where retTemp2 is 0 to handle division by zero
df.loc[df['retTemp2'] == 0, 'MomSeason16YrPlus'] = np.nan

# SAVE
# Clean up - drop rows where MomSeason16YrPlus is missing (equivalent to Stata: drop if MomSeason16YrPlus == .)
df_clean = df.dropna(subset=['MomSeason16YrPlus']).copy()

# Convert time_avail_m to yyyymm format (equivalent to Stata date conversion)
df_clean['yyyymm'] = pd.to_datetime(df_clean['time_avail_m']).dt.year * 100 + pd.to_datetime(df_clean['time_avail_m']).dt.month

# Keep only required columns and ensure correct order
df_output = df_clean[['permno', 'yyyymm', 'MomSeason16YrPlus']].copy()

# Save to CSV
output_path = '../pyData/Predictors/MomSeason16YrPlus.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_output.to_csv(output_path, index=False)

print(f"MomSeason16YrPlus predictor saved to {output_path}")
print(f"Output shape: {df_output.shape}")
print("First few rows:")
print(df_output.head())