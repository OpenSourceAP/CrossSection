# ABOUTME: Frazzini-Pedersen beta using rolling correlations and volatility ratios
# ABOUTME: Usage: python3 BetaFP.py (run from pyCode/ directory)

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
    (pl.col("ret") - pl.col("rf")).alias("ret"),
    pl.col("ret").log1p().alias("LogRet"),
    pl.col("mktrf").log1p().alias("LogMkt")
])

# Set up time index for rolling window
df = df.sort(["permno", "time_d"])
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

# Calculate 252-day rolling standard deviations
df = df.with_columns([
    pl.col("LogRet")
    .rolling_std(window_size=252, min_samples=120)
    .over("permno")
    .alias("sd252_LogRet"),
    pl.col("LogMkt")
    .rolling_std(window_size=252, min_samples=120)
    .over("permno")
    .alias("sd252_LogMkt")
])

# Create 3-day overlapping returns
df = df.with_columns([
    (pl.col("LogRet").shift(2).over("permno") + 
     pl.col("LogRet").shift(1).over("permno") + 
     pl.col("LogRet")).alias("tempRi"),
    (pl.col("LogMkt").shift(2).over("permno") + 
     pl.col("LogMkt").shift(1).over("permno") + 
     pl.col("LogMkt")).alias("tempRm")
])

# Rolling regression on 1260-day window (5 years) with min 750 observations
df = df.with_columns([
    pl.col("tempRi")
    .least_squares.rolling_ols(
        pl.col("tempRm"),
        window_size=1260,
        min_periods=750,
        mode="coefficients"
    )
    .over("permno")
    .alias("_b_coeffs")
])

# For R-squared, we need to calculate it from predictions and actuals
# First get predictions
df = df.with_columns([
    pl.col("tempRi")
    .least_squares.rolling_ols(
        pl.col("tempRm"),
        window_size=1260,
        min_periods=750,
        mode="predictions"
    )
    .over("permno")
    .alias("predictions")
])

# Calculate R-squared manually: 1 - SS_res/SS_tot
# Using rolling window approach
df = df.with_columns([
    # Calculate mean of tempRi over rolling window
    pl.col("tempRi")
    .rolling_mean(window_size=1260, min_samples=750)
    .over("permno")
    .alias("mean_tempRi"),
    # Calculate residuals
    (pl.col("tempRi") - pl.col("predictions")).alias("residuals")
])

df = df.with_columns([
    # SS_res: sum of squared residuals (using rolling sum approximation)
    (pl.col("residuals") ** 2)
    .rolling_sum(window_size=1260, min_samples=750)
    .over("permno")
    .alias("SS_res"),
    # SS_tot: total sum of squares
    ((pl.col("tempRi") - pl.col("mean_tempRi")) ** 2)
    .rolling_sum(window_size=1260, min_samples=750)
    .over("permno")
    .alias("SS_tot")
])

df = df.with_columns([
    # R-squared
    (1 - pl.col("SS_res") / pl.col("SS_tot")).alias("_R2")
])

# Calculate Frazzini-Pedersen beta
df = df.with_columns([
    (pl.col("_R2").abs().sqrt() * (pl.col("sd252_LogRet") / pl.col("sd252_LogMkt"))).alias("BetaFP")
])

# Convert to monthly and keep last observation per month
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing BetaFP per permno-month
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg([
    pl.col("BetaFP").drop_nulls().last().alias("BetaFP")
])

# Select final data
result = df.select(["permno", "time_avail_m", "BetaFP"])

# Save predictor
save_predictor(result, "BetaFP")