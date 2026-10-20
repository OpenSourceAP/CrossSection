# ABOUTME: Return on assets quarterly following Balakrishnan, Bartov and Faurel 2010, Figure 1 Overall SAR
# ABOUTME: Quarterly return on assets as quarterly income (ibq) divided by 3-month lagged quarterly assets (atq)

"""
roaq.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/roaq.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, time_avail_m, gvkey]
    - m_QCompustat.parquet: Quarterly Compustat data with columns [gvkey, time_avail_m, atq, ibq]

Outputs:
    - roaq.csv: CSV file with columns [permno, yyyymm, roaq]
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import stata_multi_lag

# DATA LOAD
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m"],
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

# Calendar lags retain missing endpoints; inserted rows are removed before calculating the signal.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "atq", [3])
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()


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
