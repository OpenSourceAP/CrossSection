# ABOUTME: DownsideBeta placebo - beta coefficient calculated only during market downside periods
# ABOUTME: Python equivalent of ZZ2_DownsideBeta.do using rolling regressions on downside market days

"""
Usage:
    python3 Placebos/ZZ2_DownsideBeta.py

Inputs:
    - dailyFF.parquet: Daily Fama-French factors with columns [time_d, mktrf, rf]
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, ret]

Outputs:
    - DownsideBeta.csv: permno, yyyymm, DownsideBeta columns
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting ZZ2_DownsideBeta.py...")

print("Step 1: Computing rolling market averages...")
# Load daily FF data and compute rolling market means
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
daily_ff = daily_ff.sort("time_d")

# Create time index for rolling window
daily_ff = daily_ff.with_columns([
    pl.int_range(pl.len()).alias("time_temp")
])

print(f"Daily FF data loaded: {len(daily_ff)} observations")

# Calculate 252-day rolling mean of market return (following asrol pattern)
# Use rolling mean with 252-day window, but allow earlier start with minimum 20 observations for early period compatibility
daily_ff = daily_ff.with_columns([
    pl.col("mktrf").rolling_mean(window_size=252, min_samples=20).alias("mu_market")
])

# Keep only downside market days (mktrf < mu_market) 
downside_ff = daily_ff.filter(
    pl.col("mktrf") < pl.col("mu_market")
).select(["time_d", "mktrf", "rf"])

print(f"Downside market days: {len(downside_ff)} observations")

print("Step 2: Loading and merging stock data...")
# Load daily CRSP data
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
df = daily_crsp.select(["permno", "time_d", "ret"])

# Merge with downside market days (inner join keeps only downside periods)
df = df.join(downside_ff, on="time_d", how="inner")

# Calculate excess returns
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("ret_excess")
])

print(f"Stock data on downside days: {len(df)} observations")

print("Step 3: Running rolling regressions...")
# Sort data for rolling regressions (following BetaVIX pattern)
df = df.sort(["permno", "time_d"])

# Set up time index for rolling window within each permno
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

# Run rolling regression of excess returns on market excess returns
# Using 252-day window with minimum 10 observations for maximum early period compatibility (Stata asreg may be more flexible)
print("Computing DownsideBeta using rolling regressions...")

df = df.with_columns(
    pl.col("ret_excess").least_squares.rolling_ols(
        pl.col("mktrf"),
        window_size=252,
        min_periods=10,
        mode="coefficients",
        add_intercept=True,
        null_policy="drop"
    ).over("permno").alias("coef")
).with_columns([
    pl.col("coef").struct.field("mktrf").alias("DownsideBeta")
])

print("Step 4: Converting to monthly and aggregating...")
# Convert to monthly frequency
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing DownsideBeta per permno-month (following gcollapse (lastnm))
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg([
    pl.col("DownsideBeta").drop_nulls().last().alias("DownsideBeta")
])

# Select final result
result = df.select(["permno", "time_avail_m", "DownsideBeta"])

# Filter out rows with missing DownsideBeta
result = result.filter(pl.col("DownsideBeta").is_not_null())

print(f"Final DownsideBeta observations: {len(result)}")

# Save
save_placebo(result, "DownsideBeta")

print("ZZ2_DownsideBeta.py completed successfully")