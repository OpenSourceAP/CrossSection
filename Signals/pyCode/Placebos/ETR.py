# ABOUTME: Calculates effective tax rate placebo signal
# ABOUTME: Inputs: m_aCompustat.parquet | Outputs: ETR.csv | Run: python Placebos/ETR.py

import polars as pl
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.stata_replication import stata_multi_lag

# DATA LOAD
# use gvkey permno time_avail_m am txt pi am epspx ajex prcc_f using "$pathDataIntermediate/m_aCompustat", clear
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['permno', 'time_avail_m', 'am', 'txt', 'pi', 'epspx', 'ajex', 'prcc_f'])

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1
df = df.unique(subset=['permno', 'time_avail_m'])

# xtset permno time_avail_m
df = df.sort(['permno', 'time_avail_m'])

# replace am = 0 if mi(am)
df = df.with_columns(pl.col('am').fill_null(0))

# gen tempTaxOverEBT = txt/(pi + am)
df = df.with_columns(
    (pl.col('txt') / (pl.col('pi') + pl.col('am'))).alias('tempTaxOverEBT')
)

# gen tempEarn = epspx/ajex
df = df.with_columns(
    (pl.col('epspx') / pl.col('ajex')).alias('tempEarn')
)

# Create lags using stata_multi_lag
df = stata_multi_lag(df, 'permno', 'time_avail_m', ['tempTaxOverEBT'], [12, 24, 36], prefix='l')
df = stata_multi_lag(df, 'permno', 'time_avail_m', ['tempEarn'], [12], prefix='l')
df = stata_multi_lag(df, 'permno', 'time_avail_m', ['prcc_f'], [1], prefix='l')

# gen ETR = ( tempTaxOverEBT - 1/3*(l12.tempTaxOverEBT + l24.tempTaxOverEBT + l36.tempTaxOverEBT))*((tempEarn - l12.tempEarn)/l.prcc_f)
df = df.with_columns(
    (
        (pl.col('tempTaxOverEBT') - (1/3) * (pl.col('l12_tempTaxOverEBT') + pl.col('l24_tempTaxOverEBT') + pl.col('l36_tempTaxOverEBT'))) *
        ((pl.col('tempEarn') - pl.col('l12_tempEarn')) / pl.col('l1_prcc_f'))
    ).alias('ETR')
)

# Keep only required columns
df = df.select(['permno', 'time_avail_m', 'ETR'])

# SAVE
# do "$pathCode/saveplacebo" ETR
save_placebo(df, 'ETR')
