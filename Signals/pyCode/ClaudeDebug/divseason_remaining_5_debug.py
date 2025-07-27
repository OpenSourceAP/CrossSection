# ABOUTME: Debug the remaining 5 missing DivSeason observations after the special dividend fix
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_remaining_5_debug.py

import pandas as pd
import numpy as np

def debug_remaining_5():
    """Debug the remaining 5 missing observations after the special dividend fix"""
    
    print("=== Debugging Remaining 5 Missing DivSeason Observations ===")
    
    # From the test output:
    remaining_obs = [
        (10209, 195009, 0),
        (65293, 200912, 0), 
        (91583, 200712, 1),
        (92823, 198510, 1),
        (92823, 198511, 1)
    ]
    
    print("Remaining missing observations:")
    for permno, yyyymm, expected in remaining_obs:
        print(f"  permno {permno}, {yyyymm}, expected DivSeason = {expected}")
    
    # Check if these exist in current output
    try:
        current_output = pd.read_csv('../pyData/Predictors/DivSeason.csv')
        current_output = current_output.set_index(['permno', 'yyyymm'])
        
        print("\\nChecking current output:")
        for permno, yyyymm, expected in remaining_obs:
            if (permno, yyyymm) in current_output.index:
                actual = current_output.loc[(permno, yyyymm), 'DivSeason']
                print(f"  {permno}, {yyyymm}: FOUND with value {actual} (expected {expected})")
            else:
                print(f"  {permno}, {yyyymm}: MISSING (expected {expected})")
                
                # Check if permno exists at all
                permno_data = current_output[current_output.index.get_level_values('permno') == permno]
                if len(permno_data) > 0:
                    min_date = permno_data.index.get_level_values('yyyymm').min()
                    max_date = permno_data.index.get_level_values('yyyymm').max()
                    print(f"    permno {permno}: {len(permno_data)} obs, range {min_date}-{max_date}")
                else:
                    print(f"    permno {permno}: NO DATA")
        
    except Exception as e:
        print(f"Error loading current output: {e}")

def analyze_patterns():
    """Analyze patterns in the remaining missing observations"""
    
    print("\\n=== Pattern Analysis ===")
    
    remaining_obs = [
        (10209, 195009, 0),
        (65293, 200912, 0), 
        (91583, 200712, 1),
        (92823, 198510, 1),
        (92823, 198511, 1)
    ]
    
    print("Analysis:")
    print("- permno 10209: 1950s date (very early)")
    print("- permno 65293: 2009 date (our test case - special dividend issue)")
    print("- permno 91583: 2007 date")
    print("- permno 92823: 1985 dates (two consecutive months)")
    
    print("\\nImprovement:")
    print("- Reduced from 13 to 5 missing observations (62% improvement)")
    print("- Fixed 8 out of 13 missing observations")
    print("- New failure rate: 5 / 1,775,339 = 0.0003%")

def check_specific_cd3_issues():
    """Check if remaining observations have cd3 issues"""
    
    print("\\n=== Checking Remaining cd3 Issues ===")
    
    # Let's specifically check permno 65293, 200912 which we know had cd3=7 issue
    target_permno = 65293
    target_yyyymm = 200912
    target_date = pd.to_datetime('2009-12-01')
    
    print(f"Checking if permno {target_permno}, {target_yyyymm} still has cd3 issue...")
    
    # Load dividend data
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Get dividend data for this permno
    permno_divs = dist_df[dist_df['permno'] == target_permno].copy()
    special_div = permno_divs[permno_divs['time_avail_m'] == target_date]
    
    if len(special_div) > 0:
        cd3_val = special_div['cd3'].iloc[0]
        divamt = special_div['divamt'].iloc[0]
        print(f"  Special dividend: cd3={cd3_val}, divamt={divamt}")
        
        if cd3_val >= 6:
            print(f"  *** Still has cd3 >= 6 issue - this month should be filtered out ***")
            print(f"  *** But Stata expects DivSeason=0 for this observation ***")
            print(f"  *** This suggests Stata handles special dividends differently ***")

if __name__ == "__main__":
    debug_remaining_5()
    analyze_patterns()
    check_specific_cd3_issues()