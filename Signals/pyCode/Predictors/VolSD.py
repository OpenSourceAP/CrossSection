# ABOUTME: Volume variance following Chordia, Subra, Anshuman 2001, Table 5B DVOL
# ABOUTME: calculates rolling standard deviation of monthly trading volume over past 36 months
"""
Usage:
    python3 Predictors/VolSD.py

Inputs:
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, vol]

Outputs:
    - VolSD.csv: CSV file with columns [permno, yyyymm, VolSD]
    - VolSD = 36-month rolling standard deviation of vol, min 24 observations required
"""

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  VolSD.py")
print("Creating volume variance predictor using 36-month rolling standard deviation")
print("=" * 80)

# Data load
print("📊 Loading monthly CRSP data...")
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
print(f"Loaded: {len(monthly_crsp):,} observations")

# Select required columns
df = monthly_crsp.select(["permno", "time_avail_m", "vol"])

# Signal construction - 36-month rolling standard deviation of volume
print("🧮 Computing 36-month rolling volume standard deviation...")
df = df.with_columns([
    pl.col("vol")
    .rolling_std(window_size=36, min_samples=24)
    .over("permno")
    .alias("VolSD")
])

# Select final data
result = df.select(["permno", "time_avail_m", "VolSD"])

# Save predictor
print("💾 Saving VolSD predictor...")
save_predictor(result, "VolSD")
print("✅ VolSD.csv saved successfully")

print("=" * 80)
print("✅ VolSD.py Complete")
print("Volume variance predictor generated successfully")
print("=" * 80)