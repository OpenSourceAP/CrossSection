# ABOUTME: Return on assets quarterly following Balakrishnan, Bartov and Faurel 2010, Figure 1 Overall SAR
# ABOUTME: Quarterly return on assets as quarterly income (ibq) divided by 3-month lagged quarterly assets (atq)

"""
roaq.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/roaq.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, time_avail_m, mve_permco, gvkey]
    - m_QCompustat.parquet: Quarterly Compustat data with columns [gvkey, time_avail_m, atq, ibq]

Outputs:
    - roaq.csv: CSV file with columns [permno, yyyymm, roaq]
"""

import pandas as pd

# DATA LOAD
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m", "mve_permco"],
)

# Keep only observations with valid company identifiers
signal_master = signal_master[~signal_master["gvkey"].isna()].copy()

# Load and prepare quarterly Compustat data
qcompustat = pd.read_parquet(
    "../pyData/Intermediate/m_QCompustat.parquet",
    columns=["gvkey", "time_avail_m", "atq", "ibq"],
)

# Merge quarterly data - only keep observations available in both datasets
df = pd.merge(signal_master, qcompustat, on=["gvkey", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Sort by company and time for historical data lookups
df = df.sort_values(["permno", "time_avail_m"])

# Get assets from 3 months ago for each observation
df["time_lag3"] = df["time_avail_m"] - pd.DateOffset(months=3)

# Self-merge to get 3-month lagged values
df_lag = df[["permno", "time_avail_m", "atq"]].copy()
df_lag.columns = ["permno", "time_lag3", "atq_lag3"]

df = pd.merge(df, df_lag, on=["permno", "time_lag3"], how="left")

# Calculate quarterly return on assets: quarterly income divided by lagged assets
df["roaq"] = df["ibq"] / df["atq_lag3"]

# Drop missing values
df = df.dropna(subset=["roaq"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "roaq"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/roaq.csv", index=False)
print(f"roaq: Saved {len(df):,} observations")
