#%%
import os
os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.chdir("..")
os.listdir()

#%%

# ABOUTME: Option trading volume predictors following Johnson and So 2012 JFE, Table 2A
# ABOUTME: OptionVolume1 = option to stock volume ratio, OptionVolume2 = abnormal option volume (current/6-month average)

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
print("Starting ZZ1_OptionVolume1_OptionVolume2.py...")

# DATA LOAD
print("Loading data...")
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor

# Load required columns from SignalMasterTable
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                     columns=['permno', 'time_avail_m', 'secid', 'prc', 'shrcd'])

# Merge with monthly CRSP data to get stock volume
crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet',
                       columns=['permno', 'time_avail_m', 'vol'])
df = df.merge(crsp, on=['permno', 'time_avail_m'], how='left')

# Temporarily separate observations with missing secid before option volume merge
temp = df[df['secid'].isna()].copy()
df = df[df['secid'].notna()].copy()

# Merge with OptionMetrics data to get option volume
optmetrics = pd.read_parquet('../pyData/Intermediate/OptionMetricsVolume.parquet',
                             columns=['secid', 'time_avail_m', 'optvolume'])
df = df.merge(optmetrics, on=['secid', 'time_avail_m'], how='left')


#%%

df.groupby(['permno', 'time_avail_m'])['secid'].nunique().sort_values(ascending=False).head(20)


#%%

# Recombine with observations that had missing secid
df = pd.concat([df, temp], ignore_index=True)

# SIGNAL CONSTRUCTION
# Sort by permno and time for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate OptionVolume1 as ratio of option volume to stock volume
df['OptionVolume1'] = df['optvolume'] / df['vol']

# Set OptionVolume1 to missing if prior period option or stock volume is missing
# Create lagged optvolume and vol for the condition check
df['l1_optvolume'] = df.groupby('permno')['optvolume'].shift(1)
df['l1_vol'] = df.groupby('permno')['vol'].shift(1)
df.loc[df['l1_optvolume'].isna() | df['l1_vol'].isna(), 'OptionVolume1'] = np.nan

# Create 6 lags of OptionVolume1 for calculating 6-month moving average
for n in range(1, 7):
    df[f'tempVol{n}'] = df.groupby('permno')['OptionVolume1'].shift(n)

# Calculate 6-month moving average of OptionVolume1
temp_cols = [f'tempVol{n}' for n in range(1, 7)]
df['tempMean'] = df[temp_cols].mean(axis=1)

# Calculate OptionVolume2 as current ratio divided by 6-month average
df['OptionVolume2'] = df['OptionVolume1'] / df['tempMean']

# OptionVolume1: Option Volume
# OptionVolume2: Option Volume (abnormal)

# SAVE
# Save OptionVolume1 predictor
save_predictor(df[['permno', 'time_avail_m', 'OptionVolume1']], 'OptionVolume1')
print("ZZ1_OptionVolume1_OptionVolume2.py completed successfully")

# Save OptionVolume2 predictor
save_predictor(df[['permno', 'time_avail_m', 'OptionVolume2']], 'OptionVolume2')
print("ZZ1_OptionVolume1_OptionVolume2.py completed successfully")