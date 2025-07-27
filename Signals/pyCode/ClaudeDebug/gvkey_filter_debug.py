# ABOUTME: Debug the gvkey filter logic difference between Stata and Python
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/gvkey_filter_debug.py

import pandas as pd
import numpy as np

print("=== Debugging gvkey filter logic ===")

# Create a test case to understand the difference
test_data = pd.DataFrame({
    'gvkey': [1010, 1010, 1010, 1010, 1010],
    'time_avail_m': pd.to_datetime(['1975-06-01', '1976-06-01', '1977-06-01', '1978-06-01', '1979-06-01']),
    'permno': [10006, 10006, 10006, 10006, 10006],
    'value': [1, 2, 3, 4, 5]
})

print("Original test data:")
print(test_data)

# Python approach: drop first 2 per group using iloc[2:]
print("\nPython approach: groupby().apply(lambda x: x.iloc[2:])")
python_result = test_data.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
print(python_result)

# Alternative approach: use head(-2) to drop last 2? No that's wrong
# Alternative approach: simulate Stata's _n <= 2 logic
print("\nSimulating Stata _n <= 2 logic:")
stata_simulation = test_data.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
print("Result should be the same:", stata_simulation.equals(python_result))

# The logic seems correct. Let me check if there's something else going on.
# Let me recreate the full pipeline but track permno 10006 more carefully

print("\n=== Full pipeline debug for permno 10006 ===")

# Load data and trace through each step
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

# Focus on gvkey 1010 before the filter
gvkey_1010_before = df[df['gvkey'] == 1010.0].sort_values('time_avail_m')
print(f"\nGvkey 1010 observations before gvkey filter:")
print(gvkey_1010_before[['permno', 'gvkey', 'time_avail_m', 'tempCitationsRD']])

# Apply the gvkey filter
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

# Check gvkey 1010 after the filter
gvkey_1010_after = df[df['gvkey'] == 1010.0].sort_values('time_avail_m')
print(f"\nGvkey 1010 observations after gvkey filter:")
print(gvkey_1010_after[['permno', 'gvkey', 'time_avail_m', 'tempCitationsRD']])

# Continue with other filters
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
df = df[df['ceq'] >= 0]

gvkey_1010_after_filters = df[df['gvkey'] == 1010.0].sort_values('time_avail_m')
print(f"\nGvkey 1010 observations after all filters:")
print(gvkey_1010_after_filters[['permno', 'gvkey', 'time_avail_m', 'tempCitationsRD']])

# Check if June 1982 is still there
june_1982 = gvkey_1010_after_filters[gvkey_1010_after_filters['time_avail_m'] == '1982-06-01']
print(f"\nJune 1982 observation for gvkey 1010 after all filters: {len(june_1982)}")
if len(june_1982) > 0:
    print(june_1982[['permno', 'gvkey', 'time_avail_m', 'tempCitationsRD', 'mve_c', 'sicCRSP', 'ceq']])

# If the June 1982 observation exists, check what happens during categorization
if len(june_1982) > 0:
    print("\n=== Checking categorization for remaining observations ===")
    
    # Size categorization
    def calculate_size_breakpoints(group):
        nyse_stocks = group[group['exchcd'] == 1]
        if len(nyse_stocks) == 0:
            return group
        
        median_mve = nyse_stocks['mve_c'].median()
        group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
        return group

    df = df.groupby('time_avail_m').apply(calculate_size_breakpoints).reset_index(drop=True)
    
    # Check June 1982 categorization
    june_1982_categorized = df[(df['gvkey'] == 1010.0) & (df['time_avail_m'] == '1982-06-01')]
    if len(june_1982_categorized) > 0:
        print(f"June 1982 size category: {june_1982_categorized.iloc[0]['sizecat']}")
        
        # Check if this creates a valid CitationsRD signal
        df['maincat'] = np.nan
        df.loc[df['tempCitationsRD'].isna(), 'maincat'] = 1.0
        
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
        
        june_1982_maincat = df[(df['gvkey'] == 1010.0) & (df['time_avail_m'] == '1982-06-01')]
        if len(june_1982_maincat) > 0:
            row = june_1982_maincat.iloc[0]
            print(f"June 1982 main category: {row['maincat']}")
            print(f"Would get CitationsRD signal: sizecat={row['sizecat']}, maincat={row['maincat']}")
            
            # Create CitationsRD signal
            df['CitationsRD'] = np.nan
            df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
            df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0
            
            final_june_1982 = df[(df['gvkey'] == 1010.0) & (df['time_avail_m'] == '1982-06-01')]
            if len(final_june_1982) > 0:
                final_signal = final_june_1982.iloc[0]['CitationsRD']
                print(f"Final CitationsRD signal: {final_signal}")
                if pd.isna(final_signal):
                    print("Signal is NaN - would be dropped!")
                else:
                    print("Signal has value - would be kept!")