# ABOUTME: Investigate cd3 assignment differences between Stata and Python
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_cd3_investigation.py

import pandas as pd
import numpy as np

def investigate_cd3_assignment():
    """Investigate how cd3 values are assigned differently in Stata vs Python"""
    
    print("=== Investigating cd3 Assignment Differences ===")
    
    # Focus on the problematic observation: permno 65293, 200912
    target_permno = 65293
    target_yyyymm = 200912
    target_date = pd.to_datetime('2009-12-01')
    
    print(f"Investigating permno {target_permno}, {target_yyyymm}...")
    
    # Get dividend data
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    
    # Keep if cd1 == 1 & cd2 == 2 (regular cash dividends)
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    
    # Select timing variable and convert to monthly
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Get dividend data for target permno
    permno_divs = dist_df[dist_df['permno'] == target_permno].copy()
    permno_divs['yyyymm'] = permno_divs['time_avail_m'].dt.year * 100 + permno_divs['time_avail_m'].dt.month
    permno_divs = permno_divs.sort_values('time_avail_m')
    
    print("\\nRaw dividend data for target permno:")
    print("yyyymm   cd3   divamt")
    print("-" * 20)
    for _, row in permno_divs.iterrows():
        print(f"{row['yyyymm']:6d}  {row['cd3']:4.1f}  {row['divamt']:7.3f}")
    
    # Run the same processing as DivSeason.py
    print("\\nAfter Python processing:")
    
    # Sum across all frequency codes
    tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()
    
    # Clean up a handful of odd two-frequency permno-months
    tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
    tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()
    
    # Get processed data for target permno
    permno_processed = tempdivamt[tempdivamt['permno'] == target_permno].copy()
    permno_processed['yyyymm'] = permno_processed['time_avail_m'].dt.year * 100 + permno_processed['time_avail_m'].dt.month
    permno_processed = permno_processed.sort_values('time_avail_m')
    
    print("yyyymm   cd3   divamt")
    print("-" * 20)
    for _, row in permno_processed.iterrows():
        print(f"{row['yyyymm']:6d}  {row['cd3']:4.1f}  {row['divamt']:7.3f}")
    
    # Now simulate the merge with SignalMasterTable and forward-fill logic
    print("\\nAfter merge with SMT and forward-fill:")
    
    # Get SMT data for this permno
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    smt_permno = smt[smt['permno'] == target_permno][['permno', 'time_avail_m']].copy()
    
    # Merge with dividend data
    merged = smt_permno.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
    merged = merged.sort_values('time_avail_m')
    
    # Forward-fill cd3 logic
    merged['cd3'] = merged.groupby('permno')['cd3'].fillna(method='ffill')
    merged['cd3'] = merged['cd3'].fillna(3)  # Default to quarterly
    
    # Show data around target date
    merged['yyyymm'] = merged['time_avail_m'].dt.year * 100 + merged['time_avail_m'].dt.month
    
    # Show window around target date
    target_year = target_yyyymm // 100
    window = merged[
        (merged['yyyymm'] >= (target_year - 1) * 100 + 1) & 
        (merged['yyyymm'] <= (target_year + 1) * 100 + 12)
    ].copy()
    
    print("yyyymm   cd3   divamt  fillna")
    print("-" * 35)
    for _, row in window.iterrows():
        cd3_val = row['cd3'] if pd.notna(row['cd3']) else 'NaN'
        divamt_val = row['divamt'] if pd.notna(row['divamt']) else 'NaN'
        is_target = "***" if row['yyyymm'] == target_yyyymm else "   "
        print(f"{row['yyyymm']:6d}  {cd3_val:>4}  {divamt_val:>7}   {is_target}")
    
    # Show the specific issue
    target_row = merged[merged['yyyymm'] == target_yyyymm]
    if len(target_row) > 0:
        target_cd3 = target_row['cd3'].iloc[0]
        print(f"\\nTarget observation cd3 = {target_cd3}")
        
        if target_cd3 >= 6:
            print("*** PROBLEM: cd3 >= 6, will be filtered out ***")
            
            # Find where this cd3 value came from
            print("\\nTracing cd3 source:")
            
            # Look at the last non-NaN cd3 value before target
            with_cd3 = merged[
                (merged['yyyymm'] <= target_yyyymm) & 
                pd.notna(merged['cd3']) & 
                (merged['cd3'] != 3)  # Not the default fill
            ]
            
            if len(with_cd3) > 0:
                source_row = with_cd3.iloc[-1]
                source_yyyymm = source_row['yyyymm']
                source_cd3 = source_row['cd3']
                print(f"  cd3 = {target_cd3} came from forward-fill of {source_yyyymm} (cd3 = {source_cd3})")
                
                # The issue might be that the special dividend cd3=7 gets forward-filled
                # But in Stata, maybe the logic is different
                print("\\n*** HYPOTHESIS ***")
                print("The issue might be that special dividends (cd3=7) should not be")
                print("forward-filled to subsequent months. They should only apply to")
                print("the specific month they occur in.")
        else:
            print(f"cd3 = {target_cd3} < 6, should pass filter")

def test_fix_approach():
    """Test approach to fix cd3 forward-fill for special dividends"""
    
    print("\\n=== Testing Fix Approach ===")
    print("Possible fix: Don't forward-fill special dividend codes (cd3 >= 6)")
    print("This would prevent cd3=7 from affecting subsequent months")

if __name__ == "__main__":
    investigate_cd3_assignment()
    test_fix_approach()