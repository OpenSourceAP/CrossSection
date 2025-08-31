# ABOUTME: Calculates probability of informed trading predictor from Easley et al
# ABOUTME: Computes probability of informed trading from microstructure parameters
#
# Run: python3 Predictors/ProbInformedTrading.py
# Input: SignalMasterTable.parquet, pin_monthly.parquet
# Output: ../pyData/Predictors/ProbInformedTrading.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_fastxtile import fastxtile

# DATA LOAD
# Load master data with market value information
master_df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = master_df[['permno', 'gvkey', 'time_avail_m', 'mve_c']].copy()

# Extract year from time_avail_m for grouping
df['time_avail_m'] = pd.to_datetime(df['time_avail_m'])
df['year'] = df['time_avail_m'].dt.year

# Merge with PIN microstructure parameters data
pin_df = pd.read_parquet('../pyData/Intermediate/pin_monthly.parquet')
pin_df['time_avail_m'] = pd.to_datetime(pin_df['time_avail_m'])
df = df.merge(pin_df[['permno', 'time_avail_m', 'a', 'u', 'es', 'eb']], 
              on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
# Calculate PIN measure: probability of informed trading
# PIN = (arrival rate * uninformed trades) / (arrival rate * uninformed trades + buy orders + sell orders)
with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
    df['pin'] = (df['a'] * df['u']) / (df['a'] * df['u'] + df['es'] + df['eb'])

# Create size quintiles based on market value within each month
df['tempsize'] = fastxtile(df, 'mve_c', by='time_avail_m', n=2)

# Set PIN to missing for large cap stocks (top size quintile)
df.loc[df['tempsize'] == 2, 'pin'] = np.nan

# Assign final predictor name
df['ProbInformedTrading'] = df['pin']

# SAVE
# Keep only required columns for output
output_df = df[['permno', 'time_avail_m', 'ProbInformedTrading']].copy()
output_df = output_df.dropna(subset=['ProbInformedTrading'])

# Convert time_avail_m to yyyymm format as integer
output_df['yyyymm'] = (output_df['time_avail_m'].dt.year * 100 + 
                       output_df['time_avail_m'].dt.month)

# Final output format
final_df = output_df[['permno', 'yyyymm', 'ProbInformedTrading']].copy()
final_df = final_df.sort_values(['permno', 'yyyymm'])

# Save to CSV
final_df.to_csv('../pyData/Predictors/ProbInformedTrading.csv', index=False)

print(f"ProbInformedTrading predictor saved with {len(final_df)} observations")