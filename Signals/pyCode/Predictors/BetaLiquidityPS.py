# ABOUTME: BetaLiquidityPS.py - generates Pastor-Stambaugh liquidity beta using polars-ols rolling regressions
# ABOUTME: Computes liquidity risk exposure coefficient from 4-factor rolling window regressions

"""
BetaLiquidityPS.py

Generates Pastor-Stambaugh liquidity beta predictor from 4-factor rolling regressions:
- BetaLiquidityPS: Coefficient of liquidity innovation from 4-factor model regression
- Rolling 60-observation windows with minimum 36 observations, computed separately for each stock

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/BetaLiquidityPS.py

Inputs:
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, ret)
    - ../pyData/Intermediate/monthlyFF.parquet (time_avail_m, rf, mktrf, hml, smb)
    - ../pyData/Intermediate/monthlyLiquidity.parquet (time_avail_m, ps_innov)

Outputs:
    - ../pyData/Predictors/BetaLiquidityPS.csv

Requirements:
    - Rolling 60-observation windows (not 60 months) with minimum 36 observations per window
    - 4-factor regression: retrf = alpha + beta_ps*ps_innov + beta_mkt*mktrf + beta_hml*hml + beta_smb*smb + residual
    - Sequential window-based regression estimation for each stock
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  BetaLiquidityPS.py")
print("Generating Pastor-Stambaugh liquidity beta predictor")
print("=" * 80)

# DATA LOAD
print("📊 Loading monthly CRSP, FF, and Liquidity data...")

# Load monthly CRSP data (permno, time_avail_m, ret)
print("Loading monthlyCRSP.parquet...")
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded CRSP: {len(crsp):,} monthly observations")

# Load monthly FF data for factors and risk-free rate
print("Loading monthlyFF.parquet...")  
ff = pl.read_parquet("../pyData/Intermediate/monthlyFF.parquet").select(["time_avail_m", "rf", "mktrf", "hml", "smb"])
print(f"Loaded FF: {len(ff):,} monthly observations")

# Load monthly Liquidity data for Pastor-Stambaugh innovation
print("Loading monthlyLiquidity.parquet...")
liquidity = pl.read_parquet("../pyData/Intermediate/monthlyLiquidity.parquet").select(["time_avail_m", "ps_innov"])
print(f"Loaded Liquidity: {len(liquidity):,} monthly observations")

# MERGE DATA
print("🔗 Merging datasets...")
df = (crsp
    .join(ff, on="time_avail_m", how="inner")
    .join(liquidity, on="time_avail_m", how="left")  # Keep missing liquidity obs  
    .sort(["permno", "time_avail_m"])
)
print(f"After merging: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("🧮 Computing Pastor-Stambaugh liquidity beta using direct polars-ols rolling 60-observation 4-factor regressions...")

# Create excess returns
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("retrf")
])

# Add observation sequence number for rolling window identification
df = df.with_columns(
    pl.int_range(pl.len()).over("permno").add(1).alias("time_temp")
)

print(f"Computing rolling 4-factor regressions for {df['permno'].n_unique():,} unique permnos...")
print("Using 60-observation rolling windows with 36-observation minimum for each stock")

# Apply direct polars-ols rolling 4-factor regression
# Sort by permno and time_temp for deterministic window order
df = df.sort(["permno", "time_temp"])

df_with_beta = df.with_columns(
    pl.col("retrf").least_squares.rolling_ols(
        pl.col("ps_innov"), pl.col("mktrf"), pl.col("hml"), pl.col("smb"),
        window_size=60,
        min_periods=36,
        mode="coefficients",
        add_intercept=True,
        null_policy="drop"
    ).over("permno").alias("coef")
).with_columns([
    pl.col("coef").struct.field("const").alias("b_const"),
    pl.col("coef").struct.field("ps_innov").alias("b_ps_innov"),
    pl.col("coef").struct.field("mktrf").alias("b_mktrf"),
    pl.col("coef").struct.field("hml").alias("b_hml"),
    pl.col("coef").struct.field("smb").alias("b_smb")
])

# Extract Pastor-Stambaugh liquidity beta coefficient and filter to non-null values
df_final = (df_with_beta
    .filter(pl.col("b_ps_innov").is_not_null())
    .select(["permno", "time_avail_m", pl.col("b_ps_innov").alias("BetaLiquidityPS")])
).filter(
    pl.col("BetaLiquidityPS").is_not_null()
)

print(f"Generated BetaLiquidityPS values: {len(df_final):,} observations")

if len(df_final) > 0:
    # Convert to pandas for summary stats (maintaining compatibility with save_predictor)
    df_final_pd = df_final.to_pandas()
    
    print(f"BetaLiquidityPS summary stats:")
    print(f"  Mean: {df_final_pd['BetaLiquidityPS'].mean():.4f}")
    print(f"  Std: {df_final_pd['BetaLiquidityPS'].std():.4f}")
    print(f"  Min: {df_final_pd['BetaLiquidityPS'].min():.4f}")  
    print(f"  Max: {df_final_pd['BetaLiquidityPS'].max():.4f}")

    # SAVE
    print("💾 Saving BetaLiquidityPS predictor...")
    save_predictor(df_final_pd, "BetaLiquidityPS")
    print("✅ BetaLiquidityPS.csv saved successfully")
else:
    print("⚠️ No BetaLiquidityPS values generated - check data and parameters")
    
print("=" * 80)
print("✅ BetaLiquidityPS.py Complete")
print("Pastor-Stambaugh liquidity beta predictor generated using rolling 4-factor regressions")
print("=" * 80)