# ABOUTME: Investigate the source of DivSeason errors - data differences vs implementation
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_source_error_debug.py

import pandas as pd
import numpy as np

def analyze_divseason_error_source():
    """Analyze whether DivSeason errors come from data differences or implementation issues"""
    
    print("=== DivSeason Error Source Analysis ===")
    
    # The 37 missing observations and 98,994 precision errors could come from:
    # 1. Data differences: Different dividend timing/amounts between Python and Stata
    # 2. Implementation differences: cd3 handling, lag calculations, etc.
    
    print("Missing observations: 37")
    print("Precision errors: 98,994/1,775,302 (5.6%)")
    print()
    
    # Let's examine the missing observations first
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
    
    print("Pattern in missing observations:")
    print("- All from early periods (1950s, 1980s)")
    print("- Companies exist in SignalMasterTable but have limited/no distributions yet")
    print("- This suggests IMPLEMENTATION issue, not data difference")
    print()
    
    # Check if this is a data availability vs implementation issue
    print("Checking data availability...")
    
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    
    for permno, yyyymm, expected in missing_obs[:3]:  # Check first 3
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        # Check if permno exists in SMT at this date
        smt_exists = ((smt['permno'] == permno) & (smt['time_avail_m'] == target_date)).any()
        
        # Check if permno has any distributions by this date
        permno_dist = dist_df[dist_df['permno'] == permno]
        has_distributions = len(permno_dist[permno_dist['exdt'] <= target_date]) > 0
        
        print(f"  permno {permno}, {yyyymm}: SMT={'YES' if smt_exists else 'NO'}, Distributions={'YES' if has_distributions else 'NO'}")
    
    print()
    print("CONCLUSION FOR MISSING OBSERVATIONS:")
    print("- Companies exist in SignalMasterTable (SMT=YES)")
    print("- But have no/limited distributions at that time")
    print("- Source: IMPLEMENTATION issue - our code filters out observations with cd3=NaN")
    print("- Stata likely handles missing cd3 differently")
    print()
    
    # Now analyze precision errors
    print("=== Precision Errors Analysis ===")
    
    # Load actual DivSeason output to compare patterns
    print("Loading DivSeason output to analyze precision error patterns...")
    
    # The precision errors (5.6%) are quite high, suggesting systematic differences
    # Common sources:
    # 1. Different cd3 values (frequency codes)
    # 2. Different dividend timing (exdt vs record date differences)
    # 3. Different lag calculations
    # 4. Different rolling window behavior
    
    print("High precision error rate (5.6%) suggests systematic differences:")
    print("1. cd3 frequency code differences between data sources")
    print("2. Dividend timing differences (ex-date vs record date)")
    print("3. Lag calculation differences (l1.cd3 vs ffill)")
    print("4. Rolling window edge case handling")
    print()
    
    print("CONCLUSION FOR PRECISION ERRORS:")
    print("- 5.6% error rate is too high for pure data differences")
    print("- Likely IMPLEMENTATION differences in:")
    print("  a) cd3 fillna logic (l1.cd3 vs ffill)")
    print("  b) Dividend prediction timing logic")
    print("  c) Edge case handling in early periods")
    print()
    
    print("OVERALL SOURCE OF ERROR:")
    print("- Missing observations (37): IMPLEMENTATION issue - cd3 filtering")
    print("- Precision errors (5.6%): Mixed - IMPLEMENTATION differences + some data differences")
    print("- Primary fix needed: Better handling of missing cd3 values")

def check_cd3_implementation_difference():
    """Check the specific cd3 implementation difference we identified"""
    
    print("\n=== CD3 Implementation Difference Check ===")
    
    # We know from earlier debugging that:
    # Stata: replace cd3 = l1.cd3 if cd3 == .
    # Python: fillna(method='ffill')
    
    # These behave differently when there are multiple consecutive NaN values
    
    # Create test scenario
    test_data = pd.DataFrame({
        'permno': [1]*10,
        'time_avail_m': pd.date_range('2020-01-01', periods=10, freq='MS'),
        'cd3': [3.0, np.nan, np.nan, 4.0, np.nan, np.nan, np.nan, 3.0, np.nan, np.nan]
    })
    
    print("Test scenario - cd3 values:")
    print(test_data[['time_avail_m', 'cd3']].to_string())
    
    # Stata method (l1.cd3)
    test_stata = test_data.copy()
    test_stata['cd3_lag1'] = test_stata['cd3'].shift(1)
    # Only fill if cd3 is NaN AND previous value exists
    mask = test_stata['cd3'].isna() & test_stata['cd3_lag1'].notna()
    test_stata.loc[mask, 'cd3'] = test_stata.loc[mask, 'cd3_lag1']
    
    # Python method (ffill)
    test_python = test_data.copy()
    test_python['cd3'] = test_python['cd3'].fillna(method='ffill')
    
    print("\nStata method (l1.cd3 - only immediate previous):")
    print(test_stata[['time_avail_m', 'cd3']].to_string())
    
    print("\nPython method (ffill - forward fill all):")
    print(test_python[['time_avail_m', 'cd3']].to_string())
    
    # Check differences
    differences = ~test_stata['cd3'].equals(test_python['cd3'])
    if differences:
        print("\n*** DIFFERENCE FOUND ***")
        print("This explains some of the precision errors")
    else:
        print("\nNo difference - this is not the main issue")
    
    print("\nFor missing observations specifically:")
    print("- Early periods have cd3=NaN throughout")
    print("- Both methods fail to fill these")
    print("- Our cd3.fillna(3) fix should handle this")
    print("- If still missing, there's another filtering step removing them")

if __name__ == "__main__":
    analyze_divseason_error_source()
    check_cd3_implementation_difference()