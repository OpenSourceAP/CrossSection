# ABOUTME: Beta.py - generates CAPM Beta predictor using 60-month rolling regressions
# ABOUTME: Python translation of Beta.do using polars-ols for performance

"""
Beta.py

Generates CAPM Beta predictor from monthly returns and market returns using rolling 60-month regressions:
- Beta: Coefficient from CAPM regression retrf ~ ewmktrf over 60-month rolling windows

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/Beta.py

Inputs:
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, ret)
    - ../pyData/Intermediate/monthlyFF.parquet (time_avail_m, rf)
    - ../pyData/Intermediate/monthlyMarket.parquet (time_avail_m, ewretd)

Outputs:
    - ../pyData/Predictors/Beta.csv

Requirements:
    - Rolling 60-month windows with minimum 20 observations per window
    - CAPM regression: retrf = alpha + beta * ewmktrf + residual
"""

import polars as pl
import polars_ols  # registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor

print("=" * 80)
print("🏗️  Beta.py")
print("Generating CAPM Beta predictor")
print("=" * 80)

# DATA LOAD
print("📊 Loading monthly CRSP, FF, and Market data...")

# Load monthly CRSP data (permno, time_avail_m, ret)
print("Loading monthlyCRSP.parquet...")
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded CRSP: {len(crsp):,} monthly observations")

# Load monthly FF data for risk-free rate
print("Loading monthlyFF.parquet...")  
ff = pl.read_parquet("../pyData/Intermediate/monthlyFF.parquet").select(["time_avail_m", "rf"])
print(f"Loaded FF: {len(ff):,} monthly observations")

# Load monthly Market data for equal-weighted return
print("Loading monthlyMarket.parquet...")
market = pl.read_parquet("../pyData/Intermediate/monthlyMarket.parquet").select(["time_avail_m", "ewretd"])
print(f"Loaded Market: {len(market):,} monthly observations")

# MERGE DATA
print("🔗 Merging datasets...")
df = (crsp
    .join(ff, on="time_avail_m", how="inner")
    .join(market, on="time_avail_m", how="inner")
    .sort(["permno", "time_avail_m"])
)
print(f"After merging: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("🧮 Computing CAPM Beta using rolling 60-month regressions...")

# Create excess returns
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("retrf"),
    (pl.col("ewretd") - pl.col("rf")).alias("ewmktrf")
])

# Add time sequence for each permno (replicates Stata's time_temp)
df = df.with_columns(
    pl.int_range(pl.len()).over("permno").alias("time_temp")
)

print(f"Computing rolling regressions for {df['permno'].n_unique():,} unique permnos...")

# Rolling CAPM regression: retrf ~ ewmktrf with 60-month windows
df_with_beta = df.with_columns(
    pl.col("retrf")
    .least_squares.rolling_ols(
        pl.col("ewmktrf"),
        window_size=60,
        mode="coefficients"
    )
    .over("permno")
    .alias("_b_coeffs")
)

# Extract Beta coefficient (slope coefficient from struct)
df_final = df_with_beta.with_columns(
    pl.col("_b_coeffs").struct.field("ewmktrf").alias("Beta")
).select(["permno", "time_avail_m", "Beta"]).filter(
    pl.col("Beta").is_not_null()
)

print(f"Generated Beta values: {len(df_final):,} observations")
print(f"Beta summary stats:")
print(f"  Mean: {df_final['Beta'].mean():.4f}")
print(f"  Std: {df_final['Beta'].std():.4f}")
print(f"  Min: {df_final['Beta'].min():.4f}")  
print(f"  Max: {df_final['Beta'].max():.4f}")

# SAVE
print("💾 Saving Beta predictor...")
save_predictor(df_final, "Beta")
print("✅ Beta.csv saved successfully")