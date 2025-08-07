# ABOUTME: Volume to market equity ratio using 12-month rolling mean of dollar volume
# ABOUTME: Usage: python3 VolMkt.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Data load
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")

# Select required columns
df = monthly_crsp.select(["permno", "time_avail_m", "vol", "prc", "shrout"])

# Signal construction
df = df.with_columns([
    # Market value
    (pl.col("shrout") * pl.col("prc").abs()).alias("mve_c"),
    # Dollar volume
    (pl.col("vol") * pl.col("prc").abs()).alias("temp")
])

# 12-month rolling mean of dollar volume
df = df.with_columns([
    pl.col("temp")
    .rolling_mean(window_size=12, min_samples=10)
    .over("permno")
    .alias("tempMean")
])

# Volume to market equity ratio
df = df.with_columns([
    (pl.col("tempMean") / pl.col("mve_c")).alias("VolMkt")
])

# Select final data
result = df.select(["permno", "time_avail_m", "VolMkt"])

# Save predictor
save_predictor(result, "VolMkt")