# ABOUTME: Systematic volatility predictor using rolling regression of returns on market and VIX changes
# ABOUTME: Usage: python3 betaVIX.py (run from pyCode/ directory)

import polars as pl
import polars_ols  # Enable polars-ols functionality
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Data load
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
d_vix = pl.read_parquet("../pyData/Intermediate/d_vix.parquet")

# Select required columns
df = daily_crsp.select(["permno", "time_d", "ret"])

# Merge with FF data
df = df.join(
    daily_ff.select(["time_d", "rf", "mktrf"]),
    on="time_d",
    how="inner"
)

# Calculate excess return
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("ret_excess")
])

# Merge with VIX data
df = df.join(
    d_vix.select(["time_d", "dVIX"]),
    on="time_d",
    how="inner"
)

# Set up time index for rolling window
df = df.sort(["permno", "time_d"])
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

# Rolling regression: ret_excess ~ mktrf + dVIX
# 20-day window with minimum 15 observations
df = df.with_columns([
    pl.col("ret_excess")
    .least_squares.rolling_ols(
        pl.col("mktrf"),
        pl.col("dVIX"),
        window_size=20,
        min_periods=15,
        mode="coefficients"
    )
    .over("permno")
    .alias("_b_coeffs")
])

# Extract betaVIX coefficient
df = df.with_columns([
    pl.col("_b_coeffs").struct.field("dVIX").alias("betaVIX")
])

# Convert to monthly and keep last observation per month
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing betaVIX per permno-month
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg([
    pl.col("betaVIX").drop_nulls().last().alias("betaVIX")
])

# Select final data
result = df.select(["permno", "time_avail_m", "betaVIX"])

# Save predictor
save_predictor(result, "betaVIX")