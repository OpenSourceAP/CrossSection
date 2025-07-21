# ABOUTME: RoE.py - calculates return on equity predictor
# ABOUTME: Return on equity as net income (ni) divided by common equity (ceq)

"""
RoE predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/RoE.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, ni, ceq)

Outputs:
    - ../pyData/Predictors/RoE.csv (permno, yyyymm, RoE)
"""

import pandas as pd

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                     columns=['gvkey', 'permno', 'time_avail_m', 'ni', 'ceq'])

# SIGNAL CONSTRUCTION
# Remove duplicates by permno and time_avail_m (keep first)
df = df.groupby(['permno', 'time_avail_m']).first().reset_index()

# Calculate RoE
df['RoE'] = df['ni'] / df['ceq']

# Drop missing values
df = df.dropna(subset=['RoE'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'RoE']].copy()

# SAVE
df.to_csv("../pyData/Predictors/RoE.csv", index=False)
print(f"RoE: Saved {len(df):,} observations")