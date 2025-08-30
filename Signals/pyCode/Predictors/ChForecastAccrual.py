# ABOUTME: ChForecastAccrual.py - computes change in forecast and accrual predictor (Barth and Hutton 2004 RAS Table 3B)
# ABOUTME: Binary indicator for earnings estimate increases within upper half of accruals distribution

"""
ChForecastAccrual.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChForecastAccrual.py

Inputs:
    - ../pyData/Intermediate/IBES_EPS_Unadj.parquet
    - ../pyData/Intermediate/m_aCompustat.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - ../pyData/Predictors/ChForecastAccrual.csv (columns: permno, yyyymm, ChForecastAccrual)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_fastxtile import fastxtile

# Load and prepare IBES earnings forecast data
ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')

# Keep only 1-year ahead forecasts 
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# Extract key IBES columns for merging
temp_ibes = ibes_df[['tickerIBES', 'time_avail_m', 'meanest']].copy()

# Load Compustat accounting data for accruals calculation
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'act', 'che', 'lct', 'dlc', 'txp', 'at'])

# Remove duplicate observations per firm-month
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first').copy()

# Merge with master table to get IBES ticker identifiers
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                               columns=['permno', 'time_avail_m', 'tickerIBES'])
df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='left')

# Merge IBES forecast data
# Left join preserves all Compustat observations
df = pd.merge(df, temp_ibes, on=['tickerIBES', 'time_avail_m'], how='left')

# Sort data by firm and time for panel calculations
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# Calculate working capital accruals using 12-month lagged values
# Working capital accruals = changes in operating assets minus operating liabilities
def create_calendar_lag(df, var_name, months=12):
    df[f'{var_name}_l{months}_date'] = df['time_avail_m'] - pd.DateOffset(months=months)
    lag_data = df[['permno', 'time_avail_m', var_name]].rename(
        columns={'time_avail_m': f'{var_name}_l{months}_date', var_name: f'{var_name}_l{months}'})
    df = df.merge(lag_data, on=['permno', f'{var_name}_l{months}_date'], how='left')
    df = df.drop(columns=[f'{var_name}_l{months}_date'])
    return df

for var in ['act', 'che', 'lct', 'dlc', 'txp', 'at']:
    df = create_calendar_lag(df, var, 12)

# Compute accruals scaled by average total assets
numerator = ((df['act'] - df['act_l12']) - (df['che'] - df['che_l12']) - 
             ((df['lct'] - df['lct_l12']) - (df['dlc'] - df['dlc_l12']) - (df['txp'] - df['txp_l12'])))
denominator = (df['at'] + df['at_l12']) / 2

df['tempAccruals'] = numerator / denominator
# Set infinite values to missing for proper handling
df.loc[denominator == 0, 'tempAccruals'] = np.nan
df.loc[np.isinf(df['tempAccruals']), 'tempAccruals'] = np.nan

# Create binary accruals ranking (median split by month)
df['tempsort'] = fastxtile(df, 'tempAccruals', by='time_avail_m', n=2)

# Create forecast change indicator based on 1-month lagged estimates
# Use position-based lag for consistency with sorted panel data
df['meanest_l'] = df.groupby('permno')['meanest'].shift(1)
df['ChForecastAccrual'] = np.nan

# Mark forecast increases
mask_increase = (df['meanest'] > df['meanest_l']) & df['meanest'].notna() & df['meanest_l'].notna()
df.loc[mask_increase, 'ChForecastAccrual'] = 1

# Mark forecast decreases
mask_decrease = (df['meanest'] < df['meanest_l']) & df['meanest'].notna() & df['meanest_l'].notna()
df.loc[mask_decrease, 'ChForecastAccrual'] = 0

# Exclude lower half of accruals distribution (focus on high accruals firms)
df.loc[df['tempsort'] == 1, 'ChForecastAccrual'] = np.nan

# Prepare output with valid observations only
result = df[['permno', 'time_avail_m', 'ChForecastAccrual']].copy()
result = result.dropna(subset=['ChForecastAccrual']).copy()

# Convert date to YYYYMM format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Format final dataset
final_result = result[['permno', 'yyyymm', 'ChForecastAccrual']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChForecastAccrual.csv', index=False)

print(f"ChForecastAccrual predictor saved: {len(final_result)} observations")