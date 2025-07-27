# ABOUTME: Translates MeanRankRevGrowth.do to create mean rank revenue growth predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MeanRankRevGrowth.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet
# Output: ../pyData/Predictors/MeanRankRevGrowth.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'revt']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Calculate 12-month revenue growth
df['revt_lag12'] = df.groupby('permno')['revt'].shift(12)
df['temp'] = np.log(df['revt']) - np.log(df['revt_lag12'])

# Create monthly rankings (descending order - highest growth gets rank 1)
df = df.sort_values(['time_avail_m', 'temp'], ascending=[True, False])
df['tempRank'] = df.groupby('time_avail_m').cumcount() + 1
df.loc[df['temp'].isna(), 'tempRank'] = np.nan

# Sort back for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate lagged ranks
df['tempRank_lag12'] = df.groupby('permno')['tempRank'].shift(12)
df['tempRank_lag24'] = df.groupby('permno')['tempRank'].shift(24)
df['tempRank_lag36'] = df.groupby('permno')['tempRank'].shift(36)
df['tempRank_lag48'] = df.groupby('permno')['tempRank'].shift(48)
df['tempRank_lag60'] = df.groupby('permno')['tempRank'].shift(60)

# Calculate weighted average rank
df['MeanRankRevGrowth'] = ((5 * df['tempRank_lag12'] + 
                           4 * df['tempRank_lag24'] + 
                           3 * df['tempRank_lag36'] + 
                           2 * df['tempRank_lag48'] + 
                           df['tempRank_lag60']) / 15)

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'MeanRankRevGrowth']].copy()
df_final = df_final.dropna(subset=['MeanRankRevGrowth'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'MeanRankRevGrowth']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/MeanRankRevGrowth.csv')

print("MeanRankRevGrowth predictor saved successfully")