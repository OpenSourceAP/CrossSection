# ABOUTME: ZZ1_ResidualMomentum6m_ResidualMomentum.py - generates ResidualMomentum6m and ResidualMomentum predictors
# ABOUTME: Python translation of ZZ1_ResidualMomentum6m_ResidualMomentum.do using polars for rolling FF3 regressions

"""
ZZ1_ResidualMomentum6m_ResidualMomentum.py

Generates two momentum predictors based on Fama-French 3-factor model residuals:
- ResidualMomentum6m: 6-month residual momentum (placebo)
- ResidualMomentum: 12-month residual momentum based on FF3 residuals (predictor)

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ZZ1_ResidualMomentum6m_ResidualMomentum.py

Inputs:
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, ret)
    - ../pyData/Intermediate/monthlyFF.parquet (time_avail_m, rf, mktrf, smb, hml)

Outputs:
    - ../pyData/Placebos/ResidualMomentum6m.csv
    - ../pyData/Predictors/ResidualMomentum.csv

Requirements:
    - Rolling 36-month FF3 regressions with minimum 36 observations
    - Residuals are lagged by 1 month before momentum calculation
    - 6-month and 11-month rolling windows for momentum signals
"""

import polars as pl
import polars.selectors as cs
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.saveplacebo import save_placebo

print("=" * 80)
print("🏗️  ZZ1_ResidualMomentum6m_ResidualMomentum.py")
print("Generating ResidualMomentum6m and ResidualMomentum predictors")
print("=" * 80)

# DATA LOAD
print("📊 Loading monthly CRSP and Fama-French data...")

# Load monthly CRSP data (permno, time_avail_m, ret)
print("Loading monthlyCRSP.parquet...")
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded CRSP: {len(crsp):,} monthly observations")

# Load monthly FF factors and merge
print("Loading monthlyFF.parquet...")
ff = pl.read_parquet("../pyData/Intermediate/monthlyFF.parquet").select(["time_avail_m", "rf", "mktrf", "hml", "smb"])
print(f"Loaded FF factors: {len(ff):,} monthly observations")

