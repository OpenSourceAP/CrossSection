# ABOUTME: Debug DivInit logic step by step
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divinit_logic_debug.py

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import asrol

def debug_divinit_step_by_step():
    """Debug DivInit logic step by step for specific failing observations"""
    
    print("=== DivInit Step-by-Step Debug ===")
    
    # Focus on permno 13563 around 202204
    target_permno = 13563
    
    # PREP DISTRIBUTIONS DATA (exactly like the script)
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[(dist_df['cd2'] == 2) | (dist_df['cd2'] == 3)]
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Sum dividends by permno and time_avail_m
    tempdivamt = dist_df.groupby(['permno', 'time_avail_m'])['divamt'].sum().reset_index()
    
    # Focus on our target permno
    target_divs = tempdivamt[tempdivamt['permno'] == target_permno].copy()
    target_divs = target_divs.sort_values('time_avail_m')
    
    print(f"All dividend data for permno {target_permno}:")
    print(target_divs.to_string())
    
    # DATA LOAD
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'shrcd']].copy()
    
    # Filter to our target permno and around the problem date
    target_date = pd.to_datetime('2022-04-01')  # 202204
    df_target = df[
        (df['permno'] == target_permno) &
        (df['time_avail_m'] >= target_date - pd.DateOffset(months=36)) &
        (df['time_avail_m'] <= target_date + pd.DateOffset(months=6))
    ].copy()
    
    print(f"\nSignalMasterTable entries around 202204 for permno {target_permno}:")
    print(df_target[['permno', 'time_avail_m']].to_string())
    
    # Merge with dividend amounts
    df_target = df_target.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
    
    # Replace missing dividend amounts with 0
    df_target['divamt'] = df_target['divamt'].fillna(0)
    
    print(f"\nAfter merging dividends:")
    print(df_target[['permno', 'time_avail_m', 'divamt']].to_string())
    
    # Rolling 24-month sum of dividends using asrol
    df_target = asrol(df_target, 'permno', 'time_avail_m', 'divamt', 24, stat='sum', new_col_name='divsum')
    
    print(f"\nAfter 24-month rolling sum:")
    print(df_target[['permno', 'time_avail_m', 'divamt', 'divsum']].to_string())
    
    # Sort by permno and time_avail_m for lag calculation
    df_target = df_target.sort_values(['permno', 'time_avail_m'])
    
    # Create dividend initiation indicator
    df_target['divsum_lag1'] = df_target.groupby('permno')['divsum'].shift(1)
    df_target['temp'] = (df_target['divamt'] > 0) & (df_target['divsum_lag1'] == 0)
    df_target['temp'] = df_target['temp'].fillna(False)
    
    print(f"\nAfter creating temp (divamt > 0 & l1.divsum == 0):")
    print(df_target[['permno', 'time_avail_m', 'divamt', 'divsum', 'divsum_lag1', 'temp']].to_string())
    
    # Keep for 6 months using asrol
    df_target = asrol(df_target, 'permno', 'time_avail_m', 'temp', 6, stat='sum', new_col_name='initsum')
    
    # Create final DivInit signal (initsum == 1)
    df_target['DivInit'] = (df_target['initsum'] == 1).astype(int)
    
    print(f"\nFinal result with DivInit:")
    print(df_target[['permno', 'time_avail_m', 'divamt', 'divsum', 'divsum_lag1', 'temp', 'initsum', 'DivInit']].to_string())
    
    # Check specifically for 202204
    target_row = df_target[df_target['time_avail_m'] == target_date]
    if len(target_row) > 0:
        print(f"\nSpecific result for 202204:")
        print(f"  divamt: {target_row['divamt'].iloc[0]}")
        print(f"  divsum: {target_row['divsum'].iloc[0]}")
        print(f"  divsum_lag1: {target_row['divsum_lag1'].iloc[0]}")
        print(f"  temp: {target_row['temp'].iloc[0]}")
        print(f"  initsum: {target_row['initsum'].iloc[0]}")
        print(f"  DivInit: {target_row['DivInit'].iloc[0]}")
        print(f"  Expected: 1 (from Stata)")
    else:
        print(f"\nNo data found for 202204 - this might be the issue!")

def check_boolean_vs_integer():
    """Check if there are boolean vs integer conversion issues"""
    
    print("\n=== Boolean vs Integer Conversion Check ===")
    
    # Check if the temp variable is being handled correctly
    # In Stata: gen temp = divamt > 0 & l1.divsum == 0
    # This creates a boolean that's treated as 0/1
    # In Python: (df['divamt'] > 0) & (df['divsum_lag1'] == 0)
    # This creates a boolean that needs explicit conversion
    
    # Test with sample data
    test_data = pd.DataFrame({
        'divamt': [0.1, 0, 0, 0.2, 0],
        'divsum_lag1': [0, 0, 0.1, 0, 0.2]
    })
    
    # Python boolean logic
    test_data['temp_bool'] = (test_data['divamt'] > 0) & (test_data['divsum_lag1'] == 0)
    test_data['temp_int'] = test_data['temp_bool'].astype(int)
    
    print("Test boolean vs integer conversion:")
    print(test_data.to_string())
    
    # Check if this affects the rolling sum
    print("\nRolling sum of boolean vs int:")
    print(f"Boolean rolling sum: {test_data['temp_bool'].rolling(3).sum().tolist()}")
    print(f"Integer rolling sum: {test_data['temp_int'].rolling(3).sum().tolist()}")

if __name__ == "__main__":
    debug_divinit_step_by_step()
    check_boolean_vs_integer()