# ABOUTME: MomOffSeason16YrPlus.py - generates off-season long-term reversal for years 16-20
# ABOUTME: Python translation of MomOffSeason16YrPlus.do using seasonal return extraction

"""
MomOffSeason16YrPlus.py

Generates off-season long-term reversal predictor for years 16-20 by removing seasonal components:
- MomOffSeason16YrPlus: (60-month momentum - seasonal returns) / (60-month count - seasonal count)
- Seasonal returns: ret[t-191], ret[t-203], ret[t-215], ret[t-227], ret[t-239] (every 12 months)
- Base lag: ret[t-180] for rolling calculation
- Higher minimum sample requirement: 36 observations (vs 1 in other variants)

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/MomOffSeason16YrPlus.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, ret)

Outputs:
    - ../pyData/Predictors/MomOffSeason16YrPlus.csv

Requirements:
    - 60-month rolling windows with minimum 36 observations
    - Seasonal return extraction at specific lags for years 16-20
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.time_based_operations import time_based_lag

print("=" * 80)
print("🏗️  MomOffSeason16YrPlus.py")
print("Generating off-season long-term reversal for years 16-20")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")

# Load SignalMasterTable data (permno, time_avail_m, ret)
print("Loading SignalMasterTable.parquet...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded SignalMasterTable: {len(df):,} monthly observations")

# SIGNAL CONSTRUCTION
print("🧮 Computing off-season long-term reversal for years 16-20...")

# Replace missing returns with 0 (following Stata logic)
df = df.with_columns(
    pl.col("ret").fill_null(0.0)
)

# Sort by permno and time for lag operations
df = df.sort(["permno", "time_avail_m"])

print("🗓️  Extracting seasonal returns for years 16-20 (every 12 months)...")

# Extract seasonal returns: ret[t-191], ret[t-203], ret[t-215], ret[t-227], ret[t-239]
# These are returns from 191, 203, 215, 227, and 239 months ago (seasonal pattern for years 16-20)
df = df.with_columns([
    pl.col("ret").shift(191).over("permno").alias("temp191"),
    pl.col("ret").shift(203).over("permno").alias("temp203"), 
    pl.col("ret").shift(215).over("permno").alias("temp215"),
    pl.col("ret").shift(227).over("permno").alias("temp227"),
    pl.col("ret").shift(239).over("permno").alias("temp239")
])

# Calculate seasonal return sum and count (following Stata's rowtotal/rownonmiss logic)
df = df.with_columns([
    # Sum of seasonal returns (only non-null values) - Polars list.sum() automatically ignores nulls
    pl.concat_list(["temp191", "temp203", "temp215", "temp227", "temp239"]).list.sum().alias("retTemp1"),
    # Count of non-null seasonal returns - use list evaluation
    pl.concat_list(["temp191", "temp203", "temp215", "temp227", "temp239"]).list.eval(
        pl.element().is_not_null().sum()
    ).list.get(0).alias("retTemp2")
])

print("📊 Computing 60-month rolling momentum base...")

# Get ret[t-180] for 60-month rolling calculation (using time-based lag to match Stata's l180.ret)
df = time_based_lag(df, lag_months=180, value_col="ret", alias="retLagTemp")

# Calculate 60-month rolling sum and count using rolling operations
# Note: This variant requires minimum 36 observations (vs 1 in other variants)
df = df.with_columns([
    pl.col("retLagTemp").rolling_sum(window_size=60, min_samples=36).over("permno").alias("sum60_retLagTemp"),
    # For rolling count: create indicator (1 if not null, 0 if null) then rolling sum
    pl.col("retLagTemp").is_not_null().cast(pl.Int32).rolling_sum(window_size=60, min_samples=36).over("permno").alias("count60_retLagTemp")
])

print("🧮 Computing final MomOffSeason16YrPlus predictor...")

# Calculate MomOffSeason16YrPlus: (60-month sum - seasonal sum) / (60-month count - seasonal count)
df_final = df.with_columns(
    ((pl.col("sum60_retLagTemp") - pl.col("retTemp1")) / 
     (pl.col("count60_retLagTemp") - pl.col("retTemp2"))).alias("MomOffSeason16YrPlus")
).select(["permno", "time_avail_m", "MomOffSeason16YrPlus"]).filter(
    pl.col("MomOffSeason16YrPlus").is_not_null() & pl.col("MomOffSeason16YrPlus").is_finite()
)

print(f"Generated MomOffSeason16YrPlus values: {len(df_final):,} observations")
print(f"MomOffSeason16YrPlus summary stats:")
print(f"  Mean: {df_final['MomOffSeason16YrPlus'].mean():.6f}")
print(f"  Std: {df_final['MomOffSeason16YrPlus'].std():.6f}")
print(f"  Min: {df_final['MomOffSeason16YrPlus'].min():.6f}")  
print(f"  Max: {df_final['MomOffSeason16YrPlus'].max():.6f}")

# SAVE
print("💾 Saving MomOffSeason16YrPlus predictor...")
save_predictor(df_final, "MomOffSeason16YrPlus")
print("✅ MomOffSeason16YrPlus.csv saved successfully")