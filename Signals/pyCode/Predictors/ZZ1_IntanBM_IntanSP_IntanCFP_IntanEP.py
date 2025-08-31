# ABOUTME: Creates 4 intangible return predictors (IntanBM, IntanSP, IntanCFP, IntanEP) using cross-sectional regressions
# ABOUTME: Calculates cumulative returns and 60-month changes, then runs regressions for each time period

"""
How to run:
    python3 Predictors/ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py

Inputs:
    - pyData/Intermediate/m_aCompustat.parquet
    - pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - pyData/Predictors/IntanBM.csv
    - pyData/Predictors/IntanSP.csv
    - pyData/Predictors/IntanCFP.csv
    - pyData/Predictors/IntanEP.csv

The script creates 4 predictors based on intangible returns:
1. IntanBM: Intangible return (BM) - Book-to-market based
2. IntanSP: Intangible return (SP) - Sales-to-price based  
3. IntanCFP: Intangible return (CFP) - Cash flow-to-price based
4. IntanEP: Intangible return (EP) - Earnings-to-price based

For each predictor, it:
- Calculates 60-month cumulative returns
- Runs cross-sectional regressions for each time period
- Saves residuals as the intangible return measure
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.winsor2 import winsor2

# Suppress sklearn warnings
warnings.filterwarnings("ignore")

print("Starting ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py")

# DATA LOAD
print("Loading data...")
# Load m_aCompustat data
compustat_cols = ['permno', 'gvkey', 'time_avail_m', 'sale', 'ib', 'dp', 'ni', 'ceq']
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', columns=compustat_cols)

# Keep one observation per permno-time_avail_m (deletes a few observations)
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')

# Merge with SignalMasterTable
signalmaster = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'time_avail_m', 'ret', 'mve_c'])
df = pd.merge(df, signalmaster, on=['permno', 'time_avail_m'], how='inner')

print(f"Data loaded. Shape: {df.shape}")

# SIGNAL CONSTRUCTION
print("Constructing signals...")
# Generate temporary accounting measures
# Handle cases where ceq/mve_c <= 0 (Stata would treat log of negative/zero as missing)
df['ceq_mve_ratio'] = df['ceq'] / df['mve_c']
df['tempAccBM'] = np.where(df['ceq_mve_ratio'] > 0, np.log(df['ceq_mve_ratio']), np.nan)
df['tempAccSP'] = df['sale'] / df['mve_c']
df['tempAccCFP'] = (df['ib'] + df['dp']) / df['mve_c'] 
df['tempAccEP'] = df['ni'] / df['mve_c']

# Set panel data (equivalent to xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# Cumulative return (based on return adjusted for splits and dividends)
print("Calculating cumulative returns...")
df['tempCumRet'] = df.groupby('permno')['ret'].transform(lambda x: np.exp(np.log(1 + x).cumsum()))

# Calculate 60-month return change using efficient calendar-based lag (matches Stata l60.)
print("Calculating 60-month calendar-based lag for cumulative returns...")

# Create target date column
df['target_date'] = df['time_avail_m'] - pd.DateOffset(months=60)

# Create lag lookup table
lag_lookup = df[['permno', 'time_avail_m', 'tempCumRet']].copy()
lag_lookup.columns = ['permno', 'target_date', 'tempCumRet_lag60']

# Merge to get calendar-based lags
df = df.merge(lag_lookup, on=['permno', 'target_date'], how='left')
df.drop('target_date', axis=1, inplace=True)

df['tempRet60'] = (df['tempCumRet'] - df['tempCumRet_lag60']) / df['tempCumRet_lag60']

# Winsorize tempRet60 at 1% and 99% percentiles using trim (set extreme values to NaN)
df = winsor2(df, ['tempRet60'], replace=True, trim=True, cuts=[1, 99])

# Loop over four measures
temp_vars = ['tempAccBM', 'tempAccSP', 'tempAccCFP', 'tempAccEP']

for v in temp_vars:
    print(f"Processing {v}...")
    
    # Calculate 60-month calendar-based lag of the variable using efficient merge (matches Stata l60.)
    print(f"  Calculating 60-month calendar-based lag for {v}...")
    
    # Create target dates for lag lookup
    df['target_date'] = df['time_avail_m'] - pd.DateOffset(months=60)
    
    # Create lag lookup table for this variable
    var_lag_lookup = df[['permno', 'time_avail_m', v]].copy()
    var_lag_lookup.columns = ['permno', 'target_date', f'{v}_lag60']
    
    # Merge to get calendar-based lags
    df = df.merge(var_lag_lookup, on=['permno', 'target_date'], how='left')
    df.drop('target_date', axis=1, inplace=True)
    
    # Generate the return-adjusted measure
    df[f'{v}Ret'] = df[v] - df[f'{v}_lag60'] + df['tempRet60']
    
    # Initialize the residual variable
    df[f'tempU_{v}'] = np.nan
    
    # Loop over cross-sectional regressions
    unique_times = df['time_avail_m'].dropna().unique()
    unique_times = sorted(unique_times)
    
    for t in unique_times:
        # Filter data for this time period
        mask = df['time_avail_m'] == t
        subset = df[mask].copy()
        
        # Check if we have enough observations and required variables
        required_vars = ['tempRet60', f'{v}_lag60', f'{v}Ret']
        subset_clean = subset[required_vars].dropna()
        
        if len(subset_clean) >= 2:  # Need at least 2 observations for regression
            try:
                # Run regression: tempRet60 ~ lag60(v) + vRet
                X = subset_clean[[f'{v}_lag60', f'{v}Ret']]
                y = subset_clean['tempRet60']
                
                # Fit regression
                reg = LinearRegression().fit(X, y)
                
                # Predict and calculate residuals
                y_pred = reg.predict(X)
                residuals = y - y_pred
                
                # Store residuals in the original dataframe
                valid_indices = subset_clean.index
                df.loc[valid_indices, f'tempU_{v}'] = residuals
                
            except:
                # If regression fails, continue to next time period
                continue

# Rename variables to final predictor names
df['IntanBM'] = df['tempU_tempAccBM']
df['IntanSP'] = df['tempU_tempAccSP']  
df['IntanCFP'] = df['tempU_tempAccCFP']
df['IntanEP'] = df['tempU_tempAccEP']

print("Regressions completed.")

# SAVE
predictors = ['IntanBM', 'IntanSP', 'IntanCFP', 'IntanEP']

for pred in predictors:
    print(f"Saving {pred}...")
    
    # Create a copy for saving
    save_df = df.copy()
    
    # Drop missing values for this predictor
    save_df = save_df.dropna(subset=[pred])
    
    # Convert time_avail_m to yyyymm format
    # time_avail_m is monthly date, need to convert to YYYYMM integer
    save_df['year'] = save_df['time_avail_m'].dt.year
    save_df['month'] = save_df['time_avail_m'].dt.month
    save_df['yyyymm'] = save_df['year'] * 100 + save_df['month']
    
    # Keep only required columns
    output_df = save_df[['permno', 'yyyymm', pred]].copy()
    output_df = output_df.sort_values(['permno', 'yyyymm'])
    
    # Save to CSV
    output_path = f'../pyData/Predictors/{pred}.csv'
    output_df.to_csv(output_path, index=False)
    
    print(f"Saved {pred} with {len(output_df)} observations")

print("ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py completed successfully!")