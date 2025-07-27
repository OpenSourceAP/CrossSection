# ABOUTME: Simple debug to understand CitationsRD missing observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_simple_missing_debug.py

import pandas as pd
import numpy as np

def debug_specific_missing():
    """Debug specific missing observation for CitationsRD"""
    
    print("=== CitationsRD Missing Observation Debug ===")
    
    # Target missing observation: permno 14755, 201706, expected CitationsRD = 0
    target_permno = 14755
    target_yyyymm = 201706
    target_date = pd.to_datetime('2017-06-01')
    target_year = 2017
    
    print(f"Debugging permno {target_permno}, {target_yyyymm}...")
    
    # Step 1: Check SignalMasterTable
    print("\\nStep 1: SignalMasterTable")
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    target_smt = smt[(smt['permno'] == target_permno) & (smt['time_avail_m'] == target_date)]
    
    if len(target_smt) == 0:
        print("  *** NOT FOUND in SignalMasterTable ***")
        return
    else:
        gvkey = target_smt['gvkey'].iloc[0]
        mve_c = target_smt['mve_c'].iloc[0]
        print(f"  FOUND: gvkey={gvkey}, mve_c={mve_c:.2f}")
    
    # Step 2: Check Compustat data
    print("\\nStep 2: Compustat data")
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    target_comp = compustat[(compustat['permno'] == target_permno) & (compustat['time_avail_m'] == target_date)]
    
    if len(target_comp) == 0:
        print("  *** NOT FOUND in Compustat ***")
        print("  This would cause the observation to be filtered out after Compustat merge")
        return
    else:
        xrd = target_comp['xrd'].iloc[0] if pd.notna(target_comp['xrd'].iloc[0]) else 'NaN'
        print(f"  FOUND: xrd={xrd}")
    
    # Step 3: Check patent data
    print("\\nStep 3: Patent data")
    patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
    
    if pd.isna(gvkey):
        print("  *** gvkey is NaN - cannot match patent data ***")
        return
    
    target_patent = patent[(patent['gvkey'] == gvkey) & (patent['year'] == target_year)]
    
    if len(target_patent) == 0:
        print(f"  *** NOT FOUND in patent data for gvkey={gvkey}, year={target_year} ***")
        print("  This means ncitscale will be NaN after merge")
        
        # Check if this gvkey has any patent data
        gvkey_patents = patent[patent['gvkey'] == gvkey]
        if len(gvkey_patents) > 0:
            years = sorted(gvkey_patents['year'].unique())
            print(f"  This gvkey has patent data for years: {years}")
        else:
            print("  This gvkey has NO patent data at all")
    else:
        ncitscale = target_patent['ncitscale'].iloc[0]
        print(f"  FOUND: ncitscale={ncitscale}")
    
    # Step 4: Simulate the current CitationsRD logic outcome
    print("\\nStep 4: Likely outcome in CitationsRD logic")
    
    # If we get to this point, the observation exists in SMT and Compustat
    # The issue is likely in subsequent filtering steps
    
    print("  Observation exists in SMT and Compustat")
    print("  Patent data determines ncitscale value")
    print("  Missing observations likely get filtered in:")
    print("  - Size categorization (NYSE median)")
    print("  - Tercile categorization (fastxtile)")
    print("  - Final CitationsRD = 0 assignment for small companies with low terciles")
    
    print("\\n  Since expected CitationsRD = 0:")
    print("  - This should be a small company (below NYSE median)")
    print("  - With low patent citations (bottom tercile)")
    print("  - But getting filtered out somewhere in the process")

def suggest_investigation():
    """Suggest next steps for investigation"""
    
    print("\\n=== Suggested Investigation ===")
    
    print("Key hypothesis:")
    print("- Missing observations exist in SMT and Compustat")
    print("- But get filtered out during size or tercile categorization")
    print("- All expected values are 0, suggesting edge cases in small company handling")
    
    print("\\nNext steps:")
    print("1. Check if these observations survive the gvkey filter")
    print("2. Check if they survive the size categorization")
    print("3. Check if they survive the tercile categorization")
    print("4. Check if they should get CitationsRD = 0 but are missing")
    
    print("\\nQuick fix hypothesis:")
    print("- Companies without patent data or with missing ncitscale")
    print("- Should get CitationsRD = 0 instead of being filtered out")
    print("- This matches the expected behavior (all missing expect 0)")

if __name__ == "__main__":
    debug_specific_missing()
    suggest_investigation()