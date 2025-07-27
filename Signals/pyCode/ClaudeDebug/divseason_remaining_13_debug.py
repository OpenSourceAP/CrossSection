# ABOUTME: Debug the remaining 13 missing DivSeason observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_remaining_13_debug.py

import pandas as pd
import numpy as np

def debug_remaining_13_observations():
    """Debug the specific remaining 13 missing observations"""
    
    print("=== Remaining 13 Missing DivSeason Observations ===")
    
    # From test output, the remaining missing observations are:
    missing_obs = [
        (10209, 195009, 0),
        (10209, 195010, 0),
        (10209, 195011, 1),
        (60506, 198502, 1),
        (60506, 198503, 1), 
        (60506, 198504, 1),
        (65293, 200912, 0),
        (65293, 201001, 1),
        (65293, 201002, 1),
        (91583, 200712, 1)
    ]
    
    print("Remaining missing observations:")
    for permno, yyyymm, expected in missing_obs:
        print(f"  permno {permno}, {yyyymm}, expected DivSeason = {expected}")
    
    # These are a mix of 0s and 1s, suggesting more complex logic issues
    # Let me check if these specific permnos exist in our current output
    
    try:
        current_output = pd.read_csv('../pyData/Predictors/DivSeason.csv')
        current_output = current_output.set_index(['permno', 'yyyymm'])
        
        print("\nChecking current output for these observations:")
        for permno, yyyymm, expected in missing_obs:
            if (permno, yyyymm) in current_output.index:
                actual = current_output.loc[(permno, yyyymm), 'DivSeason']
                print(f"  {permno}, {yyyymm}: FOUND with value {actual} (expected {expected})")
            else:
                print(f"  {permno}, {yyyymm}: MISSING (expected {expected})")
        
        # Check if these permnos exist at all in our output
        print("\nChecking if these permnos exist in our output:")
        unique_permnos = set(permno for permno, _, _ in missing_obs)
        for permno in unique_permnos:
            permno_data = current_output[current_output.index.get_level_values('permno') == permno]
            if len(permno_data) > 0:
                min_date = permno_data.index.get_level_values('yyyymm').min()
                max_date = permno_data.index.get_level_values('yyyymm').max()
                print(f"  permno {permno}: {len(permno_data)} obs, range {min_date}-{max_date}")
            else:
                print(f"  permno {permno}: NO DATA")
        
    except Exception as e:
        print(f"Error loading current output: {e}")

def check_if_edge_case_filtering():
    """Check if these are edge cases being filtered by some other logic"""
    
    print("\n=== Edge Case Analysis ===")
    
    # The pattern suggests these might be edge cases around:
    # 1. Very early dates (1950s) - data availability issues
    # 2. Specific dividend patterns that our logic doesn't handle
    
    missing_obs = [
        (10209, 195009, 0), (10209, 195010, 0), (10209, 195011, 1),
        (60506, 198502, 1), (60506, 198503, 1), (60506, 198504, 1),
        (65293, 200912, 0), (65293, 201001, 1), (65293, 201002, 1),
        (91583, 200712, 1)
    ]
    
    # Group by permno to see patterns
    permnos = {}
    for permno, yyyymm, expected in missing_obs:
        if permno not in permnos:
            permnos[permno] = []
        permnos[permno].append((yyyymm, expected))
    
    print("Grouped by permno:")
    for permno, obs_list in permnos.items():
        dates = [str(yyyymm) for yyyymm, _ in obs_list]
        values = [str(expected) for _, expected in obs_list]
        print(f"  permno {permno}: dates {dates}, expected values {values}")
    
    # Analysis:
    # - permno 10209: 1950s dates, mix of 0,0,1 pattern
    # - permno 60506: 1985 dates, all 1s 
    # - permno 65293: 2009-2010 dates, 0,1,1 pattern
    # - permno 91583: 2007 date, 1
    
    print("\nPattern analysis:")
    print("- Mix of very early (1950s) and recent (2000s) dates")
    print("- Mix of expected 0s and 1s")
    print("- Suggests these are true edge cases rather than systematic issues")
    print("- 13 out of 1.78M observations = 0.0007% failure rate")
    print("- This level of precision may be acceptable given the complexity")

def check_data_availability():
    """Check if these missing observations have data availability issues"""
    
    print("\n=== Data Availability Check ===")
    
    # Check if these permnos exist in SignalMasterTable at the problem dates
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    
    missing_obs = [(10209, 195009), (60506, 198502), (65293, 200912), (91583, 200712)]
    
    for permno, yyyymm in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        smt_exists = ((smt['permno'] == permno) & (smt['time_avail_m'] == target_date)).any()
        
        print(f"permno {permno}, {yyyymm}: {'EXISTS' if smt_exists else 'MISSING'} in SignalMasterTable")
        
        if not smt_exists:
            print(f"  *** This explains the missing observation - no SMT entry ***")

if __name__ == "__main__":
    debug_remaining_13_observations()
    check_if_edge_case_filtering()
    check_data_availability()