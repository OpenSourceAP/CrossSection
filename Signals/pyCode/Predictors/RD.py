# ABOUTME: RD.py - calculates R&D intensity predictor
# ABOUTME: R&D intensity as R&D expenditure (xrd) divided by market value of equity (mve_c)

"""
RD predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/RD.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c, gvkey)
    - ../pyData/Intermediate/m_aCompustat.parquet (gvkey, time_avail_m, xrd)

Outputs:
    - ../pyData/Predictors/RD.csv (permno, yyyymm, RD)
"""

import pandas as pd

# DATA LOAD
signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                               columns=['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# Drop observations with missing gvkey
df = signal_master.dropna(subset=['gvkey']).copy()

# Merge with Compustat data
compustat = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                           columns=['gvkey', 'time_avail_m', 'xrd'])

df = pd.merge(df, compustat, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
df['RD'] = df['xrd'] / df['mve_c']

# Drop missing values
df = df.dropna(subset=['RD'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'RD']].copy()

# SAVE
df.to_csv("../pyData/Predictors/RD.csv", index=False)
print(f"RD: Saved {len(df):,} observations")