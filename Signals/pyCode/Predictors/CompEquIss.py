# ABOUTME: CompEquIss predictor - calculates composite equity issuance
# ABOUTME: Run: python3 pyCode/Predictors/CompEquIss.py

"""
Inputs: SignalMasterTable.parquet (permno, time_avail_m, ret, mve_c)
Outputs: CompEquIss.csv (permno, yyyymm, CompEquIss)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor


print("Starting CompEquIss predictor...")

# DATA LOAD
# Stata: use permno time_avail_m ret mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                    columns=['permno', 'time_avail_m', 'ret', 'mve_c'])

print(f"Loaded {len(df):,} SignalMasterTable observations")

# SIGNAL CONSTRUCTION
print("Constructing CompEquIss signal...")

# Sort data by permno and time for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Stata: bys permno (time_avail): gen tempIdx = 1 if _n == 1
# Stata: bys permno (time_avail): replace tempIdx = (1 + ret)*l.tempIdx if _n > 1
# This creates a cumulative return index starting at 1 for each permno
df['tempIdx'] = df.groupby('permno')['ret'].transform(lambda x: (1 + x).cumprod())

# Create 60-month lags using stata_multi_lag for calendar validation
# Stata: gen tempBH = (tempIdx - l60.tempIdx)/l60.tempIdx
print("Creating 60-month lags with calendar validation...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'tempIdx', [60])
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'mve_c', [60])

# Calculate buy-and-hold returns over 60 months
df['tempBH'] = (df['tempIdx'] - df['tempIdx_lag60']) / df['tempIdx_lag60']

# Stata: gen CompEquIss = log(mve_c/l60.mve_c) - tempBH
df['CompEquIss'] = np.log(df['mve_c'] / df['mve_c_lag60']) - df['tempBH']

print(f"Generated CompEquIss values for {df['CompEquIss'].notna().sum():,} observations")
    
# SAVE
print("Saving predictor...")
save_predictor(df, 'CompEquIss')

print("CompEquIss predictor completed successfully!")
