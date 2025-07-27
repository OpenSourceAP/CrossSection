# ABOUTME: Debug DelBreadth missing observations and precision issues
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_final_debug.py

import pandas as pd
import numpy as np

def debug_delbreadth_missing():
    """Debug specific missing observations in DelBreadth"""
    
    print("=== DelBreadth Debug: Missing Observations ===")
    
    # Load Stata data to see expected results
    stata_file = '../Data/Predictors/DelBreadth.csv'
    try:
        stata_df = pd.read_csv(stata_file)
        print(f"Stata data loaded: {stata_df.shape}")
        
        # Focus on a specific missing observation: permno 11370, 201304
        missing_permno = 11370
        missing_yyyymm = 201304
        
        print(f"\n--- Checking Stata data for permno {missing_permno}, yyyymm {missing_yyyymm} ---")
        stata_subset = stata_df[(stata_df['permno'] == missing_permno) & (stata_df['yyyymm'] == missing_yyyymm)]
        print(f"Stata observations: {len(stata_subset)}")
        
        if len(stata_subset) > 0:
            print("Stata observation:")
            print(stata_subset)
        
        # Check the permno more broadly
        stata_permno = stata_df[stata_df['permno'] == missing_permno]
        print(f"\nAll Stata observations for permno {missing_permno}: {len(stata_permno)}")
        if len(stata_permno) > 0:
            print("Date range:")
            print(f"Min yyyymm: {stata_permno['yyyymm'].min()}")
            print(f"Max yyyymm: {stata_permno['yyyymm'].max()}")
        
    except Exception as e:
        print(f"Error loading Stata data: {e}")
    
    print("\n=== Tracing Python Logic ===")
    
    # Load Python output to see what we have
    try:
        python_df = pd.read_csv('../pyData/Predictors/DelBreadth.csv')
        python_df = python_df.set_index(['permno', 'yyyymm'])
        print(f"Python data loaded: {python_df.shape}")
        
        # Check if the missing permno exists at all
        python_permno = python_df[python_df.index.get_level_values('permno') == missing_permno]
        print(f"Python observations for permno {missing_permno}: {len(python_permno)}")
        
        if len(python_permno) > 0:
            print("Available yyyymm values:")
            available_yyyymm = python_permno.index.get_level_values('yyyymm').tolist()
            print(sorted(available_yyyymm))
            
            if missing_yyyymm not in available_yyyymm:
                print(f"*** Missing yyyymm {missing_yyyymm} not in Python output ***")
        else:
            print(f"*** Permno {missing_permno} completely missing from Python output ***")
            
    except Exception as e:
        print(f"Error loading Python data: {e}")

def debug_delbreadth_precision():
    """Debug the large precision differences"""
    
    print("\n=== DelBreadth Precision Debug ===")
    
    # Focus on the largest difference: permno 24205, 201011
    # Python=-1.132 vs Stata=-24.78 (diff=23.648)
    
    problematic_permno = 24205
    problematic_yyyymm = 201011
    
    print(f"Debugging permno {problematic_permno}, yyyymm {problematic_yyyymm}")
    
    # Load both datasets
    try:
        stata_df = pd.read_csv('../Data/Predictors/DelBreadth.csv')
        python_df = pd.read_csv('../pyData/Predictors/DelBreadth.csv')
        
        # Find the specific observation
        stata_obs = stata_df[(stata_df['permno'] == problematic_permno) & (stata_df['yyyymm'] == problematic_yyyymm)]
        python_obs = python_df[(python_df['permno'] == problematic_permno) & (python_df['yyyymm'] == problematic_yyyymm)]
        
        print("Stata observation:")
        print(stata_obs)
        print("\nPython observation:")
        print(python_obs)
        
        if len(stata_obs) > 0 and len(python_obs) > 0:
            stata_val = stata_obs['DelBreadth'].iloc[0]
            python_val = python_obs['DelBreadth'].iloc[0]
            
            print(f"\nValues:")
            print(f"Stata: {stata_val}")
            print(f"Python: {python_val}")
            print(f"Difference: {abs(stata_val - python_val)}")
            
            # This suggests a fundamental calculation difference
            print("\n*** ISSUE: Large calculation difference suggests logic error ***")
        
    except Exception as e:
        print(f"Error in precision debug: {e}")

def trace_delbreadth_logic():
    """Trace the DelBreadth calculation logic to find issues"""
    
    print("\n=== Tracing DelBreadth Logic ===")
    
    # The DelBreadth logic from the code:
    # 1. Load SignalMasterTable
    # 2. Merge with TR_13F data
    # 3. Forward-fill TR_13F data (quarterly -> monthly)
    # 4. Set DelBreadth = dbreadth
    # 5. Calculate 20th percentile of mve_c for NYSE stocks
    # 6. Replace DelBreadth with NaN if mve_c < 20th percentile (with tolerance)
    
    print("DelBreadth logic:")
    print("1. Merge SignalMasterTable with TR_13F")
    print("2. Forward-fill dbreadth (quarterly to monthly)")
    print("3. DelBreadth = dbreadth")
    print("4. Calculate NYSE 20th percentile market cap filter")
    print("5. Set DelBreadth = NaN if mve_c < (20th percentile - tolerance)")
    
    # The issues could be:
    # A. TR_13F data differences between Python and Stata
    # B. Forward-fill logic differences
    # C. NYSE percentile calculation differences
    # D. Tolerance handling differences
    
    print("\nPotential issues:")
    print("A. TR_13F data differences")
    print("B. Forward-fill logic (fillna method='ffill')")
    print("C. NYSE 20th percentile calculation")
    print("D. Tolerance logic in filtering")
    
    # The large differences suggest issue A or B - data/calculation differences

if __name__ == "__main__":
    debug_delbreadth_missing()
    debug_delbreadth_precision()
    trace_delbreadth_logic()