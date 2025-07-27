# ABOUTME: Debug CitationsRD June filtering and expansion logic
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_june_debug.py

import pandas as pd
import numpy as np

def debug_june_filtering():
    """Debug the June filtering step in CitationsRD"""
    
    print("=== CitationsRD June Filtering Debug ===")
    
    # Follow exact logic from CitationsRD.py but focus on debugging
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    
    # Early filtering
    df = df[df['time_avail_m'] >= '1970-01']
    df['year'] = df['time_avail_m'].dt.year
    
    # Merge Compustat
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
    compustat = compustat[compustat['time_avail_m'] >= '1970-01']
    df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
    
    # Drop missing gvkey
    df = df.dropna(subset=['gvkey'])
    
    # Patent merge
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
    
    print(f"Before filtering: {df.shape}")
    
    # Check permno 14755 before June filtering
    permno_14755 = df[df['permno'] == 14755].copy()
    print(f"Permno 14755 before June filter: {len(permno_14755)}")
    
    if len(permno_14755) > 0:
        print("Sample dates for permno 14755:")
        print(permno_14755[['time_avail_m', 'year']].head(10))
        
        # Check what months we have
        permno_14755['month'] = permno_14755['time_avail_m'].dt.month
        months = permno_14755['month'].value_counts().sort_index()
        print(f"Months available: {months.to_dict()}")
    
    # Apply date and June filters
    print("\n--- Applying filters ---")
    df = df[df['time_avail_m'] >= '1975-01']
    print(f"After 1975 filter: {df.shape}")
    
    # Check permno 14755 after 1975 filter
    permno_14755_after_1975 = df[df['permno'] == 14755]
    print(f"Permno 14755 after 1975 filter: {len(permno_14755_after_1975)}")
    
    df = df[df['time_avail_m'].dt.month == 6]  # June only
    print(f"After June filter: {df.shape}")
    
    # Check permno 14755 after June filter
    permno_14755_june = df[df['permno'] == 14755]
    print(f"Permno 14755 after June filter: {len(permno_14755_june)}")
    
    if len(permno_14755_june) > 0:
        print("June observations for permno 14755:")
        print(permno_14755_june[['time_avail_m', 'gvkey', 'xrd_lag', 'ncitscale']].head(10))
        
        # Check specific years we care about
        years_of_interest = [2017, 2018]
        june_subset = permno_14755_june[permno_14755_june['year'].isin(years_of_interest)]
        print(f"\nJune data for 2017-2018: {len(june_subset)}")
        if len(june_subset) > 0:
            print(june_subset[['time_avail_m', 'year', 'gvkey', 'xrd_lag', 'ncitscale']])
    else:
        print("*** ISSUE: No June observations for permno 14755 ***")
        # Check what June data exists for this permno in earlier steps
        original_df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
        original_14755 = original_df[original_df['permno'] == 14755].copy()
        original_14755['month'] = original_14755['time_avail_m'].dt.month
        original_june_14755 = original_14755[original_14755['month'] == 6]
        print(f"Original SignalMasterTable June data for 14755: {len(original_june_14755)}")
        if len(original_june_14755) > 0:
            print(original_june_14755[['time_avail_m', 'gvkey']].head())

def debug_expansion_logic():
    """Debug the expand-to-monthly logic"""
    
    print("\n=== CitationsRD Expansion Logic Debug ===")
    
    # Create minimal test case for expansion
    test_june_data = pd.DataFrame({
        'permno': [14755, 14755],
        'gvkey': [1234, 1234],
        'time_avail_m': [pd.to_datetime('2017-06-01'), pd.to_datetime('2018-06-01')],
        'CitationsRD': [0, 0]
    })
    
    print("Test June data:")
    print(test_june_data)
    
    # Apply expansion logic from CitationsRD.py
    keep_cols = ['permno', 'gvkey', 'time_avail_m', 'CitationsRD']
    df_slim = test_june_data[keep_cols].copy()
    
    # Use list comprehension with pre-allocated DataFrames
    df_expanded = pd.concat([
        df_slim.assign(time_avail_m=df_slim['time_avail_m'] + pd.DateOffset(months=i))
        for i in range(12)
    ], ignore_index=True)
    
    df_expanded = df_expanded.sort_values(['gvkey', 'time_avail_m'])
    
    print(f"\nAfter expansion: {len(df_expanded)} rows")
    print("Sample expanded data:")
    print(df_expanded.head(15))
    
    # Convert to final format
    df_final = df_expanded[['permno', 'time_avail_m', 'CitationsRD']].copy()
    df_final = df_final.dropna(subset=['CitationsRD'])
    df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month
    
    print("\nFinal format sample:")
    print(df_final.head(15))
    
    # Check for the specific missing dates
    missing_yyyymm = [201706, 201707, 201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803]
    final_14755 = df_final[df_final['permno'] == 14755]
    
    print(f"\nFinal data for permno 14755: {len(final_14755)} rows")
    if len(final_14755) > 0:
        print("Available yyyymm values:")
        available_yyyymm = sorted(final_14755['yyyymm'].unique())
        print(available_yyyymm)
        
        print("\nChecking for missing dates:")
        for yyyymm in missing_yyyymm:
            exists = yyyymm in available_yyyymm
            print(f"  {yyyymm}: {'EXISTS' if exists else 'MISSING'}")

if __name__ == "__main__":
    debug_june_filtering()
    debug_expansion_logic()