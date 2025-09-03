# ABOUTME: Change in put vol minus change in call vol following An, Ang, Bali, Cakici 2014, Table IIC
# ABOUTME: calculates change in call-put volume spread predictor for informed trading

# An Ang Bali Cakici 2014 Table II C
# Run from pyCode/ directory
# Inputs: OptionMetricsVolSurf.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/dCPVolSpread.csv

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from config import PATCH_OPTIONM_IV

print("Starting dCPVolSpread.py...")

# Check for Option Metrics patch
if PATCH_OPTIONM_IV:
    print("WARNING: PATCH_OPTIONM_IV is True, using 2023 vintage from openassetpricing")
    print("See https://github.com/OpenSourceAP/CrossSection/issues/156")
    from openassetpricing import OpenAP
    openap = OpenAP(2023)
    df = openap.dl_signal('polars', ['dCPVolSpread'])
    df = df.rename({'yyyymm': 'time_avail_m'})
    save_predictor(df, 'dCPVolSpread')
    sys.exit()

# Clean OptionMetrics data
print("Loading OptionMetrics volatility surface data...")
options = pd.read_parquet('../pyData/Intermediate/OptionMetricsVolSurf.parquet')

print(f"Loaded options data: {options.shape[0]} rows")
# Screen (page 2283): keep if days == 30 & abs(delta) == 50
options = options[(options['days'] == 30) & (np.abs(options['delta']) == 50)].copy()
print(f"After screening: {options.shape[0]} rows")

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
print("Calculating volatility changes...")
options_wide['dVolCall'] = options_wide.groupby('secid')['impl_volC'].diff()
options_wide['dVolPut'] = options_wide.groupby('secid')['impl_volP'].diff()
options_wide['dCPVolSpread'] = options_wide['dVolPut'] - options_wide['dVolCall']

# Keep only necessary columns
temp_data = options_wide[['secid', 'time_avail_m', 'dCPVolSpread']].copy()

# Merge onto master table
print("Merging with SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'secid']].copy()

df = df.merge(temp_data, on=['secid', 'time_avail_m'], how='left')
print(f"After merge: {df.shape[0]} rows")

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'dCPVolSpread']].copy()
print(f"Calculated dCPVolSpread for {df_final['dCPVolSpread'].notna().sum()} observations")

# SAVE
save_predictor(df_final, 'dCPVolSpread')
print("dCPVolSpread.py completed successfully")