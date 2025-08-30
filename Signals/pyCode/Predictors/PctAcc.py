# ABOUTME: Percent Operating Accruals predictor from Hafzalla, Lundholm, Van Winkle 2011 (AR), Table 4A
# ABOUTME: Calculates income before extraordinary items minus net cash flow, scaled by absolute income

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet
# Output: ../pyData/Predictors/PctAcc.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'ib', 'oancf', 'dp', 'act', 'che', 'lct', 'txp', 'dlc']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Basic percent accruals calculation
df['PctAcc'] = (df['ib'] - df['oancf']) / np.abs(df['ib'])

# Handle case when ib == 0
df.loc[df['ib'] == 0, 'PctAcc'] = (df['ib'] - df['oancf']) / 0.01

# Calculate 12-month lags for alternative calculation when oancf is missing
df['act_lag12'] = df.groupby('permno')['act'].shift(12)
df['che_lag12'] = df.groupby('permno')['che'].shift(12)
df['lct_lag12'] = df.groupby('permno')['lct'].shift(12)
df['dlc_lag12'] = df.groupby('permno')['dlc'].shift(12)
df['txp_lag12'] = df.groupby('permno')['txp'].shift(12)

# Alternative calculation when oancf is missing
alt_calc = ((df['act'] - df['act_lag12']) - (df['che'] - df['che_lag12']) - 
            ((df['lct'] - df['lct_lag12']) - (df['dlc'] - df['dlc_lag12']) - 
             (df['txp'] - df['txp_lag12']) - df['dp']))

# Use alternative when oancf is missing
missing_oancf = df['oancf'].isna()
df.loc[missing_oancf, 'PctAcc'] = alt_calc / np.abs(df['ib'])

# Handle case when both oancf is missing and ib == 0
missing_oancf_zero_ib = missing_oancf & (df['ib'] == 0)
df.loc[missing_oancf_zero_ib, 'PctAcc'] = alt_calc / 0.01

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'PctAcc']].copy()
df_final = df_final.dropna(subset=['PctAcc'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'PctAcc']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/PctAcc.csv')

print("PctAcc predictor saved successfully")