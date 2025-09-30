# ABOUTME: RealizedVol following Ang et al. 2006, Table 6A; IdioVol3F following Ang et al. 2006, Table 7B; ReturnSkew3F following Bali, Engle and Murray 2015, Table 14.10
# ABOUTME: calculates realized volatility, idiosyncratic volatility (3F), and idiosyncratic skewness (3F) predictors from daily returns

"""
ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, ret]
    - dailyFF.parquet: Daily Fama-French data with columns [time_d, rf, mktrf, smb, hml]

Outputs:
    - RealizedVol.csv: CSV file with columns [permno, yyyymm, RealizedVol]
    - IdioVol3F.csv: CSV file with columns [permno, yyyymm, IdioVol3F]
    - ReturnSkew3F.csv: CSV file with columns [permno, yyyymm, ReturnSkew3F]
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import numpy as np
from scipy.stats import skew
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("=" * 80)
print("🏗️  ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py")
print("Generating RealizedVol, IdioVol3F, and ReturnSkew3F predictors")
print("=" * 80)

# Load daily stock returns data and Fama-French 3-factor model data
# These will be merged to calculate idiosyncratic returns via regression
print("📊 Loading daily CRSP and Fama-French data...")

print("Loading dailyCRSP.parquet...")
crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet").select(
    ["permno", "time_d", "ret"]
)
print(f"Loaded CRSP: {len(crsp):,} daily observations")

print("Loading dailyFF.parquet...")
ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet").select(
    ["time_d", "rf", "mktrf", "smb", "hml"]
)
print(f"Loaded FF factors: {len(ff):,} daily observations")

print("Merging CRSP and FF data...")
df = crsp.join(ff, on="time_d", how="inner")
print(f"Merged dataset: {len(df):,} observations")

# Convert raw returns to excess returns by subtracting risk-free rate
# This is required for the Fama-French 3-factor regression
print("Adjusting returns by risk-free rate...")
df = df.with_columns((pl.col("ret") - pl.col("rf")).alias("ret")).drop("rf")


# Begin calculating the three volatility/skewness predictors
print("\n🔧 Starting signal construction...")

# Create month identifier for grouping daily observations
# All daily returns within a month will be used to calculate that month's predictors
print("Creating time_avail_m (year-month identifier)...")
df = df.with_columns(pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")).sort(
    ["permno", "time_d"]
)


print(f"Date range: {df['time_d'].min()} to {df['time_d'].max()}")

# Run Fama-French 3-factor regression for each permno-month
# Regression: excess_return = alpha + beta1*mktrf + beta2*smb + beta3*hml + residual
# The residuals represent idiosyncratic returns after removing market, size, and value factors
# Minimum 15 daily observations required per month (Bali-Hovakimian 2009)
print("Running FF3 regressions by permno-month to extract residuals...")

df = df.sort(["permno", "time_avail_m", "time_d"])

df_with_residuals = df.with_columns(
    pl.col("ret")
    .least_squares.ols(
        pl.col("mktrf"),
        pl.col("smb"),
        pl.col("hml"),
        mode="residuals",
        add_intercept=True,
        null_policy="drop",
    )
    .over(["permno", "time_avail_m"])
    .alias("resid")
).filter(pl.col("ret").count().over(["permno", "time_avail_m"]) >= 15)

df_with_residuals = df_with_residuals.rename({"resid": "_residuals"})


# Track the number of observations used in each regression
# This replicates Stata's asreg behavior which adds _Nobs to every observation
print("Adding _Nobs to track observations used in regression...")
df_with_nobs = df_with_residuals.with_columns(
    pl.col("_residuals")
    .filter(pl.col("_residuals").is_not_null())
    .count()
    .over(["permno", "time_avail_m"])
    .alias("_Nobs")
)

missing_residuals = df_with_nobs.filter(pl.col("_residuals").is_null()).height
if missing_residuals > 0:
    print(
        f"⚠️  Warning: {missing_residuals} observations with missing residuals (likely singular matrices)"
    )

print(f"Completed regressions: {len(df_with_nobs):,} observations")

# Remove observations where regression failed (e.g., singular matrix, insufficient variation)
# These would have null residuals and cannot be used for predictor calculation
print("Filtering out observations where FF3 regression failed (null residuals)...")
df_filtered = df_with_nobs.filter(pl.col("_residuals").is_not_null())
print(f"After removing null residuals: {len(df_filtered):,} observations")


groups_after_filter = df_filtered.select(["permno", "time_avail_m"]).unique().height
print(f"Permno-month groups after filtering: {groups_after_filter:,}")

# Calculate the three predictors for each permno-month:
# 1. RealizedVol: Standard deviation of daily excess returns (total volatility)
# 2. IdioVol3F: Standard deviation of FF3 residuals (idiosyncratic volatility)
# 3. ReturnSkew3F: Skewness of FF3 residuals (idiosyncratic skewness)
print("Calculating predictors using group aggregations...")
predictors = df_filtered.group_by(["permno", "time_avail_m"]).agg(
    [
        pl.col("ret").std().alias("RealizedVol"),
        pl.col("_residuals").std().alias("IdioVol3F"),
        pl.col("_residuals").skew().alias("ReturnSkew3F"),
    ]
)

print(f"Generated predictors: {len(predictors):,} permno-month observations")

print("\n📈 Predictor summary statistics:")
summary = predictors.select(
    [
        pl.col("RealizedVol").mean().alias("RealizedVol_mean"),
        pl.col("RealizedVol").std().alias("RealizedVol_std"),
        pl.col("IdioVol3F").mean().alias("IdioVol3F_mean"),
        pl.col("IdioVol3F").std().alias("IdioVol3F_std"),
        pl.col("ReturnSkew3F").mean().alias("ReturnSkew3F_mean"),
        pl.col("ReturnSkew3F").std().alias("ReturnSkew3F_std"),
    ]
)
print(summary)

# Save the three predictors to separate CSV files
# Each file contains permno, time_avail_m, and the predictor value
print("\n💾 Saving predictors...")

predictors_pd = predictors.to_pandas()

save_predictor(predictors_pd, "RealizedVol")
save_predictor(predictors_pd, "IdioVol3F")
save_predictor(predictors_pd, "ReturnSkew3F")

print("\n" + "=" * 80)
print("✅ ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py completed successfully")
print("Generated 3 predictors:")
print("  • RealizedVol: Realized (Total) Vol (Daily)")
print("  • IdioVol3F: Idiosyncratic Risk (3 factor)")
print("  • ReturnSkew3F: Skewness of daily idiosyncratic returns (3F model)")
print("=" * 80)
