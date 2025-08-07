# ABOUTME: BetaLiquidityPS.py - generates Pastor-Stambaugh liquidity beta using 60-month rolling regressions
# ABOUTME: Python translation of BetaLiquidityPS.do using polars-ols for 4-factor regressions

"""
BetaLiquidityPS.py

Generates Pastor-Stambaugh liquidity beta predictor from 4-factor rolling regressions:
- BetaLiquidityPS: Coefficient of ps_innov from regression retrf ~ ps_innov + mktrf + hml + smb

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
    - Rolling 60-month windows with minimum 36 observations per window
    - 4-factor regression: retrf = alpha + beta_ps*ps_innov + beta_mkt*mktrf + beta_hml*hml + beta_smb*smb + residual
"""

import polars as pl
import polars_ols  # registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor

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
print("🧮 Computing Pastor-Stambaugh liquidity beta using rolling 60-month 4-factor regressions...")

# Create excess returns
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("retrf")
])

# Add time sequence for each permno (replicates Stata's time_temp)
df = df.with_columns(
    pl.int_range(pl.len()).over("permno").alias("time_temp")
)

print(f"Computing rolling 4-factor regressions for {df['permno'].n_unique():,} unique permnos...")

# Rolling 4-factor regression: retrf ~ ps_innov + mktrf + hml + smb with 60-month windows
df_with_beta = df.with_columns(
    pl.col("retrf")
    .least_squares.rolling_ols(
        pl.col("ps_innov"), 
        pl.col("mktrf"), 
        pl.col("hml"), 
        pl.col("smb"),
        window_size=60,
        mode="coefficients"
    )
    .over("permno")
    .alias("_b_coeffs")
)

# Extract Pastor-Stambaugh liquidity beta coefficient 
df_final = df_with_beta.with_columns(
    pl.col("_b_coeffs").struct.field("ps_innov").alias("BetaLiquidityPS")
).select(["permno", "time_avail_m", "BetaLiquidityPS"]).filter(
    pl.col("BetaLiquidityPS").is_not_null()
)

print(f"Generated BetaLiquidityPS values: {len(df_final):,} observations")
print(f"BetaLiquidityPS summary stats:")
print(f"  Mean: {df_final['BetaLiquidityPS'].mean():.4f}")
print(f"  Std: {df_final['BetaLiquidityPS'].std():.4f}")
print(f"  Min: {df_final['BetaLiquidityPS'].min():.4f}")  
print(f"  Max: {df_final['BetaLiquidityPS'].max():.4f}")

# SAVE
print("💾 Saving BetaLiquidityPS predictor...")
save_predictor(df_final, "BetaLiquidityPS")
print("✅ BetaLiquidityPS.csv saved successfully")