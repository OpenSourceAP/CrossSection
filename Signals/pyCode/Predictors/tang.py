# ABOUTME: tang.py - calculates tangibility predictor for manufacturing firms
# ABOUTME: Asset tangibility measure using weighted average of cash, receivables, inventory, and PPE

"""
tang predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/tang.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, che, rect, invt, ppegt, at, sic)

Outputs:
    - ../pyData/Predictors/tang.csv (permno, yyyymm, tang)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                     columns=['permno', 'time_avail_m', 'che', 'rect', 'invt', 'ppegt', 'at', 'sic'])

# Remove duplicates by permno and time_avail_m (keep first)
df = df.groupby(['permno', 'time_avail_m']).first().reset_index()

# SIGNAL CONSTRUCTION
# Convert sic to numeric
df['sic'] = pd.to_numeric(df['sic'], errors='coerce')

# Keep only manufacturing firms (2000 <= SIC <= 3999)
df = df[(df['sic'] >= 2000) & (df['sic'] <= 3999)]

# Create size deciles for financial constraint measure
df['tempFC'] = df.groupby('time_avail_m')['at'].transform(
    lambda x: pd.qcut(x, q=10, labels=range(1, 11), duplicates='drop')
)

# Define financially constrained firms (lower three deciles)
df['FC'] = np.where(df['tempFC'] <= 3, 1, np.nan)
df['FC'] = np.where(df['tempFC'] >= 8, 0, df['FC'])

# Calculate tangibility
df['tang'] = (df['che'] + 0.715*df['rect'] + 0.547*df['invt'] + 0.535*df['ppegt']) / df['at']

# Drop missing values
df = df.dropna(subset=['tang'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'tang']].copy()

# SAVE
df.to_csv("../pyData/Predictors/tang.csv", index=False)
print(f"tang: Saved {len(df):,} observations")