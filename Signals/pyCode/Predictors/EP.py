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

# Create 6-month lagged mve_permco using calendar-based approach
# Look back exactly 6 months in calendar time to align earnings with appropriate market value
df["time_lag6"] = df["time_avail_m"] - pd.DateOffset(months=6)

# Self-merge to get 6-month lagged values
df_lag = df[["permno", "time_avail_m", "mve_permco"]].copy()
df_lag.columns = ["permno", "time_lag6", "mve_permco_lag6"]

df = pd.merge(df, df_lag, on=["permno", "time_lag6"], how="left")

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
