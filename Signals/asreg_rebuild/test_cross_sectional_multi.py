#!/usr/bin/env python3
# ABOUTME: Test _asreg_cross_sectional with multiple grouping columns
# ABOUTME: Verifies that it handles multiple by columns correctly

import pandas as pd
import numpy as np
from stata_regress import asreg

# Create test data with two grouping columns
np.random.seed(42)
data = []
for region in ['North', 'South']:
    for year in [2020, 2021]:
        for _ in range(10):
            data.append({
                'region': region,
                'year': year,
                'x1': np.random.randn(),
                'x2': np.random.randn(),
                'y': np.random.randn()
            })

df = pd.DataFrame(data)

print("Input data shape:", df.shape)
print("\nGroup counts:")
print(df.groupby(['region', 'year']).size())

# Run cross-sectional regression with multiple grouping columns
result = asreg(
    df,
    y='y',
    X=['x1', 'x2'],
    by=['region', 'year'],
    cross_sectional=True,
    add_constant=True,
    drop_collinear=True
)

print("\n\nResult shape:", result.shape)
print("\nResult columns:")
print(result.columns.tolist())
print("\nResult data:")
print(result)

# Verify we have one row per group combination
expected_groups = 4  # 2 regions × 2 years
assert len(result) == expected_groups, f"Expected {expected_groups} rows, got {len(result)}"

# Verify both group columns are present
assert 'region' in result.columns, "Group column 'region' is missing"
assert 'year' in result.columns, "Group column 'year' is missing"

# Verify group values are correct
unique_regions = set(result['region'].values)
unique_years = set(result['year'].values)
assert unique_regions == {'North', 'South'}, f"Region values don't match: {unique_regions}"
assert unique_years == {2020, 2021}, f"Year values don't match: {unique_years}"

print("\n✓ All tests passed for multiple grouping columns!")