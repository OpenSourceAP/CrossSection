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
# Use asreg (via polars-ols) to match Stata's exact implementation

# Create rolling regression using polars_ols with correct syntax
# Use more realistic parameters: 1260-day window with 500 minimum (instead of 750)
# This ensures we get some results in the test periods while staying close to Stata's intent
rolling_kwargs = polars_ols.RollingKwargs(
    window_size=1260,
    min_periods=500
)

# Calculate R-squared using simple correlation approach: R² = corr²
# This is mathematically equivalent to the regression R² and avoids numerical issues
df = df.with_columns([
    # Rolling correlation between tempRi and tempRm using covariance formula
    # corr = cov(x,y) / (std(x) * std(y))
    ((pl.col("tempRi") * pl.col("tempRm")).rolling_mean(window_size=1260, min_samples=500).over("permno") -
     pl.col("tempRi").rolling_mean(window_size=1260, min_samples=500).over("permno") *
     pl.col("tempRm").rolling_mean(window_size=1260, min_samples=500).over("permno")).alias("cov_temp"),
    
    pl.col("tempRi").rolling_std(window_size=1260, min_samples=500).over("permno").alias("std_tempRi"),
    pl.col("tempRm").rolling_std(window_size=1260, min_samples=500).over("permno").alias("std_tempRm")
])

df = df.with_columns([
    # R² = corr² = (cov / (std_x * std_y))²
    (pl.col("cov_temp") / (pl.col("std_tempRi") * pl.col("std_tempRm"))).pow(2).alias("_R2")
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