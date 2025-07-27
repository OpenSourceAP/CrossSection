# ABOUTME: Debug what DivSeason values the missing observations should have
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_values_debug.py

import pandas as pd
import numpy as np

def check_missing_observation_values():
    """Check what values the missing observations should have according to Stata"""
    
    print("=== Missing Observation Values Debug ===")
    
    # From test output, missing observations are:
    missing_obs = [
        (10209, 195009, 0),
        (10209, 195010, 0), 
        (10209, 195011, 1),
        (12072, 198807, 1),
        (12072, 198808, 1),
        (12072, 198809, 1),
        (12072, 198810, 1),
        (12072, 198811, 1),
        (12072, 198812, 1),
        (12072, 198901, 1)
    ]
    
    print("Missing observations and their expected Stata values:")
    for permno, yyyymm, expected_value in missing_obs:
        print(f"  permno {permno}, {yyyymm}: expected DivSeason = {expected_value}")
    
    # The key insight: some are expected to be 0, some are expected to be 1
    # This means the logic should produce SOME output for these observations
    # But currently they're being filtered out entirely
    
    # The problem might be that even with cd3=3, other conditions aren't met
    # Let me check what conditions are needed for DivSeason=1:
    
    print("\nConditions for DivSeason=1:")
    print("temp3: (cd3 in [0,1,3]) & (divpaid_lag2==1 | divpaid_lag5==1 | divpaid_lag8==1 | divpaid_lag11==1)")
    print("temp4: (cd3==4) & (divpaid_lag5==1 | divpaid_lag11==1)")  
    print("temp5: (cd3==5) & (divpaid_lag11==1)")
    print("DivSeason = 1 if temp3 | temp4 | temp5")
    
    print("\nConditions for DivSeason=0:")
    print("DivSeason = 0 if div12 > 0 (had dividend in last 12 months)")
    
    print("\nFor early periods with no distributions:")
    print("- cd3 = 3 (quarterly, after our fix)")
    print("- divamt = 0 (no dividends)")
    print("- divpaid = 0 (no dividends)")
    print("- div12 = 0 (no dividends in last 12 months)")
    print("- divpaid_lag2, lag5, lag8, lag11 = 0 (no dividends in past)")
    print("- temp3 = False (no past dividends)")
    print("- DivSeason should be NaN (div12 == 0, so not assigned 0 or 1)")
    
    print("\n*** INSIGHT: Early periods with no dividends should get DivSeason=NaN ***")
    print("*** But Stata expects some of them to be 0 or 1 ***")
    print("*** This suggests Stata handles early data differently ***")

def debug_specific_case():
    """Debug a specific case to understand the pattern"""
    
    print("\n=== Specific Case Debug ===")
    
    # Focus on permno 10209, 195011 which should be DivSeason=1
    # For this to be 1, it needs:
    # temp3 = (cd3 in [0,1,3]) & (divpaid 2,5,8,or 11 months ago)
    
    print("Permno 10209, 195011 (Nov 1950) should be DivSeason=1")
    print("For temp3=True, need dividend 2,5,8,or 11 months ago:")
    print("- 2 months ago: Sep 1950")
    print("- 5 months ago: Jun 1950") 
    print("- 8 months ago: Mar 1950")
    print("- 11 months ago: Dec 1949")
    
    # From our earlier debug, permno 10209 has distributions:
    # 1949-09-13, 1949-12-05, 1950-03-13, 1950-06-12, 1950-09-12, etc.
    
    print("\nActual distributions around this time:")
    print("- Dec 1949: 1949-12-05 (YES - 11 months ago)")
    print("- Mar 1950: 1950-03-13 (YES - 8 months ago)")
    print("- Jun 1950: 1950-06-12 (YES - 5 months ago)")
    print("- Sep 1950: 1950-09-12 (YES - 2 months ago)")
    
    print("\nSo temp3 should be True, DivSeason should be 1")
    print("But our Python code is filtering this out entirely")
    print("The issue might be in how the exdt->time_avail_m conversion works")
    
    print("\nNext step: Check if the monthly conversion is causing timing issues")

if __name__ == "__main__":
    check_missing_observation_values()
    debug_specific_case()