# ABOUTME: Check the remaining 324 missing observations after the tercile fix
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/check_remaining_missing.py

import pandas as pd
import numpy as np

print("=== Checking remaining missing observations ===")

# Load both datasets
stata_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/Data/Predictors/CitationsRD.csv')
python_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/pyData/Predictors/CitationsRD.csv')

print(f"Stata: {len(stata_df)} observations")
print(f"Python: {len(python_df)} observations")

# Find missing observations
stata_keys = set(zip(stata_df['permno'], stata_df['yyyymm']))
python_keys = set(zip(python_df['permno'], python_df['yyyymm']))

missing_in_python = stata_keys - python_keys
print(f"Missing in Python: {len(missing_in_python)} observations")

# Analyze the missing observations by time period
if len(missing_in_python) > 0:
    missing_df = pd.DataFrame(list(missing_in_python), columns=['permno', 'yyyymm'])
    missing_df['year'] = missing_df['yyyymm'] // 100
    missing_df['month'] = missing_df['yyyymm'] % 100
    
    print(f"\nMissing observations by year:")
    year_counts = missing_df['year'].value_counts().sort_index()
    print(year_counts)
    
    print(f"\nMissing observations by month:")
    month_counts = missing_df['month'].value_counts().sort_index()  
    print(month_counts)
    
    # Check some specific missing observations
    print(f"\nSample of missing observations:")
    sample_missing = missing_df.head(10)
    for _, row in sample_missing.iterrows():
        permno, yyyymm = row['permno'], row['yyyymm']
        stata_row = stata_df[(stata_df['permno'] == permno) & (stata_df['yyyymm'] == yyyymm)]
        if len(stata_row) > 0:
            print(f"  permno {permno}, yyyymm {yyyymm}: Stata CitationsRD = {stata_row.iloc[0]['CitationsRD']}")

# Check precision differences
print(f"\n=== Checking precision differences ===")

# Find common observations
common_keys = stata_keys & python_keys
print(f"Common observations: {len(common_keys)}")

if len(common_keys) > 0:
    # Create comparison DataFrame
    stata_common = stata_df[stata_df.set_index(['permno', 'yyyymm']).index.isin(common_keys)].copy()
    python_common = python_df[python_df.set_index(['permno', 'yyyymm']).index.isin(common_keys)].copy()
    
    # Merge for comparison
    stata_common = stata_common.set_index(['permno', 'yyyymm']).sort_index()
    python_common = python_common.set_index(['permno', 'yyyymm']).sort_index()
    
    comparison = stata_common.join(python_common, lsuffix='_stata', rsuffix='_python')
    
    # Check for differences
    comparison['diff'] = comparison['CitationsRD_python'] - comparison['CitationsRD_stata']
    
    diff_mask = comparison['diff'].abs() > 1e-6
    differences = comparison[diff_mask]
    
    print(f"Observations with differences: {len(differences)}")
    
    if len(differences) > 0:
        print(f"\nSample of differences:")
        print(differences[['CitationsRD_stata', 'CitationsRD_python', 'diff']].head(10))
        
        # Check the pattern of differences
        print(f"\nDifference patterns:")
        print(differences['diff'].value_counts().sort_index())

# Check if the remaining issues are similar to what we saw before
print(f"\n=== Pattern analysis ===")

# Look at recent missing observations that might indicate ongoing issues
if len(missing_in_python) > 0:
    recent_missing = missing_df[missing_df['year'] >= 2015]
    print(f"Recent missing observations (2015+): {len(recent_missing)}")
    
    if len(recent_missing) > 0:
        print(f"Recent missing by year:")
        print(recent_missing['year'].value_counts().sort_index())
        
        # Check if these are end-of-sample issues or systematic issues
        recent_permnos = recent_missing['permno'].unique()
        print(f"Number of unique permnos with recent missing observations: {len(recent_permnos)}")
        
        # Check a few examples
        print(f"\nSample recent missing observations:")
        for permno in recent_permnos[:5]:
            permno_missing = recent_missing[recent_missing['permno'] == permno]
            print(f"  Permno {permno}: missing {len(permno_missing)} observations")
            print(f"    Periods: {sorted(permno_missing['yyyymm'].tolist())[:10]}")  # Show first 10