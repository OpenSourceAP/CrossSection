# ABOUTME: Debug DivInit precision errors
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divinit_debug.py

import pandas as pd
import numpy as np

def debug_divinit_precision():
    """Debug specific failing observations from DivInit test"""
    
    print("=== DivInit Precision Debug ===")
    
    # From test output, the most recent bad observation:
    # permno 13563, 202204: Python=0, Stata=1 (diff=-1)
    
    problem_permno = 13563
    problem_date = 202204  # yyyymm format
    
    print(f"Debugging permno {problem_permno}, {problem_date}")
    print("Expected: Python=0, Stata=1 (Python missing a dividend initiation)")
    
    # Load the distributions data to trace the logic
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    
    # Apply Stata filters
    dist_df = dist_df[(dist_df['cd2'] == 2) | (dist_df['cd2'] == 3)]
    
    # Convert timing
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Check this permno's dividend history
    permno_dist = dist_df[dist_df['permno'] == problem_permno].copy()
    permno_dist = permno_dist.sort_values('time_avail_m')
    
    print(f"Dividend history for permno {problem_permno}: {len(permno_dist)} observations")
    
    if len(permno_dist) > 0:
        # Look around the problem date
        problem_month = pd.to_datetime(f"{problem_date//100}-{problem_date%100:02d}-01")
        
        # Check dividends around this time
        nearby_div = permno_dist[
            (permno_dist['time_avail_m'] >= problem_month - pd.DateOffset(months=36)) &
            (permno_dist['time_avail_m'] <= problem_month + pd.DateOffset(months=6))
        ]
        
        print(f"\nDividend history around {problem_date}:")
        if len(nearby_div) > 0:
            print(nearby_div[['time_avail_m', 'divamt', 'cd2']].to_string())
        else:
            print("No dividends found around this period")
        
        # Check for dividend initiation pattern:
        # divamt > 0 & l1.divsum == 0
        # This means: dividend this month AND no dividends in previous 24 months
        
        # For 202204 to be an initiation, there should be:
        # 1. A dividend in 202204 
        # 2. No dividends in the 24 months before 202204 (i.e., 202004-202203)
        
        div_in_target = permno_dist[permno_dist['time_avail_m'] == problem_month]
        print(f"\nDividend in target month {problem_date}: {len(div_in_target) > 0}")
        if len(div_in_target) > 0:
            print(f"  Amount: {div_in_target['divamt'].iloc[0]}")
        
        # Check 24 months before
        start_window = problem_month - pd.DateOffset(months=24)
        end_window = problem_month - pd.DateOffset(months=1)  # l1 = previous month
        
        div_in_window = permno_dist[
            (permno_dist['time_avail_m'] >= start_window) &
            (permno_dist['time_avail_m'] <= end_window)
        ]
        
        total_divs_24m = div_in_window['divamt'].sum() if len(div_in_window) > 0 else 0
        
        print(f"Total dividends in 24 months before {problem_date}: {total_divs_24m}")
        print(f"Should be initiation: divamt > 0 ({len(div_in_target) > 0}) & l1.divsum == 0 ({total_divs_24m == 0})")
        
        expected_initiation = (len(div_in_target) > 0) and (total_divs_24m == 0)
        print(f"Expected DivInit = 1: {expected_initiation}")

def debug_edge_cases():
    """Debug potential edge cases in the DivInit logic"""
    
    print("\n=== DivInit Edge Cases Debug ===")
    
    # The key difference might be in:
    # 1. How the 24-month rolling sum is calculated (asrol behavior)
    # 2. How missing values are handled in the lag calculation
    # 3. Boolean vs integer conversion differences
    
    # Check a few more problematic observations
    problem_obs = [
        (10234, 197906),  # Python=1, Stata=0 (opposite direction)
        (47546, 199408),  # Python=0, Stata=1 
        (51925, 199808),  # Python=1, Stata=0
    ]
    
    for permno, yyyymm in problem_obs:
        print(f"\n--- Checking permno {permno}, {yyyymm} ---")
        
        # Quick check without full logic - just see if there are dividends
        dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
        dist_df = dist_df[(dist_df['cd2'] == 2) | (dist_df['cd2'] == 3)]
        dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
        
        permno_data = dist_df[dist_df['permno'] == permno]
        target_month = pd.to_datetime(f"{yyyymm//100}-{yyyymm%100:02d}-01")
        
        # Check ±12 months around target
        nearby = permno_data[
            (permno_data['time_avail_m'] >= target_month - pd.DateOffset(months=12)) &
            (permno_data['time_avail_m'] <= target_month + pd.DateOffset(months=12))
        ].sort_values('time_avail_m')
        
        if len(nearby) > 0:
            print(f"Dividends ±12 months around {yyyymm}:")
            print(nearby[['time_avail_m', 'divamt']].to_string())
        else:
            print(f"No dividends found around {yyyymm}")

if __name__ == "__main__":
    debug_divinit_precision()
    debug_edge_cases()