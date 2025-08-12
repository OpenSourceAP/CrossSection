# ABOUTME: Momentum among high volume stocks - independent double sort by momentum and volume
# ABOUTME: Usage: python3 MomVol.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile

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

# Sort by permno and time_avail_m (critical for proper lag operations)
df = df.sort(["permno", "time_avail_m"])

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

# Calculate 6-month momentum using calendar-based lags (like Stata l.ret, l2.ret, etc.)
df = df.with_columns([
    pl.col("ret").shift(1).over("permno").alias("l1_ret"),
    pl.col("ret").shift(2).over("permno").alias("l2_ret"),
    pl.col("ret").shift(3).over("permno").alias("l3_ret"),
    pl.col("ret").shift(4).over("permno").alias("l4_ret"),
    pl.col("ret").shift(5).over("permno").alias("l5_ret")
])

df = df.with_columns([
    ((1 + pl.col("l1_ret")) *
     (1 + pl.col("l2_ret")) *
     (1 + pl.col("l3_ret")) *
     (1 + pl.col("l4_ret")) *
     (1 + pl.col("l5_ret")) - 1).alias("Mom6m")
])

# Calculate 6-month rolling mean volume (like Stata asrol)
df = df.with_columns([
    pl.col("vol")
    .rolling_mean(window_size=6, min_samples=5)
    .over("permno")
    .alias("temp")
])

# Convert to pandas for proper quantile operations (fastxtile equivalent)
import pandas as pd
import numpy as np

df_pd = df.to_pandas()

# Create momentum deciles within each time_avail_m (like fastxtile)
df_pd['catMom'] = fastxtile(df_pd, 'Mom6m', by='time_avail_m', n=10)
df_pd['catVol'] = fastxtile(df_pd, 'temp', by='time_avail_m', n=3)

# Convert back to polars
df = pl.from_pandas(df_pd)

# MomVol = momentum decile only for high volume stocks (tercile 3)
df = df.with_columns([
    pl.when(pl.col("catVol") == 3)  # tercile 3 (fastxtile returns 1-based)
    .then(pl.col("catMom"))  # catMom is already 1-based from fastxtile
    .otherwise(None)
    .alias("MomVol")
])

# Filter: set to missing if observation number < 24 (like Stata _n < 24)
# Add observation number within each permno group
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("obs_num")
])

df = df.with_columns([
    pl.when(pl.col("obs_num") < 23)  # 0-indexed, so < 24 means obs_num < 23
    .then(None)
    .otherwise(pl.col("MomVol"))
    .alias("MomVol")
])

# Drop temporary columns
df = df.drop(["l1_ret", "l2_ret", "l3_ret", "l4_ret", "l5_ret", "obs_num", "temp"])

# Select final data
result = df.select(["permno", "time_avail_m", "MomVol"])

# Save predictor
save_predictor(result, "MomVol")