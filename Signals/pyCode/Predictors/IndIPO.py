# ABOUTME: Translates IndIPO.do to create industry IPO activity predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IndIPO.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, IPODates.parquet
# Output: ../pyData/Predictors/IndIPO.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m']].copy()

# Merge with IPO dates
ipo = pd.read_parquet('../pyData/Intermediate/IPODates.parquet')
df = df.merge(ipo, on='permno', how='left')

# SIGNAL CONSTRUCTION
# Calculate months since IPO
df['months_since_ipo'] = (df['time_avail_m'].dt.year - df['IPOdate'].dt.year) * 12 + \
                        (df['time_avail_m'].dt.month - df['IPOdate'].dt.month)

# IPO indicator: between 3 months and 3 years (36 months) after IPO
df['IndIPO'] = ((df['months_since_ipo'] <= 36) & (df['months_since_ipo'] >= 3)).astype(int)

# Set to 0 if IPOdate is missing
df.loc[df['IPOdate'].isna(), 'IndIPO'] = 0

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'IndIPO']].copy()

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'IndIPO']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/IndIPO.csv')

print("IndIPO predictor saved successfully")