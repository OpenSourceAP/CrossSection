# ABOUTME: Return Seasonality (years 2 to 5) predictor translation from Stata
# ABOUTME: Calculates seasonal momentum by averaging returns from lags 23-59 months

import pandas as pd
import numpy as np
import os

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort data for processing
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 (equivalent to Stata: replace ret = 0 if mi(ret))
df['ret'] = df['ret'].fillna(0)

# Create temp columns for each lag using calendar-based lookups
# foreach n of numlist 23(12)59 { gen temp`n' = l`n'.ret }
temp_columns = []
for n in [23, 35, 47, 59]:
    col_name = f'temp{n}'
    temp_columns.append(col_name)
    
    # Calculate target date (n months before each observation)
    df['target_date'] = df['time_avail_m'] - pd.DateOffset(months=n)
    
    # Create lookup table for lagged returns
    lag_lookup = df[['permno', 'time_avail_m', 'ret']].rename(columns={
        'time_avail_m': 'lag_date',
        'ret': 'lag_ret'
    })
    
    # Merge to get lagged values (equivalent to Stata's l23.ret, l35.ret, etc.)
    merged = df.merge(
        lag_lookup,
        left_on=['permno', 'target_date'],
        right_on=['permno', 'lag_date'],
        how='left'
    )
    
    # Store the lagged return (NaN if no data available for that exact date)
    df[col_name] = merged['lag_ret']
    
    # Clean up temporary columns
    df = df.drop(columns=['target_date'])

# Calculate row totals and counts like Stata
# egen retTemp1 = rowtotal(temp*), missing
df['retTemp1'] = df[temp_columns].sum(axis=1, skipna=True)

# egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[temp_columns].notna().sum(axis=1)

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