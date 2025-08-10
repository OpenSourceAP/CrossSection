# ABOUTME: BetaLiquidityPS.py - generates Pastor-Stambaugh liquidity beta using asreg rolling regressions
# ABOUTME: Python translation of BetaLiquidityPS.do using polars and asreg helper for exact Stata replication

"""
BetaLiquidityPS.py

Generates Pastor-Stambaugh liquidity beta predictor from 4-factor rolling regressions:
- BetaLiquidityPS: Coefficient of ps_innov from regression retrf ~ ps_innov + mktrf + hml + smb
- Exact replication of Stata: asreg retrf ps_innov mktrf hml smb, window(time_temp 60) min(36) by(permno)

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
    - Exact replication of Stata's asreg behavior
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.asreg import asreg

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
print("🧮 Computing Pastor-Stambaugh liquidity beta using asreg rolling 60-observation 4-factor regressions...")

# Create excess returns (matching Stata exactly)
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("retrf")
])

# Add time sequence for each permno (replicates Stata's time_temp = _n)
df = df.with_columns(
    pl.int_range(pl.len()).over("permno").add(1).alias("time_temp")
)

print(f"Computing rolling 4-factor regressions for {df['permno'].n_unique():,} unique permnos...")
print("This matches: asreg retrf ps_innov mktrf hml smb, window(time_temp 60) min(36) by(permno)")

# Apply asreg rolling 4-factor regression
df_with_beta = asreg(
    df,
    y="retrf", 
    X=["ps_innov", "mktrf", "hml", "smb"],
    by=["permno"], 
    t="time_temp",
    mode="rolling", 
    window_size=60, 
    min_samples=36,
    outputs=("coef",),
    coef_prefix="b_"
)

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
print("Pastor-Stambaugh liquidity beta predictor generated using polars asreg exact Stata replication")
print("=" * 80)