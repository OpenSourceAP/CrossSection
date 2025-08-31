# ABOUTME: Calculates intermediate momentum following Novy-Marx 2012 Table 2
# ABOUTME: Stock returns between months t-12 and t-6 (intermediate horizon)

# Run from pyCode/ directory: python3 Predictors/IntMom.py
# Inputs: ../pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
# Outputs: ../pyData/Predictors/IntMom.csv (columns: permno, yyyymm, IntMom)

import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'ret']]

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 for momentum calculations
df.loc[df['ret'].isna(), 'ret'] = 0

# Convert time_avail_m to datetime for time-based lag calculations
df['time_avail_m'] = pd.to_datetime(df['time_avail_m'])

# Sort data for proper processing
df = df.sort_values(['permno', 'time_avail_m'])

# Create time-based lags for months t-7 to t-12 (intermediate momentum period)

# Generate calendar-based lags (not position-based)
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

# Missing lagged values result in missing IntMom (consistent with methodology)

# Calculate intermediate momentum by compounding returns over months t-12 to t-6
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
save_predictor(df, 'IntMom')

print(f"Saved {len(df)} observations to IntMom.csv")