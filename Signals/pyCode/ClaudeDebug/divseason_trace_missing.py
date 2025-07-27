# ABOUTME: Trace DivSeason logic for specific missing observations to find where they get filtered
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_trace_missing.py

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import asrol

def trace_specific_observation():
    """Trace a specific missing observation through the DivSeason logic"""
    
    print("=== Tracing DivSeason Logic for Missing Observation ===")
    
    # Let's trace permno 65293, 200912 (expected 0)
    target_permno = 65293
    target_yyyymm = 200912
    target_date = pd.to_datetime('2009-12-01')
    
    print(f"Tracing permno {target_permno}, {target_yyyymm}...")
    
    # Step 1: Check if it exists in SignalMasterTable
    print("\\nStep 1: SignalMasterTable")
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    target_smt = smt[(smt['permno'] == target_permno) & (smt['time_avail_m'] == target_date)]
    
    if len(target_smt) == 0:
        print("  *** NOT FOUND in SignalMasterTable ***")
        return
    else:
        print("  FOUND in SignalMasterTable")
    
    # Step 2: Run DivSeason logic step by step
    print("\\nStep 2: DivSeason Logic")
    
    # PREP DISTRIBUTIONS DATA
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    
    # Keep if cd1 == 1 & cd2 == 2 (regular cash dividends)
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    
    # Select timing variable and convert to monthly
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Sum across all frequency codes
    tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()
    
    # Clean up a handful of odd two-frequency permno-months
    tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
    tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()
    
    # Check if target permno has dividend data around target date
    print("\\nDividend data for target permno around target date:")
    permno_divs = tempdivamt[tempdivamt['permno'] == target_permno].copy()
    permno_divs['yyyymm'] = permno_divs['time_avail_m'].dt.year * 100 + permno_divs['time_avail_m'].dt.month
    
    # Show data around target date
    target_year = target_yyyymm // 100
    nearby_divs = permno_divs[
        (permno_divs['yyyymm'] >= (target_year - 2) * 100 + 1) & 
        (permno_divs['yyyymm'] <= (target_year + 1) * 100 + 12)
    ]
    
    if len(nearby_divs) > 0:
        print("  Found dividend data:")
        for _, row in nearby_divs.iterrows():
            print(f"    {row['yyyymm']}: cd3={row['cd3']}, divamt={row['divamt']:.3f}")
    else:
        print("  No dividend data found around target date")
    
    # DATA LOAD - Run full logic for this permno
    print("\\nStep 3: Full DivSeason logic for this permno")
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m']].copy()
    
    # Focus on target permno
    df_permno = df[df['permno'] == target_permno].copy()
    print(f"  SMT observations for permno {target_permno}: {len(df_permno)}")
    
    # Merge with dividend amounts
    df_permno = df_permno.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
    df_permno = df_permno.sort_values(['permno', 'time_avail_m'])
    
    # Fill missing cd3 with previous value
    df_permno['cd3'] = df_permno.groupby('permno')['cd3'].fillna(method='ffill')
    
    # Replace missing dividend amounts with 0
    df_permno['divamt'] = df_permno['divamt'].fillna(0)
    
    # Handle cd3 = NaN for early periods
    df_permno['cd3'] = df_permno['cd3'].fillna(3)
    
    # Create dividend paid indicator
    df_permno['divpaid'] = (df_permno['divamt'] > 0).astype(int)
    
    # Drop monthly dividends
    df_permno = df_permno[df_permno['cd3'] != 2]
    
    # Keep if cd3 < 6
    df_permno = df_permno[df_permno['cd3'] < 6]
    
    print(f"  After cd3 filters: {len(df_permno)} observations")
    
    # Check if target observation still exists
    target_row = df_permno[df_permno['time_avail_m'] == target_date]
    if len(target_row) == 0:
        print(f"  *** TARGET OBSERVATION FILTERED OUT BY cd3 logic ***")
        
        # Check what cd3 value caused the filter
        target_before_filter = df[df['permno'] == target_permno]
        target_before_filter = target_before_filter.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
        target_before_filter = target_before_filter.sort_values('time_avail_m')
        target_before_filter['cd3'] = target_before_filter.groupby('permno')['cd3'].fillna(method='ffill')
        target_before_filter['cd3'] = target_before_filter['cd3'].fillna(3)
        
        target_orig = target_before_filter[target_before_filter['time_avail_m'] == target_date]
        if len(target_orig) > 0:
            cd3_val = target_orig['cd3'].iloc[0]
            print(f"    cd3 value was: {cd3_val}")
            if cd3_val == 2:
                print("    *** FILTERED OUT: cd3 == 2 (monthly dividends) ***")
            elif cd3_val >= 6:
                print(f"    *** FILTERED OUT: cd3 >= 6 (cd3 = {cd3_val}) ***")
        return
    else:
        print(f"  Target observation survives cd3 filters")
        target_row = target_row.iloc[0]
        print(f"    cd3 = {target_row['cd3']}, divamt = {target_row['divamt']}, divpaid = {target_row['divpaid']}")
    
    # Continue with signal construction
    df_permno = asrol(df_permno, 'permno', 'time_avail_m', 'divpaid', 12, stat='sum', new_col_name='div12')
    
    # Initialize DivSeason
    df_permno['DivSeason'] = np.where(df_permno['div12'] > 0, 0, 0)
    
    # Check target observation after div12 calculation
    target_row = df_permno[df_permno['time_avail_m'] == target_date]
    if len(target_row) > 0:
        target_row = target_row.iloc[0]
        print(f"  After div12 calculation: div12 = {target_row['div12']}, DivSeason = {target_row['DivSeason']}")
    
    # Create lags for dividend prediction logic
    for lag in [2, 5, 8, 11]:
        df_permno[f'divpaid_lag{lag}'] = df_permno.groupby('permno')['divpaid'].shift(lag)
    
    # temp3: quarterly, unknown, or missing frequency with expected dividend timing
    df_permno['temp3'] = ((df_permno['cd3'].isin([0, 1, 3])) & 
                         ((df_permno['divpaid_lag2'] == 1) | (df_permno['divpaid_lag5'] == 1) | 
                          (df_permno['divpaid_lag8'] == 1) | (df_permno['divpaid_lag11'] == 1))).astype(int)
    
    # temp4: semi-annual
    df_permno['temp4'] = ((df_permno['cd3'] == 4) & 
                         ((df_permno['divpaid_lag5'] == 1) | (df_permno['divpaid_lag11'] == 1))).astype(int)
    
    # temp5: annual
    df_permno['temp5'] = ((df_permno['cd3'] == 5) & (df_permno['divpaid_lag11'] == 1)).astype(int)
    
    # Replace DivSeason = 1 if any temp condition is met
    df_permno.loc[(df_permno['temp3'] == 1) | (df_permno['temp4'] == 1) | (df_permno['temp5'] == 1), 'DivSeason'] = 1
    
    # Check final result
    target_row = df_permno[df_permno['time_avail_m'] == target_date]
    if len(target_row) > 0:
        target_row = target_row.iloc[0]
        print(f"  FINAL RESULT: DivSeason = {target_row['DivSeason']}")
        print(f"    temp3 = {target_row['temp3']}, temp4 = {target_row['temp4']}, temp5 = {target_row['temp5']}")
        print(f"    divpaid_lag2 = {target_row.get('divpaid_lag2', 'NaN')}")
        print(f"    divpaid_lag5 = {target_row.get('divpaid_lag5', 'NaN')}")
        print(f"    divpaid_lag8 = {target_row.get('divpaid_lag8', 'NaN')}")
        print(f"    divpaid_lag11 = {target_row.get('divpaid_lag11', 'NaN')}")
    
    # Keep only necessary columns for output
    df_final = df_permno[['permno', 'time_avail_m', 'DivSeason']].copy()
    df_final = df_final.dropna(subset=['DivSeason'])
    
    print(f"\\nStep 4: Final filtering")
    print(f"  Before dropna: {len(df_permno)} observations")
    print(f"  After dropna: {len(df_final)} observations")
    
    # Check if target observation survives
    target_final = df_final[df_final['time_avail_m'] == target_date]
    if len(target_final) == 0:
        print("  *** TARGET OBSERVATION LOST IN FINAL FILTERING ***")
        
        # Check if DivSeason was NaN
        target_before_dropna = df_permno[df_permno['time_avail_m'] == target_date]
        if len(target_before_dropna) > 0:
            divseason_val = target_before_dropna['DivSeason'].iloc[0]
            print(f"    DivSeason was: {divseason_val}")
            if pd.isna(divseason_val):
                print("    *** FILTERED OUT: DivSeason was NaN ***")
    else:
        print("  Target observation survives final filtering")
        target_final = target_final.iloc[0]
        print(f"    Final DivSeason = {target_final['DivSeason']}")

if __name__ == "__main__":
    trace_specific_observation()