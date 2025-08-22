#%%


#!/usr/bin/env python3
# ABOUTME: Test asreg function on MWE
# ABOUTME: Verifies that asreg with cross_sectional=True matches Stata's "bys time_avail_m: asreg"

import pandas as pd
from stata_regress import asreg

#%%

csv_path = "mwe/tf_mwe5.csv"

# Load data
df = pd.read_csv(csv_path)

print(f"Testing asreg on {csv_path}")
print("=" * 55)

# Run cross-sectional asreg using the enhanced asreg function
results = asreg(
    df,
    y="fRet",
    X="A_*",  # Will be expanded to all A_* columns
    by="time_avail_m",
    cross_sectional=True,  # This is the key parameter!
    add_constant=True,
    drop_collinear=True,
)

print(f"Results shape: {results.shape}")
print(f"Columns: {list(results.columns)}")

#%%

results

