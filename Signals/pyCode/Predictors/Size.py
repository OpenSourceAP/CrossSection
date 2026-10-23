# ABOUTME: Size following Banz 1981, Table 3, alpha_1 n=50
# ABOUTME: calculates log of market value of equity as size predictor

"""
Size.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/Size.py

Inputs:
    - monthlyCRSP.parquet: monthly CRSP with columns [permno, time_avail_m, shrcd, exchcd, mve_c]

Reads monthly CRSP directly, not SignalMasterTable, so the CRSP predictors can be
built without Compustat (see crsp_only.py). The share and exchange code screen
is the same as in SignalMasterTable.py, so the output is unchanged.

Outputs:
    - Size.csv: CSV file with columns [permno, yyyymm, Size]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/monthlyCRSP.parquet",
    columns=["permno", "time_avail_m", "shrcd", "exchcd", "mve_c"],
)

# Common stocks on major exchanges, as in SignalMasterTable.py
df = df[df["shrcd"].isin([10, 11, 12]) & df["exchcd"].isin([1, 2, 3])]

# SIGNAL CONSTRUCTION
df["Size"] = np.log(df["mve_c"])

# Drop missing values
df = df.dropna(subset=["Size"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "Size"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/Size.csv", index=False)
print(f"Size: Saved {len(df):,} observations")
