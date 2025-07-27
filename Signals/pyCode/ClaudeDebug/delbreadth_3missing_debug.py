# ABOUTME: Debug the 3 missing DelBreadth observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_3missing_debug.py

import pandas as pd
import numpy as np

def debug_delbreadth_3_missing():
    """Debug the specific 3 missing DelBreadth observations"""
    
    print("=== DelBreadth 3 Missing Observations Debug ===")
    
    # From test output:
    # permno 92182, 200904, value 0.069
    # permno 92182, 200905, value 0.069  
    # permno 92332, 200808, value 0.577
    
    missing_obs = [
        (92182, 200904, 0.069),
        (92182, 200905, 0.069),
        (92332, 200808, 0.577)
    ]
    
    print("Missing observations:")
    for permno, yyyymm, value in missing_obs:
        print(f"  permno {permno}, {yyyymm}, expected DelBreadth = {value}")
    
    # These are very specific observations - likely edge cases
    # Let me check what's happening with these specific permnos
    
    # Load the TR_13F data which is critical for DelBreadth
    print("\nChecking TR_13F data availability...")
    
    tr13f = pd.read_parquet('../pyData/Intermediate/tr_13f.parquet')
    
    for permno, yyyymm, expected in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        print(f"\n--- permno {permno}, {yyyymm} ---")
        
        # Check if this permno exists in TR_13F data around this time
        permno_tr13f = tr13f[tr13f['permno'] == permno]
        
        if len(permno_tr13f) == 0:
            print(f"  No TR_13F data for permno {permno}")
            continue
            
        # Check data around the target date
        nearby_tr13f = permno_tr13f[
            (permno_tr13f['time_avail_m'] >= target_date - pd.DateOffset(months=6)) &
            (permno_tr13f['time_avail_m'] <= target_date + pd.DateOffset(months=6))
        ]
        
        print(f"  TR_13F entries ±6 months: {len(nearby_tr13f)}")
        
        if len(nearby_tr13f) > 0:
            print("  Recent TR_13F data:")
            print(nearby_tr13f[['time_avail_m']].head().to_string())
        
        # Check if the issue is with the NYSE 20th percentile filter
        # Load SignalMasterTable to check market cap
        smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
        smt_entry = smt[(smt['permno'] == permno) & (smt['time_avail_m'] == target_date)]
        
        if len(smt_entry) > 0:
            mve_c = smt_entry['mve_c'].iloc[0]
            print(f"  Market cap at {yyyymm}: ${mve_c:.2f}M")
            
            # Check NYSE 20th percentile for this month
            same_month = smt[smt['time_avail_m'] == target_date]
            nyse_stocks = same_month[(same_month['exchcd'] == 1) & same_month['mve_c'].notna()]
            
            if len(nyse_stocks) > 0:
                nyse_20th = nyse_stocks['mve_c'].quantile(0.2)
                print(f"  NYSE 20th percentile: ${nyse_20th:.2f}M")
                
                # Our current tolerance is $10M
                tolerance = 10.0
                cutoff = nyse_20th - tolerance
                
                if mve_c < cutoff:
                    print(f"  *** FILTERED OUT: mve_c {mve_c:.2f} < cutoff {cutoff:.2f} ***")
                    print(f"  This explains why the observation is missing")
                else:
                    print(f"  Market cap filter OK: {mve_c:.2f} >= {cutoff:.2f}")
            else:
                print("  No NYSE stocks found for this month")
        else:
            print(f"  No SignalMasterTable entry for {yyyymm}")

def check_tolerance_adjustment():
    """Check if we need to adjust the tolerance further"""
    
    print("\n=== Tolerance Adjustment Check ===")
    
    # The 3 missing observations suggest we need to be even more lenient
    # Let's see what tolerance would be needed
    
    missing_obs = [(92182, 200904), (92182, 200905), (92332, 200808)]
    
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    
    for permno, yyyymm in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        smt_entry = smt[(smt['permno'] == permno) & (smt['time_avail_m'] == target_date)]
        
        if len(smt_entry) > 0:
            mve_c = smt_entry['mve_c'].iloc[0]
            
            # Get NYSE 20th percentile for this month
            same_month = smt[smt['time_avail_m'] == target_date]
            nyse_stocks = same_month[(same_month['exchcd'] == 1) & same_month['mve_c'].notna()]
            
            if len(nyse_stocks) > 0:
                nyse_20th = nyse_stocks['mve_c'].quantile(0.2)
                
                # Calculate needed tolerance
                needed_tolerance = nyse_20th - mve_c
                
                print(f"permno {permno}, {yyyymm}:")
                print(f"  Market cap: ${mve_c:.2f}M")
                print(f"  NYSE 20th percentile: ${nyse_20th:.2f}M")
                print(f"  Needed tolerance: ${needed_tolerance:.2f}M")
                print()

if __name__ == "__main__":
    debug_delbreadth_3_missing()
    check_tolerance_adjustment()