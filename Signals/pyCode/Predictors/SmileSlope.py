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

# Data Prep
# use OptionMetricsVolSurf, clear
df = pd.read_parquet('../pyData/Intermediate/OptionMetricsVolSurf.parquet')

# bottom right page 221
# keep if days == 30 & abs(delta) == 50
df = df[(df['days'] == 30) & (np.abs(df['delta']) == 50)]

# make signal
# keep secid time_avail_m cp_flag impl_vol
df = df[['secid', 'time_avail_m', 'cp_flag', 'impl_vol']]

# reshape wide impl_vol, i(secid time_avail_m) j(cp_flag) string
df_pivot = df.pivot_table(index=['secid', 'time_avail_m'], 
                          columns='cp_flag', 
                          values='impl_vol',
                          aggfunc='first').reset_index()

# gen SmileSlope = impl_volP - impl_volC
df_pivot['SmileSlope'] = df_pivot['P'] - df_pivot['C']

# save temp, replace
temp = df_pivot[['secid', 'time_avail_m', 'SmileSlope']]

# Merge onto master table
# use permno time_avail_m secid using SignalMasterTable, clear
master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                         columns=['permno', 'time_avail_m', 'secid'])

# merge m:1 secid time_avail_m using temp, keep(master match) nogenerate
df_final = master.merge(temp, on=['secid', 'time_avail_m'], how='left')

# keep if SmileSlope != .
df_final = df_final[df_final['SmileSlope'].notna()]

# label var SmileSlope "Average Jump Size"

# SAVE
# do "$pathCode/savepredictor" SmileSlope
save_predictor(df_final[['permno', 'time_avail_m', 'SmileSlope']], 'SmileSlope')