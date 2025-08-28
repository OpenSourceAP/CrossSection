# ABOUTME: Systematic volatility predictor using rolling regression of returns on market and VIX changes
# ABOUTME: Usage: python3 betaVIX.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.asreg import asreg_polars
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

# Set up time index for rolling window (Stata: time_temp = _n)
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

# Use utils/asreg.py helper for rolling regression
# This replicates: asreg ret mktrf dVIX, window(time_temp 20) min(15) by(permno)
df = asreg_polars(
    df,
    y="ret_excess",  # Stata: ret (but we already subtracted rf)
    X=["mktrf", "dVIX"],
    by=["permno"],
    t="time_temp", 
    mode="rolling",
    window_size=20,
    min_samples=15,
    outputs=("coef",),
    coef_prefix="b_"
)

# Extract betaVIX coefficient (rename _b_dVIX betaVIX in Stata)
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