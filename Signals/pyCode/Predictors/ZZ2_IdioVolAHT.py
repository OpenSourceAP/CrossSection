# ABOUTME: Idiosyncratic risk predictor using RMSE from 252-day rolling CAPM regression
# ABOUTME: Usage: python3 ZZ2_IdioVolAHT.py (run from pyCode/ directory)

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting ZZ2_IdioVolAHT.py...")

# Data load
print("Loading daily CRSP and Fama-French data...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")


# Select required columns
df = daily_crsp.select(["permno", "time_d", "ret"])
print(f"Daily CRSP data: {df.shape[0]} rows")

# Merge with FF data
print("Merging with Fama-French factors...")
df = df.join(
    daily_ff.select(["time_d", "rf", "mktrf"]),
    on="time_d",
    how="inner"
)
print(f"After merge: {df.shape[0]} rows")

# Calculate excess return (Stata: replace ret = ret - rf)
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("ret")
])


# Critical: Filter out missing returns before creating time index
# This ensures rolling windows contain exactly 252 valid observations
df = df.filter(pl.col("ret").is_not_null() & pl.col("mktrf").is_not_null())

# Critical: Sort data first (from Beta.py success pattern)
df = df.sort(["permno", "time_d"])

# Set up time index for rolling window (Stata: time_temp = _n)
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])


# Use direct polars-ols for rolling regression to get residuals, then compute RMSE
print("Running 252-day rolling CAPM regressions...")
# This replicates: asreg ret mktrf, window(time_temp 252) min(100) by(permno) rmse

# Get rolling residuals
df = df.with_columns(
    pl.col("ret").least_squares.rolling_ols(
        pl.col("mktrf"),
        window_size=252,
        min_periods=100,
        mode="residuals",
        add_intercept=True,
        null_policy="drop"
    ).over("permno").alias("resid")
)

# Calculate RMSE for each window
# RMSE = sqrt(mean(residuals^2))
df = df.with_columns(
    (pl.col("resid") ** 2)
    .rolling_mean(window_size=252, min_periods=100)
    .over("permno")
    .sqrt()
    .alias("rmse")
)


print("Calculating idiosyncratic volatility...")
# Extract IdioVolAHT from RMSE (rename _rmse IdioVolAHT in Stata)
df = df.with_columns([
    pl.col("rmse").alias("IdioVolAHT")
])

# Convert to monthly and keep last observation per month
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing IdioVolAHT per permno-month (Stata: gcollapse (lastnm))
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg([
    pl.col("IdioVolAHT").drop_nulls().last().alias("IdioVolAHT")
])


# Select final data
result = df.select(["permno", "time_avail_m", "IdioVolAHT"])
print(f"Calculated IdioVolAHT for {result.shape[0]} observations")

# Save predictor
save_predictor(result, "IdioVolAHT")
print("ZZ2_IdioVolAHT.py completed successfully")