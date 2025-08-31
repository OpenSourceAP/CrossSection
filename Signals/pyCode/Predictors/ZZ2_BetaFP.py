# ABOUTME: Frazzini-Pedersen Beta following Frazzini and Pedersen 2014, Table 3 BAB
# ABOUTME: calculates beta using R-squared from 3-day overlapping returns regressed on market, times ratio of stock to market volatility
"""
Usage:
    python3 Predictors/ZZ2_BetaFP.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP returns with columns [permno, time_d, ret]
    - dailyFF.parquet: Daily Fama-French factors with columns [time_d, rf, mktrf]

Outputs:
    - BetaFP.csv: CSV file with columns [permno, yyyymm, BetaFP]
    - BetaFP = sqrt(R²) × (σ_stock/σ_market) where R² from 3-day overlapping returns regression
"""

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("=" * 80)
print("🏗️  ZZ2_BetaFP.py")
print("Generating Frazzini-Pedersen beta using rolling correlations")
print("=" * 80)

# Data load
print("📊 Loading daily CRSP and Fama-French data...")
df = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet",
    columns=["permno", "time_d", "ret"])
print(f"Loaded CRSP: {len(df):,} daily observations")

ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
print(f"Loaded FF factors: {len(ff):,} daily observations")

# Merge with FF data
df = df.join(ff.select(["time_d", "rf", "mktrf"]), on="time_d", how="inner")
print(f"Merged dataset: {len(df):,} observations")

print("\n🔧 Starting signal construction...")
print("Calculating excess log returns...")
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("ret"),
    pl.col("ret").log1p().alias("LogRet"),
    pl.col("mktrf").log1p().alias("LogMkt")
])

# sort
df = df.sort(["permno", "time_d"])

# == Calculate 252-day return volatility ==
print("Computing 252-day rolling volatilities...")

# Standard deviations of log returns
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

# == Calculate R-sq from regressing 3-day stock returns on 3-day market returns ==
print("Creating 3-day overlapping returns...")

# Create 3-day returns
df = df.with_columns([
    (pl.col("LogRet").shift(2).over("permno") + 
     pl.col("LogRet").shift(1).over("permno") + 
     pl.col("LogRet")).alias("tempRi"),
    (pl.col("LogMkt").shift(2).over("permno") + 
     pl.col("LogMkt").shift(1).over("permno") + 
     pl.col("LogMkt")).alias("tempRm")
])

print("Calculating rolling R-squared (1260-day window, min 500 obs)...")
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

# == Calculate Frazzini-Pedersen beta ==
print("Computing Frazzini-Pedersen beta...")

df = df.with_columns([
    (pl.col("_R2").abs().sqrt() * (pl.col("sd252_LogRet") / pl.col("sd252_LogMkt"))).alias("BetaFP")
])


print("\n📅 Converting to monthly frequency...")
# Convert to monthly and keep last observation per month
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

print("Aggregating to permno-month level...")

# save last non-missing BetaFP per permno-month
df_monthly = df.select(['permno', 'time_avail_m', 'time_d', 'BetaFP']).filter(
    pl.col("BetaFP").is_finite()
).sort(["permno", "time_avail_m", "time_d"]).group_by(
    ["permno", "time_avail_m"]
).agg(
    pl.col("BetaFP").last().alias("BetaFP")
)

print(f"Generated predictors: {len(df_monthly):,} permno-month observations")

# Show summary statistics
print("\n📈 Predictor summary statistics:")
print(df_monthly.select("BetaFP").describe())

print("\n💾 Saving predictor...")
# Save predictor
save_predictor(df_monthly, "BetaFP")

print("\n" + "=" * 80)
print("✅ ZZ2_BetaFP.py completed successfully")
print("Generated predictor: BetaFP (Frazzini-Pedersen Beta)")
print("=" * 80)
