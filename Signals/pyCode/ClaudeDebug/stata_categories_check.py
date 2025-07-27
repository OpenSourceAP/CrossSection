# ABOUTME: Check how Stata categorizes permno 10006 vs Python
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/stata_categories_check.py

import pandas as pd
import numpy as np

# Load the actual Stata output to see what it shows for similar observations
print("=== Checking Stata vs Python categorization patterns ===")

stata_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/Data/Predictors/CitationsRD.csv')
print(f"Stata data shape: {stata_df.shape}")
print(f"Stata CitationsRD value counts:")
print(stata_df['CitationsRD'].value_counts())

# Check some observations around 1982-1983 timeframe
stata_1982_1983 = stata_df[(stata_df['yyyymm'] >= 198206) & (stata_df['yyyymm'] <= 198306)]
print(f"\nStata observations June 1982 - June 1983: {len(stata_1982_1983)}")
print(f"CitationsRD distribution:")
print(stata_1982_1983['CitationsRD'].value_counts())

# Let's look at the permno distribution around this time
print(f"\nSample of Stata data June 1982 - June 1983:")
sample_data = stata_1982_1983.head(20)
print(sample_data)

# Check if there are any permno 10006 observations in Stata
stata_10006 = stata_df[stata_df['permno'] == 10006]
print(f"\nStata permno 10006 observations: {len(stata_10006)}")
if len(stata_10006) > 0:
    print(stata_10006)

# Let's also check what the earliest observations are in Stata
print(f"\nEarliest Stata observations:")
print(stata_df.head(20))

# Let's check the size distribution in our Python processing to see if there's an issue
print("\n=== Checking Python size categories for June 1982 ===")

# Recreate the Python pipeline to get size categories
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

df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
df = df[df['ceq'] >= 0]

# Check June 1982 specifically
june_1982 = df[df['time_avail_m'] == '1982-06-01']
print(f"Python June 1982 observations: {len(june_1982)}")

# Size categorization
def calculate_size_breakpoints(group):
    nyse_stocks = group[group['exchcd'] == 1]
    if len(nyse_stocks) == 0:
        return group
    
    median_mve = nyse_stocks['mve_c'].median()
    group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
    return group

df = df.groupby('time_avail_m').apply(calculate_size_breakpoints).reset_index(drop=True)

june_1982 = df[df['time_avail_m'] == '1982-06-01']
print(f"June 1982 size category distribution:")
print(june_1982['sizecat'].value_counts())

# Check NYSE stocks specifically
nyse_june_1982 = june_1982[june_1982['exchcd'] == 1]
print(f"NYSE stocks in June 1982: {len(nyse_june_1982)}")
if len(nyse_june_1982) > 0:
    print(f"NYSE median mve_c: {nyse_june_1982['mve_c'].median()}")
    print(f"NYSE mve_c range: {nyse_june_1982['mve_c'].min()} to {nyse_june_1982['mve_c'].max()}")

# Check if permno 10006 appears and its categorization
target_10006 = june_1982[june_1982['permno'] == 10006]
if len(target_10006) > 0:
    print(f"\nPermno 10006 in June 1982:")
    print(target_10006[['permno', 'mve_c', 'exchcd', 'sizecat', 'tempCitationsRD']].iloc[0])
else:
    print(f"\nPermno 10006 not found in June 1982 Python data!")