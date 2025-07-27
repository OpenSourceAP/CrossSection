# ABOUTME: Debug CitationsRD categorization step for permno 10006
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_categories.py

import pandas as pd
import numpy as np

# Recreate the pipeline up to the categorization step
target_permno = 10006
target_date = '1982-06-01'

print(f"=== Debugging categorization for permno {target_permno} ===")

# Load and process data through filtering steps (simplified version)
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

# Create lags
df = df.sort_values(['permno', 'time_avail_m'])
df['temp'] = df.groupby('permno')['ncitscale'].shift(6)
df['temp'] = df['temp'].fillna(0)
df['ncitscale'] = df['temp']
df = df.drop(columns=['temp'])

df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)
df['xrd_lag'] = df['xrd_lag'].fillna(0)

# Filter to 1975+ and June only
df = df[df['time_avail_m'] >= '1975-01']
df = df[df['time_avail_m'].dt.month == 6]

# Create rolling sums
df = df.sort_values(['permno', 'time_avail_m'])
df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
    lambda x: x.rolling(window=4, min_periods=1).sum()
)
df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
    lambda x: x.rolling(window=4, min_periods=1).sum()
)

df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)

# Apply gvkey filter
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

# Apply other filters 
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
df = df[df['ceq'] >= 0]

print(f"Before categorization: {len(df)} total observations")
target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
print(f"Target June 1982 row exists: {len(target_june_1982) > 0}")

if len(target_june_1982) > 0:
    row = target_june_1982.iloc[0]
    print(f"Target row data: permno={row['permno']}, time_avail_m={row['time_avail_m']}")
    print(f"  mve_c={row['mve_c']}, exchcd={row['exchcd']}")
    print(f"  tempCitationsRD={row['tempCitationsRD']}")
    print(f"  sicCRSP={row['sicCRSP']}, ceq={row['ceq']}")

# Now do the categorization step by step
print("\n=== Size categorization ===")

# Size categories 
def calculate_size_breakpoints(group):
    nyse_stocks = group[group['exchcd'] == 1]
    if len(nyse_stocks) == 0:
        return group
    
    median_mve = nyse_stocks['mve_c'].median()
    group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
    return group

df = df.groupby('time_avail_m').apply(calculate_size_breakpoints).reset_index(drop=True)

target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
if len(target_june_1982) > 0:
    row = target_june_1982.iloc[0]
    print(f"Size category: {row['sizecat']}")
    
    # Show NYSE median for that period
    june_1982_data = df[df['time_avail_m'] == target_date]
    nyse_june_1982 = june_1982_data[june_1982_data['exchcd'] == 1]
    if len(nyse_june_1982) > 0:
        median_mve = nyse_june_1982['mve_c'].median()
        print(f"NYSE median mve_c in June 1982: {median_mve}")
        print(f"Target mve_c: {row['mve_c']} ({'small' if row['mve_c'] <= median_mve else 'large'})")

print("\n=== Main categorization (terciles) ===")

# Initialize maincat
df['maincat'] = np.nan

# Assign maincat=1 to observations with missing tempCitationsRD
df.loc[df['tempCitationsRD'].isna(), 'maincat'] = 1.0

# For observations with valid tempCitationsRD, create terciles by time period
def fast_terciles(series):
    try:
        return pd.qcut(series, q=3, labels=False, duplicates='drop') + 1
    except (ValueError, TypeError):
        ranks = series.rank(method='first')
        n = len(ranks)
        result = pd.Series(index=series.index, dtype='float64')
        result.loc[ranks <= n/3] = 1.0
        result.loc[(ranks > n/3) & (ranks <= 2*n/3)] = 2.0
        result.loc[ranks > 2*n/3] = 3.0
        return result

valid_mask = df['tempCitationsRD'].notna()
if valid_mask.sum() > 0:
    df.loc[valid_mask, 'maincat'] = df[valid_mask].groupby('time_avail_m')['tempCitationsRD'].transform(fast_terciles)

target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
if len(target_june_1982) > 0:
    row = target_june_1982.iloc[0]
    print(f"Main category: {row['maincat']}")
    
    # Show tercile breakpoints for that period
    june_1982_data = df[df['time_avail_m'] == target_date]
    valid_june_1982 = june_1982_data[june_1982_data['tempCitationsRD'].notna()]
    if len(valid_june_1982) > 0:
        terciles = valid_june_1982['tempCitationsRD'].quantile([0.333, 0.667])
        print(f"Tercile breakpoints in June 1982: {terciles.to_dict()}")
        print(f"Target tempCitationsRD: {row['tempCitationsRD']}")

print("\n=== Creating CitationsRD signal ===")

# Create CitationsRD signal
df['CitationsRD'] = np.nan
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0

target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
if len(target_june_1982) > 0:
    row = target_june_1982.iloc[0]
    print(f"Final CitationsRD value: {row['CitationsRD']}")
    print(f"Condition check: sizecat={row['sizecat']}, maincat={row['maincat']}")
    
    if pd.isna(row['CitationsRD']):
        print("CitationsRD is NaN - this observation will be dropped!")
    else:
        print("CitationsRD has a value - this observation should be kept")