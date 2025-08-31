# ABOUTME: SmileSlope.py - Generates SmileSlope predictor (Average Jump Size)
# ABOUTME: Measures implied volatility smile slope from options data (Yan 2011 JFE)

"""
Usage:
    python3 Predictors/SmileSlope.py

Inputs:
    - pyData/Intermediate/OptionMetricsVolSurf.parquet
    - pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - pyData/Predictors/SmileSlope.csv - Put IV minus Call IV for 30-day 50-delta options
"""

# --------------
# Yan 2011 JFE

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor

# Load option volatility surface data
df = pd.read_parquet('../pyData/Intermediate/OptionMetricsVolSurf.parquet')

# Filter to 30-day options with 50 delta (per page 221)
df = df[(df['days'] == 30) & (np.abs(df['delta']) == 50)]

# Select relevant columns for smile slope calculation
df = df[['secid', 'time_avail_m', 'cp_flag', 'impl_vol']]

# Pivot to get separate columns for put and call implied volatilities
df_pivot = df.pivot_table(index=['secid', 'time_avail_m'], 
                          columns='cp_flag', 
                          values='impl_vol',
                          aggfunc='first').reset_index()

# Calculate smile slope as put IV minus call IV
df_pivot['SmileSlope'] = df_pivot['P'] - df_pivot['C']

# Keep relevant columns for merging
temp = df_pivot[['secid', 'time_avail_m', 'SmileSlope']]

# Load SignalMasterTable for merging
master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                         columns=['permno', 'time_avail_m', 'secid'])

# Merge smile slope data with master table
df_final = master.merge(temp, on=['secid', 'time_avail_m'], how='left')

# Keep only observations with non-missing smile slope values
df_final = df_final[df_final['SmileSlope'].notna()]

# SmileSlope represents average jump size (option volatility smile slope)

# Save standardized predictor output
save_predictor(df_final[['permno', 'time_avail_m', 'SmileSlope']], 'SmileSlope')