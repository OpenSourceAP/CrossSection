# ABOUTME: Debug CitationsRD pipeline step by step for permno 10006 
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_pipeline.py

import pandas as pd
import numpy as np

# Focus on permno 10006 and trace through each step
target_permno = 10006
target_date = '1982-06-01'

print(f"=== Tracing permno {target_permno} through CitationsRD pipeline ===")

# Step 1: Load SignalMasterTable
print("\n1. Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()

target_rows = df[df['permno'] == target_permno]
print(f"   Target permno count: {len(target_rows)}")

# Step 2: Filter to post-1970
df = df[df['time_avail_m'] >= '1970-01']
target_rows = df[df['permno'] == target_permno]
print(f"   After 1970 filter: {len(target_rows)}")

# Step 3: Generate year
df['year'] = df['time_avail_m'].dt.year
target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
print(f"   June 1982 row exists: {len(target_june_1982) > 0}")
if len(target_june_1982) > 0:
    print(f"   June 1982 data: {target_june_1982[['permno', 'time_avail_m', 'gvkey', 'year']].iloc[0].to_dict()}")

# Step 4: Merge with Compustat
print("\n2. Merging with Compustat...")
compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
compustat = compustat[compustat['time_avail_m'] >= '1970-01']

# Check if target has Compustat data
target_compustat = compustat[(compustat['permno'] == target_permno) & (compustat['time_avail_m'] == target_date)]
print(f"   Target has Compustat data for June 1982: {len(target_compustat) > 0}")
if len(target_compustat) > 0:
    print(f"   Compustat data: {target_compustat[['permno', 'time_avail_m', 'xrd', 'ceq']].iloc[0].to_dict()}")

df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
target_rows = df[df['permno'] == target_permno]
target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
print(f"   After Compustat merge: {len(target_rows)} total rows")
print(f"   June 1982 row still exists: {len(target_june_1982) > 0}")

# Step 5: Drop missing gvkey
df = df.dropna(subset=['gvkey'])
target_rows = df[df['permno'] == target_permno]
target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
print(f"   After dropping missing gvkey: {len(target_rows)} total rows")
print(f"   June 1982 row still exists: {len(target_june_1982) > 0}")

# Step 6: Merge with patent data
print("\n3. Merging with patent data...")
patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
patent = patent[['gvkey', 'year', 'ncitscale']].copy()

# Check if target gvkey has patent data for 1982
if len(target_june_1982) > 0:
    target_gvkey = target_june_1982.iloc[0]['gvkey']
    target_year = target_june_1982.iloc[0]['year']
    target_patent = patent[(patent['gvkey'] == target_gvkey) & (patent['year'] == target_year)]
    print(f"   Target gvkey {target_gvkey} has patent data for {target_year}: {len(target_patent) > 0}")
    if len(target_patent) > 0:
        print(f"   Patent data: {target_patent.iloc[0].to_dict()}")

df = df.merge(patent, on=['gvkey', 'year'], how='left')
target_rows = df[df['permno'] == target_permno]
target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
print(f"   After patent merge: {len(target_rows)} total rows")
print(f"   June 1982 row still exists: {len(target_june_1982) > 0}")

# Step 7: Create lags
print("\n4. Creating lags...")
df = df.sort_values(['permno', 'time_avail_m'])
df['temp'] = df.groupby('permno')['ncitscale'].shift(6)
df['temp'] = df['temp'].fillna(0)
df['ncitscale'] = df['temp']
df = df.drop(columns=['temp'])

df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)
df['xrd_lag'] = df['xrd_lag'].fillna(0)

target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
print(f"   June 1982 row still exists: {len(target_june_1982) > 0}")
if len(target_june_1982) > 0:
    row = target_june_1982.iloc[0]
    print(f"   Lag values - ncitscale: {row['ncitscale']}, xrd_lag: {row['xrd_lag']}")

# Step 8: Filter to 1975+ and June only
print("\n5. Filtering to 1975+ and June only...")
df = df[df['time_avail_m'] >= '1975-01']
target_rows = df[df['permno'] == target_permno]
print(f"   After 1975 filter: {len(target_rows)} total rows")

df = df[df['time_avail_m'].dt.month == 6]
target_rows = df[df['permno'] == target_permno]
target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
print(f"   After June filter: {len(target_rows)} total rows")
print(f"   June 1982 row still exists: {len(target_june_1982) > 0}")

# Step 9: Check rolling sums and filters
if len(target_june_1982) > 0:
    print("\n6. Computing rolling sums...")
    df = df.sort_values(['permno', 'time_avail_m'])
    df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    
    df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)
    
    target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
    if len(target_june_1982) > 0:
        row = target_june_1982.iloc[0]
        print(f"   Rolling sums - sum_xrd: {row['sum_xrd']}, sum_ncit: {row['sum_ncit']}")
        print(f"   tempCitationsRD: {row['tempCitationsRD']}")
    
    # Step 10: Apply gvkey filter (drop if _n <= 2)
    print("\n7. Applying gvkey filter...")
    df = df.sort_values(['gvkey', 'time_avail_m'])
    before_count = len(df[df['permno'] == target_permno])
    df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
    after_count = len(df[df['permno'] == target_permno])
    print(f"   Before gvkey filter: {before_count}, After: {after_count}")
    
    target_june_1982 = df[(df['permno'] == target_permno) & (df['time_avail_m'] == target_date)]
    print(f"   June 1982 row still exists after gvkey filter: {len(target_june_1982) > 0}")