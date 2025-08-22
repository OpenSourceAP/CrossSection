#!/usr/bin/env python3
# ABOUTME: Test the modified _asreg_cross_sectional function
# ABOUTME: Verifies that it returns one row per group with group columns

import pandas as pd
import numpy as np
from stata_regress import asreg

# Create test data
np.random.seed(42)
n_groups = 3
n_obs_per_group = 10

data = []
for group in range(1, n_groups + 1):
    for _ in range(n_obs_per_group):
        data.append({
            'group_id': group,
            'x1': np.random.randn(),
            'x2': np.random.randn(),
            'y': np.random.randn()
        })

df = pd.DataFrame(data)

print("Input data shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

# Run cross-sectional regression
result = asreg(
    df,
    y='y',
    X=['x1', 'x2'],
    by='group_id',
    cross_sectional=True,
    add_constant=True,
    drop_collinear=True
)

print("\n\nResult shape:", result.shape)
print("\nResult columns:")
print(result.columns.tolist())
print("\nResult data:")
print(result)

# Verify we have one row per group
assert len(result) == n_groups, f"Expected {n_groups} rows, got {len(result)}"

# Verify group column is present
assert 'group_id' in result.columns, "Group column 'group_id' is missing"

# Verify group values are correct
assert set(result['group_id'].values) == set(range(1, n_groups + 1)), "Group values don't match"

print("\n✓ All tests passed!")