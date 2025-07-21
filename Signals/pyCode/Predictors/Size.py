# ABOUTME: Size.py - calculates market capitalization size predictor
# ABOUTME: Simple log transformation of market value of equity (mve_c) from SignalMasterTable

"""
Size predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/Size.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c)

Outputs:
    - ../pyData/Predictors/Size.csv (permno, yyyymm, Size)
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