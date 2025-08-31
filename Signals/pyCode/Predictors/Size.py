# ABOUTME: Size following Banz 1981, Table 3, alpha_1 n=50
# ABOUTME: calculates log of market value of equity as size predictor
"""
Usage:
    python3 Predictors/Size.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, mve_c]

Outputs:
    - Size.csv: CSV file with columns [permno, yyyymm, Size]
    - Size = log(mve_c), log transformation of market value of equity
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                     columns=['permno', 'time_avail_m', 'mve_c'])

# SIGNAL CONSTRUCTION
df['Size'] = np.log(df['mve_c'])

# Drop missing values
df = df.dropna(subset=['Size'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'Size']].copy()

# SAVE
df.to_csv("../pyData/Predictors/Size.csv", index=False)
print(f"Size: Saved {len(df):,} observations")