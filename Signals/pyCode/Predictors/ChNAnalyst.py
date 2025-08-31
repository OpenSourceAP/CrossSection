# ABOUTME: ChNAnalyst.py - calculates decline in analyst coverage predictor
# ABOUTME: Line-by-line translation of ChNAnalyst.do following CLAUDE.md translation philosophy

"""
ChNAnalyst.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChNAnalyst.py

Inputs:
    - ../pyData/Intermediate/IBES_EPS_Unadj.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - ../pyData/Predictors/ChNAnalyst.csv (columns: permno, yyyymm, ChNAnalyst)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_fastxtile import fastxtile

# Load IBES earnings per share data
ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')

# Filter to annual forecasts only
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# Create indicator for valid forecasts (end date exists and is at least 30 days after statement period)
ibes_df['tmp'] = np.where(
    ibes_df['fpedats'].notna() & (ibes_df['fpedats'] > ibes_df['statpers'] + pd.Timedelta(days=30)),
    1, 
    np.nan
)

# For invalid forecasts with same end date as previous record, use previous mean estimate
ibes_df = ibes_df.sort_values(['tickerIBES', 'time_avail_m'])
ibes_df['meanest_lag1'] = ibes_df.groupby('tickerIBES')['meanest'].shift(1)
ibes_df['fpedats_lag1'] = ibes_df.groupby('tickerIBES')['fpedats'].shift(1)

mask_replace = ibes_df['tmp'].isna() & (ibes_df['fpedats'] == ibes_df['fpedats_lag1'])
ibes_df.loc[mask_replace, 'meanest'] = ibes_df.loc[mask_replace, 'meanest_lag1']

# Clean up temporary variables
ibes_df = ibes_df.drop(columns=['tmp', 'meanest_lag1', 'fpedats_lag1'])

# Keep only required analyst coverage variables
temp_ibes = ibes_df[['tickerIBES', 'time_avail_m', 'numest', 'statpers', 'fpedats']].copy()

# Load master table with stock identifiers and market values
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                     columns=['permno', 'time_avail_m', 'tickerIBES', 'mve_c'])

# Merge in analyst coverage data by ticker and month
df = pd.merge(df, temp_ibes, on=['tickerIBES', 'time_avail_m'], how='left')

# Sort data for time series operations
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# Calculate 3-month lagged analyst coverage for comparison
df['numest_l3_date'] = df['time_avail_m'] - pd.DateOffset(months=3)
numest_lag = df[['permno', 'time_avail_m', 'numest']].rename(columns={'time_avail_m': 'numest_l3_date', 'numest': 'numest_l3'})
df = df.merge(numest_lag, on=['permno', 'numest_l3_date'], how='left')
df = df.drop(columns=['numest_l3_date'])
df['ChNAnalyst'] = np.nan

# Set indicator to 1 if current analyst count is less than 3 months ago
mask_decline = (df['numest'] < df['numest_l3']) & df['numest_l3'].notna()
df.loc[mask_decline, 'ChNAnalyst'] = 1

# Set indicator to 0 if current analyst count is greater than or equal to 3 months ago
mask_no_decline = (df['numest'] >= df['numest_l3']) & df['numest'].notna()
df.loc[mask_no_decline, 'ChNAnalyst'] = 0

# Exclude data from July-September 1987 due to data quality issues
mask_1987 = (df['time_avail_m'] >= pd.Timestamp('1987-07-01')) & (df['time_avail_m'] <= pd.Timestamp('1987-09-01'))
df.loc[mask_1987, 'ChNAnalyst'] = np.nan

# Calculate size quintiles based on market value (predictor only works for small firms)
df['temp'] = fastxtile(df, 'mve_c', n=5)

# Keep only smallest two quintiles (small firms)
df = df[df['temp'] <= 2].copy()

# Keep only needed columns and non-missing values
result = df[['permno', 'time_avail_m', 'ChNAnalyst']].copy()
result = result.dropna(subset=['ChNAnalyst']).copy()

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'ChNAnalyst']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChNAnalyst.csv', index=False)

print(f"ChNAnalyst predictor saved: {len(final_result)} observations")