# ABOUTME: Debug DelBreadth filtering logic (NYSE percentile filter)
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_filter_debug.py

import pandas as pd
import numpy as np

def debug_nyse_filter():
    """Debug the NYSE 20th percentile market cap filter"""
    
    print("=== DelBreadth NYSE Filter Debug ===")
    
    # Replicate the DelBreadth logic step by step
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    # Merge with TR_13F
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()
    
    df = df.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')
    
    # Forward-fill TR_13F data
    df = df.sort_values(['permno', 'time_avail_m'])
    df['dbreadth'] = df.groupby('permno')['dbreadth'].fillna(method='ffill')
    
    # Set DelBreadth = dbreadth
    df['DelBreadth'] = df['dbreadth']
    
    print(f"After forward-fill and DelBreadth assignment: {df.shape}")
    
    # Focus on the problematic observation: permno 11370, 2013-04-01
    permno = 11370
    target_date = '2013-04-01'
    
    # Check this observation before filtering
    target_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == target_date)]
    print(f"\nTarget observation (permno {permno}, {target_date}) before filter:")
    if len(target_obs) > 0:
        print(target_obs[['permno', 'time_avail_m', 'exchcd', 'mve_c', 'DelBreadth']])
        
        mve_c = target_obs['mve_c'].iloc[0]
        exchcd = target_obs['exchcd'].iloc[0]
        delBreadth = target_obs['DelBreadth'].iloc[0]
        
        print(f"Market cap: {mve_c}")
        print(f"Exchange code: {exchcd}")
        print(f"DelBreadth: {delBreadth}")
    else:
        print("*** Target observation not found before filter ***")
        return
    
    # Calculate NYSE 20th percentile for this time period
    april_2013_data = df[df['time_avail_m'] == target_date].copy()
    nyse_stocks = april_2013_data[april_2013_data['exchcd'] == 1]
    
    print(f"\n{target_date} data: {len(april_2013_data)} total observations")
    print(f"NYSE stocks: {len(nyse_stocks)}")
    
    if len(nyse_stocks) > 0:
        percentile_20 = nyse_stocks['mve_c'].quantile(0.20)
        print(f"NYSE 20th percentile: {percentile_20}")
        
        # Apply the filter logic from DelBreadth.py
        tolerance = 1.0  # $1M tolerance
        cutoff = percentile_20 - tolerance
        
        print(f"Cutoff (20th percentile - tolerance): {cutoff}")
        print(f"Target mve_c: {mve_c}")
        print(f"mve_c < cutoff? {mve_c < cutoff}")
        
        if mve_c < cutoff:
            print("*** ISSUE FOUND: Target observation filtered out by market cap filter ***")
            print("This explains why it's missing from the final output")
            
            # Check if this is correct behavior or if there's a logic error
            print(f"\nFilter logic: mve_c < (20th percentile - {tolerance})")
            print(f"Filter logic: {mve_c} < ({percentile_20} - {tolerance}) = {cutoff}")
            print(f"Result: {mve_c < cutoff}")
            
        else:
            print("Target observation should pass the filter - issue elsewhere")

def debug_large_difference():
    """Debug the large precision difference for permno 24205"""
    
    print("\n=== Large Difference Debug ===")
    
    # Focus on permno 24205, 201011 where Python=-1.132, Stata=-24.78
    permno = 24205
    target_date = '2010-11-01'
    
    # Replicate the DelBreadth logic
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()
    
    df = df.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Check this permno's data around the target date
    permno_data = df[df['permno'] == permno].copy()
    around_target = permno_data[
        (permno_data['time_avail_m'] >= '2010-09-01') & 
        (permno_data['time_avail_m'] <= '2010-12-01')
    ].copy()
    
    print(f"Permno {permno} data around {target_date}:")
    print(around_target[['time_avail_m', 'dbreadth']])
    
    # Apply forward-fill
    permno_data['dbreadth'] = permno_data['dbreadth'].fillna(method='ffill')
    
    # Check after forward-fill
    around_target_ffill = permno_data[
        (permno_data['time_avail_m'] >= '2010-09-01') & 
        (permno_data['time_avail_m'] <= '2010-12-01')
    ].copy()
    
    print(f"\nAfter forward-fill:")
    print(around_target_ffill[['time_avail_m', 'dbreadth']])
    
    # Check the specific target observation
    target_obs = permno_data[permno_data['time_avail_m'] == target_date]
    if len(target_obs) > 0:
        dbreadth_val = target_obs['dbreadth'].iloc[0]
        print(f"\nTarget observation dbreadth: {dbreadth_val}")
        print(f"Python output: -1.132")
        print(f"Stata output: -24.78")
        
        if abs(dbreadth_val - (-1.132)) < 0.001:
            print("*** Python dbreadth matches Python output ***")
            print("*** Issue: Python TR_13F data differs from Stata TR_13F data ***")
        else:
            print(f"*** Python dbreadth ({dbreadth_val}) differs from Python output (-1.132) ***")
            print("*** Issue: Logic error in DelBreadth calculation ***")

if __name__ == "__main__":
    debug_nyse_filter()
    debug_large_difference()