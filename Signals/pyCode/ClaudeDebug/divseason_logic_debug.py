# ABOUTME: Debug DivSeason logic differences between Python and Stata
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_logic_debug.py

import pandas as pd
import numpy as np

def debug_cd3_logic():
    """Debug the cd3 frequency code logic and fillna differences"""
    
    print("=== DivSeason cd3 Logic Debug ===")
    
    # Focus on the missing observations - early dates with issues
    missing_permno = 10209  # From the test output
    missing_dates = ['1950-09-01', '1950-10-01', '1950-11-01']
    
    print(f"Debugging permno {missing_permno} around missing dates")
    
    # Load and replicate the DivSeason logic step by step
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    
    # Apply Stata filters
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    
    # Convert timing
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Check this permno's data
    permno_dist = dist_df[dist_df['permno'] == missing_permno].copy()
    print(f"Distributions data for permno {missing_permno}: {len(permno_dist)} rows")
    
    if len(permno_dist) > 0:
        # Check around the missing dates
        early_data = permno_dist[permno_dist['time_avail_m'] <= '1951-01-01']
        early_data = early_data.sort_values('time_avail_m')
        print("Early distributions data:")
        print(early_data[['time_avail_m', 'cd3', 'divamt']])
    
    # Sum across frequency codes (gcollapse in Stata)
    tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()
    
    # Clean up two-frequency permno-months (Stata logic)
    # Stata: sort permno time_avail_m cd3; by permno time_avail_m: keep if _n == 1
    tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
    tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()
    
    print(f"\nAfter collapse and cleanup: {len(tempdivamt)} rows")
    
    # Check this permno after cleanup
    permno_clean = tempdivamt[tempdivamt['permno'] == missing_permno]
    if len(permno_clean) > 0:
        early_clean = permno_clean[permno_clean['time_avail_m'] <= '1951-01-01']
        print("After cleanup (early data):")
        print(early_clean[['time_avail_m', 'cd3', 'divamt']])

def debug_cd3_fillna_logic():
    """Debug the cd3 fillna logic - lag vs forward-fill difference"""
    
    print("\n=== CD3 Fillna Logic Debug ===")
    
    # The key difference:
    # Stata: replace cd3 = l1.cd3 if cd3 == .  (use PREVIOUS period's cd3)
    # Python: fillna(method='ffill')  (use PREVIOUS non-null cd3)
    
    # These are similar but not identical if there are multiple missing periods
    
    # Create test data to show the difference
    test_data = pd.DataFrame({
        'permno': [1, 1, 1, 1, 1],
        'time_avail_m': pd.date_range('2020-01-01', periods=5, freq='MS'),
        'cd3': [3.0, np.nan, np.nan, 4.0, np.nan]
    })
    
    print("Test data:")
    print(test_data)
    
    # Stata method: cd3 = l1.cd3 if cd3 == .
    test_data_stata = test_data.copy()
    test_data_stata['cd3_lag1'] = test_data_stata['cd3'].shift(1)
    test_data_stata['cd3_stata'] = test_data_stata['cd3'].fillna(test_data_stata['cd3_lag1'])
    
    # Python method: fillna(method='ffill')
    test_data_python = test_data.copy()
    test_data_python['cd3_python'] = test_data_python['cd3'].fillna(method='ffill')
    
    print("\nStata method (l1.cd3):")
    print(test_data_stata[['time_avail_m', 'cd3', 'cd3_lag1', 'cd3_stata']])
    
    print("\nPython method (ffill):")
    print(test_data_python[['time_avail_m', 'cd3', 'cd3_python']])
    
    # Check if they're different
    if not test_data_stata['cd3_stata'].equals(test_data_python['cd3_python']):
        print("\n*** DIFFERENCE FOUND: Stata l1.cd3 != Python ffill ***")
        print("This could explain some of the precision differences")
    else:
        print("\nSame result - not the main issue")

def debug_recent_bad_observations():
    """Debug recent bad observations to understand the pattern"""
    
    print("\n=== Recent Bad Observations Debug ===")
    
    # From test output: permno 22515, 202412 (Python=0, Stata=1)
    problem_permno = 22515
    problem_date = '2024-12-01'
    
    print(f"Debugging permno {problem_permno}, {problem_date}")
    print("Expected: Python=0, Stata=1 (Python missing a dividend prediction)")
    
    # This suggests Python is NOT predicting a dividend when Stata IS
    # This means the lag conditions are failing in Python
    
    # Check the dividend payment history for this permno
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Check this permno's dividend history
    permno_div = dist_df[dist_df['permno'] == problem_permno].copy()
    permno_div = permno_div.sort_values('time_avail_m')
    
    print(f"Dividend history for permno {problem_permno}: {len(permno_div)} observations")
    
    if len(permno_div) > 0:
        # Check recent dividends (last 24 months)
        recent_div = permno_div[permno_div['time_avail_m'] >= '2023-01-01']
        print("Recent dividend history:")
        print(recent_div[['time_avail_m', 'cd3', 'divamt']].tail(10))
        
        # For quarterly dividends (cd3=3), we expect dividends every 3 months
        # If there was a dividend 3 months ago (Sep 2024), we'd expect one in Dec 2024
        
        # Check if there were dividends at the expected lag periods for quarterly (2, 5, 8, 11 months ago)
        target_date = pd.to_datetime(problem_date)
        lag_dates = [target_date - pd.DateOffset(months=lag) for lag in [2, 5, 8, 11]]
        
        print(f"\nChecking for dividends at lag dates (for {problem_date}):")
        for i, lag_date in enumerate([2, 5, 8, 11]):
            check_date = target_date - pd.DateOffset(months=lag_date)
            check_month = check_date.to_period('M').start_time
            
            div_at_date = permno_div[permno_div['time_avail_m'] == check_month]
            has_div = len(div_at_date) > 0 and (div_at_date['divamt'] > 0).any()
            
            print(f"  {lag_date} months ago ({check_month.strftime('%Y-%m')}): {'YES' if has_div else 'NO'}")

if __name__ == "__main__":
    debug_cd3_logic()
    debug_cd3_fillna_logic()
    debug_recent_bad_observations()