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

# Load and prepare quarterly Compustat data
qcompustat = pd.read_parquet("../pyData/Intermediate/m_QCompustat.parquet", 
                            columns=['gvkey', 'time_avail_m', 'atq', 'ibq'])

# Merge quarterly data - only keep observations that match in both datasets (like Stata's keep(match))
df = pd.merge(signal_master, qcompustat, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Sort for proper lagging (equivalent to Stata's xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Create 3-month lagged assets using calendar-based approach (not position-based)
# This replicates Stata's l3.atq which looks back exactly 3 months in calendar time
df['time_lag3'] = df['time_avail_m'] - pd.DateOffset(months=3)

# Self-merge to get 3-month lagged values
df_lag = df[['permno', 'time_avail_m', 'atq']].copy()
df_lag.columns = ['permno', 'time_lag3', 'atq_lag3']

df = pd.merge(df, df_lag, on=['permno', 'time_lag3'], how='left')

# Calculate roaq (matching Stata's ibq/l3.atq)
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