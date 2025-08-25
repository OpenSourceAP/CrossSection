# ABOUTME: WW.py - calculates Whited-Wu index placebo
# ABOUTME: Python equivalent of WW.do, translates line-by-line from Stata code

"""
WW.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sic, sale, ib, dp, at, dvpsx_c, dltt columns
    - SignalMasterTable.parquet: permno, time_avail_m, sicCRSP columns

Outputs:
    - WW.csv: permno, yyyymm, WW columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/WW.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting WW.py")

# DATA LOAD
# use gvkey permno time_avail_m sic sale ib dp at dvpsx_c dltt at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sic', 'sale', 'ib', 'dp', 'at', 'dvpsx_c', 'dltt'])

print(f"Loaded data: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(sicCRSP)
print("Loading SignalMasterTable...")
signal = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal = signal.select(['permno', 'time_avail_m', 'sicCRSP'])

print("Merging with SignalMasterTable...")
df = df.join(signal, on=['permno', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# Sort for lag operations
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempSIC = sicCRSP
# tostring tempSIC, replace
# gen tempSIC3 = substr(tempSIC, 1, 3)
print("Creating 3-digit SIC codes...")
df = df.with_columns([
    pl.col('sicCRSP').cast(pl.Utf8).str.slice(0, 3).alias('tempSIC3')
])

# egen tempIndSales = total(sale), by(tempSIC3 time_avail_m)
print("Computing industry sales totals...")
df = df.with_columns([
    pl.col('sale').sum().over(['tempSIC3', 'time_avail_m']).alias('tempIndSales')
])

# Create 12-month lag of tempIndSales and 1-month lag of sale
print("Computing lags...")
df = df.with_columns([
    pl.col('tempIndSales').shift(12).over('permno').alias('l12_tempIndSales'),
    pl.col('sale').shift(1).over('permno').alias('l1_sale')
])

# * Divide CF and growth rates by 4 to approximate quarterly rates
# gen WW = -.091* (ib+dp)/(4*at) -.062*(dvpsx_c>0 & !mi(dvpsx_c)) + .021*dltt/at ///
#          -.044*log(at) + .102*(tempIndSales/l12.tempIndSales - 1)/4 - .035*(sale/l.sale - 1)/4
print("Computing WW index...")
df = df.with_columns([
    (
        -0.091 * ((pl.col('ib') + pl.col('dp')) / (4 * pl.col('at')))
        - 0.062 * ((pl.col('dvpsx_c') > 0) & pl.col('dvpsx_c').is_not_null()).cast(pl.Float64)
        + 0.021 * (pl.col('dltt') / pl.col('at'))
        - 0.044 * pl.col('at').log()
        + 0.102 * ((pl.col('tempIndSales') / pl.col('l12_tempIndSales') - 1) / 4)
        - 0.035 * ((pl.col('sale') / pl.col('l1_sale') - 1) / 4)
    ).alias('WW')
])

print(f"Generated WW for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'WW'])

# SAVE
# do "$pathCode/saveplacebo" WW
save_placebo(df_final, 'WW')

print("WW.py completed")