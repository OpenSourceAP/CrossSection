# ABOUTME: Attempt to fix DelBreadth's 3 missing observations using better fill logic
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_fix_attempt.py

import pandas as pd
import numpy as np

def test_improved_logic():
    """Test improved DelBreadth logic to handle missing TR_13F data"""
    
    print("=== Testing Improved DelBreadth Logic ===")
    
    # Load data exactly like DelBreadth.py
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()
    
    # Merge with TR_13F data  
    df = df.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')
    
    # Sort for fill operations
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Try different fill strategies:
    
    # Strategy 1: Forward-fill only (current approach)
    df['dbreadth_ffill'] = df.groupby('permno')['dbreadth'].ffill()
    
    # Strategy 2: Both forward and backward fill
    df['dbreadth_bfill'] = df.groupby('permno')['dbreadth'].bfill()
    df['dbreadth_both'] = df['dbreadth_ffill'].fillna(df['dbreadth_bfill'])
    
    # Strategy 3: Interpolation within permno (linear between known points)
    df['dbreadth_interp'] = df.groupby('permno')['dbreadth'].apply(lambda x: x.interpolate(method='linear'))
    
    # Test the specific missing observations
    missing_obs = [
        (92182, 200904, 0.069),
        (92182, 200905, 0.069), 
        (92332, 200808, 0.577)
    ]
    
    print("\\nTesting fill strategies on missing observations:")
    print("permno   yyyymm   expected  original  ffill   bfill   both    interp")
    print("-" * 75)
    
    for permno, yyyymm, expected in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        row = df[(df['permno'] == permno) & (df['time_avail_m'] == target_date)]
        
        if len(row) > 0:
            r = row.iloc[0]
            orig = r['dbreadth'] if pd.notna(r['dbreadth']) else 'NaN'
            ffill = r['dbreadth_ffill'] if pd.notna(r['dbreadth_ffill']) else 'NaN'
            bfill = r['dbreadth_bfill'] if pd.notna(r['dbreadth_bfill']) else 'NaN'
            both = r['dbreadth_both'] if pd.notna(r['dbreadth_both']) else 'NaN'
            interp = r['dbreadth_interp'] if pd.notna(r['dbreadth_interp']) else 'NaN'
            
            print(f"{permno:6d}   {yyyymm:6d}   {expected:7.3f}   {orig:>7}   {ffill:>7}   {bfill:>7}   {both:>7}   {interp:>7}")
        else:
            print(f"{permno:6d}   {yyyymm:6d}   {expected:7.3f}   NOT FOUND IN SMT")
    
    # Check what values each strategy would provide
    print("\\n=== Strategy Analysis ===")
    
    for permno, yyyymm, expected in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        print(f"\\npermno {permno}, {yyyymm} (expected {expected}):")
        
        # Look at nearby TR_13F data for this permno
        permno_data = df[df['permno'] == permno].copy()
        
        # Find TR_13F data before and after
        before = permno_data[(permno_data['time_avail_m'] < target_date) & 
                           pd.notna(permno_data['dbreadth'])]
        after = permno_data[(permno_data['time_avail_m'] > target_date) & 
                          pd.notna(permno_data['dbreadth'])]
        
        if len(before) > 0:
            closest_before = before.iloc[-1]  # Most recent before
            before_yyyymm = closest_before['time_avail_m'].year * 100 + closest_before['time_avail_m'].month
            print(f"  Closest before: {before_yyyymm}, dbreadth = {closest_before['dbreadth']:.3f}")
        else:
            print("  No data before")
            
        if len(after) > 0:
            closest_after = after.iloc[0]  # Earliest after
            after_yyyymm = closest_after['time_avail_m'].year * 100 + closest_after['time_avail_m'].month  
            print(f"  Closest after:  {after_yyyymm}, dbreadth = {closest_after['dbreadth']:.3f}")
        else:
            print("  No data after")

if __name__ == "__main__":
    test_improved_logic()