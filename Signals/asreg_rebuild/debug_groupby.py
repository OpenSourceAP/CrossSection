#!/usr/bin/env python3
import pandas as pd
import numpy as np

# Create test data
np.random.seed(42)
data = []
for group in range(1, 4):
    for _ in range(3):
        data.append({
            'group_id': group,
            'x': np.random.randn(),
            'y': np.random.randn()
        })

df = pd.DataFrame(data)
print("DataFrame:")
print(df)

# Test groupby with single column
print("\nGroupby with single column:")
by = ['group_id']
for name, group in df.groupby(by):
    print(f"Name: {name}, Type: {type(name)}, Is tuple: {isinstance(name, tuple)}")
    
# Test groupby with single column as string
print("\nGroupby with single column as string:")
by = 'group_id'
for name, group in df.groupby(by):
    print(f"Name: {name}, Type: {type(name)}")