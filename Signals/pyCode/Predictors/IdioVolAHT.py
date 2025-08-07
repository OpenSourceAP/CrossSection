# ABOUTME: Idiosyncratic risk predictor using RMSE from 252-day rolling CAPM regression
# ABOUTME: Usage: python3 IdioVolAHT.py (run from pyCode/ directory)

import polars as pl
import polars_ols  # Enable polars-ols functionality
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Data load
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")

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

# Set up time index for rolling window
df = df.sort(["permno", "time_d"])
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

# Rolling regression: ret_excess ~ mktrf
# 252-day window with minimum 100 observations
# Get residuals to calculate RMSE
df = df.with_columns([
    pl.col("ret_excess")
    .least_squares.rolling_ols(
        pl.col("mktrf"),
        window_size=252,
        min_periods=100,
        mode="residuals"
    )
    .over("permno")
    .alias("residuals")
])

# Calculate rolling RMSE (root mean squared error of residuals)
# RMSE = sqrt(mean(residuals^2))
df = df.with_columns([
    (pl.col("residuals") ** 2)
    .rolling_mean(window_size=252, min_samples=100)
    .over("permno")
    .sqrt()
    .alias("IdioVolAHT")
])

# Convert to monthly and keep last observation per month
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing IdioVolAHT per permno-month
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg([
    pl.col("IdioVolAHT").drop_nulls().last().alias("IdioVolAHT")
])

# Select final data
result = df.select(["permno", "time_avail_m", "IdioVolAHT"])

# Save predictor
save_predictor(result, "IdioVolAHT")