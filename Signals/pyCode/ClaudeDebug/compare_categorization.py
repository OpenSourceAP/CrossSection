# ABOUTME: Compare Stata vs Python categorization for June 1982 to find discrepancy
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/compare_categorization.py

import pandas as pd
import numpy as np

print("=== Comparing Stata vs Python categorization for June 1982 ===")

# Recreate the Python pipeline up to categorization
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

# Focus on June 1982
june_1982 = df[df['time_avail_m'] == '1982-06-01'].copy()
print(f"June 1982 total observations: {len(june_1982)}")

# Check permno 10006
target_10006 = june_1982[june_1982['permno'] == 10006]
if len(target_10006) > 0:
    print(f"\nPermno 10006 in June 1982:")
    row = target_10006.iloc[0]
    print(f"  mve_c: {row['mve_c']}")
    print(f"  exchcd: {row['exchcd']}")
    print(f"  tempCitationsRD: {row['tempCitationsRD']}")

# Do size categorization exactly as in Python code
def calculate_size_breakpoints(group):
    nyse_stocks = group[group['exchcd'] == 1]
    if len(nyse_stocks) == 0:
        return group
    
    median_mve = nyse_stocks['mve_c'].median()
    group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
    return group

june_1982 = calculate_size_breakpoints(june_1982)

# Check NYSE median and permno 10006's classification
nyse_june_1982 = june_1982[june_1982['exchcd'] == 1]
nyse_median = nyse_june_1982['mve_c'].median()
print(f"\nJune 1982 NYSE median mve_c: {nyse_median}")
print(f"NYSE stocks count: {len(nyse_june_1982)}")

target_10006 = june_1982[june_1982['permno'] == 10006]
if len(target_10006) > 0:
    row = target_10006.iloc[0]
    print(f"Permno 10006 mve_c: {row['mve_c']} ({'small' if row['mve_c'] <= nyse_median else 'large'})")
    print(f"Permno 10006 sizecat: {row['sizecat']}")

# Check the distribution of size categories
print(f"\nSize category distribution in June 1982:")
print(june_1982['sizecat'].value_counts().sort_index())

# Do tercile categorization
june_1982['maincat'] = np.nan
june_1982.loc[june_1982['tempCitationsRD'].isna(), 'maincat'] = 1.0

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

valid_mask = june_1982['tempCitationsRD'].notna()
valid_june_1982 = june_1982[valid_mask]

print(f"\nValid tempCitationsRD observations in June 1982: {len(valid_june_1982)}")
if len(valid_june_1982) > 0:
    terciles = valid_june_1982['tempCitationsRD'].quantile([0.333, 0.667])
    print(f"Tercile breakpoints: {terciles.to_dict()}")
    
    # Apply terciles
    june_1982.loc[valid_mask, 'maincat'] = fast_terciles(valid_june_1982['tempCitationsRD'])
    
    # Check maincat distribution
    print(f"Main category distribution:")
    print(june_1982['maincat'].value_counts().sort_index())
    
    # Check permno 10006's maincat
    target_10006 = june_1982[june_1982['permno'] == 10006]
    if len(target_10006) > 0:
        row = target_10006.iloc[0]
        print(f"\nPermno 10006 tempCitationsRD: {row['tempCitationsRD']}")
        print(f"Permno 10006 maincat: {row['maincat']}")

# Create final CitationsRD signal
june_1982['CitationsRD'] = np.nan
june_1982.loc[(june_1982['sizecat'] == 1) & (june_1982['maincat'] == 3), 'CitationsRD'] = 1
june_1982.loc[(june_1982['sizecat'] == 1) & (june_1982['maincat'] == 1), 'CitationsRD'] = 0

print(f"\nCitationsRD signal distribution in June 1982:")
print(june_1982['CitationsRD'].value_counts(dropna=False).sort_index())

target_10006 = june_1982[june_1982['permno'] == 10006]
if len(target_10006) > 0:
    row = target_10006.iloc[0]
    print(f"\nPermno 10006 final classification:")
    print(f"  sizecat: {row['sizecat']} ({'small' if row['sizecat'] == 1 else 'large'})")
    print(f"  maincat: {row['maincat']} ({'low' if row['maincat'] == 1 else 'mid' if row['maincat'] == 2 else 'high'})")
    print(f"  CitationsRD: {row['CitationsRD']}")

# Let's check some stats to understand if there might be a different interpretation
print(f"\n=== Additional debugging ===")

# Check if there are any edge cases or ties in the data
valid_citations = june_1982[june_1982['tempCitationsRD'].notna()]['tempCitationsRD']
print(f"tempCitationsRD stats for June 1982:")
print(valid_citations.describe())

# Check for duplicates or ties that might affect ranking
print(f"\nAny duplicates in tempCitationsRD? {valid_citations.duplicated().any()}")
if valid_citations.duplicated().any():
    print(f"Number of duplicates: {valid_citations.duplicated().sum()}")

# Check what percentile permno 10006 is at
if len(target_10006) > 0:
    target_value = target_10006.iloc[0]['tempCitationsRD']
    percentile = (valid_citations < target_value).mean() * 100
    print(f"Permno 10006 tempCitationsRD ({target_value}) is at {percentile:.1f}th percentile")

# What if we tried alternative tercile methods?
print(f"\n=== Alternative tercile methods ===")

# Method 1: Simple quantile-based
q33, q67 = valid_citations.quantile([0.333, 0.667])
print(f"33rd percentile: {q33}, 67th percentile: {q67}")

alt_maincat = np.where(valid_citations <= q33, 1, 
                      np.where(valid_citations <= q67, 2, 3))
alt_df = pd.DataFrame({'tempCitationsRD': valid_citations, 'alt_maincat': alt_maincat})

target_alt = alt_df[alt_df.index.isin(target_10006.index)]
if len(target_alt) > 0:
    print(f"Alternative method - Permno 10006 maincat: {target_alt.iloc[0]['alt_maincat']}")

print(f"Alternative maincat distribution: {pd.Series(alt_maincat).value_counts().sort_index().to_dict()}")