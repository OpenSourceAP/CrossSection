# ABOUTME: Short-term reversal following Jegadeesh 1990, Table 2, Jan-Dec
# ABOUTME: calculates stock return over the previous month (1-month momentum/reversal)

"""
STreversal.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/STreversal.py

Inputs:
    - monthlyCRSP.parquet: monthly CRSP with columns [permno, time_avail_m, shrcd, exchcd, ret]

Reads monthly CRSP directly, not SignalMasterTable, so the CRSP predictors can be
built without Compustat (see crsp_only.py). The share and exchange code screen
is the same as in SignalMasterTable.py, so the output is unchanged.

Outputs:
    - STreversal.csv: CSV file with columns [permno, yyyymm, STreversal]
"""

import polars as pl
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting STreversal.py...")

# Data load
print("Loading monthly CRSP...")
df = pl.read_parquet(
    "../pyData/Intermediate/monthlyCRSP.parquet",
    columns=["permno", "time_avail_m", "shrcd", "exchcd", "ret"],
)

# Common stocks on major exchanges, as in SignalMasterTable.py
df = df.filter(
    pl.col("shrcd").cast(pl.Int64).is_in([10, 11, 12])
    & pl.col("exchcd").cast(pl.Int64).is_in([1, 2, 3])
)
df = df.select(["permno", "time_avail_m", "ret"])
print(f"Loaded data: {df.shape[0]} rows")

# Signal construction
print("Calculating STreversal...")
df = df.with_columns(
    [
        # Fill missing returns with 0 and use as STreversal
        pl.col("ret")
        .fill_null(0)
        .alias("STreversal")
    ]
)

# Select final data
result = df.select(["permno", "time_avail_m", "STreversal"])
print(f"Calculated STreversal for {result.shape[0]} observations")

# Save predictor
save_predictor(result, "STreversal")
print("STreversal.py completed successfully")
