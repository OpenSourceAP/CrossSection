# ABOUTME: Debug DelBreadth TR_13F data and forward-fill logic
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_tr13f_debug.py

import pandas as pd
import numpy as np

def debug_tr13f_data():
    """Debug the TR_13F data and merge logic"""
    
    print("=== DelBreadth TR_13F Debug ===")
    
    # Check the TR_13F data for the problematic permnos
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    print(f"TR_13F data: {tr_13f.shape}")
    print("Columns:", tr_13f.columns.tolist())
    
    # Check the date range
    if 'time_avail_m' in tr_13f.columns:
        print(f"Date range: {tr_13f['time_avail_m'].min()} to {tr_13f['time_avail_m'].max()}")
    
    # Check problematic permnos
    problematic_permnos = [11370, 24205]  # Missing and precision issues
    
    for permno in problematic_permnos:
        print(f"\n--- Permno {permno} in TR_13F ---")
        permno_data = tr_13f[tr_13f['permno'] == permno].copy()
        print(f"Observations: {len(permno_data)}")
        
        if len(permno_data) > 0:
            permno_data = permno_data.sort_values('time_avail_m')
            print("First few observations:")
            print(permno_data[['permno', 'time_avail_m', 'dbreadth']].head(10))
            
            # Check around the problematic dates
            if permno == 11370:
                # Missing 201304, available from 201305
                around_date = permno_data[permno_data['time_avail_m'] >= '2013-01-01']
                around_date = around_date[around_date['time_avail_m'] <= '2013-06-01']
                print(f"\nData around 2013-03/04 for permno {permno}:")
                print(around_date[['time_avail_m', 'dbreadth']])
                
            elif permno == 24205:
                # Large difference in 201011
                around_date = permno_data[permno_data['time_avail_m'] >= '2010-10-01']
                around_date = around_date[around_date['time_avail_m'] <= '2010-12-01']
                print(f"\nData around 2010-11 for permno {permno}:")
                print(around_date[['time_avail_m', 'dbreadth']])
        else:
            print(f"*** No TR_13F data for permno {permno} ***")

def debug_forward_fill_logic():
    """Debug the forward-fill logic in DelBreadth"""
    
    print("\n=== Forward-Fill Logic Debug ===")
    
    # Replicate the DelBreadth logic step by step
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    # Focus on a specific permno for debugging
    permno = 11370  # The one missing 201304
    
    df_permno = df[df['permno'] == permno].copy()
    print(f"SignalMasterTable for permno {permno}: {len(df_permno)} observations")
    
    if len(df_permno) > 0:
        df_permno = df_permno.sort_values('time_avail_m')
        print("Date range in SignalMasterTable:")
        print(f"Min: {df_permno['time_avail_m'].min()}")
        print(f"Max: {df_permno['time_avail_m'].max()}")
        
        # Check specific dates around 201304
        march_2013 = df_permno[df_permno['time_avail_m'] == '2013-03-01']
        april_2013 = df_permno[df_permno['time_avail_m'] == '2013-04-01']
        may_2013 = df_permno[df_permno['time_avail_m'] == '2013-05-01']
        
        print(f"\n2013-03-01 in SignalMasterTable: {len(march_2013)} rows")
        print(f"2013-04-01 in SignalMasterTable: {len(april_2013)} rows")
        print(f"2013-05-01 in SignalMasterTable: {len(may_2013)} rows")
        
        # Merge with TR_13F
        tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
        tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()
        
        # Check TR_13F for this permno around this time
        tr_13f_permno = tr_13f[tr_13f['permno'] == permno].copy()
        if len(tr_13f_permno) > 0:
            tr_13f_permno = tr_13f_permno.sort_values('time_avail_m')
            tr_13f_early = tr_13f_permno[tr_13f_permno['time_avail_m'] <= '2013-06-01']
            print(f"\nTR_13F data for permno {permno} (early 2013):")
            print(tr_13f_early)
        
        # Perform the merge
        merged = df_permno.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')
        print(f"\nAfter merge: {len(merged)} observations")
        
        # Apply forward-fill
        merged = merged.sort_values(['permno', 'time_avail_m'])
        merged['dbreadth_before_ffill'] = merged['dbreadth'].copy()
        merged['dbreadth'] = merged.groupby('permno')['dbreadth'].fillna(method='ffill')
        
        # Check the result around 201304
        early_2013 = merged[merged['time_avail_m'] <= '2013-06-01']
        print(f"\nAfter forward-fill (early 2013):")
        print(early_2013[['time_avail_m', 'dbreadth_before_ffill', 'dbreadth']].head(10))
        
        # Check if 201304 (2013-04-01) has a value after forward-fill
        april_2013_merged = merged[merged['time_avail_m'] == '2013-04-01']
        if len(april_2013_merged) > 0:
            dbreadth_val = april_2013_merged['dbreadth'].iloc[0]
            print(f"\n2013-04-01 dbreadth after forward-fill: {dbreadth_val}")
            
            if pd.isna(dbreadth_val):
                print("*** ISSUE: 2013-04-01 still has NaN after forward-fill ***")
                print("This explains why it gets filtered out later")
            else:
                print("Forward-fill worked, but observation still missing - check other filters")

if __name__ == "__main__":
    debug_tr13f_data()
    debug_forward_fill_logic()