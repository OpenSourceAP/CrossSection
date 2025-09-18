# ABOUTME: Price predictor following Blume and Husic 1973, Table 2 column c
# ABOUTME: Log of absolute value of stock price (prc) from SignalMasterTable

"""
Price predictor calculation

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/Price.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, prc)

Outputs:
    - ../pyData/Predictors/Price.csv (permno, yyyymm, Price)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "prc"],
)

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
