# ABOUTME: Test the tercile logic issue in CitationsRD
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_tercile_test.py

import pandas as pd
import numpy as np

def test_exact_citationsrd_logic():
    """Test the exact logic from CitationsRD.py to find the issue"""
    
    print("=== Testing Exact CitationsRD Logic ===")
    
    # Load the current Python output
    try:
        python_output = pd.read_csv('../pyData/Predictors/CitationsRD.csv')
        python_output = python_output.set_index(['permno', 'yyyymm'])
        print(f"Current Python output: {len(python_output)} rows")
        
        # Check if permno 14755 is in the output at all
        permno_14755_output = python_output[python_output.index.get_level_values('permno') == 14755]
        print(f"Permno 14755 in current output: {len(permno_14755_output)} rows")
        
        if len(permno_14755_output) > 0:
            print("Sample of permno 14755 output:")
            print(permno_14755_output.head(10))
            
            # Check if the missing dates are covered
            missing_yyyymm = [201706, 201707, 201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803]
            output_yyyymm = permno_14755_output.index.get_level_values('yyyymm').tolist()
            
            print("\nChecking missing dates in current output:")
            for yyyymm in missing_yyyymm:
                exists = yyyymm in output_yyyymm
                print(f"  {yyyymm}: {'EXISTS' if exists else 'MISSING'}")
        else:
            print("*** CONFIRMED: Permno 14755 is completely missing from Python output ***")
    
    except Exception as e:
        print(f"Error loading Python output: {e}")
    
    # Now test a simple case to understand the tercile logic
    print("\n=== Simple Tercile Test ===")
    
    # Create test data with one time period and multiple observations
    test_data = pd.DataFrame({
        'permno': [1, 2, 3, 4, 5, 14755],
        'time_avail_m': [pd.to_datetime('2017-06-01')] * 6,
        'tempCitationsRD': [0.1, 0.2, 0.3, 0.4, 0.5, 0.0],  # 14755 has 0.0
        'sizecat': [1, 1, 1, 1, 1, 1]  # All small stocks
    })
    
    print("Test data:")
    print(test_data)
    
    # Apply the exact logic from CitationsRD.py
    test_data['maincat'] = np.nan
    
    # KEY FIX: Assign maincat=1 to observations with missing tempCitationsRD
    test_data.loc[test_data['tempCitationsRD'].isna(), 'maincat'] = 1.0
    
    # For observations with valid tempCitationsRD, create terciles by time period
    def create_terciles_per_period(group_df):
        if len(group_df) == 0:
            return group_df
        
        citations = group_df['tempCitationsRD']
        
        # Calculate 33rd and 67th percentiles
        q33 = citations.quantile(0.333)
        q67 = citations.quantile(0.667)
        
        print(f"Citations: {citations.tolist()}")
        print(f"Q33: {q33}, Q67: {q67}")
        
        # Assign terciles based on percentile breakpoints
        group_df['maincat'] = np.where(citations <= q33, 1.0, 
                                      np.where(citations <= q67, 2.0, 3.0))
        
        print(f"Assigned maincats: {group_df['maincat'].tolist()}")
        
        return group_df
    
    # Apply terciles only to valid data (this is the exact logic from CitationsRD.py)
    valid_mask = test_data['tempCitationsRD'].notna()
    if valid_mask.sum() > 0:
        valid_df = test_data[valid_mask].copy()
        tercile_df = valid_df.groupby('time_avail_m').apply(create_terciles_per_period).reset_index(drop=True)
        test_data.loc[valid_mask, 'maincat'] = tercile_df['maincat'].values
    
    print("\nAfter tercile assignment:")
    print(test_data[['permno', 'tempCitationsRD', 'sizecat', 'maincat']])
    
    # Create CitationsRD signal
    test_data['CitationsRD'] = np.nan
    test_data.loc[(test_data['sizecat'] == 1) & (test_data['maincat'] == 3), 'CitationsRD'] = 1
    test_data.loc[(test_data['sizecat'] == 1) & (test_data['maincat'] == 1), 'CitationsRD'] = 0
    
    print("\nFinal signals:")
    print(test_data[['permno', 'tempCitationsRD', 'sizecat', 'maincat', 'CitationsRD']])
    
    # Check what happened to permno 14755
    permno_14755_test = test_data[test_data['permno'] == 14755]
    if len(permno_14755_test) > 0:
        signal = permno_14755_test['CitationsRD'].iloc[0]
        print(f"\nPermno 14755 got signal: {signal}")
        
        if pd.isna(signal):
            print("*** ISSUE: Permno 14755 got NaN signal - this explains why it's missing! ***")
            sizecat = permno_14755_test['sizecat'].iloc[0]
            maincat = permno_14755_test['maincat'].iloc[0]
            print(f"Sizecat: {sizecat}, Maincat: {maincat}")
            print("Signal assignment logic:")
            print(f"  sizecat == 1 and maincat == 3: {sizecat == 1 and maincat == 3} -> CitationsRD = 1")
            print(f"  sizecat == 1 and maincat == 1: {sizecat == 1 and maincat == 1} -> CitationsRD = 0")
            print(f"  Neither condition met -> CitationsRD = NaN")

if __name__ == "__main__":
    test_exact_citationsrd_logic()