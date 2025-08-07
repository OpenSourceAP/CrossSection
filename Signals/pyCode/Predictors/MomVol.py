# ABOUTME: Momentum among high volume stocks - independent double sort by momentum and volume
# ABOUTME: Usage: python3 MomVol.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Data load
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")

# Start with signal master table
df = signal_master.select(["permno", "time_avail_m", "ret"])

# Merge with monthly CRSP for volume
df = df.join(
    monthly_crsp.select(["permno", "time_avail_m", "vol"]),
    on=["permno", "time_avail_m"],
    how="inner"
)

# Signal construction
df = df.with_columns([
    # Clean volume (set negative to null)
    pl.when(pl.col("vol") < 0)
    .then(None)
    .otherwise(pl.col("vol"))
    .alias("vol"),
    # Fill missing returns with 0
    pl.col("ret").fill_null(0)
])

# Calculate 6-month momentum (compound returns over 6 months)
df = df.with_columns([
    ((1 + pl.col("ret").shift(1).over("permno")) *
     (1 + pl.col("ret").shift(2).over("permno")) *
     (1 + pl.col("ret").shift(3).over("permno")) *
     (1 + pl.col("ret").shift(4).over("permno")) *
     (1 + pl.col("ret").shift(5).over("permno")) - 1).alias("Mom6m")
])

# Create momentum deciles (10 portfolios)
df = df.with_columns([
    pl.col("Mom6m")
    .qcut(10, allow_duplicates=True)
    .over("time_avail_m")
    .cast(pl.Int32)
    .alias("catMom")
])

# Calculate 6-month average volume
df = df.with_columns([
    pl.col("vol")
    .rolling_mean(window_size=6, min_samples=5)
    .over("permno")
    .alias("temp")
])

# Create volume terciles (3 portfolios)
df = df.with_columns([
    pl.col("temp")
    .qcut(3, allow_duplicates=True)
    .over("time_avail_m")
    .cast(pl.Int32)
    .alias("catVol")
])

# MomVol = momentum decile only for high volume stocks (tercile 3)
df = df.with_columns([
    pl.when(pl.col("catVol") == 2)  # 0-indexed, so tercile 3 is index 2
    .then(pl.col("catMom") + 1)  # Convert to 1-based
    .otherwise(None)
    .alias("MomVol")
])

# Filter: set to missing if less than 24 observations per permno
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("obs_num")
])

df = df.with_columns([
    pl.when(pl.col("obs_num") < 23)  # 0-indexed, so < 24 means obs_num < 23
    .then(None)
    .otherwise(pl.col("MomVol"))
    .alias("MomVol")
])

# Select final data
result = df.select(["permno", "time_avail_m", "MomVol"])

# Save predictor
save_predictor(result, "MomVol")