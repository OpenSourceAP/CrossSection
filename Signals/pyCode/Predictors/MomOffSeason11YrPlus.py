# ABOUTME: MomOffSeason11YrPlus.py - generates off-season long-term reversal for years 11-15
# ABOUTME: Python translation of MomOffSeason11YrPlus.do using seasonal return extraction

"""
MomOffSeason11YrPlus.py

Generates off-season long-term reversal predictor for years 11-15 by removing seasonal components:
- MomOffSeason11YrPlus: (60-month momentum - seasonal returns) / (60-month count - seasonal count)
- Seasonal returns: ret[t-131], ret[t-143], ret[t-155], ret[t-167], ret[t-179] (every 12 months)
- Base lag: ret[t-120] for rolling calculation

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/MomOffSeason11YrPlus.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, ret)

Outputs:
    - ../pyData/Predictors/MomOffSeason11YrPlus.csv

Requirements:
    - 60-month rolling windows for base momentum calculation
    - Seasonal return extraction at specific lags for years 11-15
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.time_based_operations import time_based_lag

print("=" * 80)
print("🏗️  MomOffSeason11YrPlus.py")
print("Generating off-season long-term reversal for years 11-15")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")

# Load SignalMasterTable data (permno, time_avail_m, ret)
print("Loading SignalMasterTable.parquet...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded SignalMasterTable: {len(df):,} monthly observations")

# SIGNAL CONSTRUCTION
print("🧮 Computing off-season long-term reversal for years 11-15...")

# Replace missing returns with 0 (following Stata logic)
df = df.with_columns(
    pl.col("ret").fill_null(0.0)
)

# Sort by permno and time for lag operations
df = df.sort(["permno", "time_avail_m"])

print("🗓️  Extracting seasonal returns for years 11-15 (every 12 months)...")

# Extract seasonal returns: ret[t-131], ret[t-143], ret[t-155], ret[t-167], ret[t-179]
# These are returns from 131, 143, 155, 167, and 179 months ago (seasonal pattern for years 11-15)
df = df.with_columns([
    pl.col("ret").shift(131).over("permno").alias("temp131"),
    pl.col("ret").shift(143).over("permno").alias("temp143"), 
    pl.col("ret").shift(155).over("permno").alias("temp155"),
    pl.col("ret").shift(167).over("permno").alias("temp167"),
    pl.col("ret").shift(179).over("permno").alias("temp179")
])

# Calculate seasonal return sum and count (following Stata's rowtotal/rownonmiss logic)
df = df.with_columns([
    # Sum of seasonal returns (only non-null values) - Polars list.sum() automatically ignores nulls
    pl.concat_list(["temp131", "temp143", "temp155", "temp167", "temp179"]).list.sum().alias("retTemp1"),
    # Count of non-null seasonal returns - use list evaluation
    pl.concat_list(["temp131", "temp143", "temp155", "temp167", "temp179"]).list.eval(
        pl.element().is_not_null().sum()
    ).list.get(0).alias("retTemp2")
])

print("📊 Computing 60-month rolling momentum base...")

# Get ret[t-120] for 60-month rolling calculation (using time-based lag to match Stata's l120.ret)
df = time_based_lag(df, lag_months=120, value_col="ret", alias="retLagTemp")

# Calculate 60-month rolling sum and count using rolling operations
df = df.with_columns([
    pl.col("retLagTemp").rolling_sum(window_size=60, min_samples=1).over("permno").alias("retLagTemp_sum60"),
    # For rolling count: create indicator (1 if not null, 0 if null) then rolling sum
    pl.col("retLagTemp").is_not_null().cast(pl.Int32).rolling_sum(window_size=60, min_samples=1).over("permno").alias("retLagTemp_count60")
])

print("🧮 Computing final MomOffSeason11YrPlus predictor...")

# Calculate MomOffSeason11YrPlus: (60-month sum - seasonal sum) / (60-month count - seasonal count)
df_final = df.with_columns(
    ((pl.col("retLagTemp_sum60") - pl.col("retTemp1")) / 
     (pl.col("retLagTemp_count60") - pl.col("retTemp2"))).alias("MomOffSeason11YrPlus")
).select(["permno", "time_avail_m", "MomOffSeason11YrPlus"]).filter(
    pl.col("MomOffSeason11YrPlus").is_not_null() & pl.col("MomOffSeason11YrPlus").is_finite()
)

print(f"Generated MomOffSeason11YrPlus values: {len(df_final):,} observations")
print(f"MomOffSeason11YrPlus summary stats:")
print(f"  Mean: {df_final['MomOffSeason11YrPlus'].mean():.6f}")
print(f"  Std: {df_final['MomOffSeason11YrPlus'].std():.6f}")
print(f"  Min: {df_final['MomOffSeason11YrPlus'].min():.6f}")  
print(f"  Max: {df_final['MomOffSeason11YrPlus'].max():.6f}")

# SAVE
print("💾 Saving MomOffSeason11YrPlus predictor...")
save_predictor(df_final, "MomOffSeason11YrPlus")
print("✅ MomOffSeason11YrPlus.csv saved successfully")