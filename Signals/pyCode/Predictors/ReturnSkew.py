# ABOUTME: ReturnSkew.py - generates ReturnSkew predictor (skewness of daily returns)
# ABOUTME: Python translation of ReturnSkew.do using polars for performance

"""
ReturnSkew.py

Generates ReturnSkew predictor: Skewness of daily stock returns within each month.

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ReturnSkew.py

Inputs:
    - ../pyData/Intermediate/dailyCRSP.parquet (permno, time_d, ret)

Outputs:
    - ../pyData/Predictors/ReturnSkew.csv

Requirements:
    - Minimum 15 daily observations per permno-month for valid calculation
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  ReturnSkew.py")
print("Generating ReturnSkew predictor (skewness of daily returns)")
print("=" * 80)

# DATA LOAD
print("📊 Loading daily CRSP data...")
crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet").select(["permno", "time_d", "ret"])
print(f"Loaded CRSP: {len(crsp):,} daily observations")

# SIGNAL CONSTRUCTION
print("\n🔧 Starting signal construction...")

# Create time_avail_m (year-month) equivalent to Stata's "gen time_avail_m = mofd(time_d)"
print("Creating time_avail_m (year-month identifier)...")
crsp = crsp.with_columns(
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
)

print(f"Date range: {crsp['time_d'].min()} to {crsp['time_d'].max()}")

# Calculate skewness and count of observations by permno-month
# Equivalent to Stata's "gcollapse (count) ndays = days (skewness) ReturnSkew = ret, by(permno time_avail_m)"
# Note: Stata counts ALL rows (including those with missing ret), not just non-null values
print("Calculating return skewness by permno-month...")
predictors = crsp.group_by(["permno", "time_avail_m"]).agg([
    pl.len().alias("ndays"),                    # Count ALL rows (Stata's behavior)
    pl.col("ret").skew().alias("ReturnSkew")    # Skewness of returns (ignores nulls)
])

print(f"Generated {len(predictors):,} permno-month observations before filtering")

# Filter to keep only observations with >= 15 days
# Equivalent to Stata's "replace ReturnSkew = . if ndays < 15"
print("Filtering to permno-months with >=15 observations...")
predictors_filtered = predictors.filter(pl.col("ndays") >= 15).drop("ndays")

print(f"After >=15 filter: {len(predictors_filtered):,} observations")

# Show sample statistics
print("\n📈 Predictor summary statistics:")
summary = predictors_filtered.select([
    pl.col("ReturnSkew").mean().alias("ReturnSkew_mean"),
    pl.col("ReturnSkew").std().alias("ReturnSkew_std"),
    pl.col("ReturnSkew").min().alias("ReturnSkew_min"),
    pl.col("ReturnSkew").max().alias("ReturnSkew_max")
])
print(summary)

# SAVE
print("\n💾 Saving predictor...")

# Convert to pandas for compatibility with existing save_predictor utility
predictors_pd = predictors_filtered.to_pandas()

# Save predictor using existing utility (equivalent to savepredictor.do call)
save_predictor(predictors_pd, 'ReturnSkew')

print("\n" + "=" * 80)
print("✅ ReturnSkew.py completed successfully")
print("Generated 1 predictor:")
print("  • ReturnSkew: Return Skewness")
print("=" * 80)