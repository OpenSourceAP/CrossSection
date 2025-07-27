# ABOUTME: Debug the cd3 filling logic to understand the difference
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/cd3_logic_debug.py

import pandas as pd
import numpy as np

print("=== Debugging cd3 filling logic ===")

# Let's create a test scenario to understand the difference between:
# 1. Stata: replace cd3 = l1.cd3 if cd3 == .
# 2. Python forward-fill: fillna(method='ffill')  
# 3. Python 1-period lag: fillna(shift(1))

# Create test data similar to what we might see
test_data = pd.DataFrame({
    'permno': [1, 1, 1, 1, 1, 1, 1, 1],
    'time_avail_m': pd.date_range('2020-01-01', periods=8, freq='M'),
    'cd3': [3.0, np.nan, np.nan, 4.0, np.nan, np.nan, 5.0, np.nan]
})

print("Original test data:")
print(test_data)

# Method 1: Forward-fill (original Python approach)
test_ffill = test_data.copy()
test_ffill['cd3_ffill'] = test_ffill['cd3'].fillna(method='ffill')

# Method 2: 1-period lag (new Python approach)
test_lag = test_data.copy()
test_lag['cd3_lag1'] = test_lag['cd3'].shift(1)
test_lag['cd3_fixed'] = test_lag['cd3'].fillna(test_lag['cd3_lag1'])

# Method 3: What Stata actually does - replace cd3 = l1.cd3 if cd3 == .
# This should be equivalent to: if cd3 is missing, use the previous period's cd3
test_stata = test_data.copy()
test_stata['cd3_stata'] = test_stata['cd3']
for i in range(1, len(test_stata)):
    if pd.isna(test_stata.loc[i, 'cd3_stata']):
        test_stata.loc[i, 'cd3_stata'] = test_stata.loc[i-1, 'cd3_stata']

print(f"\nMethod comparison:")
comparison = pd.DataFrame({
    'original': test_data['cd3'],
    'ffill': test_ffill['cd3_ffill'],  
    'lag_fill': test_lag['cd3_fixed'],
    'stata_logic': test_stata['cd3_stata']
})
print(comparison)

print(f"\nAs we can see:")
print(f"- forward-fill and stata_logic should be equivalent")
print(f"- lag_fill is more restrictive (only uses immediate previous period)")

# The issue is that my 'fixed' approach is too restrictive!
# Let me revert to forward-fill but check if there are other issues

print(f"\n=== Testing on actual data ===")

# Load the distributions data to understand cd3 patterns
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]

print(f"CRSPdistributions data shape: {dist_df.shape}")
print(f"cd3 missing values: {dist_df['cd3'].isna().sum()}")
print(f"cd3 value counts:")
print(dist_df['cd3'].value_counts().sort_index())

# Check a specific permno to see the cd3 pattern
sample_permno = dist_df['permno'].iloc[100]  # Pick a permno
sample_data = dist_df[dist_df['permno'] == sample_permno].sort_values('exdt').head(10)
print(f"\nSample permno {sample_permno} cd3 pattern:")
print(sample_data[['permno', 'exdt', 'cd3', 'divamt']])

print(f"\n=== Conclusion ===")
print(f"The issue is NOT in the cd3 filling logic.")  
print(f"Forward-fill (fillna(method='ffill')) is equivalent to Stata's l1.cd3 logic.")
print(f"The 1-period lag approach was wrong and overly restrictive.")
print(f"Need to revert to forward-fill and look for other issues.")
print(f"The original 5.6% error rate might be due to other differences in the logic.")