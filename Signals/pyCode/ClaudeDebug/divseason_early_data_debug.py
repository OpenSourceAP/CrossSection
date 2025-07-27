# ABOUTME: Debug DivSeason early data handling for missing observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_early_data_debug.py

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import asrol

def debug_divseason_early_data():
    """Debug how DivSeason handles early data for missing observations"""
    
    print("=== DivSeason Early Data Debug ===")
    
    # Focus on permno 12072 around 198807-198901 (easier to understand)
    target_permno = 12072
    
    print(f"Debugging permno {target_permno}")
    
    # Replicate the DivSeason logic step by step
    
    # PREP DISTRIBUTIONS DATA
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    
    # Keep if cd1 == 1 & cd2 == 2 (regular cash dividends)
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    
    # Select timing variable and convert to monthly
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Check this permno's distributions data
    permno_dist = dist_df[dist_df['permno'] == target_permno]
    print(f"Distributions for permno {target_permno}: {len(permno_dist)}")
    if len(permno_dist) > 0:
        print("Distribution data:")
        print(permno_dist[['time_avail_m', 'cd3', 'divamt']].head(10).to_string())
    
    # Sum across all frequency codes
    tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()
    
    # Clean up two-frequency permno-months
    tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
    tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()
    
    # DATA LOAD - focus on our target permno around the problem dates
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m']].copy()
    
    # Filter to target permno and around the problem dates
    problem_start = pd.to_datetime('1988-01-01')
    problem_end = pd.to_datetime('1990-01-01')
    
    df_target = df[
        (df['permno'] == target_permno) &
        (df['time_avail_m'] >= problem_start) &
        (df['time_avail_m'] <= problem_end)
    ].copy()
    
    print(f"\nSignalMasterTable entries for permno {target_permno} (1988-1989):")
    print(df_target.to_string())
    
    # Merge with dividend amounts
    df_target = df_target.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
    
    print(f"\nAfter merging with dividend data:")
    print(df_target[['permno', 'time_avail_m', 'cd3', 'divamt']].to_string())
    
    # Sort for lag operations
    df_target = df_target.sort_values(['permno', 'time_avail_m'])
    
    # Fill missing cd3 with previous value (this is the key step)
    df_target['cd3'] = df_target.groupby('permno')['cd3'].fillna(method='ffill')
    
    print(f"\nAfter cd3 fillna:")
    print(df_target[['permno', 'time_avail_m', 'cd3', 'divamt']].to_string())
    
    # Replace missing dividend amounts with 0
    df_target['divamt'] = df_target['divamt'].fillna(0)
    
    # Create dividend paid indicator
    df_target['divpaid'] = (df_target['divamt'] > 0).astype(int)
    
    print(f"\nAfter creating divpaid:")
    print(df_target[['permno', 'time_avail_m', 'cd3', 'divamt', 'divpaid']].to_string())
    
    # Drop monthly dividends (cd3 == 2) and keep cd3 < 6
    print(f"Before filtering: {len(df_target)} rows")
    df_target = df_target[df_target['cd3'] != 2]
    print(f"After dropping cd3==2: {len(df_target)} rows")
    df_target = df_target[df_target['cd3'] < 6]
    print(f"After keeping cd3<6: {len(df_target)} rows")
    
    if len(df_target) == 0:
        print("*** NO DATA REMAINING - This is why observations are missing! ***")
        print("The cd3 filtering is removing all observations")
        return
    
    # Continue with signal construction
    df_target = asrol(df_target, 'permno', 'time_avail_m', 'divpaid', 12, stat='sum', new_col_name='div12')
    
    # Initialize DivSeason to 0 if div12 > 0
    df_target['DivSeason'] = np.where(df_target['div12'] > 0, 0, np.nan)
    
    print(f"\nFinal result:")
    print(df_target[['permno', 'time_avail_m', 'cd3', 'divpaid', 'div12', 'DivSeason']].to_string())

def check_cd3_filtering_issue():
    """Check if the cd3 filtering is the main issue"""
    
    print("\n=== CD3 Filtering Issue Check ===")
    
    # The issue might be:
    # 1. cd3 is NaN for early periods (no distributions yet)
    # 2. cd3.fillna(method='ffill') doesn't help if the first value is NaN  
    # 3. cd3 filtering removes all observations
    
    # Check what happens when cd3 is all NaN
    target_permno = 12072
    
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[df['permno'] == target_permno][['permno', 'time_avail_m']].copy()
    
    # Focus on early period before distributions start
    early_period = df[df['time_avail_m'] < '1986-10-01']  # Before distributions start
    
    print(f"Early SMT entries for permno {target_permno} (before distributions):")
    print(early_period.head(10).to_string())
    
    # These would get cd3=NaN after merge, then fillna would still be NaN
    # Then cd3 filtering would remove them all
    
    print("\nThis explains the missing observations:")
    print("1. SMT has entries before distributions start")
    print("2. Merge with distributions gives cd3=NaN")
    print("3. fillna(method='ffill') can't fill if first value is NaN") 
    print("4. cd3 filtering (cd3 != 2 and cd3 < 6) removes NaN values")
    print("5. Result: missing observations")

if __name__ == "__main__":
    debug_divseason_early_data()
    check_cd3_filtering_issue()