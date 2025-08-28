# ABOUTME: Volume variance using 36-month rolling standard deviation
# ABOUTME: Usage: python3 VolSD.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

# Data load
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")

# Select required columns
df = monthly_crsp.select(["permno", "time_avail_m", "vol"])

# Signal construction - 36-month rolling standard deviation of volume
df = df.with_columns([
    pl.col("vol")
    .rolling_std(window_size=36, min_samples=24)
    .over("permno")
    .alias("VolSD")
])

# Select final data
result = df.select(["permno", "time_avail_m", "VolSD"])

# Save predictor
save_predictor(result, "VolSD")