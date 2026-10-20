# ABOUTME: Earnings-to-Price Ratio following Basu 1977, Table 1 average annual rate
# ABOUTME: calculates earnings-to-price ratio as income before extraordinary items divided by 6-month lagged market value

"""
EP.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/EP.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ib]
    - SignalMasterTable.parquet: Signal master table with columns [permno, time_avail_m, mve_permco]

Outputs:
    - EP.csv: CSV file with columns [permno, yyyymm, EP]
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import stata_multi_lag

# DATA LOAD
# Load Compustat data
compustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "ib"],
)

# Remove duplicates by permno and time_avail_m (keep first)
compustat = compustat.groupby(["permno", "time_avail_m"]).first().reset_index()

# Merge with SignalMasterTable (keep using match logic)
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_permco"],
)

df = pd.merge(
    signal_master,
    compustat[["permno", "time_avail_m", "ib"]],
    on=["permno", "time_avail_m"],
    how="left",
)

# SIGNAL CONSTRUCTION
# Sort for proper lagging
df = df.sort_values(["permno", "time_avail_m"])

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "mve_permco", [6])
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate EP with 6-month lagged market value
df["EP"] = df["ib"] / df["mve_permco_lag6"]

# Exclude negative EP values
df.loc[df["EP"] < 0, "EP"] = pd.NA

# Drop missing values
df = df.dropna(subset=["EP"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "EP"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/EP.csv", index=False)
print(f"EP: Saved {len(df):,} observations")
