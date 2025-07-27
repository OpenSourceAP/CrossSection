# ABOUTME: Simple approach to fix DelBreadth's 3 missing observations 
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_simple_fix.py

import pandas as pd
import numpy as np

def analyze_specific_missing():
    """Analyze the specific missing observations to understand what values they should have"""
    
    print("=== Analyzing Specific Missing Observations ===")
    
    missing_obs = [
        (92182, 200904, 0.069),
        (92182, 200905, 0.069),
        (92332, 200808, 0.577)
    ]
    
    # Load TR_13F data to see the pattern
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    
    for permno, yyyymm, expected in missing_obs:
        print(f"\\nAnalyzing permno {permno}, {yyyymm} (expected {expected}):")
        
        # Get all TR_13F data for this permno
        permno_data = tr_13f[tr_13f['permno'] == permno].copy()
        permno_data['yyyymm'] = permno_data['time_avail_m'].dt.year * 100 + permno_data['time_avail_m'].dt.month
        permno_data = permno_data.sort_values('yyyymm')
        
        print("  TR_13F data for this permno:")
        for _, row in permno_data.iterrows():
            print(f"    {row['yyyymm']}: {row['dbreadth']:.3f}")
        
        # Find closest values
        before = permno_data[permno_data['yyyymm'] < yyyymm]
        after = permno_data[permno_data['yyyymm'] > yyyymm]
        
        if len(before) > 0:
            closest_before = before.iloc[-1]
            print(f"  Closest before: {closest_before['yyyymm']}, value = {closest_before['dbreadth']:.3f}")
        
        if len(after) > 0:
            closest_after = after.iloc[0]
            print(f"  Closest after:  {closest_after['yyyymm']}, value = {closest_after['dbreadth']:.3f}")
        
        # Check if expected value matches either neighbor
        if len(before) > 0 and abs(before.iloc[-1]['dbreadth'] - expected) < 0.001:
            print(f"  *** Expected value matches closest before value! ***")
        if len(after) > 0 and abs(after.iloc[0]['dbreadth'] - expected) < 0.001:
            print(f"  *** Expected value matches closest after value! ***")

def try_backward_fill_fix():
    """Try using backward fill to capture missing values"""
    
    print("\\n=== Testing Backward Fill Solution ===")
    
    # Load data like DelBreadth.py
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()
    
    df = df.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Current approach: forward fill only
    df['dbreadth_current'] = df.groupby('permno')['dbreadth'].ffill()
    
    # New approach: backward fill first, then forward fill
    df['dbreadth_bfill'] = df.groupby('permno')['dbreadth'].bfill()
    df['dbreadth_new'] = df['dbreadth_current'].fillna(df['dbreadth_bfill'])
    
    # Test on specific observations
    missing_obs = [(92182, 200904), (92182, 200905), (92332, 200808)]
    
    print("Results for missing observations:")
    print("permno   yyyymm   current   new_approach")
    print("-" * 45)
    
    found_fixes = 0
    for permno, yyyymm in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        row = df[(df['permno'] == permno) & (df['time_avail_m'] == target_date)]
        
        if len(row) > 0:
            r = row.iloc[0]
            current = r['dbreadth_current'] if pd.notna(r['dbreadth_current']) else 'NaN'
            new = r['dbreadth_new'] if pd.notna(r['dbreadth_new']) else 'NaN'
            
            print(f"{permno:6d}   {yyyymm:6d}   {current:>7}   {new:>7}")
            
            if pd.isna(r['dbreadth_current']) and pd.notna(r['dbreadth_new']):
                found_fixes += 1
                print(f"         *** POTENTIAL FIX: {new} ***")
        else:
            print(f"{permno:6d}   {yyyymm:6d}   NOT IN SMT")
    
    print(f"\\nFound potential fixes for {found_fixes} out of 3 missing observations")
    return found_fixes > 0

if __name__ == "__main__":
    analyze_specific_missing()
    has_fix = try_backward_fill_fix()
    
    if has_fix:
        print("\\n=== RECOMMENDATION ===")
        print("Modify DelBreadth.py to use backward fill for missing observations")
        print("This should capture the missing values from subsequent TR_13F data")
    else:
        print("\\n=== NO SIMPLE FIX FOUND ===")
        print("The missing observations may require more complex logic or data investigation")