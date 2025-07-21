# ABOUTME: GP.py - calculates gross profitability predictor
# ABOUTME: Gross profitability as (revenue - cost of goods sold) / assets, excluding financial firms

"""
GP predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/GP.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, revt, cogs, at, sic)

Outputs:
    - ../pyData/Predictors/GP.csv (permno, yyyymm, GP)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                     columns=['gvkey', 'permno', 'time_avail_m', 'revt', 'cogs', 'at', 'sic', 'datadate'])

# Convert sic to numeric, handling string values
df['sic'] = pd.to_numeric(df['sic'], errors='coerce')

# Keep only non-financial firms (SIC < 6000 or SIC >= 7000)
df = df[(df['sic'] < 6000) | (df['sic'] >= 7000)]

# SIGNAL CONSTRUCTION
df['GP'] = (df['revt'] - df['cogs']) / df['at']

# Drop missing values
df = df.dropna(subset=['GP'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'GP']].copy()

# SAVE
df.to_csv("../pyData/Predictors/GP.csv", index=False)
print(f"GP: Saved {len(df):,} observations")