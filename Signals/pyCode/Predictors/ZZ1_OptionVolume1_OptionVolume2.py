# ABOUTME: ZZ1_OptionVolume1_OptionVolume2.py - Generates OptionVolume1 and OptionVolume2 predictors
# ABOUTME: Measures option trading volume relative to stock volume (Johnson and So 2012 JFE)

"""
Usage:
    python3 Predictors/ZZ1_OptionVolume1_OptionVolume2.py

Inputs:
    - pyData/Intermediate/SignalMasterTable.parquet
    - pyData/Intermediate/monthlyCRSP.parquet  
    - pyData/Intermediate/OptionMetricsVolume.parquet

Outputs:
    - pyData/Predictors/OptionVolume1.csv - Option to stock volume ratio
    - pyData/Predictors/OptionVolume2.csv - Abnormal option volume (current/6-month average)
"""

# --------------
# Johnson and So 2012 JFE
# DATA LOAD
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor

# use permno time_avail_m secid prc shrcd using SignalMasterTable
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                     columns=['permno', 'time_avail_m', 'secid', 'prc', 'shrcd'])

# add stock volume
# merge 1:1 permno time_avail_m using monthlyCRSP, keep(master match) nogenerate keepusing(vol)
crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet',
                       columns=['permno', 'time_avail_m', 'vol'])
df = df.merge(crsp, on=['permno', 'time_avail_m'], how='left')

# preserve
# keep if mi(secid)
# save temp, replace
# restore
# drop if mi(secid)
temp = df[df['secid'].isna()].copy()
df = df[df['secid'].notna()].copy()

# add option volume
# merge m:1 secid time_avail_m using OptionMetricsVolume, keep(master match) nogenerate keepusing(optvolume)
optmetrics = pd.read_parquet('../pyData/Intermediate/OptionMetricsVolume.parquet',
                             columns=['secid', 'time_avail_m', 'optvolume'])
df = df.merge(optmetrics, on=['secid', 'time_avail_m'], how='left')

# append using temp
df = pd.concat([df, temp], ignore_index=True)

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# gen OptionVolume1 = optvolume/vol
df['OptionVolume1'] = df['optvolume'] / df['vol']

# replace OptionVolume1 = . if mi(l1.optvolume) | mi(l1.vol)
# Create lagged optvolume and vol for the condition check
df['l1_optvolume'] = df.groupby('permno')['optvolume'].shift(1)
df['l1_vol'] = df.groupby('permno')['vol'].shift(1)
df.loc[df['l1_optvolume'].isna() | df['l1_vol'].isna(), 'OptionVolume1'] = np.nan

# foreach n of numlist 1/6
# gen tempVol`n' = l`n'.OptionVolume1
for n in range(1, 7):
    df[f'tempVol{n}'] = df.groupby('permno')['OptionVolume1'].shift(n)

# egen tempMean = rowmean(tempVol*)
temp_cols = [f'tempVol{n}' for n in range(1, 7)]
df['tempMean'] = df[temp_cols].mean(axis=1)

# gen OptionVolume2 = OptionVolume1/tempMean
df['OptionVolume2'] = df['OptionVolume1'] / df['tempMean']

# label var OptionVolume1 "Option Volume"
# label var OptionVolume2 "Option Volume (abnormal)"

# SAVE
# do "$pathCode/savepredictor" OptionVolume1
save_predictor(df[['permno', 'time_avail_m', 'OptionVolume1']], 'OptionVolume1')

# do "$pathCode/savepredictor" OptionVolume2
save_predictor(df[['permno', 'time_avail_m', 'OptionVolume2']], 'OptionVolume2')