# Merge CRSP and FF data (equivalent to Stata's merge m:1 ... keep(match))
print("Merging CRSP and FF data...")
df = crsp.join(ff, on="time_avail_m", how="inner")
print(f"Merged dataset: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("\n🔧 Starting signal construction...")

# Calculate excess returns: retrf = ret - rf
print("Calculating excess returns (retrf = ret - rf)...")
df = df.with_columns((pl.col("ret") - pl.col("rf")).alias("retrf"))

# Sort by permno and time_avail_m (important for time series operations)
df = df.sort(["permno", "time_avail_m"])

print("Running rolling 36-observation FF3 regressions by permno (manual implementation)...")
print("Processing", df['permno'].n_unique(), "unique permnos...")

# Manual rolling FF3 regression to exactly match Stata's asreg behavior
# polars-ols was giving incorrect results, so implementing manual calculation
result_dfs = []

for permno in df['permno'].unique():
    permno_data = df.filter(pl.col("permno") == permno).sort("time_avail_m")
    n_obs = len(permno_data)
    
    residuals = [None] * n_obs
    
    # Convert to numpy for faster calculation
    pdf = permno_data.to_pandas()
    retrf_vals = pdf['retrf'].values
    mktrf_vals = pdf['mktrf'].values  
    hml_vals = pdf['hml'].values
    smb_vals = pdf['smb'].values
    
    # Rolling 36-observation regressions
    for i in range(n_obs):
        if i >= 35:  # Need at least 36 observations (0-indexed)
            try:
                # Get 36-observation window ending at position i
                y_window = retrf_vals[i-35:i+1]
                X_window = np.column_stack([
                    np.ones(36),  # Intercept
                    mktrf_vals[i-35:i+1],
                    hml_vals[i-35:i+1], 
                    smb_vals[i-35:i+1]
                ])
                
                # OLS regression
                coeffs = np.linalg.lstsq(X_window, y_window, rcond=None)[0]
                alpha, beta_mkt, beta_hml, beta_smb = coeffs
                
                # Calculate residual for current observation (position i)
                predicted = alpha + beta_mkt * mktrf_vals[i] + beta_hml * hml_vals[i] + beta_smb * smb_vals[i]
                residual = retrf_vals[i] - predicted
                
                residuals[i] = residual
                
            except Exception as e:
                # Handle any numerical issues
                residuals[i] = None
    
    # Add residuals back to permno data
    # Ensure float64 type for residuals to avoid concat schema error
    residuals_float = [float(r) if r is not None else None for r in residuals]
    permno_with_residuals = permno_data.with_columns(
        pl.Series("_residuals", residuals_float, dtype=pl.Float64)
    )
    result_dfs.append(permno_with_residuals)

# Combine all permno results
df = pl.concat(result_dfs)
df = df.sort(["permno", "time_avail_m"])

print(f"Completed rolling regressions for {len(df):,} observations")

# Calculate lagged residuals and rolling momentum signals using pure Polars
print("Calculating lagged residuals and momentum signals...")
df = df.with_columns([
    # Lag residuals by 1 observation: temp = l1._residuals
    pl.col("_residuals").shift(1).over("permno").alias("temp")
]).with_columns([
    # 6-observation rolling statistics (position-based, min 6 observations)
    pl.col("temp").rolling_mean(window_size=6, min_samples=6).over("permno").alias("mean6_temp"),
    pl.col("temp").rolling_std(window_size=6, min_samples=6).over("permno").alias("sd6_temp"),
    # 11-observation rolling statistics (position-based, min 11 observations)
    pl.col("temp").rolling_mean(window_size=11, min_samples=11).over("permno").alias("mean11_temp"),
    pl.col("temp").rolling_std(window_size=11, min_samples=11).over("permno").alias("sd11_temp")
]).with_columns([
    # Calculate momentum signals
    (pl.col("mean6_temp") / pl.col("sd6_temp")).alias("ResidualMomentum6m"),
    (pl.col("mean11_temp") / pl.col("sd11_temp")).alias("ResidualMomentum")
])

print("Calculating 6-observation and 11-observation rolling momentum signals...")

# Display signal summary statistics
print("\n📈 Signal summary statistics:")
print(f"ResidualMomentum6m - Mean: {df.select(pl.col('ResidualMomentum6m').mean()).item():.4f}, Std: {df.select(pl.col('ResidualMomentum6m').std()).item():.4f}")
print(f"ResidualMomentum - Mean: {df.select(pl.col('ResidualMomentum').mean()).item():.4f}, Std: {df.select(pl.col('ResidualMomentum').std()).item():.4f}")
print(f"Non-missing ResidualMomentum6m: {df.select(pl.col('ResidualMomentum6m').is_not_null().sum()).item():,}")
print(f"Non-missing ResidualMomentum: {df.select(pl.col('ResidualMomentum').is_not_null().sum()).item():,}")

# SAVE
print("\n💾 Saving signals...")

# Convert to pandas for save functions (they expect pandas DataFrames)
final_df = df.select(['permno', 'time_avail_m', 'ResidualMomentum6m', 'ResidualMomentum']).to_pandas()

# Save ResidualMomentum6m as placebo
save_placebo(final_df[['permno', 'time_avail_m', 'ResidualMomentum6m']], 'ResidualMomentum6m')

# Save ResidualMomentum as predictor
save_predictor(final_df[['permno', 'time_avail_m', 'ResidualMomentum']], 'ResidualMomentum')

print("\n" + "=" * 80)
print("✅ ZZ1_ResidualMomentum6m_ResidualMomentum.py completed successfully")
print("Generated 2 signals:")
print("  • ResidualMomentum6m: 6 month residual momentum (Placebo)")
print("  • ResidualMomentum: Momentum based on FF3 residuals (Predictor)")
print("=" * 80)