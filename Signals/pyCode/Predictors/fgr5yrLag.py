# ABOUTME: Translates fgr5yrLag.do to create 5-year lagged growth predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/fgr5yrLag.py

# Run from pyCode/ directory
# Inputs: IBES_EPS_Unadj.parquet, m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/fgr5yrLag.csv

import pandas as pd
import numpy as np

# Prep IBES data
print("Loading IBES data...")
ibes = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
print(f"IBES loaded: {len(ibes):,} rows")
print("Filtering IBES...")
ibes = ibes[ibes['fpi'] == '0'].copy()
print("Renaming IBES columns...")
ibes = ibes.rename(columns={'meanest': 'fgr5yr'})
print(f"IBES ready: {len(ibes):,} rows")

# DATA LOAD
print("Loading Compustat data...")
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp']].copy()
print(f"Compustat loaded: {len(df):,} rows")

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])
print(f"After dedup: {len(df):,} rows")

# Merge with SignalMasterTable
print("Merging with SignalMasterTable...")
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'tickerIBES']].copy()
df = df.merge(smt, on=['permno', 'time_avail_m'], how='inner')
print(f"After SMT merge: {len(df):,} rows")

# Merge with IBES data - optimized filtering first
print("Optimizing IBES merge...")
# Pre-filter IBES to only relevant tickers and dates
relevant_tickers = set(df['tickerIBES'].unique())
relevant_dates = set(df['time_avail_m'].unique())

ibes_filtered = ibes[
    (ibes['tickerIBES'].isin(relevant_tickers)) & 
    (ibes['time_avail_m'].isin(relevant_dates))
].copy()

print(f"IBES filtered from {len(ibes):,} to {len(ibes_filtered):,} rows")

# Now do the merge
df = df.merge(ibes_filtered[['tickerIBES', 'time_avail_m', 'fgr5yr']], 
              on=['tickerIBES', 'time_avail_m'], how='inner')
print(f"After IBES merge: {len(df):,} rows")

# Drop rows with missing required variables
print("Filtering required variables...")
required_vars = ['ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp', 'fgr5yr']
df = df.dropna(subset=required_vars)
print(f"After dropna: {len(df):,} rows")

# Keep only necessary variables for signal construction
df = df[['permno', 'time_avail_m', 'fgr5yr']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION - Calendar-based lag matching Stata's l6.
print("Calculating 6-month calendar lags...")
# Create lag lookup table for calendar-based 6-month lag
df['lag6_date'] = df['time_avail_m'] - pd.DateOffset(months=6)

# Create lookup dictionary for efficient merging
lag_lookup = df[['permno', 'time_avail_m', 'fgr5yr']].rename(columns={
    'time_avail_m': 'lag6_date',
    'fgr5yr': 'fgr5yrLag'
})

# Merge to get calendar-based lagged values
df = df.merge(lag_lookup, on=['permno', 'lag6_date'], how='left')
df = df.drop(columns=['lag6_date'])

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