# ABOUTME: BetaBDLeverage.py - calculates broker-dealer leverage beta placebo
# ABOUTME: Python equivalent of BetaBDLeverage.do, translates line-by-line from Stata code

"""
BetaBDLeverage.py

Inputs:
    - SignalMasterTable.parquet: permno, time_avail_m, ret columns
    - brokerLev.parquet: year, qtr, levfac columns
    - TBill3M.parquet: year, qtr, TbillRate3M columns

Outputs:
    - BetaBDLeverage.csv: permno, yyyymm, BetaBDLeverage columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/BetaBDLeverage.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.asreg import asreg

print("Starting BetaBDLeverage.py")

# DATA LOAD
# use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'time_avail_m', 'ret'])

print(f"Loaded SignalMasterTable: {len(df)} rows")

# SIGNAL CONSTRUCTION
# replace ret = 0 if mi(ret)
df = df.with_columns([
    pl.col('ret').fill_null(0)
])

# * Collapse to quarterly returns
# gen year = year(dofm(time_avail_m))
# gen qtr = quarter(dofm(time_avail_m))
print("Creating year and quarter variables...")
df = df.with_columns([
    pl.col('time_avail_m').dt.year().alias('year'),
    pl.col('time_avail_m').dt.quarter().alias('qtr')
])

# Sort for quarterly return calculation
print("Sorting by permno, year, qtr, time...")
df = df.sort(['permno', 'year', 'qtr', 'time_avail_m'])

# Convert to pandas for complex quarterly return calculation
print("Converting to pandas for quarterly return calculation...")
df_pandas = df.to_pandas()

# bys permno year qtr (time_avail_m): gen RetQ = (1+ret)*(1+ret[_n+1])*(1+ret[_n+2]) - 1 if _n == 1
print("Computing quarterly returns...")
def compute_quarterly_returns(group):
    if len(group) >= 3:
        ret_vals = group['ret'].values
        # Take first month as base, compound with next 2 months
        retq = (1 + ret_vals[0]) * (1 + ret_vals[1]) * (1 + ret_vals[2]) - 1
        group.loc[group.index[0], 'RetQ'] = retq
    return group

df_pandas['RetQ'] = np.nan
df_pandas = df_pandas.groupby(['permno', 'year', 'qtr']).apply(compute_quarterly_returns)

# keep if !mi(RetQ)
df_pandas = df_pandas.dropna(subset=['RetQ'])

# keep permno year qtr RetQ
df_quarterly = df_pandas[['permno', 'year', 'qtr', 'RetQ']].copy()

print(f"After quarterly aggregation: {len(df_quarterly)} rows")

# * Merge BD leverage and T-bill rate
# merge m:1 year qtr using "$pathDataIntermediate/brokerLev", keep(master match) nogenerate
print("Loading broker leverage data...")
broker_lev = pl.read_parquet("../pyData/Intermediate/brokerLev.parquet")
broker_lev = broker_lev.select(['year', 'qtr', 'levfac'])
broker_lev_pandas = broker_lev.to_pandas()

print("Merging with broker leverage...")
df_quarterly = df_quarterly.merge(broker_lev_pandas, on=['year', 'qtr'], how='left')

# merge m:1 year qtr using "$pathDataIntermediate/TBill3M", keep(master match) nogenerate
print("Loading T-bill data...")
tbill = pl.read_parquet("../pyData/Intermediate/TBill3M.parquet")
tbill = tbill.select(['year', 'qtr', 'TbillRate3M'])
tbill_pandas = tbill.to_pandas()

print("Merging with T-bill data...")
df_quarterly = df_quarterly.merge(tbill_pandas, on=['year', 'qtr'], how='left')

print(f"After merging external data: {len(df_quarterly)} rows")

# * Prepare and run regression
# replace RetQ = RetQ - TbillRate3M
print("Converting to excess returns...")
df_quarterly['RetQ'] = df_quarterly['RetQ'] - df_quarterly['TbillRate3M']

# gen tempTime = yq(year, qtr)
print("Creating quarterly time variable...")
df_quarterly['tempTime'] = df_quarterly['year'] * 4 + df_quarterly['qtr'] - 1

# Convert back to polars for asreg
df_quarterly_pl = pl.from_pandas(df_quarterly)

# asreg RetQ levfac, window(tempTime 40) min(20) by(permno)
print("Running rolling regressions with 40-quarter window...")
df_regression = asreg(
    df_quarterly_pl, 
    y="RetQ", 
    X=["levfac"], 
    by=["permno"], 
    t="tempTime", 
    mode="rolling", 
    window_size=40, 
    min_samples=20,
    outputs=["coeff"]
)

# * Lag by one quarter to make sure that beta is available
# gen BetaBDLeverage = l._b_levfac
print("Creating lagged beta...")
df_regression = df_regression.sort(['permno', 'tempTime'])
df_regression = df_regression.with_columns([
    pl.col('levfac_coeff').shift(1).over('permno').alias('BetaBDLeverage')
])

# keep permno year qtr BetaBDLeverage
regression_result = df_regression.select(['permno', 'year', 'qtr', 'BetaBDLeverage'])

print(f"After regression: {len(regression_result)} rows")

# * Spread out to monthly dataset
# use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading monthly dataset for expansion...")
monthly_df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
monthly_df = monthly_df.select(['permno', 'time_avail_m'])

# gen qtr = quarter(dofm(time_avail_m))
# gen year = year(dofm(time_avail_m))
monthly_df = monthly_df.with_columns([
    pl.col('time_avail_m').dt.year().alias('year'),
    pl.col('time_avail_m').dt.quarter().alias('qtr')
])

# merge m:1 permno year qtr using temp
print("Merging quarterly results to monthly data...")
final_df = monthly_df.join(regression_result, on=['permno', 'year', 'qtr'], how='left')

# * remove firms with less than 20 quarters of return dataset
# sort permno time_avail_m
# bys permno: gen age = _n
# replace BetaBDLeverage = . if age <= 20/4*12
print("Filtering by firm age...")
final_df = final_df.sort(['permno', 'time_avail_m'])
final_df = final_df.with_columns([
    pl.int_range(1, pl.count() + 1).over('permno').alias('age')
])

min_age_months = int(20/4*12)  # 20 quarters in months = 60 months
final_df = final_df.with_columns([
    pl.when(pl.col('age') <= min_age_months)
    .then(None)
    .otherwise(pl.col('BetaBDLeverage'))
    .alias('BetaBDLeverage')
])

print(f"Generated BetaBDLeverage for {len(final_df)} observations")

# Keep only required columns
df_final = final_df.select(['permno', 'time_avail_m', 'BetaBDLeverage'])

# SAVE
# do "$pathCode/saveplacebo" BetaBDLeverage
save_placebo(df_final, 'BetaBDLeverage')

print("BetaBDLeverage.py completed")