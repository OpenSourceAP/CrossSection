# ABOUTME: Creates sales forecast error predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/sfe.py

# Run from pyCode/ directory
# Inputs: IBES_EPS_Unadj.parquet, SignalMasterTable.parquet, m_aCompustat.parquet
# Output: ../pyData/Predictors/sfe.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_fastxtile import fastxtile

# Prep IBES data
ibes = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
ibes = ibes[ibes['fpi'] == '1'].copy()
ibes = ibes[pd.to_datetime(ibes['statpers']).dt.month == 3].copy()  # Use March forecasts
ibes = ibes[(~ibes['fpedats'].isna()) & (ibes['fpedats'] > ibes['statpers'] + pd.Timedelta(days=90))].copy()

# For merge with dec stock price
ibes['prc_time'] = ibes['time_avail_m'] - pd.DateOffset(months=3)

# Merge with CRSP/Comp
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'tickerIBES', 'prc', 'mve_c']].copy()
smt = smt.rename(columns={'time_avail_m': 'prc_time'})

df = smt.merge(ibes, on=['tickerIBES', 'prc_time'], how='inner')

# Merge with Compustat for datadate
comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'datadate']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# Only December fiscal year ends
df = df[pd.to_datetime(df['datadate']).dt.month == 12].copy()

# Lower analyst coverage only
df['tempcoverage'] = fastxtile(df, 'numest', by='time_avail_m', n=2)
df = df[df['tempcoverage'] == 1].copy()

# SIGNAL CONSTRUCTION
df['sfe'] = df['medest'] / np.abs(df['prc'])
df = df[['permno', 'time_avail_m', 'sfe']].copy()

# Hold for one year
df_expanded = []
for _, row in df.iterrows():
    for month_offset in range(12):
        new_row = row.copy()
        new_row['time_avail_m'] = row['time_avail_m'] + pd.DateOffset(months=month_offset)
        df_expanded.append(new_row)

df_final = pd.DataFrame(df_expanded)
df_final = df_final.dropna(subset=['sfe'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'sfe']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/sfe.csv')

print("sfe predictor saved successfully")