# ABOUTME: Idiosyncratic risk predictor using RMSE from 252-day rolling CAPM regression
# ABOUTME: Usage: python3 ZZ2_IdioVolAHT.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.asreg import asreg_polars
from utils.savepredictor import save_predictor


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


# Use utils/asreg.py helper for rolling regression with RMSE
# This replicates: asreg ret mktrf, window(time_temp 252) min(100) by(permno) rmse
df = asreg_polars(
    df,
    y="ret",  # Excess return (already calculated above)
    X=["mktrf"],
    by=["permno"],
    t="time_temp", 
    mode="rolling",
    window_size=252,
    min_samples=100,
    add_intercept=True,  # Stata's asreg includes intercept by default
    outputs=("rmse",),  # Only need RMSE output (equivalent to Stata's _rmse)
    coef_prefix="b_"
)


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

# Save predictor
save_predictor(result, "IdioVolAHT")