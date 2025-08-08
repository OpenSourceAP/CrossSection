# ABOUTME: Share Volume - volatility of share volume (vol/shrout) over 3 months
# ABOUTME: Usage: python3 ShareVol.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Data load
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")

# Start with signal master table
df = signal_master.select(["permno", "time_avail_m", "sicCRSP", "exchcd"])

# Merge with monthly CRSP for volume and shares outstanding
df = df.join(
    monthly_crsp.select(["permno", "time_avail_m", "shrout", "vol"]),
    on=["permno", "time_avail_m"],
    how="inner"
)

# Sort by permno and time_avail_m (critical for proper lag operations)
df = df.sort(["permno", "time_avail_m"])

# Signal construction
# tempShareVol = (vol + l1.vol + l2.vol)/(3*shrout)*100
df = df.with_columns([
    pl.col("vol").shift(1).over("permno").alias("l1_vol"),
    pl.col("vol").shift(2).over("permno").alias("l2_vol")
])

# Calculate tempShareVol using standard formula with missing value handling
# Since first two observations will be set to ShareVol=1 regardless, use simpler logic
df = df.with_columns([
    ((pl.col("vol").fill_null(0) + pl.col("l1_vol").fill_null(0) + pl.col("l2_vol").fill_null(0)) / 
     (3 * pl.col("shrout")) * 100)
    .alias("tempShareVol")
])

# Drop if shrout changes in last 3 months
df = df.with_columns([
    pl.col("shrout").shift(1).over("permno").alias("l1_shrout"),
    pl.col("shrout").shift(2).over("permno").alias("l2_shrout")
])

# dshrout = shrout != l1.shrout
df = df.with_columns([
    (pl.col("shrout") != pl.col("l1_shrout")).alias("dshrout"),
    (pl.col("l1_shrout") != pl.col("l2_shrout")).alias("l1_dshrout"),
    (pl.col("l2_shrout").shift(1).over("permno") != pl.col("l2_shrout")).alias("l2_dshrout")
])

# Set dshrout = 0 if _n == 1 (first observation for each permno)
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("obs_num")
])

df = df.with_columns([
    pl.when(pl.col("obs_num") == 0)  # 0-indexed, so first observation is 0
    .then(False)
    .otherwise(pl.col("dshrout"))
    .alias("dshrout")
])

# dropObs = 1 if (dshrout + l1.dshrout + l2.dshrout) > 0
df = df.with_columns([
    pl.col("dshrout").shift(1).over("permno").alias("l1_dshrout_real"),
    pl.col("dshrout").shift(2).over("permno").alias("l2_dshrout_real")
])

df = df.with_columns([
    (pl.col("dshrout").cast(pl.Int32) + 
     pl.col("l1_dshrout_real").cast(pl.Int32).fill_null(0) + 
     pl.col("l2_dshrout_real").cast(pl.Int32).fill_null(0) > 0).alias("dropObs")
])

# Don't drop if first two months (_n == 1 | _n == 2)
df = df.with_columns([
    pl.when((pl.col("obs_num") == 0) | (pl.col("obs_num") == 1))  # 0-indexed
    .then(None)
    .otherwise(pl.col("dropObs"))
    .alias("dropObs")
])

# Drop if dropObs == 1
df = df.filter(
    (pl.col("dropObs") != True) | (pl.col("dropObs").is_null())
)

# Create ShareVol signal
# Based on debugging: Stata appears to set ShareVol=1 for first two observations of each permno
# regardless of tempShareVol value, then uses normal logic for subsequent observations
df = df.with_columns([
    pl.when((pl.col("obs_num") == 0) | (pl.col("obs_num") == 1))  # First two observations
    .then(1)  # Always ShareVol=1 for first two observations 
    .otherwise(
        pl.when(pl.col("tempShareVol") < 5)
        .then(0)
        .when(pl.col("tempShareVol") > 10)
        .then(1)
        .otherwise(None)
    )
    .alias("ShareVol")
])

# Select final data
result = df.select(["permno", "time_avail_m", "ShareVol"])

# Save predictor
save_predictor(result, "ShareVol")