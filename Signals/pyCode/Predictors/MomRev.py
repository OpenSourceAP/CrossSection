# ABOUTME: Translates MomRev predictor from Stata to Python
# ABOUTME: Creates momentum and long-term reversal signal based on 6m and 36m momentum

# Translation of Code/Predictors/MomRev.do
# Run from pyCode/ directory: python3 Predictors/MomRev.py
# Inputs: pyData/Intermediate/SignalMasterTable.parquet
# Outputs: pyData/Predictors/MomRev.csv

import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  MomRev.py")
print("Creating momentum and long-term reversal signal based on 6m and 36m momentum")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")
# use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'ret']].copy()
print(f"Loaded: {len(df):,} observations")

# Sort data for proper lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
print("🧮 Computing 6m and 36m momentum signals...")
# replace ret = 0 if mi(ret)
df.loc[df['ret'].isna(), 'ret'] = 0

# Create lag variables using stata_multi_lag for calendar validation
# Mom6m uses lags 1-5
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5])

df['Mom6m'] = ((1 + df['ret_lag1']) * (1 + df['ret_lag2']) * (1 + df['ret_lag3']) * 
               (1 + df['ret_lag4']) * (1 + df['ret_lag5'])) - 1

# Mom36m uses lags 13-36
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', list(range(13, 37)))

# Calculate Mom36m using lag columns with new naming convention
mom36m_product = 1
for i in range(13, 37):
    mom36m_product *= (1 + df[f'ret_lag{i}'])
df['Mom36m'] = mom36m_product - 1


# Handle infinite values before quintile calculation (critical for pd.qcut)
df['Mom6m_clean'] = df['Mom6m'].replace([np.inf, -np.inf], np.nan)
df['Mom36m_clean'] = df['Mom36m'].replace([np.inf, -np.inf], np.nan)

# egen tempMom6  = fastxtile(Mom6m), by(time_avail_m) n(5)
df['tempMom6'] = fastxtile(df, 'Mom6m_clean', by='time_avail_m', n=5)


# egen tempMom36 = fastxtile(Mom36m), by(time_avail_m) n(5)
df['tempMom36'] = fastxtile(df, 'Mom36m_clean', by='time_avail_m', n=5)


# gen MomRev = 1 if tempMom6 == 5 & tempMom36 == 1
df['MomRev'] = np.nan
df.loc[(df['tempMom6'] == 5) & (df['tempMom36'] == 1), 'MomRev'] = 1

# replace MomRev = 0 if tempMom6 == 1 & tempMom36 == 5
df.loc[(df['tempMom6'] == 1) & (df['tempMom36'] == 5), 'MomRev'] = 0


# label var MomRev "Momentum and LT Reversal"
# (Labels are comments in Python)

# SAVE
print("💾 Saving MomRev predictor...")
save_predictor(df, 'MomRev')
print("✅ MomRev.csv saved successfully")

print("=" * 80)
print("✅ MomRev.py Complete")
print("Momentum and long-term reversal signal generated successfully")
print("=" * 80)