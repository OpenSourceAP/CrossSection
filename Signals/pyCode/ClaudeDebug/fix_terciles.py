# ABOUTME: Debug and fix the tercile calculation issue
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/fix_terciles.py

import pandas as pd
import numpy as np

print("=== Debugging tercile calculation ===")

# Create test data similar to June 1982
test_data = pd.Series([0.0] * 689 + [0.1] * 176 + [2.4] * 432)  # Simulate the distribution
test_data = test_data.sample(frac=1).reset_index(drop=True)  # Shuffle

print(f"Test data shape: {len(test_data)}")
print(f"Test data percentiles:")
print(test_data.quantile([0.33, 0.67]))

print(f"\n=== Current Python method (pd.qcut with duplicates='drop') ===")

try:
    current_result = pd.qcut(test_data, q=3, labels=False, duplicates='drop') + 1
    print(f"Current method result distribution:")
    print(pd.Series(current_result).value_counts().sort_index())
    
    # Check what happens to high values
    high_value_indices = test_data[test_data > 2.0].index
    if len(high_value_indices) > 0:
        print(f"High values (>2.0) get terciles: {current_result[high_value_indices].unique()}")
except Exception as e:
    print(f"Current method failed: {e}")

print(f"\n=== Alternative method (manual percentile-based) ===")

q33 = test_data.quantile(0.333)
q67 = test_data.quantile(0.667)
print(f"Breakpoints: 33rd={q33}, 67th={q67}")

manual_result = np.where(test_data <= q33, 1, 
                        np.where(test_data <= q67, 2, 3))
print(f"Manual method result distribution:")
print(pd.Series(manual_result).value_counts().sort_index())

high_value_indices = test_data[test_data > 2.0].index
if len(high_value_indices) > 0:
    print(f"High values (>2.0) get terciles: {pd.Series(manual_result)[high_value_indices].unique()}")

print(f"\n=== Testing with actual June 1982 data ===")

# Load actual June 1982 data
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

june_1982 = df[df['time_avail_m'] == '1982-06-01'].copy()
valid_citations = june_1982[june_1982['tempCitationsRD'].notna()]['tempCitationsRD']

print(f"Actual June 1982 valid citations: {len(valid_citations)}")
print(f"Unique values: {valid_citations.nunique()}")
print(f"Value counts for zeros: {(valid_citations == 0.0).sum()}")

# Test both methods on actual data
print(f"\n=== Current method on actual data ===")
try:
    current_actual = pd.qcut(valid_citations, q=3, labels=False, duplicates='drop') + 1
    print(f"Distribution: {pd.Series(current_actual).value_counts().sort_index()}")
    
    # Check permno 10006
    target_10006_idx = june_1982[june_1982['permno'] == 10006].index
    if len(target_10006_idx) > 0:
        target_idx_in_valid = valid_citations.index.get_loc(target_10006_idx[0]) if target_10006_idx[0] in valid_citations.index else None
        if target_idx_in_valid is not None:
            print(f"Permno 10006 gets tercile: {current_actual.iloc[target_idx_in_valid]}")
except Exception as e:
    print(f"Current method failed: {e}")

print(f"\n=== Fixed method on actual data ===")
q33_actual = valid_citations.quantile(0.333)
q67_actual = valid_citations.quantile(0.667)
print(f"Breakpoints: 33rd={q33_actual}, 67th={q67_actual}")

fixed_actual = np.where(valid_citations <= q33_actual, 1, 
                       np.where(valid_citations <= q67_actual, 2, 3))
print(f"Distribution: {pd.Series(fixed_actual).value_counts().sort_index()}")

# Check permno 10006 with fixed method
target_10006_idx = june_1982[june_1982['permno'] == 10006].index
if len(target_10006_idx) > 0 and target_10006_idx[0] in valid_citations.index:
    target_value = valid_citations.loc[target_10006_idx[0]]
    target_idx_in_valid = valid_citations.index.get_loc(target_10006_idx[0])
    print(f"Permno 10006 tempCitationsRD: {target_value}")
    print(f"Permno 10006 gets tercile: {fixed_actual[target_idx_in_valid]}")
    
    # Double-check the logic
    if target_value <= q33_actual:
        expected = 1
    elif target_value <= q67_actual:
        expected = 2
    else:
        expected = 3
    print(f"Expected tercile based on breakpoints: {expected}")

print(f"\n=== Proposed fix ===")
print("Replace the fast_terciles function with manual percentile-based calculation")
print("This should fix the issue with pd.qcut and duplicates")