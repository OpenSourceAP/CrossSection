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

import os
import sys

import pandas as pd
import polars as pl
import polars_ols as pls  # Registers .least_squares namespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("=" * 80)
print("ZZ2_betaVIX.py")
print("Generating betaVIX predictor from daily market and VIX data")
print("=" * 80)

# DATA LOAD
print("Loading daily datasets...")
print("Loading dailyCRSP.parquet...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
print(f"Loaded daily CRSP observations: {len(daily_crsp):,}")

print("Loading dailyFF.parquet...")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
print(f"Loaded daily Fama-French observations: {len(daily_ff):,}")

print("Loading d_vix.parquet...")
d_vix = pl.read_parquet("../pyData/Intermediate/d_vix.parquet")
print(f"Loaded daily VIX change observations: {len(d_vix):,}")

# MERGE DATA SOURCES
print("Merging CRSP returns with factors and VIX changes...")
df = (
    daily_crsp.select(["permno", "time_d", "ret"])
    .join(daily_ff.select(["time_d", "rf", "mktrf"]), on="time_d", how="inner")
    .with_columns((pl.col("ret") - pl.col("rf")).alias("ret_excess"))
    .join(d_vix.select(["time_d", "dVIX"]), on="time_d", how="inner")
    .sort(["permno", "time_d"])
)
print(f"Combined daily panel observations: {len(df):,}")
print(f"Unique permnos in panel: {df['permno'].n_unique():,}")

# ROLLING REGRESSION
print("Running rolling 20-day regressions (min 15 obs) per permno...")
df = df.with_columns(
    pl.col("ret_excess")
    .least_squares.rolling_ols(
        pl.col("mktrf"),
        pl.col("dVIX"),
        window_size=20,
        min_periods=15,
        mode="coefficients",
        add_intercept=True,
        null_policy="drop",
    )
    .over("permno")
    .alias("coef")
).with_columns(pl.col("coef").struct.field("dVIX").alias("betaVIX"))
print("Extracted betaVIX coefficients from rolling regressions")

# MONTHLY AGGREGATION
print("Aggregating daily coefficients to month-end values...")
monthly = (
    df.drop("coef")
    .with_columns(pl.col("time_d").dt.truncate("1mo").alias("time_avail_m"))
    .sort(["permno", "time_avail_m", "time_d"])
    .group_by(["permno", "time_avail_m"])
    .agg(pl.col("betaVIX").drop_nulls().last().alias("betaVIX"))
    .select(["permno", "time_avail_m", "betaVIX"])
)
print(f"Monthly betaVIX rows: {len(monthly):,}")

if len(monthly) > 0:
    monthly_pd = monthly.to_pandas()
    print("betaVIX summary stats:")
    print(f"  Mean: {monthly_pd['betaVIX'].mean():.6f}")
    print(f"  Std: {monthly_pd['betaVIX'].std():.6f}")
    print(f"  Min: {monthly_pd['betaVIX'].min():.6f}")
    print(f"  Max: {monthly_pd['betaVIX'].max():.6f}")

    # SAVE OUTPUT
    print("Saving betaVIX predictor...")
    save_predictor(monthly_pd, "betaVIX")
    print("betaVIX predictor saved")
else:
    print("No betaVIX values produced; skipping save")

print("=" * 80)
print("betaVIX pipeline complete")
print("=" * 80)
