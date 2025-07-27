# ABOUTME: Debug DivSeason missing 37 observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_missing_debug.py

import pandas as pd
import numpy as np

def debug_divseason_missing():
    """Debug the 37 missing observations in DivSeason"""
    
    print("=== DivSeason Missing Observations Debug ===")
    
    # Focus on the missing observations from test output:
    # permno 10209, 195009-195011
    # permno 12072, 198807-198901
    
    missing_cases = [
        (10209, [195009, 195010, 195011]),
        (12072, [198807, 198808, 198809, 198810, 198811, 198812, 198901])
    ]
    
    for permno, missing_months in missing_cases:
        print(f"\n--- Debugging permno {permno} ---")
        
        # Check if this permno exists in SignalMasterTable
        smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
        smt_permno = smt[smt['permno'] == permno]
        
        print(f"SignalMasterTable entries for permno {permno}: {len(smt_permno)}")
        
        if len(smt_permno) > 0:
            # Check the date range
            min_date = smt_permno['time_avail_m'].min()
            max_date = smt_permno['time_avail_m'].max()
            print(f"Date range: {min_date} to {max_date}")
            
            # Check if the missing months are in this range
            for yyyymm in missing_months:
                year = yyyymm // 100
                month = yyyymm % 100
                target_date = pd.to_datetime(f"{year}-{month:02d}-01")
                
                exists_in_smt = (smt_permno['time_avail_m'] == target_date).any()
                print(f"  {yyyymm} ({target_date.strftime('%Y-%m')}): {'EXISTS' if exists_in_smt else 'MISSING'} in SMT")
        
        # Check dividend distributions for this permno
        dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
        dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
        
        permno_dist = dist_df[dist_df['permno'] == permno]
        print(f"Distribution entries for permno {permno}: {len(permno_dist)}")
        
        if len(permno_dist) > 0:
            # Look at dates around the missing months
            for yyyymm in missing_months[:3]:  # Just check first 3 to save space
                year = yyyymm // 100
                month = yyyymm % 100
                target_date = pd.to_datetime(f"{year}-{month:02d}-01")
                
                # Check ±12 months around target
                nearby_dist = permno_dist[
                    (permno_dist['exdt'] >= target_date - pd.DateOffset(months=12)) &
                    (permno_dist['exdt'] <= target_date + pd.DateOffset(months=12))
                ]
                
                if len(nearby_dist) > 0:
                    print(f"  Distributions around {yyyymm}:")
                    print(nearby_dist[['exdt', 'cd3', 'divamt']].to_string())

def check_early_data_availability():
    """Check if the issue is with early data availability"""
    
    print("\n=== Early Data Availability Check ===")
    
    # The missing observations seem to be in very early dates (1950s, 1980s)
    # This might be a data availability issue
    
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    
    # Check the earliest dates in SignalMasterTable
    earliest_dates = smt.groupby('permno')['time_avail_m'].min().sort_values()
    print("Earliest dates for first 10 permnos:")
    print(earliest_dates.head(10))
    
    # Check permnos that start very early
    early_permnos = earliest_dates[earliest_dates <= '1960-01-01']
    print(f"\nNumber of permnos starting before 1960: {len(early_permnos)}")
    
    if len(early_permnos) > 0:
        print("Sample early permnos:")
        print(early_permnos.head())
    
    # Check distributions data availability
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    
    earliest_dist = dist_df.groupby('permno')['exdt'].min().sort_values()
    print(f"\nEarliest distribution dates for first 10 permnos:")
    print(earliest_dist.head(10))
    
    # Check overlap between SMT and distributions for problem permnos
    problem_permnos = [10209, 12072]
    
    for permno in problem_permnos:
        smt_start = smt[smt['permno'] == permno]['time_avail_m'].min() if permno in smt['permno'].values else None
        dist_start = dist_df[dist_df['permno'] == permno]['exdt'].min() if permno in dist_df['permno'].values else None
        
        print(f"\nPermno {permno}:")
        print(f"  SMT start: {smt_start}")
        print(f"  Dist start: {dist_start}")

if __name__ == "__main__":
    debug_divseason_missing()
    check_early_data_availability()