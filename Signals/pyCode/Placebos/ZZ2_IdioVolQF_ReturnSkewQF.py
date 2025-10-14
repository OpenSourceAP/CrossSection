# ABOUTME: IdioVolQF and ReturnSkewQF placebos - idiosyncratic volatility and skewness using Q factors
# ABOUTME: Python equivalent of ZZ2_IdioVolQF_ReturnSkewQF.do using Q factors instead of FF3 factors

"""
Usage:
    python3 Placebos/ZZ2_IdioVolQF_ReturnSkewQF.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, ret]
    - d_qfactor.parquet: Daily Q factors with columns [time_d, r_f_qfac, r_mkt_qfac, r_me_qfac, r_ia_qfac, r_roe_qfac]

Outputs:
    - IdioVolQF.csv: permno, yyyymm, IdioVolQF columns
    - ReturnSkewQF.csv: permno, yyyymm, ReturnSkewQF columns
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting ZZ2_IdioVolQF_ReturnSkewQF.py...")

# Check if Q factor data exists
qfactor_file = "../pyData/Intermediate/d_qfactor.parquet"
if not Path(qfactor_file).exists():
    print(f"WARNING: {qfactor_file} not found!")
    print("Creating empty placeholder results...")
    
    # Create empty DataFrames
    empty_vol = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime("us")),
        'IdioVolQF': pl.Series([], dtype=pl.Float64)
    })
    
    empty_skew = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime("us")),
        'ReturnSkewQF': pl.Series([], dtype=pl.Float64)
    })
    
    save_placebo(empty_vol, 'IdioVolQF')
    save_placebo(empty_skew, 'ReturnSkewQF')
    print("Generated 0 IdioVolQF observations (missing Q-factor data)")
    print("Generated 0 ReturnSkewQF observations (missing Q-factor data)")
    exit()

print("Step 1: Loading daily CRSP and Q factor data...")
# Load daily CRSP data
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
crsp = daily_crsp.select(["permno", "time_d", "ret"])
print(f"Loaded CRSP: {len(crsp):,} daily observations")

# Load daily Q factors
d_qfactor = pl.read_parquet(qfactor_file)
qf = d_qfactor.select(["time_d", "r_f_qfac", "r_mkt_qfac", "r_me_qfac", "r_ia_qfac", "r_roe_qfac"])
print(f"Loaded Q factors: {len(qf):,} daily observations")

print("Step 2: Merging CRSP and Q factor data...")
# Merge CRSP and Q factors
df = crsp.join(qf, on="time_d", how="inner")
print(f"Merged dataset: {len(df):,} observations")

# Adjust returns: ret = ret - r_f_qfac (following Stata logic)
df = df.with_columns([
    (pl.col("ret") - pl.col("r_f_qfac")).alias("ret")
]).drop("r_f_qfac")

print("Step 3: Setting up for monthly Q factor regressions...")
# Create time_avail_m (year-month identifier)
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
]).sort(["permno", "time_avail_m", "time_d"])

print(f"Date range: {df['time_d'].min()} to {df['time_d'].max()}")

print("Step 4: Running Q factor regressions by permno-month...")
# Run Q factor regressions by permno-month to get residuals
# Following: bys permno time_avail_m: asreg ret r_mkt_qfac r_me_qfac r_ia_qfac r_roe_qfac, fit
df_with_residuals = df.with_columns([
    pl.col("ret").least_squares.ols(
        pl.col("r_mkt_qfac"), pl.col("r_me_qfac"), pl.col("r_ia_qfac"), pl.col("r_roe_qfac"),
        mode="residuals",
        add_intercept=True,
        null_policy="drop"
    ).over(["permno", "time_avail_m"]).alias("_residuals")
]).filter(
    # Require minimum observations per group (following typical asreg practice)
    pl.col("ret").count().over(["permno", "time_avail_m"]) >= 15
)

# Filter out observations where Q factor regression failed
df_filtered = df_with_residuals.filter(pl.col("_residuals").is_not_null())
print(f"After Q factor regressions: {len(df_filtered):,} observations")

print("Step 5: Computing IdioVolQF and ReturnSkewQF...")
# Collapse into standard deviation (IdioVolQF) and skewness (ReturnSkewQF)
# Following: gcollapse (sd) IdioVolQF = _residuals (skewness) ReturnSkewQF = _residuals, by(permno time_avail_m)

results = df_filtered.group_by(["permno", "time_avail_m"]).agg([
    # Standard deviation of residuals
    pl.col("_residuals").std().alias("IdioVolQF"),
    # Skewness of residuals (using polars' built-in skew function)
    pl.col("_residuals").skew().alias("ReturnSkewQF")
])

# Filter out rows with missing values
results = results.filter(
    pl.col("IdioVolQF").is_not_null() & 
    pl.col("ReturnSkewQF").is_not_null()
)

print(f"Final results: {len(results):,} permno-month observations")

print("Step 6: Separating and saving results...")
# Separate IdioVolQF and ReturnSkewQF
idio_vol_qf = results.select(["permno", "time_avail_m", "IdioVolQF"])
return_skew_qf = results.select(["permno", "time_avail_m", "ReturnSkewQF"])

# Save both placebos
save_placebo(idio_vol_qf, "IdioVolQF")
save_placebo(return_skew_qf, "ReturnSkewQF")

print(f"Generated {len(idio_vol_qf)} IdioVolQF observations")
print(f"Generated {len(return_skew_qf)} ReturnSkewQF observations")

print("ZZ2_IdioVolQF_ReturnSkewQF.py completed successfully")