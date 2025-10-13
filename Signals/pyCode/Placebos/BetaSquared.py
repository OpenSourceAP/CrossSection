# ABOUTME: BetaSquared.py - calculates beta squared placebo using rolling CAPM regression
# ABOUTME: Python equivalent of BetaSquared.do, translates line-by-line from Stata code

"""
BetaSquared.py

Inputs:
    - monthlyCRSP.parquet: permno, time_avail_m, ret columns
    - monthlyFF.parquet: time_avail_m, rf columns
    - monthlyMarket.parquet: time_avail_m, ewretd columns

Outputs:
    - BetaSquared.csv: permno, yyyymm, BetaSquared columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/BetaSquared.py
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting BetaSquared.py")

# DATA LOAD
# use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
print("Loading monthlyCRSP...")
df = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = df.select(['permno', 'time_avail_m', 'ret'])

print(f"After loading monthlyCRSP: {len(df)} rows")

# merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf)
print("Loading monthlyFF...")
ff = pl.read_parquet("../pyData/Intermediate/monthlyFF.parquet")
ff = ff.select(['time_avail_m', 'rf'])

print("Merging with monthlyFF...")
df = df.join(ff, on='time_avail_m', how='inner')

print(f"After merge with monthlyFF: {len(df)} rows")

# merge m:1 time_avail_m using "$pathDataIntermediate/monthlyMarket", nogenerate keep(match) keepusing(ewretd)
print("Loading monthlyMarket...")
market = pl.read_parquet("../pyData/Intermediate/monthlyMarket.parquet")
market = market.select(['time_avail_m', 'ewretd'])

print("Merging with monthlyMarket...")
df = df.join(market, on='time_avail_m', how='inner')

print(f"After merge with monthlyMarket: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen retrf = ret - rf
# gen ewmktrf = ewretd - rf
print("Computing excess returns...")
df = df.with_columns([
    (pl.col('ret') - pl.col('rf')).alias('retrf'),
    (pl.col('ewretd') - pl.col('rf')).alias('ewmktrf')
])

# Stata: bys permno (time_avail_m): gen time_temp = _n
# xtset permno time_temp
# asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)
print("Computing rolling CAPM beta with 60-month window...")
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns(
    pl.col('retrf')
    .least_squares.rolling_ols(
        pl.col('ewmktrf'),
        window_size=60,
        min_periods=20,
        mode='coefficients',
        add_intercept=True,
        null_policy='drop'
    )
    .over('permno')
    .alias('coef')
).with_columns([
    pl.col('coef').struct.field('ewmktrf').alias('Beta')
])

# gen BetaSquared = Beta^2
print("Computing BetaSquared...")
df = df.with_columns([
    (pl.col('Beta') ** 2).alias('BetaSquared')
])

print(f"Generated BetaSquared for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'BetaSquared'])

# SAVE
# do "$pathCode/saveplacebo" BetaSquared
save_placebo(df_final, 'BetaSquared')

print("BetaSquared.py completed")
