# ABOUTME: Translates FirmAgeMom.do to create firm age-momentum interaction predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/FirmAgeMom.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet  
# Output: ../pyData/Predictors/FirmAgeMom.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import stata_multi_lag

# DATA LOAD
# use permno time_avail_m ret prc using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret', 'prc']].copy()

# SIGNAL CONSTRUCTION

# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# bys permno (time_avail_m): gen tempage = _n
df = df.sort_values(['permno', 'time_avail_m'])
df['tempage'] = df.groupby('permno').cumcount() + 1

# drop if abs(prc) < 5 | tempage < 12
# In Stata, missing prc values are treated as infinity, so they pass the abs(prc) < 5 test (infinity >= 5)
# We need to explicitly handle missing values: keep them (like Stata) and filter the rest
price_condition = (df['prc'].abs() >= 5) | df['prc'].isna()
df = df[price_condition & (df['tempage'] >= 12)].copy()

# gen FirmAgeMom = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
# Create lagged returns using calendar-based lags (matching Stata behavior)
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5], prefix='l')

# Calculate FirmAgeMom
df['FirmAgeMom'] = ((1 + df['l1_ret']) * 
                    (1 + df['l2_ret']) * 
                    (1 + df['l3_ret']) * 
                    (1 + df['l4_ret']) * 
                    (1 + df['l5_ret'])) - 1

# egen temp = fastxtile(tempage), by(time_avail_m) n(5)  // Find bottom age quintile
df['temp'] = fastxtile(df, 'tempage', by='time_avail_m', n=5)

# replace FirmAgeMom =. if temp > 1 & temp !=.
# Set FirmAgeMom to NaN for firms not in bottom (youngest) quintile
condition = (df['temp'] > 1) & df['temp'].notna()
df.loc[condition, 'FirmAgeMom'] = np.nan

# SAVE
# do "$pathCode/savepredictor" FirmAgeMom
save_predictor(df, 'FirmAgeMom')

print("FirmAgeMom predictor completed")