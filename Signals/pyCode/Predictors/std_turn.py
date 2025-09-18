# ABOUTME: Share turnover volatility following Chordia, Subrahmanyam and Anshuman 2001, Table 5B
# ABOUTME: calculates standard deviation of turnover (vol/shrout) over the past 36 months
"""
std_turn.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/std_turn.py

Inputs:
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, vol, shrout, prc]

Outputs:
    - std_turn.csv: CSV file with columns [permno, yyyymm, std_turn]
    - std_turn = standard deviation of turnover over past 36 months, set to missing for size quintiles 4-5
"""

import polars as pl
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting std_turn.py...")

# Data load
print("Loading data...")
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = monthly_crsp.select(["permno", "time_avail_m", "vol", "shrout", "prc"])

# Sort by permno and time to ensure proper rolling window calculation
df = df.sort(["permno", "time_avail_m"])

# Signal construction
df = df.with_columns(
    [
        # Generate turnover
        (pl.col("vol") / pl.col("shrout")).alias("tempturn"),
        # Market value
        (pl.col("shrout") * pl.col("prc").abs()).alias("mve_c"),
    ]
)

# Rolling standard deviation of turnover using 36-month window, min 24 observations
df = df.with_columns(
    pl.col("tempturn")
    .rolling_std(window_size=36, min_samples=24)
    .over("permno")
    .alias("std_turn")
)

# Size quintiles by time_avail_m using groupby+qcut pattern
df_pandas = df.to_pandas()
df_pandas["tempqsize"] = df_pandas.groupby("time_avail_m")["mve_c"].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates="drop") + 1
)
df = pl.from_pandas(df_pandas)

# Set to null for size quintiles 4 and 5 (tiny spread per OP Tab3B)
df = df.with_columns(
    pl.when(pl.col("tempqsize") >= 4)
    .then(None)
    .otherwise(pl.col("std_turn"))
    .alias("std_turn")
)

# Select final data
result = df.select(["permno", "time_avail_m", "std_turn"])

# Save predictor
save_predictor(result, "std_turn")
print("std_turn.py completed successfully")
