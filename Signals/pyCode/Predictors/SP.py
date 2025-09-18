# ABOUTME: Sales-to-price following Barbee, Mukherji and Raines 1996, Table 2 model 1
# ABOUTME: calculates sales-to-price ratio as sales (sale) divided by market value of equity (mve_c)

"""
SP.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/SP.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, sale]
    - SignalMasterTable.parquet: Signal master table with columns [permno, time_avail_m, mve_c]

Outputs:
    - SP.csv: CSV file with columns [permno, yyyymm, SP]
"""

import pandas as pd

# DATA LOAD
# Load Compustat data
compustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["permno", "time_avail_m", "sale"],
)

# Remove duplicates by permno and time_avail_m (keep first)
compustat = compustat.groupby(["permno", "time_avail_m"]).first().reset_index()

# Merge with SignalMasterTable
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_c"],
)

df = pd.merge(compustat, signal_master, on=["permno", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
df["SP"] = df["sale"] / df["mve_c"]

# Drop missing values
df = df.dropna(subset=["SP"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "SP"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/SP.csv", index=False)
print(f"SP: Saved {len(df):,} observations")
