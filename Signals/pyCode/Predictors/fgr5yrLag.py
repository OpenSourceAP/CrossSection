# ABOUTME: Translates fgr5yrLag.do to create 5-year lagged growth predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/fgr5yrLag.py

# Run from pyCode/ directory
# Inputs: IBES_EPS_Unadj.parquet, m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/fgr5yrLag.csv

import pandas as pd
import numpy as np

# Prep IBES data
ibes = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
ibes = ibes[ibes['fpi'] == '0'].copy()
ibes = ibes.rename(columns={'meanest': 'fgr5yr'})

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'tickerIBES']].copy()
df = df.merge(smt, on=['permno', 'time_avail_m'], how='inner')

# Merge with IBES data
df = df.merge(ibes[['tickerIBES', 'time_avail_m', 'fgr5yr']], on=['tickerIBES', 'time_avail_m'], how='inner')

# Drop rows with missing required variables
required_vars = ['ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp', 'fgr5yr']
df = df.dropna(subset=required_vars)

# Keep only necessary variables for signal construction
df = df[['permno', 'time_avail_m', 'fgr5yr']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Lag 6 months
df['fgr5yrLag'] = df.groupby('permno')['fgr5yr'].shift(6)

# Keep only June observations
df = df[df['time_avail_m'].dt.month == 6].copy()

# Expand to monthly
df_expanded = []
for _, row in df.iterrows():
    for month_offset in range(12):
        new_row = row.copy()
        new_row['time_avail_m'] = row['time_avail_m'] + pd.DateOffset(months=month_offset)
        df_expanded.append(new_row)

df_final = pd.DataFrame(df_expanded)
df_final = df_final.dropna(subset=['fgr5yrLag'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'fgr5yrLag']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/fgr5yrLag.csv')

print("fgr5yrLag predictor saved successfully")