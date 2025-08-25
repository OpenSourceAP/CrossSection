# ABOUTME: WW_Q.py - calculates quarterly Whited-Wu index placebo
# ABOUTME: Python equivalent of WW_Q.do, translates line-by-line from Stata code

"""
WW_Q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, sicCRSP columns
    - m_QCompustat.parquet: gvkey, time_avail_m, atq, ibq, dpq, dvpsxq, dlttq, saleq columns

Outputs:
    - WW_Q.csv: permno, yyyymm, WW_Q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/WW_Q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting WW_Q.py")

# DATA LOAD
# use permno gvkey time_avail_m sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'sicCRSP'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ibq dpq dvpsxq dlttq saleq) nogenerate keep(match)
print("Loading m_QCompustat...")
comp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
comp = comp.select(['gvkey', 'time_avail_m', 'atq', 'ibq', 'dpq', 'dvpsxq', 'dlttq', 'saleq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
comp = comp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(comp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# Sort for lag operations
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# tostring sicCRSP, replace
# gen tempSIC3 = substr(sicCRSP, 1, 3)
print("Creating 3-digit SIC codes...")
df = df.with_columns([
    pl.col('sicCRSP').cast(pl.Utf8).str.slice(0, 3).alias('tempSIC3')
])

# egen tempIndSales = total(saleq), by(tempSIC3 time_avail_m)
print("Computing industry sales totals...")
df = df.with_columns([
    pl.col('saleq').sum().over(['tempSIC3', 'time_avail_m']).alias('tempIndSales')
])

# Create 3-month lag of tempIndSales and 1-quarter lag of saleq
print("Computing lags...")
df = df.with_columns([
    pl.col('tempIndSales').shift(3).over('permno').alias('l3_tempIndSales'),
    pl.col('saleq').shift(1).over('permno').alias('l1_saleq')
])

# gen WW_Q = -.091* (ibq+dpq)/atq -.062*(dvpsxq>0 & !mi(dvpsxq)) + .021*dlttq/atq ///
#          -.044*log(atq) + .102*(tempIndSales/l3.tempIndSales - 1) - .035*(saleq/l.saleq - 1)
print("Computing WW_Q index...")
df = df.with_columns([
    (
        -0.091 * ((pl.col('ibq') + pl.col('dpq')) / pl.col('atq'))
        - 0.062 * ((pl.col('dvpsxq') > 0) & pl.col('dvpsxq').is_not_null()).cast(pl.Float64)
        + 0.021 * (pl.col('dlttq') / pl.col('atq'))
        - 0.044 * pl.col('atq').log()
        + 0.102 * (pl.col('tempIndSales') / pl.col('l3_tempIndSales') - 1)
        - 0.035 * (pl.col('saleq') / pl.col('l1_saleq') - 1)
    ).alias('WW_Q')
])

print(f"Generated WW_Q for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'WW_Q'])

# SAVE
# do "$pathCode/saveplacebo" WW_Q
save_placebo(df_final, 'WW_Q')

print("WW_Q.py completed")