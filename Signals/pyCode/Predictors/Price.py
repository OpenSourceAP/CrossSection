# ABOUTME: Price predictor following Blume and Husic 1973, Table 2 column c
# ABOUTME: Log of absolute value of stock price (prc) from monthly CRSP

"""
Price.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/Price.py

Inputs:
    - monthlyCRSP.parquet: monthly CRSP with columns [permno, time_avail_m, shrcd, exchcd, prc]

Reads monthly CRSP directly, not SignalMasterTable, so the CRSP predictors can be
built without Compustat (see crsp_only.py). The share and exchange code screen
is the same as in SignalMasterTable.py, so the output is unchanged.

Outputs:
    - Price.csv: CSV file with columns [permno, yyyymm, Price]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/monthlyCRSP.parquet",
    columns=["permno", "time_avail_m", "shrcd", "exchcd", "prc"],
)

# Common stocks on major exchanges, as in SignalMasterTable.py
df = df[df["shrcd"].isin([10, 11, 12]) & df["exchcd"].isin([1, 2, 3])]

# SIGNAL CONSTRUCTION
df["Price"] = np.log(abs(df["prc"]))

# Drop missing values
df = df.dropna(subset=["Price"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "Price"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/Price.csv", index=False)
print(f"Price: Saved {len(df):,} observations")
