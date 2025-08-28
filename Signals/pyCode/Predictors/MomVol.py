# ABOUTME: Momentum among high volume stocks - independent double sort by momentum and volume
# ABOUTME: Usage: python3 MomVol.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append('.')
from utils.savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.asrol import asrol
from utils.stata_replication import stata_multi_lag

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

# Calculate 6-month momentum using stata_multi_lag for calendar validation
# Convert to pandas for calendar-based lag operations
import pandas as pd
import numpy as np

df_pd = df.to_pandas()
df_pd = df_pd.sort_values(['permno', 'time_avail_m'])

# Use stata_multi_lag for calendar-validated lag operations
df_pd = stata_multi_lag(df_pd, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5])

# Calculate 6-month momentum: (1+l.ret)*(1+l2.ret)*...*(1+l5.ret) - 1
df_pd['Mom6m'] = (
    (1 + df_pd['ret_lag1']) *
    (1 + df_pd['ret_lag2']) *
    (1 + df_pd['ret_lag3']) *
    (1 + df_pd['ret_lag4']) *
    (1 + df_pd['ret_lag5']) - 1
)


# Calculate 6-month calendar-based rolling mean volume (like Stata asrol window(time_avail_m 6))
# Use the asrol utility but with calendar-based approach
print("Calculating 6-month calendar-based rolling mean volume...")
df_pd = asrol(
    df_pd, 
    group_col='permno', 
    time_col='time_avail_m', 
    value_col='vol', 
    window=6, 
    stat='mean', 
    new_col_name='temp', 
    min_periods=5
)

# time_avail_m is already a column, no need to reset index

# Create momentum deciles within each time_avail_m (like fastxtile)
df_pd['catMom'] = fastxtile(df_pd, 'Mom6m', by='time_avail_m', n=10)


# Volume terciles within each time_avail_m
df_pd['catVol'] = fastxtile(df_pd, 'temp', by='time_avail_m', n=3)


# Convert back to polars (we're already in pandas from lag calculation)
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


# Drop temporary columns (including new lag columns)
df = df.drop(["ret_lag1", "ret_lag2", "ret_lag3", "ret_lag4", "ret_lag5", "obs_num", "temp", "catMom", "catVol"])

# Select final data
result = df.select(["permno", "time_avail_m", "MomVol"])

# Save predictor
save_predictor(result, "MomVol")