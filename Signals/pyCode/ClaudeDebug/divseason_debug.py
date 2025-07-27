# ABOUTME: Debug DivSeason high error rate (5.6% precision differences)
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_debug.py

import pandas as pd
import numpy as np

print("=== Debugging DivSeason high error rate ===")

# Load both datasets
stata_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/Data/Predictors/DivSeason.csv')
python_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/pyData/Predictors/DivSeason.csv')

print(f"Stata: {len(stata_df)} observations")
print(f"Python: {len(python_df)} observations")

# The test results showed 98,994/1,775,302 precision differences (5.6%)
# This is well above the 0.1% tolerance and needs investigation

# Find common observations for comparison
stata_keys = set(zip(stata_df['permno'], stata_df['yyyymm']))
python_keys = set(zip(python_df['permno'], python_df['yyyymm']))
common_keys = stata_keys & python_keys

print(f"Common observations: {len(common_keys)}")

# Create comparison DataFrame
stata_common = stata_df[stata_df.set_index(['permno', 'yyyymm']).index.isin(common_keys)].copy()
python_common = python_df[python_df.set_index(['permno', 'yyyymm']).index.isin(common_keys)].copy()

stata_common = stata_common.set_index(['permno', 'yyyymm']).sort_index()
python_common = python_common.set_index(['permno', 'yyyymm']).sort_index()

comparison = stata_common.join(python_common, lsuffix='_stata', rsuffix='_python')
comparison['diff'] = comparison['DivSeason_python'] - comparison['DivSeason_stata']

diff_mask = comparison['diff'].abs() > 1e-6
differences = comparison[diff_mask]

print(f"Actual differences: {len(differences)} ({len(differences)/len(comparison)*100:.1f}%)")

if len(differences) > 0:
    print(f"\nDifference patterns:")
    print(differences['diff'].value_counts().sort_index())
    
    print(f"\nSample differences:")
    sample_diffs = differences.head(15)
    print(sample_diffs[['DivSeason_stata', 'DivSeason_python', 'diff']])
    
    # Check temporal distribution
    sample_reset = differences.reset_index()
    sample_reset['year'] = sample_reset['yyyymm'] // 100
    print(f"\nDifferences by year (top 10):")
    year_counts = sample_reset['year'].value_counts().sort_index()
    print(year_counts.head(10))
    
    # Check if differences are systematic (always 0→1 or 1→0)
    stata_zeros_to_python_ones = differences[(differences['DivSeason_stata'] == 0) & (differences['DivSeason_python'] == 1)]
    stata_ones_to_python_zeros = differences[(differences['DivSeason_stata'] == 1) & (differences['DivSeason_python'] == 0)]
    
    print(f"\nPattern analysis:")
    print(f"Stata 0 → Python 1: {len(stata_zeros_to_python_ones)} cases")
    print(f"Stata 1 → Python 0: {len(stata_ones_to_python_zeros)} cases")
    
    # Look at some specific cases to understand the issue
    print(f"\nAnalyzing sample cases...")
    
    # Pick a few cases where Stata=0 and Python=1
    if len(stata_zeros_to_python_ones) > 0:
        sample_case = stata_zeros_to_python_ones.iloc[0]
        permno, yyyymm = sample_case.name
        print(f"\nSample case: permno {permno}, yyyymm {yyyymm}")
        print(f"Stata: {sample_case['DivSeason_stata']}, Python: {sample_case['DivSeason_python']}")
        
        # This suggests the issue might be in the dividend prediction logic
        # or in the cd3 forward-filling logic

print(f"\n=== Investigating potential causes ===")

# The high error rate suggests a systematic difference in logic
# Most likely candidates:
# 1. cd3 forward-filling (l1.cd3 vs fillna(method='ffill'))
# 2. Dividend lag calculations 
# 3. Missing data handling

print(f"Potential causes of high error rate:")
print(f"1. cd3 filling logic difference (l1.cd3 vs forward-fill)")
print(f"2. Dividend lag calculation differences")
print(f"3. Missing data handling differences")
print(f"4. Different interpretation of dividend frequency codes")

# Let's check the value distributions
print(f"\n=== Value distributions ===")
print(f"Stata DivSeason distribution:")
print(stata_df['DivSeason'].value_counts().sort_index())

print(f"\nPython DivSeason distribution:")
print(python_df['DivSeason'].value_counts().sort_index())

# Check if the issue might be in recent periods (data availability)
missing_in_python = stata_keys - python_keys
if len(missing_in_python) > 0:
    missing_df = pd.DataFrame(list(missing_in_python), columns=['permno', 'yyyymm'])
    missing_df['year'] = missing_df['yyyymm'] // 100
    print(f"\nMissing observations by year:")
    print(missing_df['year'].value_counts().sort_index().tail(10))

print(f"\n=== Conclusion ===")
print(f"The 5.6% error rate is too high and needs fixing.")
print(f"Most likely cause is the cd3 forward-filling logic difference.")
print(f"Need to change from fillna(method='ffill') to proper l1.cd3 lag logic.")