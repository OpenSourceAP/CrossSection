# ABOUTME: Systematic volatility following Ang, Hodrick, Xing, and Zhang 2006, Table 1A
# ABOUTME: calculates betaVIX coefficient from rolling regression of stock returns on market and VIX changes
"""
Usage:
    python3 Predictors/ZZ2_betaVIX.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, ret]
    - dailyFF.parquet: Daily Fama-French factors with columns [time_d, rf, mktrf]
    - d_vix.parquet: Daily VIX changes with columns [time_d, dVIX]

Outputs:
    - betaVIX.csv: CSV file with columns [permno, yyyymm, betaVIX]
    - betaVIX = coefficient on daily change in VIX from 1-month rolling regression (20-day window, min 15 obs)
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting ZZ2_betaVIX.py...")

# Data load
print("Loading data...")
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

# Critical: Sort data first (from Beta.py success pattern)
df = df.sort(["permno", "time_d"])

# Set up time index for rolling window
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

# Use direct polars-ols for rolling regression
# Rolling regression of excess returns on market factor and VIX changes using 20-day window with minimum 15 observations

# Sort is already done above
df = df.with_columns(
    pl.col("ret_excess").least_squares.rolling_ols(
        pl.col("mktrf"), pl.col("dVIX"),
        window_size=20,
        min_periods=15,
        mode="coefficients",
        add_intercept=True,
        null_policy="drop"
    ).over("permno").alias("coef")
).with_columns([
    pl.col("coef").struct.field("const").alias("b_const"),
    pl.col("coef").struct.field("mktrf").alias("b_mktrf"),
    pl.col("coef").struct.field("dVIX").alias("b_dVIX")
])

# Extract betaVIX coefficient from dVIX regression term
df = df.with_columns([
    pl.col("b_dVIX").alias("betaVIX")
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
print("ZZ2_betaVIX.py completed successfully")