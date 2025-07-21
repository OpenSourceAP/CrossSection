# ABOUTME: roaq.py - calculates return on assets quarterly predictor
# ABOUTME: Quarterly return on assets as quarterly income (ibq) divided by 3-month lagged quarterly assets (atq)

"""
roaq predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/roaq.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c, gvkey)
    - ../pyData/Intermediate/m_QCompustat.parquet (gvkey, time_avail_m, atq, ibq)

Outputs:
    - ../pyData/Predictors/roaq.csv (permno, yyyymm, roaq)
"""

import pandas as pd

# DATA LOAD
signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                               columns=['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# Keep only observations with non-missing gvkey (equivalent to Stata's keep if !mi(gvkey))
signal_master = signal_master[~signal_master['gvkey'].isna()].copy()

# Merge with quarterly Compustat data (equivalent to Stata's merge 1:1 ... keep(match))
qcompustat = pd.read_parquet("../pyData/Intermediate/m_QCompustat.parquet", 
                            columns=['gvkey', 'time_avail_m', 'atq', 'ibq'])

df = pd.merge(signal_master, qcompustat, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Sort for proper lagging
df = df.sort_values(['permno', 'time_avail_m'])

# Create 3-month lagged assets (quarterly)
# In Stata, l3.atq means 3 months back in calendar time, not 3 positions back
# We need to match each observation with its value from exactly 3 months earlier
df['time_lag3'] = df['time_avail_m'] - pd.DateOffset(months=3)

# Merge with self to get lagged values
df_lag = df[['permno', 'time_avail_m', 'atq']].copy()
df_lag.columns = ['permno', 'time_lag3', 'atq_lag3']

df = pd.merge(df, df_lag, on=['permno', 'time_lag3'], how='left')

# Calculate roaq
df['roaq'] = df['ibq'] / df['atq_lag3']

# Drop missing values
df = df.dropna(subset=['roaq'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'roaq']].copy()

# SAVE
df.to_csv("../pyData/Predictors/roaq.csv", index=False)
print(f"roaq: Saved {len(df):,} observations")