# ABOUTME: Translates OScore_q.do to create quarterly O-Score bankruptcy predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/OScore_q.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_QCompustat.parquet, GNPdefl.parquet
# Output: ../pyData/Predictors/OScore_q.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'sicCRSP', 'prc']].copy()
df = df[~df['gvkey'].isna()].copy()

# Merge with quarterly Compustat
qcomp = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet')
qcomp = qcomp[['gvkey', 'time_avail_m', 'foptyq', 'atq', 'ltq', 'actq', 'lctq', 'ibq', 'oancfyq']].copy()
df = df.merge(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

# Merge with GNP deflator
gnp = pd.read_parquet('../pyData/Intermediate/GNPdefl.parquet')
df = df.merge(gnp, on='time_avail_m', how='inner')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing foptyq with oancfyq
df['foptyq'] = df['foptyq'].fillna(df['oancfyq'])

# Calculate 12-month lag of ibq
df['ibq_lag12'] = df.groupby('permno')['ibq'].shift(12)

# O-Score quarterly calculation
df['OScore_q'] = (-1.32 - 0.407 * np.log(df['atq'] / df['gnpdefl']) + 
                  6.03 * (df['ltq'] / df['atq']) - 
                  1.43 * ((df['actq'] - df['lctq']) / df['atq']) + 
                  0.076 * (df['lctq'] / df['actq']) - 
                  1.72 * (df['ltq'] > df['atq']).astype(int) - 
                  2.37 * (df['ibq'] / df['atq']) - 
                  1.83 * (df['foptyq'] / df['ltq']) + 
                  0.285 * ((df['ibq'] + df['ibq_lag12']) < 0).astype(int) - 
                  0.521 * ((df['ibq'] - df['ibq_lag12']) / (np.abs(df['ibq']) + np.abs(df['ibq_lag12']))))

# Apply industry filters using sicCRSP
df.loc[((df['sicCRSP'] > 3999) & (df['sicCRSP'] < 5000)) | (df['sicCRSP'] > 5999), 'OScore_q'] = np.nan

# Create deciles and form long-short following Table 5
df['tempsort'] = df.groupby('time_avail_m')['OScore_q'].transform(
    lambda x: pd.qcut(x, q=10, labels=False, duplicates='drop') + 1)

# Reset OScore_q and create binary signal
df['OScore_q_final'] = np.nan
df.loc[df['tempsort'] == 10, 'OScore_q_final'] = 1
df.loc[(df['tempsort'] >= 1) & (df['tempsort'] <= 7), 'OScore_q_final'] = 0

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'OScore_q_final']].copy()
df_final = df_final.rename(columns={'OScore_q_final': 'OScore_q'})
df_final = df_final.dropna(subset=['OScore_q'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'OScore_q']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/OScore_q.csv')

print("OScore_q predictor saved successfully")