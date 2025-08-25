# ABOUTME: ZZ2_BetaDimson.py - calculates Dimson beta placebo using daily data
# ABOUTME: Python equivalent of ZZ2_BetaDimson.do, translates line-by-line from Stata code

"""
ZZ2_BetaDimson.py

Inputs:
    - dailyCRSP.parquet: permno, time_d, ret columns
    - dailyFF.parquet: time_d, rf, mktrf columns

Outputs:
    - BetaDimson.csv: permno, yyyymm, BetaDimson columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ2_BetaDimson.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.asreg import asreg

print("Starting ZZ2_BetaDimson.py")

# DATA LOAD
# use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
print("Loading dailyCRSP...")
df = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
df = df.select(['permno', 'time_d', 'ret'])

print(f"Loaded dailyCRSP: {len(df)} rows")

# merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
print("Loading dailyFF...")
ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
ff = ff.select(['time_d', 'rf', 'mktrf'])

print("Merging with dailyFF...")
df = df.join(ff, on=['time_d'], how='inner')

print(f"After merge: {len(df)} rows")

# replace ret = ret - rf
# drop rf
print("Converting to excess returns...")
df = df.with_columns([
    (pl.col('ret') - pl.col('rf')).alias('ret')
])
df = df.drop('rf')

# SIGNAL CONSTRUCTION
# bys permno (time_d): gen time_temp = _n
# xtset permno time_temp
print("Creating time index and sorting...")
df = df.sort(['permno', 'time_d'])
df = df.with_columns([
    pl.int_range(1, pl.len() + 1).over('permno').alias('time_temp')
])

# gen tempMktLead = f.mktrf
# gen tempMktLag  = l.mktrf
print("Creating lead and lag market returns...")
df = df.with_columns([
    pl.col('mktrf').shift(-1).over('permno').alias('tempMktLead'),
    pl.col('mktrf').shift(1).over('permno').alias('tempMktLag')
])

# asreg ret tempMktLead mktrf tempMktLag, window(time_temp 20) min(15) by(permno)
print("Running rolling Dimson regressions...")
df_regression = asreg(
    df, 
    y="ret", 
    X=["tempMktLead", "mktrf", "tempMktLag"], 
    by=["permno"], 
    t="time_temp", 
    mode="rolling", 
    window_size=20, 
    min_samples=15,
    outputs=["coeff"]
)

# gen BetaDimson = _b_tempMktLead + _b_mktrf + _b_tempMktLag
print("Computing BetaDimson...")
df_regression = df_regression.with_columns([
    (pl.col('b_tempMktLead') + pl.col('b_mktrf') + pl.col('b_tempMktLag')).alias('BetaDimson')
])

# gen time_avail_m = mofd(time_d)
df_regression = df_regression.with_columns([
    pl.col('time_d').dt.truncate('1mo').alias('time_avail_m')
])

# sort permno time_avail_m time_d
# gcollapse (lastnm) BetaDimson, by(permno time_avail_m)
print("Collapsing to monthly data...")
df_regression = df_regression.sort(['permno', 'time_avail_m', 'time_d'])
df_monthly = df_regression.group_by(['permno', 'time_avail_m']).agg([
    pl.col('BetaDimson').last().alias('BetaDimson')
])

print(f"Generated BetaDimson for {len(df_monthly)} observations")

# Keep only required columns
df_final = df_monthly.select(['permno', 'time_avail_m', 'BetaDimson'])

# SAVE
# do "$pathCode/saveplacebo" BetaDimson
save_placebo(df_final, 'BetaDimson')

print("ZZ2_BetaDimson.py completed")