# ABOUTME: Momentum among high volume stocks - independent double sort by momentum and volume
# ABOUTME: Usage: python3 MomVol.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append('.')
from utils.savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.asrol import asrol

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
# Convert to pandas for calendar-based lag operations
import pandas as pd
import numpy as np

df_pd = df.to_pandas()
df_pd = df_pd.sort_values(['permno', 'time_avail_m'])

# Create calendar-based lag values like Stata l.ret, l2.ret, etc.
lag_dfs = []
for lag in range(1, 6):  # l.ret through l5.ret
    lag_df = df_pd[['permno', 'time_avail_m', 'ret']].copy()
    lag_df['time_avail_m'] = lag_df['time_avail_m'] + pd.DateOffset(months=lag)
    lag_df = lag_df.rename(columns={'ret': f'l{lag}_ret'})
    lag_dfs.append(lag_df)

# Merge all lag values
for lag_df in lag_dfs:
    df_pd = df_pd.merge(lag_df, on=['permno', 'time_avail_m'], how='left')

# Calculate 6-month momentum: (1+l.ret)*(1+l2.ret)*...*(1+l5.ret) - 1
# Don't fill missing values - let pandas handle missing propagation naturally
df_pd['Mom6m'] = (
    (1 + df_pd['l1_ret']) *
    (1 + df_pd['l2_ret']) *
    (1 + df_pd['l3_ret']) *
    (1 + df_pd['l4_ret']) *
    (1 + df_pd['l5_ret']) - 1
)

# CHECKPOINT 1: Debug momentum calculation for problematic observations  
print("CHECKPOINT 1: Momentum calculation")
debug_obs = df_pd[(df_pd["permno"] == 10006) & (df_pd["time_avail_m"] == pd.Timestamp('1943-01-01'))]
if len(debug_obs) > 0:
    print(debug_obs[["permno", "time_avail_m", "ret", "l1_ret", "l2_ret", "l3_ret", "l4_ret", "l5_ret", "Mom6m"]])

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

# CHECKPOINT 2: Debug momentum quantiles
print("CHECKPOINT 2: Momentum quantiles")
debug_obs = df_pd[(df_pd["permno"] == 10006) & (df_pd["time_avail_m"] == pd.Timestamp('1943-01-01'))]
if len(debug_obs) > 0:
    print(debug_obs[["permno", "time_avail_m", "Mom6m", "catMom"]])
time_subset = df_pd[df_pd["time_avail_m"] == pd.Timestamp('1943-01-01')]["Mom6m"].dropna()
if len(time_subset) > 0:
    print(f"Momentum stats for 1943-01: {time_subset.describe()}")
    print(f"Momentum decile cutoffs: {np.percentile(time_subset, [10, 20, 30, 40, 50, 60, 70, 80, 90])}")

# CHECKPOINT 3: Debug volume rolling calculation
print("CHECKPOINT 3: Volume rolling calculation")
debug_obs = df_pd[(df_pd["permno"] == 10006) & (df_pd["time_avail_m"] == pd.Timestamp('1943-01-01'))]
if len(debug_obs) > 0:
    print(debug_obs[["permno", "time_avail_m", "vol", "temp"]])
# Volume terciles within each time_avail_m
df_pd['catVol'] = fastxtile(df_pd, 'temp', by='time_avail_m', n=3)

# CHECKPOINT 4: Debug volume quantiles
print("CHECKPOINT 4: Volume quantiles")
debug_obs = df_pd[(df_pd["permno"] == 10006) & (df_pd["time_avail_m"] == pd.Timestamp('1943-01-01'))]
if len(debug_obs) > 0:
    print(debug_obs[["permno", "time_avail_m", "temp", "catVol"]])
time_subset = df_pd[df_pd["time_avail_m"] == pd.Timestamp('1943-01-01')]["temp"].dropna()
if len(time_subset) > 0:
    print(f"Volume stats for 1943-01: {time_subset.describe()}")
    print(f"Volume tercile cutoffs: {np.percentile(time_subset, [33.33, 66.67])}")
    print(f"Volume tercile counts: {df_pd[df_pd['time_avail_m'] == pd.Timestamp('1943-01-01')]['catVol'].value_counts().sort_index()}")

# Convert back to polars (we're already in pandas from lag calculation)
df = pl.from_pandas(df_pd)

# MomVol = momentum decile only for high volume stocks (tercile 3)
df = df.with_columns([
    pl.when(pl.col("catVol") == 3)  # tercile 3 (fastxtile returns 1-based)
    .then(pl.col("catMom"))  # catMom is already 1-based from fastxtile
    .otherwise(None)
    .alias("MomVol")
])

# CHECKPOINT 5: Debug final signal assignment  
print("CHECKPOINT 5: Final signal assignment")
debug_obs = df.filter((pl.col("permno") == 10006) & (pl.col("time_avail_m") == pl.date(1943, 1, 1)))
if len(debug_obs) > 0:
    print(debug_obs.select(["permno", "time_avail_m", "catMom", "catVol", "MomVol"]))
high_vol_count = len(df.filter((pl.col("catVol") == 3) & (pl.col("time_avail_m") == pl.date(1943, 1, 1))))
non_missing_count = len(df.filter((pl.col("MomVol").is_not_null()) & (pl.col("time_avail_m") == pl.date(1943, 1, 1))))
print(f"High volume stocks (catVol==3): {high_vol_count}")
print(f"Non-missing MomVol: {non_missing_count}")

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

# CHECKPOINT 6: Debug time filter
print("CHECKPOINT 6: Time filter") 
debug_obs = df.filter((pl.col("permno") == 10006) & (pl.col("time_avail_m") == pl.date(1943, 1, 1)))
if len(debug_obs) > 0:
    print(debug_obs.select(["permno", "time_avail_m", "obs_num", "MomVol"]))

# Drop temporary columns (including new lag columns)
df = df.drop(["l1_ret", "l2_ret", "l3_ret", "l4_ret", "l5_ret", "obs_num", "temp", "catMom", "catVol"])

# Select final data
result = df.select(["permno", "time_avail_m", "MomVol"])

# Save predictor
save_predictor(result, "MomVol")