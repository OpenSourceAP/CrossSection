# ABOUTME: Market leverage following Bhandari 1988, Table 1 DER
# ABOUTME: calculates market leverage as total liabilities divided by market value of equity

"""
Leverage predictor calculation

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/Leverage.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, lt)
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c)

Outputs:
    - ../pyData/Predictors/Leverage.csv (permno, yyyymm, Leverage)
"""

import pandas as pd

# DATA LOAD
# Load Compustat data
compustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "lt"],
)

# Remove duplicates by permno and time_avail_m (keep first)
compustat = compustat.groupby(["permno", "time_avail_m"]).first().reset_index()

# Merge with SignalMasterTable
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_c"],
)

df = pd.merge(
    signal_master,
    compustat[["permno", "time_avail_m", "lt"]],
    on=["permno", "time_avail_m"],
    how="inner",
)

# SIGNAL CONSTRUCTION
df["Leverage"] = df["lt"] / df["mve_c"]

# Drop missing values
df = df.dropna(subset=["Leverage"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "Leverage"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/Leverage.csv", index=False)
print(f"Leverage: Saved {len(df):,} observations")
