# ABOUTME: R&D intensity following Chan, Lakonishok and Sougiannis 2001, Table 4, first year
# ABOUTME: calculates R&D expenditure (xrd) divided by market value of equity (mve_permco)

"""
RD.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/RD.py

Inputs:
    - SignalMasterTable.parquet: Signal master table with columns [permno, gvkey, time_avail_m, mve_permco]
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, time_avail_m, xrd]

Outputs:
    - RD.csv: CSV file with columns [permno, yyyymm, RD]
"""

import pandas as pd

# DATA LOAD
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m", "mve_permco"],
)

# Drop observations with missing gvkey
df = signal_master.dropna(subset=["gvkey"]).copy()

# Merge with Compustat data
compustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "time_avail_m", "xrd"],
)

df = pd.merge(df, compustat, on=["gvkey", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
df["RD"] = df["xrd"] / df["mve_permco"]

# Drop missing values
df = df.dropna(subset=["RD"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "RD"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/RD.csv", index=False)
print(f"RD: Saved {len(df):,} observations")
