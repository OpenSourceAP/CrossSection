# ABOUTME: Beta.py - generates CAPM Beta predictor using asreg rolling regressions
# ABOUTME: Python translation of Beta.do using polars and asreg helper for exact Stata replication
# BetaSquared was weak in OP

"""
Beta.py

Generates CAPM Beta predictor from monthly returns and market returns using rolling 60-observation regressions:
- Beta: Coefficient from CAPM regression retrf ~ ewmktrf over 60-observation rolling windows
- Exact replication of Stata: asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)

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
    - Rolling 60-observation windows (not 60 months) with minimum 20 observations per window
    - CAPM regression: retrf = alpha + beta * ewmktrf + residual
    - Exact replication of Stata's asreg behavior
"""

import polars as pl
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.asreg import asreg_polars

print("=" * 80)
print("🏗️  Beta.py")
print("Generating CAPM Beta predictor using polars asreg rolling regression")
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
print("🧮 Computing CAPM Beta using asreg rolling 60-observation regressions...")

# Create excess returns (matching Stata exactly)
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("retrf"),
    (pl.col("ewretd") - pl.col("rf")).alias("ewmktrf")
])

# Add time sequence for each permno (replicates Stata's time_temp = _n)
df = df.with_columns(
    pl.int_range(pl.len()).over("permno").add(1).alias("time_temp")
)

print("Computing rolling regressions by permno (exact Stata replication)...")
print("This matches: asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)")

# Apply asreg rolling regression
print(f"Processing {df['permno'].n_unique():,} unique permnos...")
df_with_beta = asreg_polars(
    df,
    y="retrf", 
    X=["ewmktrf"],
    by=["permno"], 
    t="time_temp",
    mode="rolling", 
    window_size=60, 
    min_samples=20,
    outputs=("coef",),
    coef_prefix="b_"
)

# Extract Beta coefficient and filter to non-null values
df_final = (df_with_beta
    .filter(pl.col("b_ewmktrf").is_not_null())
    .select(["permno", "time_avail_m", pl.col("b_ewmktrf").alias("Beta")])
)

print(f"Generated Beta values: {len(df_final):,} observations")

if len(df_final) > 0:
    # Convert to pandas for summary stats (maintaining compatibility with save_predictor)
    df_final_pd = df_final.to_pandas()
    
    print(f"Beta summary stats:")
    print(f"  Mean: {df_final_pd['Beta'].mean():.4f}")
    print(f"  Std: {df_final_pd['Beta'].std():.4f}")
    print(f"  Min: {df_final_pd['Beta'].min():.4f}")  
    print(f"  Max: {df_final_pd['Beta'].max():.4f}")

    # SAVE
    print("💾 Saving Beta predictor...")
    save_predictor(df_final_pd, "Beta")
    print("✅ Beta.csv saved successfully")

else:
    print("⚠️ No Beta values generated - check data and parameters")
    
print("=" * 80)
print("✅ Beta.py Complete")
print("CAPM Beta predictor generated using polars asreg exact Stata replication")
print("=" * 80)