# ABOUTME: Debug CitationsRD signal construction and filtering logic
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_signal_debug.py

import pandas as pd
import numpy as np

def debug_signal_construction():
    """Debug the full signal construction process for CitationsRD"""
    
    print("=== CitationsRD Signal Construction Debug ===")
    
    # Follow exact logic from CitationsRD.py
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    df = df[df['time_avail_m'] >= '1970-01']
    df['year'] = df['time_avail_m'].dt.year
    
    # Compustat merge
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
    compustat = compustat[compustat['time_avail_m'] >= '1970-01']
    df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
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
    
    # Filter to June observations
    df = df[df['time_avail_m'] >= '1975-01']
    df = df[df['time_avail_m'].dt.month == 6]
    
    print(f"June data: {df.shape}")
    
    # Check permno 14755
    permno_14755 = df[df['permno'] == 14755].copy()
    print(f"Permno 14755 in June data: {len(permno_14755)}")
    
    if len(permno_14755) > 0:
        print("Sample data for permno 14755:")
        print(permno_14755[['time_avail_m', 'gvkey', 'xrd_lag', 'ncitscale', 'ceq', 'sicCRSP']].head())
    
    # Create rolling sums
    df = df.sort_values(['permno', 'time_avail_m'])
    df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    
    # Create temporary signal
    df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)
    
    print(f"After rolling sums: {df.shape}")
    
    # Check permno 14755 after rolling sums
    permno_14755_rolled = df[df['permno'] == 14755].copy()
    print(f"Permno 14755 after rolling sums: {len(permno_14755_rolled)}")
    
    if len(permno_14755_rolled) > 0:
        print("Rolling sum data for permno 14755:")
        print(permno_14755_rolled[['time_avail_m', 'sum_xrd', 'sum_ncit', 'tempCitationsRD']].head())
    
    # Apply filtering steps
    print("\n--- Applying Filtering Steps ---")
    
    # Filter 1: bysort gvkey (time_avail_m): drop if _n <= 2
    df_before_gvkey_filter = df.copy()
    df = df.sort_values(['gvkey', 'time_avail_m'])
    df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
    print(f"After gvkey filter (drop first 2): {df.shape}")
    
    permno_14755_after_gvkey = df[df['permno'] == 14755]
    print(f"Permno 14755 after gvkey filter: {len(permno_14755_after_gvkey)}")
    
    if len(permno_14755_after_gvkey) == 0:
        print("*** FOUND ISSUE: permno 14755 filtered out by gvkey filter ***")
        gvkey_14755 = permno_14755_rolled['gvkey'].iloc[0] if len(permno_14755_rolled) > 0 else None
        if gvkey_14755:
            gvkey_data = df_before_gvkey_filter[df_before_gvkey_filter['gvkey'] == gvkey_14755]
            print(f"Gvkey {gvkey_14755} data before filter: {len(gvkey_data)}")
            print("First few observations for this gvkey:")
            print(gvkey_data[['permno', 'time_avail_m', 'gvkey']].head(5))
            
            if len(gvkey_data) <= 2:
                print(f"*** PROBLEM: Only {len(gvkey_data)} observations for gvkey {gvkey_14755}, all dropped by filter ***")
        return
    
    # Filter 2: Drop financial firms
    df_before_sic = df.copy()
    df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
    print(f"After SIC filter: {df.shape}")
    
    permno_14755_after_sic = df[df['permno'] == 14755]
    print(f"Permno 14755 after SIC filter: {len(permno_14755_after_sic)}")
    
    if len(permno_14755_after_sic) == 0:
        print("*** FOUND ISSUE: permno 14755 filtered out by SIC filter ***")
        sic_14755 = permno_14755_after_gvkey['sicCRSP'].iloc[0] if len(permno_14755_after_gvkey) > 0 else None
        print(f"SIC code for permno 14755: {sic_14755}")
        return
    
    # Filter 3: Drop if ceq < 0
    df_before_ceq = df.copy()
    df = df[df['ceq'] >= 0]
    print(f"After CEQ filter: {df.shape}")
    
    permno_14755_after_ceq = df[df['permno'] == 14755]
    print(f"Permno 14755 after CEQ filter: {len(permno_14755_after_ceq)}")
    
    if len(permno_14755_after_ceq) == 0:
        print("*** FOUND ISSUE: permno 14755 filtered out by CEQ filter ***")
        ceq_14755 = permno_14755_after_sic['ceq'].iloc[0] if len(permno_14755_after_sic) > 0 else None
        print(f"CEQ value for permno 14755: {ceq_14755}")
        return
    
    print("\nPermno 14755 survived all filters!")
    print("Final data for permno 14755:")
    print(permno_14755_after_ceq[['time_avail_m', 'tempCitationsRD', 'mve_c', 'exchcd']].head())

def compare_with_stata_logic():
    """Compare the filtering logic with what Stata does"""
    
    print("\n=== Comparing with Stata Logic ===")
    
    # Check the original Stata logic:
    # bysort gvkey (time_avail_m): drop if _n <= 2
    # This means: within each gvkey, sort by time_avail_m, then drop the first 2 observations
    
    print("Stata logic: bysort gvkey (time_avail_m): drop if _n <= 2")
    print("This drops the first 2 time periods for each gvkey")
    
    # Load just the gvkey data for permno 14755 to see the issue
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m']].copy()
    df = df[df['permno'] == 14755]
    
    if len(df) > 0:
        gvkey_14755 = df['gvkey'].iloc[0]
        print(f"\nGvkey for permno 14755: {gvkey_14755}")
        
        # Check all data for this gvkey
        all_gvkey_data = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
        all_gvkey_data = all_gvkey_data[all_gvkey_data['gvkey'] == gvkey_14755]
        
        # Get June data only (after other processing)
        june_data = all_gvkey_data[all_gvkey_data['time_avail_m'].dt.month == 6]
        june_data = june_data[june_data['time_avail_m'] >= '1975-01']
        june_data = june_data.sort_values('time_avail_m')
        
        print(f"\nJune observations for gvkey {gvkey_14755}: {len(june_data)}")
        print("First few June observations:")
        print(june_data[['permno', 'time_avail_m']].head(5))
        
        if len(june_data) <= 2:
            print(f"*** PROBLEM FOUND: Only {len(june_data)} June observations for gvkey {gvkey_14755}")
            print("After dropping first 2, no observations remain!")
        else:
            print(f"After dropping first 2, {len(june_data) - 2} observations remain")
            remaining = june_data.iloc[2:]
            print("Remaining observations:")
            print(remaining[['permno', 'time_avail_m']].head())

if __name__ == "__main__":
    debug_signal_construction()
    compare_with_stata_logic()