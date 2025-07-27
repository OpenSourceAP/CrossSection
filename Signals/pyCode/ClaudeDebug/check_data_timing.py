# ABOUTME: Check data timing differences between Stata and Python for key problematic observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/check_data_timing.py

import pandas as pd
import numpy as np

print("=== Checking data timing issues ===")

# Load both Stata and Python final outputs
stata_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/Data/Predictors/CitationsRD.csv')
python_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/pyData/Predictors/CitationsRD.csv')

print(f"Stata range: {stata_df['yyyymm'].min()} to {stata_df['yyyymm'].max()}")
print(f"Python range: {python_df['yyyymm'].min()} to {python_df['yyyymm'].max()}")

# Check the pattern - Stata starts earlier
print(f"\nStata earliest observations:")
earliest_stata = stata_df.nsmallest(20, 'yyyymm')
print(earliest_stata)

print(f"\nPython earliest observations:")
earliest_python = python_df.nsmallest(20, 'yyyymm')
print(earliest_python)

# Check why Python starts later - maybe the gvkey filter is dropping early observations
print("\n=== Checking gvkey filter effect ===")

# Recreate pipeline up to gvkey filter to see what gets dropped
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
df = df[df['time_avail_m'] >= '1970-01']
df['year'] = df['time_avail_m'].dt.year

compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
compustat = compustat[compustat['time_avail_m'] >= '1970-01']
df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
df = df.dropna(subset=['gvkey'])

patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
patent = patent[['gvkey', 'year', 'ncitscale']].copy()
df = df.merge(patent, on=['gvkey', 'year'], how='left')

df = df.sort_values(['permno', 'time_avail_m'])
df['temp'] = df.groupby('permno')['ncitscale'].shift(6)
df['temp'] = df['temp'].fillna(0)
df['ncitscale'] = df['temp']
df = df.drop(columns=['temp'])

df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)
df['xrd_lag'] = df['xrd_lag'].fillna(0)

df = df[df['time_avail_m'] >= '1975-01']
df = df[df['time_avail_m'].dt.month == 6]

df = df.sort_values(['permno', 'time_avail_m'])
df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
    lambda x: x.rolling(window=4, min_periods=1).sum()
)
df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
    lambda x: x.rolling(window=4, min_periods=1).sum()
)

df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)

print(f"Before gvkey filter - earliest time_avail_m: {df['time_avail_m'].min()}")
print(f"Number of unique time periods: {df['time_avail_m'].nunique()}")

# Check which time periods have observations before the gvkey filter
early_periods = df[df['time_avail_m'] <= '1985-06-01']['time_avail_m'].value_counts().sort_index()
print(f"\nObservations in early periods (before gvkey filter):")
print(early_periods.head(10))

# Apply gvkey filter and see what gets dropped
print(f"\n=== Applying gvkey filter ===")
df = df.sort_values(['gvkey', 'time_avail_m'])

# Show what gets dropped by the gvkey filter for early periods
early_df = df[df['time_avail_m'] <= '1985-06-01'].copy()
print(f"Before gvkey filter (early periods): {len(early_df)} observations")

df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

early_df_after = df[df['time_avail_m'] <= '1985-06-01'].copy()
print(f"After gvkey filter (early periods): {len(early_df_after)} observations")
print(f"Dropped by gvkey filter: {len(early_df) - len(early_df_after)} observations")

# Check earliest periods after gvkey filter
if len(early_df_after) > 0:
    print(f"Earliest period after gvkey filter: {early_df_after['time_avail_m'].min()}")
    periods_after = early_df_after['time_avail_m'].value_counts().sort_index()
    print(f"Observations in early periods (after gvkey filter):")
    print(periods_after.head(10))

# Let's specifically check permno 10006 and see what happens with the gvkey filter
print(f"\n=== Checking permno 10006 and gvkey filter ===")

# Re-run up to gvkey filter for permno 10006
df_before_gvkey = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df_before_gvkey = df_before_gvkey[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
df_before_gvkey = df_before_gvkey[df_before_gvkey['time_avail_m'] >= '1970-01']
df_before_gvkey['year'] = df_before_gvkey['time_avail_m'].dt.year

compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
compustat = compustat[compustat['time_avail_m'] >= '1970-01']
df_before_gvkey = df_before_gvkey.merge(compustat, on=['permno', 'time_avail_m'], how='left')
df_before_gvkey = df_before_gvkey.dropna(subset=['gvkey'])

patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
patent = patent[['gvkey', 'year', 'ncitscale']].copy()
df_before_gvkey = df_before_gvkey.merge(patent, on=['gvkey', 'year'], how='left')

df_before_gvkey = df_before_gvkey.sort_values(['permno', 'time_avail_m'])
df_before_gvkey['temp'] = df_before_gvkey.groupby('permno')['ncitscale'].shift(6)
df_before_gvkey['temp'] = df_before_gvkey['temp'].fillna(0)
df_before_gvkey['ncitscale'] = df_before_gvkey['temp']
df_before_gvkey = df_before_gvkey.drop(columns=['temp'])

df_before_gvkey['xrd_lag'] = df_before_gvkey.groupby('permno')['xrd'].shift(24)
df_before_gvkey['xrd_lag'] = df_before_gvkey['xrd_lag'].fillna(0)

df_before_gvkey = df_before_gvkey[df_before_gvkey['time_avail_m'] >= '1975-01']
df_before_gvkey = df_before_gvkey[df_before_gvkey['time_avail_m'].dt.month == 6]

target_10006_before = df_before_gvkey[df_before_gvkey['permno'] == 10006].sort_values('time_avail_m')
print(f"Permno 10006 observations before gvkey filter: {len(target_10006_before)}")
if len(target_10006_before) > 0:
    print(f"First observation: {target_10006_before.iloc[0]['time_avail_m']}")
    print(target_10006_before[['permno', 'gvkey', 'time_avail_m']].head())

# Check what happens with gvkey filter for permno 10006's gvkey
if len(target_10006_before) > 0:
    target_gvkey = target_10006_before.iloc[0]['gvkey']
    print(f"\nPermno 10006 has gvkey: {target_gvkey}")
    
    # Check all observations for this gvkey
    gvkey_obs = df_before_gvkey[df_before_gvkey['gvkey'] == target_gvkey].sort_values('time_avail_m')
    print(f"Total observations for gvkey {target_gvkey}: {len(gvkey_obs)}")
    print(f"First 3 observations (should be dropped by gvkey filter):")
    print(gvkey_obs[['permno', 'gvkey', 'time_avail_m']].head(3))
    print(f"Observations that should remain (after dropping first 2):")
    remaining = gvkey_obs.iloc[2:]
    print(remaining[['permno', 'gvkey', 'time_avail_m']].head())
    
    if len(remaining) > 0:
        print(f"First remaining observation: {remaining.iloc[0]['time_avail_m']}")