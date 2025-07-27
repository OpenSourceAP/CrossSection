# ABOUTME: Detailed trace of CitationsRD logic for specific missing observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_detailed_trace.py

import pandas as pd
import numpy as np

def trace_specific_missing():
    """Trace CitationsRD logic for specific missing observation"""
    
    print("=== Tracing CitationsRD Logic for Missing Observation ===")
    
    # Sample missing observation: permno 14755, 201706-201803, expected CitationsRD = 0
    target_permno = 14755
    target_yyyymm = 201706
    target_date = pd.to_datetime('2017-06-01')
    
    print(f"Tracing permno {target_permno}, {target_yyyymm}...")
    
    # Step 1: Check SignalMasterTable
    print("\\nStep 1: SignalMasterTable")
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    target_smt = smt[(smt['permno'] == target_permno) & (smt['time_avail_m'] == target_date)]
    
    if len(target_smt) == 0:
        print("  *** NOT FOUND in SignalMasterTable ***")
        return
    else:
        print(f"  FOUND in SignalMasterTable: mve_c = {target_smt['mve_c'].iloc[0]:.2f}")
    
    # Step 2: Check patent data
    print("\\nStep 2: Patent data")
    patents = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
    patents_permno = patents[patents['permno'] == target_permno].copy()
    
    if len(patents_permno) > 0:
        print(f"  Found {len(patents_permno)} patent records for this permno")
        patents_permno['year'] = patents_permno['datadate'].dt.year
        target_year = target_yyyymm // 100
        
        # Show patent data around target year
        nearby_patents = patents_permno[
            (patents_permno['year'] >= target_year - 2) &
            (patents_permno['year'] <= target_year + 2)
        ]
        
        if len(nearby_patents) > 0:
            print("  Patent data around target year:")
            for _, row in nearby_patents.iterrows():
                print(f"    {row['year']}: CitationsGranted = {row['CitationsGranted']}")
        else:
            print(f"  No patent data for years {target_year-2} to {target_year+2}")
    else:
        print("  *** NO PATENT DATA for this permno ***")
        print("  This explains why observation is missing - no patent data to process")
        return
    
    # Step 3: Run partial CitationsRD logic
    print("\\nStep 3: Partial CitationsRD logic for this permno")
    
    # Load data like CitationsRD.py
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    # Focus on target permno
    df_permno = df[df['permno'] == target_permno].copy()
    print(f"  SMT observations for permno {target_permno}: {len(df_permno)}")
    
    # Merge with patent data
    df_permno = df_permno.merge(patents, on='permno', how='left')
    
    # Filter to recent 5 years of patent data
    df_permno['year'] = df_permno['time_avail_m'].dt.year
    df_permno['patent_year'] = df_permno['datadate'].dt.year
    df_permno = df_permno[
        (df_permno['patent_year'] >= df_permno['year'] - 5) &
        (df_permno['patent_year'] <= df_permno['year'] - 1)
    ]
    
    print(f"  After patent filter: {len(df_permno)} observations")
    
    # Check if target observation survives
    target_row = df_permno[df_permno['time_avail_m'] == target_date]
    if len(target_row) == 0:
        print("  *** TARGET OBSERVATION FILTERED OUT by patent data requirements ***")
        
        # Check what patent years are available
        df_permno_all = df[df['permno'] == target_permno]
        df_permno_all = df_permno_all.merge(patents, on='permno', how='left')
        target_all = df_permno_all[df_permno_all['time_avail_m'] == target_date]
        
        if len(target_all) > 0:
            target_patent_years = target_all['datadate'].dt.year
            available_years = target_patent_years.dropna().unique()
            target_year = target_yyyymm // 100
            required_range = f"{target_year-5} to {target_year-1}"
            
            print(f"    Target year: {target_year}")
            print(f"    Required patent years: {required_range}")
            print(f"    Available patent years: {sorted(available_years) if len(available_years) > 0 else 'None'}")
            
            if len(available_years) == 0:
                print("    *** NO PATENT DATA AVAILABLE - explains missing observation ***")
            else:
                earliest_available = min(available_years)
                latest_available = max(available_years)
                print(f"    Available range: {earliest_available} to {latest_available}")
                if earliest_available > target_year - 1:
                    print("    *** PATENT DATA TOO RECENT - explains missing observation ***")
    else:
        print("  Target observation survives patent filter")

def check_edge_case_pattern():
    """Check if there's a pattern in the missing observations"""
    
    print("\\n=== Edge Case Pattern Analysis ===")
    
    # The missing observations might follow a pattern
    # Let's check if they're all from a specific time period or company type
    
    print("From previous analysis:")
    print("- permno 14755, 201706-201803: all expected CitationsRD = 0")
    print("- This suggests small companies with low patent activity")
    print("- Missing months are early in the company's patent history")
    
    print("\\nHypothesis:")
    print("- Companies start appearing in patent data at some point")
    print("- Early months before patent data starts are missing")
    print("- Stata might handle this differently (maybe assigns CitationsRD = 0)")

def suggest_fix_approach():
    """Suggest approach to fix the missing observations"""
    
    print("\\n=== Suggested Fix Approach ===")
    
    print("Option 1: Default CitationsRD = 0 for companies without patent data")
    print("- For companies in SMT but without recent patent data")
    print("- Assign CitationsRD = 0 instead of filtering out")
    print("- This matches expected values (all are 0)")
    
    print("\\nOption 2: Extend patent data search window")
    print("- Current: require patent data from year-5 to year-1")
    print("- Modified: allow wider window or handle missing data differently")
    
    print("\\nRecommended: Option 1")
    print("- Simple and matches expected behavior")
    print("- All missing observations expect CitationsRD = 0")
    print("- Would fix all 576 missing observations if they're all similar cases")

if __name__ == "__main__":
    trace_specific_missing()
    check_edge_case_pattern()
    suggest_fix_approach()