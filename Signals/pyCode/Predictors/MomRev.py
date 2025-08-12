# ABOUTME: Translates MomRev predictor from Stata to Python
# ABOUTME: Creates momentum and long-term reversal signal based on 6m and 36m momentum

# Translation of Code/Predictors/MomRev.do
# Run from pyCode/ directory: python3 Predictors/MomRev.py
# Inputs: pyData/Intermediate/SignalMasterTable.parquet
# Outputs: pyData/Predictors/MomRev.csv

import pandas as pd
import numpy as np
import os
from utils.stata_fastxtile import fastxtile

# DATA LOAD
# use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'ret']].copy()

# Sort data for proper lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# replace ret = 0 if mi(ret)
df.loc[df['ret'].isna(), 'ret'] = 0

# Create lag variables for momentum calculations
# gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
for i in range(1, 6):
    df[f'l{i}_ret'] = df.groupby('permno')['ret'].shift(i)

df['Mom6m'] = ((1 + df['l1_ret']) * (1 + df['l2_ret']) * (1 + df['l3_ret']) * 
               (1 + df['l4_ret']) * (1 + df['l5_ret'])) - 1

# gen Mom36m = (   (1+l13.ret)*(1+l14.ret)*(1+l15.ret)*(1+l16.ret)*(1+l17.ret)*(1+l18.ret)   * ///
#     (1+l19.ret)*(1+l20.ret)*(1+l21.ret)*(1+l22.ret)*(1+l23.ret)*(1+l24.ret)* ///
#     (1+l25.ret)*(1+l26.ret)*(1+l27.ret)*(1+l28.ret)*(1+l29.ret)*(1+l30.ret)     * ///
#     (1+l31.ret)*(1+l32.ret)*(1+l33.ret)*(1+l34.ret)*(1+l35.ret)*(1+l36.ret)  ) - 1
for i in range(13, 37):
    df[f'l{i}_ret'] = df.groupby('permno')['ret'].shift(i)

mom36m_product = 1
for i in range(13, 37):
    mom36m_product *= (1 + df[f'l{i}_ret'])
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
# do "$pathCode/savepredictor" MomRev
# Keep only required columns and save
output_df = df[['permno', 'time_avail_m', 'MomRev']].copy()

# Convert time_avail_m to YYYYMM format
output_df['yyyymm'] = output_df['time_avail_m'].dt.year * 100 + output_df['time_avail_m'].dt.month
output_df = output_df[['permno', 'yyyymm', 'MomRev']].copy()

# Remove rows where MomRev is missing
output_df = output_df[output_df['MomRev'].notna()]

# Create output directory if needed
os.makedirs('../pyData/Predictors', exist_ok=True)

# Save to CSV
output_df.to_csv('../pyData/Predictors/MomRev.csv', index=False)

print(f"MomRev predictor saved to pyData/Predictors/MomRev.csv")
print(f"Output shape: {output_df.shape}")
print("Sample output:")
print(output_df.head())