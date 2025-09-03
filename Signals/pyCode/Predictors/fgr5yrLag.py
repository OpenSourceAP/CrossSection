# ABOUTME: Long-term EPS forecast following La Porta 1996, Table 3 E{g}
# ABOUTME: calculates 6-month lagged long-term earnings growth forecasts from IBES with June-only observations
"""
Usage:
    python3 Predictors/fgr5yrLag.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES long-term EPS forecasts with columns [tickerIBES, time_avail_m, meanest, fpi]
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, ceq, ib, txdi, dv, sale, ni, dp]
    - SignalMasterTable.parquet: Monthly master table with tickerIBES mapping

Outputs:
    - fgr5yrLag.csv: CSV file with columns [permno, yyyymm, fgr5yrLag]
    - fgr5yrLag = 6-month lagged long-term growth forecast, June observations forward-filled for 12 months
"""

import pandas as pd
import numpy as np

# Load long-term growth forecasts from IBES
print("Loading IBES data...")
ibes = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
print(f"IBES loaded: {len(ibes):,} rows")
print("Filtering IBES...")
ibes = ibes[ibes['fpi'] == '0'].copy()
print("Renaming IBES columns...")
ibes = ibes.rename(columns={'meanest': 'fgr5yr'})
print(f"IBES ready: {len(ibes):,} rows")

# Load Compustat accounting fundamentals
print("Loading Compustat data...")
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp']].copy()
print(f"Compustat loaded: {len(df):,} rows")

# Remove duplicate firm-month observations
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])
print(f"After dedup: {len(df):,} rows")

# Add IBES ticker identifiers from master table
print("Merging with SignalMasterTable...")
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'tickerIBES']].copy()
df = df.merge(smt, on=['permno', 'time_avail_m'], how='inner')
print(f"After SMT merge: {len(df):,} rows")

# Optimize IBES merge by pre-filtering to relevant data
print("Optimizing IBES merge...")
# Filter IBES to only firms and dates in our sample
relevant_tickers = set(df['tickerIBES'].unique())
relevant_dates = set(df['time_avail_m'].unique())

ibes_filtered = ibes[
    (ibes['tickerIBES'].isin(relevant_tickers)) & 
    (ibes['time_avail_m'].isin(relevant_dates))
].copy()

print(f"IBES filtered from {len(ibes):,} to {len(ibes_filtered):,} rows")

# Merge filtered IBES long-term forecasts
df = df.merge(ibes_filtered[['tickerIBES', 'time_avail_m', 'fgr5yr']], 
              on=['tickerIBES', 'time_avail_m'], how='inner')
print(f"After IBES merge: {len(df):,} rows")

# Apply data completeness screens
print("Filtering required variables...")
required_vars = ['ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp', 'fgr5yr']
df = df.dropna(subset=required_vars)
print(f"After dropna: {len(df):,} rows")

# Retain variables needed for forecast lag calculation
df = df[['permno', 'time_avail_m', 'fgr5yr']].copy()

# Sort data by firm and time for lag calculations
df = df.sort_values(['permno', 'time_avail_m'])

# Apply 6-month calendar-based lag to long-term forecasts
print("Calculating 6-month calendar lags...")
# Generate 6-month lagged date for each observation
df['lag6_date'] = df['time_avail_m'] - pd.DateOffset(months=6)

# Prepare lookup table for lagged forecast values
lag_lookup = df[['permno', 'time_avail_m', 'fgr5yr']].rename(columns={
    'time_avail_m': 'lag6_date',
    'fgr5yr': 'fgr5yrLag'
})

# Add lagged forecast values using calendar-based matching
df = df.merge(lag_lookup, on=['permno', 'lag6_date'], how='left')
df = df.drop(columns=['lag6_date'])

# Restrict to June observations per original methodology
df = df[df['time_avail_m'].dt.month == 6].copy()

# Expand June signal to 12 monthly observations
df_expanded = []
for _, row in df.iterrows():
    for month_offset in range(12):
        new_row = row.copy()
        new_row['time_avail_m'] = row['time_avail_m'] + pd.DateOffset(months=month_offset)
        df_expanded.append(new_row)

df_final = pd.DataFrame(df_expanded)
df_final = df_final.dropna(subset=['fgr5yrLag'])

# Convert date to YYYYMM integer format
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Ensure integer data types
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Format final output columns
df_final = df_final[['permno', 'yyyymm', 'fgr5yrLag']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/fgr5yrLag.csv')

print("fgr5yrLag predictor saved successfully")