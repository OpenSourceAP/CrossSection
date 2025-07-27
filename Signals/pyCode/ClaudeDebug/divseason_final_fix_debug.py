# ABOUTME: Final debug to fix DivSeason's 37 missing observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_final_fix_debug.py

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import asrol

def debug_divseason_missing_step_by_step():
    """Debug DivSeason logic step by step to find where the 37 observations are lost"""
    
    print("=== DivSeason Step-by-Step Debug ===")
    
    # Focus on the problematic permno 12072 from earlier debug
    target_permno = 12072
    problem_dates = [198807, 198808, 198809, 198810, 198811, 198812, 198901]
    
    print(f"Focusing on permno {target_permno}, dates {problem_dates}")
    
    # Replicate the exact DivSeason logic with detailed logging
    
    print("\nStep 1: PREP DISTRIBUTIONS DATA")
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    
    # Keep if cd1 == 1 & cd2 == 2 (regular cash dividends)
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    
    # Convert timing
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Check distributions for target permno
    target_dist = dist_df[dist_df['permno'] == target_permno]
    print(f"  Distributions for permno {target_permno}: {len(target_dist)}")
    if len(target_dist) > 0:
        print(f"  First distribution: {target_dist['time_avail_m'].min()}")
        print(f"  Last distribution: {target_dist['time_avail_m'].max()}")
    
    # Sum across all frequency codes
    tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()
    
    # Clean up two-frequency permno-months
    tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
    tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()
    
    print("\nStep 2: DATA LOAD")
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m']].copy()
    
    # Filter to target permno and problem dates
    problem_date_objs = [pd.to_datetime(f"{d//100}-{d%100:02d}-01") for d in problem_dates]
    df_target = df[
        (df['permno'] == target_permno) &
        (df['time_avail_m'].isin(problem_date_objs))
    ].copy()
    
    print(f"  SignalMasterTable entries for problem dates: {len(df_target)}")
    print("  Problem dates in SMT:")
    for _, row in df_target.iterrows():
        yyyymm = row['time_avail_m'].year * 100 + row['time_avail_m'].month
        print(f"    {yyyymm}")
    
    if len(df_target) == 0:
        print("  *** NO ENTRIES IN SMT - This explains the missing observations! ***")
        return
    
    print("\nStep 3: MERGE WITH DIVIDEND DATA")
    df_target = df_target.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
    
    print("  After merge:")
    for _, row in df_target.iterrows():
        yyyymm = row['time_avail_m'].year * 100 + row['time_avail_m'].month
        cd3 = row['cd3'] if pd.notna(row['cd3']) else 'NaN'
        divamt = row['divamt'] if pd.notna(row['divamt']) else 'NaN'
        print(f"    {yyyymm}: cd3={cd3}, divamt={divamt}")
    
    print("\nStep 4: CD3 PROCESSING")
    df_target = df_target.sort_values(['permno', 'time_avail_m'])
    
    # Fill missing cd3 with previous value
    df_target['cd3'] = df_target.groupby('permno')['cd3'].fillna(method='ffill')
    print("  After ffill:")
    for _, row in df_target.iterrows():
        yyyymm = row['time_avail_m'].year * 100 + row['time_avail_m'].month
        cd3 = row['cd3'] if pd.notna(row['cd3']) else 'NaN'
        print(f"    {yyyymm}: cd3={cd3}")
    
    # Replace missing dividend amounts with 0
    df_target['divamt'] = df_target['divamt'].fillna(0)
    
    # Handle cd3 = NaN for early periods (my fix)
    df_target['cd3'] = df_target['cd3'].fillna(3)
    print("  After fillna(3):")
    for _, row in df_target.iterrows():
        yyyymm = row['time_avail_m'].year * 100 + row['time_avail_m'].month
        cd3 = row['cd3']
        print(f"    {yyyymm}: cd3={cd3}")
    
    # Create dividend paid indicator
    df_target['divpaid'] = (df_target['divamt'] > 0).astype(int)
    
    print("\nStep 5: FILTERING")
    print(f"  Before filtering: {len(df_target)} rows")
    
    # Drop monthly dividends (cd3 == 2)
    df_target = df_target[df_target['cd3'] != 2]
    print(f"  After dropping cd3==2: {len(df_target)} rows")
    
    # Keep if cd3 < 6
    df_target = df_target[df_target['cd3'] < 6]
    print(f"  After keeping cd3<6: {len(df_target)} rows")
    
    if len(df_target) == 0:
        print("  *** ALL ROWS FILTERED OUT - This is the issue! ***")
        return
    
    print("  Remaining rows:")
    for _, row in df_target.iterrows():
        yyyymm = row['time_avail_m'].year * 100 + row['time_avail_m'].month
        print(f"    {yyyymm}: cd3={row['cd3']}, divpaid={row['divpaid']}")
    
    print("\nStep 6: SIGNAL CONSTRUCTION")
    # This is where we'd continue with the signal logic...
    
def check_current_implementation():
    """Check if my cd3.fillna(3) fix is actually working in the current code"""
    
    print("\n=== Current Implementation Check ===")
    
    # Run a quick version of DivSeason on the problematic permno
    target_permno = 12072
    
    # Load current DivSeason output
    try:
        current_output = pd.read_csv('../pyData/Predictors/DivSeason.csv')
        current_output = current_output.set_index(['permno', 'yyyymm'])
        
        # Check if target permno exists in current output
        target_in_output = target_permno in current_output.index.get_level_values('permno')
        print(f"  Permno {target_permno} in current output: {target_in_output}")
        
        if target_in_output:
            target_data = current_output[current_output.index.get_level_values('permno') == target_permno]
            print(f"  Observations for permno {target_permno}: {len(target_data)}")
            
            # Check specific problem dates
            problem_dates = [198807, 198808, 198809, 198810, 198811, 198812, 198901]
            for yyyymm in problem_dates:
                if (target_permno, yyyymm) in current_output.index:
                    value = current_output.loc[(target_permno, yyyymm), 'DivSeason']
                    print(f"    {yyyymm}: DivSeason = {value}")
                else:
                    print(f"    {yyyymm}: MISSING")
        
    except Exception as e:
        print(f"  Error loading current output: {e}")

if __name__ == "__main__":
    debug_divseason_missing_step_by_step()
    check_current_implementation()