# ABOUTME: Translate IntMom predictor from Stata to Python
# ABOUTME: Calculates Intermediate Momentum using 6 months of lagged returns (7th to 12th month)

# Run from pyCode/ directory: python3 Predictors/IntMom.py
# Inputs: ../pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
# Outputs: ../pyData/Predictors/IntMom.csv (columns: permno, yyyymm, IntMom)

import pandas as pd
import numpy as np

# DATA LOAD
# Stata: use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'ret']]

# SIGNAL CONSTRUCTION
# Stata: replace ret = 0 if mi(ret)
df.loc[df['ret'].isna(), 'ret'] = 0

# Convert time_avail_m to datetime for time-based lag calculations
df['time_avail_m'] = pd.to_datetime(df['time_avail_m'])

# Sort data for proper processing
df = df.sort_values(['permno', 'time_avail_m'])

# Create time-based lagged return values (l7 to l12 in Stata)
# Stata's lag operators look for values at specific dates, not positions
# We need to use merge-based approach for time-based lags

# For each lag period (7 through 12 months), create the lag date and merge
for months_back in range(7, 13):
    # Create lag date (months_back months before current date)
    df[f'lag_date_{months_back}'] = df['time_avail_m'] - pd.DateOffset(months=months_back)
    
    # Create a copy of data for merging (source for lag values)
    lag_data = df[['permno', 'time_avail_m', 'ret']].copy()
    lag_data.columns = ['permno', f'lag_date_{months_back}', f'l{months_back}_ret']
    
    # Merge to get the lagged values
    df = df.merge(lag_data, on=['permno', f'lag_date_{months_back}'], how='left')
    
    # Clean up temporary lag date column
    df = df.drop(f'lag_date_{months_back}', axis=1)

# Do NOT fill missing lagged values - let them stay NaN so IntMom becomes NaN
# This matches Stata behavior where missing lags result in missing IntMom

# Calculate IntMom
# Stata: gen IntMom = ( (1+l7.ret)*(1+l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret)*(1+l12.ret) ) - 1
df['IntMom'] = (
    (1 + df['l7_ret']) * 
    (1 + df['l8_ret']) * 
    (1 + df['l9_ret']) * 
    (1 + df['l10_ret']) * 
    (1 + df['l11_ret']) * 
    (1 + df['l12_ret'])
) - 1

# Clean up temporary lagged variables
df = df.drop([f'l{lag}_ret' for lag in range(7, 13)], axis=1)

# SAVE
# Stata equivalent: do "$pathCode/savepredictor" IntMom

# Drop missing IntMom observations (equivalent to Stata: drop if IntMom == .)
df = df[df['IntMom'].notna()]

# Convert time_avail_m to yyyymm format for CSV output
df['yyyymm'] = (df['time_avail_m'].dt.year * 100 + 
                df['time_avail_m'].dt.month)

# Keep only required columns and order them
df = df[['permno', 'yyyymm', 'IntMom']]

# Save to CSV
df.to_csv('../pyData/Predictors/IntMom.csv', index=False)

print(f"Saved {len(df)} observations to IntMom.csv")