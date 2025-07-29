# ABOUTME: Translates OScore.do to create O-Score bankruptcy predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/OScore.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet, GNPdefl.parquet
# Output: ../pyData/Predictors/OScore.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'fopt', 'at', 'lt', 'act', 'lct', 'ib', 'oancf', 'sic']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'prc']].copy()
df = df.merge(smt, on=['permno', 'time_avail_m'], how='inner')

# Merge with GNP deflator
gnp = pd.read_parquet('../pyData/Intermediate/GNPdefl.parquet')
df = df.merge(gnp, on='time_avail_m', how='inner')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing fopt with oancf
df['fopt'] = df['fopt'].fillna(df['oancf'])

# Calculate 12-month lag of ib using calendar-based approach (like Stata l12.)
df['time_avail_m_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
df_lag = df[['permno', 'time_avail_m', 'ib']].copy()
df_lag = df_lag.rename(columns={'time_avail_m': 'time_avail_m_lag12', 'ib': 'ib_lag12'})
df = df.merge(df_lag, on=['permno', 'time_avail_m_lag12'], how='left')
df = df.drop('time_avail_m_lag12', axis=1)

# O-Score calculation with proper handling of infinite values
# Handle division by zero and log of negative values like Stata
def safe_divide(a, b):
    return np.where((b == 0) | b.isna(), np.nan, a / b)

def safe_log(x):
    return np.where((x <= 0) | x.isna(), np.nan, np.log(x))

df['OScore'] = (-1.32 - 0.407 * safe_log(df['at'] / df['gnpdefl']) + 
                6.03 * safe_divide(df['lt'], df['at']) - 
                1.43 * safe_divide((df['act'] - df['lct']), df['at']) + 
                0.076 * safe_divide(df['lct'], df['act']) - 
                1.72 * (df['lt'] > df['at']).astype(int) - 
                2.37 * safe_divide(df['ib'], df['at']) - 
                1.83 * safe_divide(df['fopt'], df['lt']) + 
                0.285 * ((df['ib'] + df['ib_lag12']) < 0).astype(int) - 
                0.521 * safe_divide((df['ib'] - df['ib_lag12']), (np.abs(df['ib']) + np.abs(df['ib_lag12']))))

# Convert sic to numeric and apply industry filters
df['sic'] = pd.to_numeric(df['sic'], errors='coerce')
df.loc[((df['sic'] > 3999) & (df['sic'] < 5000)) | (df['sic'] > 5999), 'OScore'] = np.nan

# Create deciles and form long-short following Table 5
def safe_qcut(x):
    try:
        if len(x.dropna()) < 10:  # Need at least 10 observations for deciles
            return pd.Series(np.nan, index=x.index)
        return pd.qcut(x, q=10, labels=False, duplicates='drop') + 1
    except:
        return pd.Series(np.nan, index=x.index)

df['tempsort'] = df.groupby('time_avail_m')['OScore'].transform(safe_qcut)

# Reset OScore and create binary signal
df['OScore'] = np.nan
df.loc[df['tempsort'] == 10, 'OScore'] = 1
df.loc[(df['tempsort'] >= 1) & (df['tempsort'] <= 7), 'OScore'] = 0

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'OScore']].copy()
df_final = df_final.dropna(subset=['OScore'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'OScore']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/OScore.csv')

print("OScore predictor saved successfully")