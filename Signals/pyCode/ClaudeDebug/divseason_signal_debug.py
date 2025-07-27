# ABOUTME: Debug DivSeason signal construction to find where observations are lost
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_signal_debug.py

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import asrol

def debug_divseason_signal_construction():
    """Debug the signal construction phase where observations are lost"""
    
    print("=== DivSeason Signal Construction Debug ===")
    
    # Continue from where the previous debug left off
    target_permno = 12072
    problem_dates = [198807, 198808, 198809, 198810, 198811, 198812, 198901]
    
    # Replicate the prep work quickly
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()
    tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
    tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()
    
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m']].copy()
    
    # Focus on a broader time range around the target permno to get context
    df_target = df[
        (df['permno'] == target_permno) &
        (df['time_avail_m'] >= '1988-01-01') &
        (df['time_avail_m'] <= '1990-01-01')
    ].copy()
    
    df_target = df_target.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
    df_target = df_target.sort_values(['permno', 'time_avail_m'])
    
    # Apply the processing
    df_target['cd3'] = df_target.groupby('permno')['cd3'].fillna(method='ffill')
    df_target['divamt'] = df_target['divamt'].fillna(0)
    df_target['cd3'] = df_target['cd3'].fillna(3)  # My fix
    df_target['divpaid'] = (df_target['divamt'] > 0).astype(int)
    
    # Apply filters
    df_target = df_target[df_target['cd3'] != 2]
    df_target = df_target[df_target['cd3'] < 6]
    
    print(f"After filtering: {len(df_target)} observations for permno {target_permno}")
    
    print("\nStep 6: SIGNAL CONSTRUCTION")
    
    # Rolling 12-month sum of dividends
    df_target = asrol(df_target, 'permno', 'time_avail_m', 'divpaid', 12, stat='sum', new_col_name='div12')
    
    print("After div12 calculation:")
    problem_date_objs = [pd.to_datetime(f"{d//100}-{d%100:02d}-01") for d in problem_dates]
    for date_obj in problem_date_objs:
        row = df_target[df_target['time_avail_m'] == date_obj]
        if len(row) > 0:
            yyyymm = date_obj.year * 100 + date_obj.month
            print(f"  {yyyymm}: div12={row['div12'].iloc[0]}")
    
    # Initialize DivSeason to 0 if div12 > 0
    df_target['DivSeason'] = np.where(df_target['div12'] > 0, 0, np.nan)
    
    print("After initial DivSeason assignment:")
    for date_obj in problem_date_objs:
        row = df_target[df_target['time_avail_m'] == date_obj]
        if len(row) > 0:
            yyyymm = date_obj.year * 100 + date_obj.month
            divseason = row['DivSeason'].iloc[0]
            divseason_str = str(divseason) if pd.notna(divseason) else 'NaN'
            print(f"  {yyyymm}: DivSeason={divseason_str}")
    
    # Create lags for dividend prediction logic
    for lag in [2, 5, 8, 11]:
        df_target[f'divpaid_lag{lag}'] = df_target.groupby('permno')['divpaid'].shift(lag)
    
    # temp3: quarterly, unknown, or missing frequency with expected dividend timing
    df_target['temp3'] = ((df_target['cd3'].isin([0, 1, 3])) & 
                          ((df_target['divpaid_lag2'] == 1) | (df_target['divpaid_lag5'] == 1) | 
                           (df_target['divpaid_lag8'] == 1) | (df_target['divpaid_lag11'] == 1))).astype(int)
    
    # temp4: semi-annual (cd3 == 4) with dividends 5 or 11 months ago
    df_target['temp4'] = ((df_target['cd3'] == 4) & 
                          ((df_target['divpaid_lag5'] == 1) | (df_target['divpaid_lag11'] == 1))).astype(int)
    
    # temp5: annual (cd3 == 5) with dividend 11 months ago
    df_target['temp5'] = ((df_target['cd3'] == 5) & (df_target['divpaid_lag11'] == 1)).astype(int)
    
    # Replace DivSeason = 1 if any temp condition is met
    df_target.loc[(df_target['temp3'] == 1) | (df_target['temp4'] == 1) | (df_target['temp5'] == 1), 'DivSeason'] = 1
    
    print("After dividend prediction logic:")
    for date_obj in problem_date_objs:
        row = df_target[df_target['time_avail_m'] == date_obj]
        if len(row) > 0:
            yyyymm = date_obj.year * 100 + date_obj.month
            divseason = row['DivSeason'].iloc[0]
            temp3 = row['temp3'].iloc[0]
            temp4 = row['temp4'].iloc[0]
            temp5 = row['temp5'].iloc[0]
            div12 = row['div12'].iloc[0]
            divseason_str = str(divseason) if pd.notna(divseason) else 'NaN'
            print(f"  {yyyymm}: DivSeason={divseason_str}, temp3={temp3}, temp4={temp4}, temp5={temp5}, div12={div12}")
    
    # Final filtering - this might be where we lose them
    df_final = df_target[['permno', 'time_avail_m', 'DivSeason']].copy()
    print(f"\nBefore dropna: {len(df_final)} observations")
    
    df_final = df_final.dropna(subset=['DivSeason'])
    print(f"After dropna: {len(df_final)} observations")
    
    print("Final observations in problem date range:")
    for date_obj in problem_date_objs:
        row = df_final[df_final['time_avail_m'] == date_obj]
        if len(row) > 0:
            yyyymm = date_obj.year * 100 + date_obj.month
            print(f"  {yyyymm}: DivSeason={row['DivSeason'].iloc[0]}")
        else:
            yyyymm = date_obj.year * 100 + date_obj.month
            print(f"  {yyyymm}: MISSING (filtered out by dropna)")
    
    if len(df_final) == 0 or not any(df_final['time_avail_m'].isin(problem_date_objs)):
        print("\n*** FOUND THE ISSUE: Observations getting DivSeason=NaN and filtered out by dropna! ***")
        print("*** This means div12=0 (no dividends in 12 months) and no predicted dividends ***")
        print("*** But Stata expects these to have DivSeason=1 (predicted dividends) ***")

if __name__ == "__main__":
    debug_divseason_signal_construction()