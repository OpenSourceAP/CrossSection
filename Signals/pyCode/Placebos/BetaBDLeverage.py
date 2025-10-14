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

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

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

# Compute quarterly returns directly in Polars for efficiency
print("Computing quarterly returns...")
df_grouped = df.group_by(['permno', 'year', 'qtr']).agg([
    pl.col('ret').sort_by('time_avail_m').alias('ret_sorted'),
    pl.len().alias('n_months')
])

# Only keep quarters with exactly 3 months of data
df_grouped = df_grouped.filter(pl.col('n_months') == 3)

# Compute quarterly return: (1+ret1)*(1+ret2)*(1+ret3) - 1
df_quarterly = df_grouped.with_columns([
    ((1 + pl.col('ret_sorted').list.get(0)) * 
     (1 + pl.col('ret_sorted').list.get(1)) * 
     (1 + pl.col('ret_sorted').list.get(2)) - 1).alias('RetQ')
]).select(['permno', 'year', 'qtr', 'RetQ'])

# Remove any NaN quarterly returns
df_quarterly = df_quarterly.filter(pl.col('RetQ').is_not_null())

print(f"After quarterly aggregation: {len(df_quarterly)} rows")

# * Merge BD leverage and T-bill rate
# merge m:1 year qtr using "$pathDataIntermediate/brokerLev", keep(master match) nogenerate
print("Loading broker leverage data...")
broker_lev = pl.read_parquet("../pyData/Intermediate/brokerLev.parquet")
broker_lev = broker_lev.select(['year', 'qtr', 'levfac'])

print("Merging with broker leverage...")
df_quarterly = df_quarterly.join(broker_lev, on=['year', 'qtr'], how='inner')

# merge m:1 year qtr using "$pathDataIntermediate/TBill3M", keep(master match) nogenerate
print("Loading T-bill data...")
tbill = pl.read_parquet("../pyData/Intermediate/TBill3M.parquet")
tbill = tbill.select(['year', 'qtr', 'TbillRate3M'])

print("Merging with T-bill data...")
df_quarterly = df_quarterly.join(tbill, on=['year', 'qtr'], how='inner')

print(f"After merging external data: {len(df_quarterly)} rows")

# * Prepare and run regression
# replace RetQ = RetQ - TbillRate3M
print("Converting to excess returns...")
df_quarterly = df_quarterly.with_columns([
    (pl.col('RetQ') - pl.col('TbillRate3M')).alias('RetQ')
])

# gen tempTime = yq(year, qtr)
print("Creating quarterly time variable...")
df_quarterly = df_quarterly.with_columns([
    (pl.col('year') * 4 + pl.col('qtr') - 1).alias('tempTime')
])

# asreg RetQ levfac, window(tempTime 40) min(20) by(permno)
print("Running rolling regressions with 40-quarter window...")
df_quarterly = df_quarterly.sort(['permno', 'tempTime'])
df_quarterly = df_quarterly.with_columns(
    pl.col('RetQ')
    .least_squares.rolling_ols(
        pl.col('levfac'),
        window_size=40,
        min_periods=20,
        mode='coefficients',
        add_intercept=True,
        null_policy='drop'
    )
    .over('permno')
    .alias('coef')
).with_columns([
    pl.col('coef').struct.field('levfac').alias('BetaRaw')
])

# * Lag by one quarter to make sure that beta is available
# gen BetaBDLeverage = l._b_levfac
print("Creating lagged beta...")
df_quarterly = df_quarterly.with_columns([
    pl.col('BetaRaw').shift(1).over('permno').alias('BetaBDLeverage')
])

# keep permno year qtr BetaBDLeverage
regression_result = df_quarterly.select(['permno', 'year', 'qtr', 'BetaBDLeverage'])

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
    pl.int_range(1, pl.len() + 1).over('permno').alias('age')
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
