# ABOUTME: Translates dCPVolSpread.do to create change in call-put volume spread predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/dCPVolSpread.py

# Run from pyCode/ directory
# Inputs: OptionMetricsVolSurf.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/dCPVolSpread.csv

import pandas as pd
import numpy as np

# Clean OptionMetrics data
options = pd.read_parquet('../pyData/Intermediate/OptionMetricsVolSurf.parquet')

# Screen (page 2283): keep if days == 30 & abs(delta) == 50
options = options[(options['days'] == 30) & (np.abs(options['delta']) == 50)].copy()

# Create signal (page 2290)
options = options[['secid', 'time_avail_m', 'cp_flag', 'impl_vol']].copy()

# Reshape wide: pivot cp_flag to columns
options_wide = options.pivot_table(
    index=['secid', 'time_avail_m'], 
    columns='cp_flag', 
    values='impl_vol', 
    aggfunc='first'
).reset_index()

# Flatten column names
options_wide.columns.name = None
options_wide = options_wide.rename(columns={'C': 'impl_volC', 'P': 'impl_volP'})

# Sort for lag operations
options_wide = options_wide.sort_values(['secid', 'time_avail_m'])

# Create changes in implied volatility
options_wide['dVolCall'] = options_wide.groupby('secid')['impl_volC'].diff()
options_wide['dVolPut'] = options_wide.groupby('secid')['impl_volP'].diff()
options_wide['dCPVolSpread'] = options_wide['dVolPut'] - options_wide['dVolCall']

# Keep only necessary columns
temp_data = options_wide[['secid', 'time_avail_m', 'dCPVolSpread']].copy()

# Merge onto master table
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'secid']].copy()

df = df.merge(temp_data, on=['secid', 'time_avail_m'], how='left')

# Keep only observations with non-missing dCPVolSpread
df_final = df[df['dCPVolSpread'].notna()].copy()

# Keep only necessary columns for output
df_final = df_final[['permno', 'time_avail_m', 'dCPVolSpread']].copy()

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'dCPVolSpread']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/dCPVolSpread.csv')

print("dCPVolSpread predictor saved successfully")