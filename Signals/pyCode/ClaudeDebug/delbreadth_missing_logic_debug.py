# ABOUTME: Debug DelBreadth missing logic to understand Stata behavior
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_missing_logic_debug.py

import pandas as pd
import numpy as np

def debug_missing_logic():
    """Debug the specific logic for handling missing TR_13F data"""
    
    print("=== DelBreadth Missing Logic Debug ===")
    
    # The 3 missing observations
    missing_obs = [
        (92182, 200904, 0.069),
        (92182, 200905, 0.069),
        (92332, 200808, 0.577)
    ]
    
    # Load the data
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()
    
    # Check the specific observations in SMT
    for permno, yyyymm, expected in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        print(f"\\nChecking permno {permno}, {yyyymm} (expected {expected})")
        
        # Check SMT
        smt_row = df[(df['permno'] == permno) & (df['time_avail_m'] == target_date)]
        if len(smt_row) > 0:
            print(f"  SMT: mve_c = {smt_row['mve_c'].iloc[0]:.2f}")
        else:
            print("  SMT: NOT FOUND")
            continue
            
        # Check TR_13F 
        tr13f_row = tr_13f[(tr_13f['permno'] == permno) & (tr_13f['time_avail_m'] == target_date)]
        if len(tr13f_row) > 0:
            print(f"  TR_13F: dbreadth = {tr13f_row['dbreadth'].iloc[0]:.3f}")
        else:
            print("  TR_13F: NOT FOUND")
            
            # Check if there's any TR_13F data for this permno around this time
            permno_tr13f = tr_13f[tr_13f['permno'] == permno].copy()
            if len(permno_tr13f) > 0:
                permno_tr13f['date_diff'] = abs((permno_tr13f['time_avail_m'] - target_date).dt.days)
                closest = permno_tr13f.loc[permno_tr13f['date_diff'].idxmin()]
                closest_yyyymm = closest['time_avail_m'].year * 100 + closest['time_avail_m'].month
                print(f"    Closest TR_13F: {closest_yyyymm}, dbreadth = {closest['dbreadth']:.3f}, {closest['date_diff']} days away")
                
                # Check what forward-fill would do
                permno_all = df[df['permno'] == permno].copy()
                permno_all = permno_all.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')
                permno_all = permno_all.sort_values('time_avail_m')
                permno_all['dbreadth_ffill'] = permno_all['dbreadth'].fillna(method='ffill')
                
                target_row = permno_all[permno_all['time_avail_m'] == target_date]
                if len(target_row) > 0:
                    ffill_value = target_row['dbreadth_ffill'].iloc[0]
                    if pd.notna(ffill_value):
                        print(f"    Forward-fill would give: {ffill_value:.3f}")
                    else:
                        print("    Forward-fill would give: NaN (no prior data)")
            else:
                print("    No TR_13F data for this permno at all")

def check_stata_behavior():
    """Check what Stata behavior should be for missing TR_13F"""
    
    print("\\n=== Expected Stata Behavior ===")
    print("Based on DelBreadth.do:")
    print("1. merge 1:1 with keep(master match) - keeps all SMT rows")
    print("2. gen DelBreadth = dbreadth - DelBreadth = missing if no TR_13F match")  
    print("3. No forward-fill logic in Stata")
    print("4. But our expected values are NOT missing - they are specific numbers!")
    print("\\nThis suggests:")
    print("- The Stata data might use a different TR_13F expansion method")
    print("- Or there's a different quarterly->monthly logic we're missing")

if __name__ == "__main__":
    debug_missing_logic()
    check_stata_behavior()