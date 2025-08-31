# ABOUTME: RealizedVol following Ang et al. 2006, Table 6A; IdioVol3F following Ang et al. 2006, Table 7B; ReturnSkew3F following Bali, Engle and Murray 2015, Table 14.10
# ABOUTME: calculates realized volatility, idiosyncratic volatility (3F), and idiosyncratic skewness (3F) predictors from daily returns

"""
ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py

Generates three volatility and skewness predictors from daily CRSP returns and Fama-French 3-factor model:
- RealizedVol: Standard deviation of daily returns within each month
- IdioVol3F: Standard deviation of daily idiosyncratic returns (residuals from FF3 model) 
- ReturnSkew3F: Skewness of daily idiosyncratic returns (residuals from FF3 model)

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py

Inputs:
    - ../pyData/Intermediate/dailyCRSP.parquet (permno, time_d, ret)
    - ../pyData/Intermediate/dailyFF.parquet (time_d, rf, mktrf, smb, hml)

Outputs:
    - ../pyData/Predictors/RealizedVol.csv
    - ../pyData/Predictors/IdioVol3F.csv  
    - ../pyData/Predictors/ReturnSkew3F.csv

Requirements:
    - Minimum 15 daily observations per permno-month (Bali-Hovak 2009 footnote 9)
    - FF3 regression: ret = alpha + beta1*mktrf + beta2*smb + beta3*hml + residual
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import numpy as np
from scipy.stats import skew
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("=" * 80)
print("🏗️  ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py")
print("Generating RealizedVol, IdioVol3F, and ReturnSkew3F predictors")
print("=" * 80)

# DATA LOAD
print("📊 Loading daily CRSP and Fama-French data...")

# Load daily CRSP data (permno, time_d, ret)
print("Loading dailyCRSP.parquet...")
crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet").select(["permno", "time_d", "ret"])
print(f"Loaded CRSP: {len(crsp):,} daily observations")

# Load daily FF factors and merge
print("Loading dailyFF.parquet...")
ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet").select(["time_d", "rf", "mktrf", "smb", "hml"])
print(f"Loaded FF factors: {len(ff):,} daily observations")

# Merge CRSP and FF data
print("Merging CRSP and FF data...")
df = crsp.join(ff, on="time_d", how="inner")
print(f"Merged dataset: {len(df):,} observations")

# Adjust returns: ret = ret - rf (equivalent to the's "Update ret - rf")
print("Adjusting returns by risk-free rate...")
df  to df.with_columns((pl.col("ret") - pl.col("rf")).alias("ret")).drop("rf")


# SIGNAL CONSTRUCTION
print("\n🔧 Starting signal construction...")

# Create time_avail_m (year-month) equivalent to the's "Generate mofd(time_d)"
print("Creating time_avail_m (year-month identifier)...")
df = df.with_columns(
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
).sort(["permno", "time_d"])


print(f"Date range: {df['time_d'].min()} to {df['time_d'].max()}")

# Run FF3 regressions by permno-month using direct polars-ols helper to get residuals
# equivalent to the's "bys permno time_avail_m: asreg ret mktrf smb hml, fit"
print("Running FF3 regressions by permno-month to extract residuals...")

# Sort data first (required for asreg)
df = df.sort(["permno", "time_avail_m", "time_d"])

# Use direct polars-ols with group mode for per-group regressions
df_with_residuals = df.with_columns(
    pl.col("ret").least_squares.ols(
        pl.col("mktrf"), pl.col("smb"), pl.col("hml"),
        mode="residuals",
        add_intercept=True,
        null_policy="drop"
    ).over(['permno', 'time_avail_m']).alias("resid")
).filter(
    pl.col("ret").count().over(['permno', 'time_avail_m']) >= 15
)

# Rename residual column to match original naming
df_with_residuals = df_with_residuals.rename({"resid": "_residuals"})


# Add _Nobs for each observation (replicates Stata's asreg behavior)
# In Stata, asreg adds _Nobs to every observation in the group
print("Adding _Nobs to track observations used in regression...")
df_with_nobs = df_with_residuals.with_columns(
    # Count non-null residuals per group - this is what asreg's _Nobs represents
    pl.col("_residuals").filter(pl.col("_residuals").is_not_null()).count()
    .over(["permno", "time_avail_m"]).alias("_Nobs")
)

# Check for any missing residuals
missing_residuals = df_with_nobs.filter(pl.col("_residuals").is_null()).height
if missing_residuals > 0:
    print(f"⚠️  Warning: {missing_residuals} observations with missing residuals (likely singular matrices)")

print(f"Completed regressions: {len(df_with_nobs):,} observations")

# Apply Stata-equivalent filtering: keep observations where regression succeeded  
# The original Stata code "keep if _Nobs >= 15" is effectively handled by our regression
# since failed regressions (insufficient data) produce null residuals
print("Filtering out observations where FF3 regression failed (null residuals)...")
df_filtered = df_with_nobs.filter(pl.col("_residuals").is_not_null())
print(f"After removing null residuals: {len(df_filtered):,} observations")


# Check how many permno-month groups this represents  
groups_after_filter = df_filtered.select(["permno", "time_avail_m"]).unique().height
print(f"Permno-month groups after filtering: {groups_after_filter:,}")


# Calculate the three predictors with targeted fix for extreme cases
print("Calculating predictors using group aggregations...")
predictors = df_filtered.group_by(["permno", "time_avail_m"]).agg([
    pl.col("ret").std().alias("RealizedVol"),              # (sd) RealizedVol = ret
    pl.col("_residuals").std().alias("IdioVol3F"),         # (sd) IdioVol3F = _residuals  
    pl.col("_residuals").skew().alias("ReturnSkew3F")      # (skewness) ReturnSkew3F = _residuals
])


# NO POST-PROCESSING: Stata code does not modify ReturnSkew3F values

print(f"Generated predictors: {len(predictors):,} permno-month observations")

# Show sample statistics
print("\n📈 Predictor summary statistics:")
summary = predictors.select([
    pl.col("RealizedVol").mean().alias("RealizedVol_mean"),
    pl.col("RealizedVol").std().alias("RealizedVol_std"),
    pl.col("IdioVol3F").mean().alias("IdioVol3F_mean"), 
    pl.col("IdioVol3F").std().alias("IdioVol3F_std"),
    pl.col("ReturnSkew3F").mean().alias("ReturnSkew3F_mean"),
    pl.col("ReturnSkew3F").std().alias("ReturnSkew3F_std")
])
print(summary)

# SAVE
print("\n💾 Saving predictors...")

# Convert to pandas for compatibility with existing save_predictor utility
predictors_pd = predictors.to_pandas()

# Save each predictor using existing utility (equivalent to savepredictor.do calls)
save_predictor(predictors_pd, 'RealizedVol')
save_predictor(predictors_pd, 'IdioVol3F') 
save_predictor(predictors_pd, 'ReturnSkew3F')

print("\n" + "=" * 80)
print("✅ ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py completed successfully")
print("Generated 3 predictors:")
print("  • RealizedVol: Realized (Total) Vol (Daily)")
print("  • IdioVol3F: Idiosyncratic Risk (3 factor)")  
print("  • ReturnSkew3F: Skewness of daily idiosyncratic returns (3F model)")
print("=" * 80)