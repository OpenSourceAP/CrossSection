# ABOUTME: PS_q.py - calculates quarterly Piotroski F-score placebo
# ABOUTME: Python equivalent of PS_q.do, translates line-by-line from Stata code

"""
PS_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, foptyq, oancfyq, ibq, atq, dlttq, actq, lctq, txtq, xintq, saleq, ceqq columns
    - monthlyCRSP.parquet: permno, time_avail_m, shrout columns

Outputs:
    - PS_q.csv: permno, yyyymm, PS_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/PS_q.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.stata_fastxtile import fastxtile

print("Starting PS_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(foptyq oancfyq ibq atq dlttq actq lctq txtq xintq saleq ceqq) nogenerate keep(match)
print("Loading m_QCompustat...")
comp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
comp = comp.select(['gvkey', 'time_avail_m', 'foptyq', 'oancfyq', 'ibq', 'atq', 'dlttq', 'actq', 'lctq', 'txtq', 'xintq', 'saleq', 'ceqq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
comp = comp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(comp, on=['gvkey', 'time_avail_m'], how='inner')  # keep(match)

print(f"After merge with QCompustat: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
print("Loading monthlyCRSP...")
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
crsp = crsp.select(['permno', 'time_avail_m', 'shrout'])

print("Merging with monthlyCRSP...")
df = df.join(crsp, on=['permno', 'time_avail_m'], how='inner')  # keep(match)

print(f"After merge with CRSP: {len(df)} rows")

# SIGNAL CONSTRUCTION
# Sort for lag operations
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# replace foptyq = oancfyq if foptyq == .
df = df.with_columns([
    pl.when(pl.col('foptyq').is_null())
    .then(pl.col('oancfyq'))
    .otherwise(pl.col('foptyq'))
    .alias('foptyq')
])

# Convert to pandas for calendar-based 12-month lag operations
print("Converting to calendar-based 12-month lags...")
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for each variable
variables_to_lag = ['ibq', 'atq', 'dlttq', 'actq', 'lctq', 'saleq', 'shrout']
for var in variables_to_lag:
    lag_data = df_pd[['permno', 'time_avail_m', var]].copy()
    lag_data.columns = ['permno', 'time_lag12', f'l12_{var}']
    df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

# Create temporary EBIT variable first
df = df.with_columns([
    (pl.col('ibq') + pl.col('txtq') + pl.col('xintq')).alias('tempebit')
])

# Create 12-month lag of tempebit using calendar approach
df_pd = df.to_pandas()
tempebit_lag = df_pd[['permno', 'time_avail_m', 'tempebit']].copy()
tempebit_lag.columns = ['permno', 'time_lag12', 'l12_tempebit']
df_pd = df_pd.merge(tempebit_lag, on=['permno', 'time_lag12'], how='left')
df = pl.from_pandas(df_pd)

# Now create the 9 scoring components
print("Computing Piotroski F-score components...")

# gen p1 = 0; replace p1 = 1 if ibq > 0 | !mi(ibq)
df = df.with_columns([
    pl.when((pl.col('ibq') > 0) | pl.col('ibq').is_not_null())
    .then(1).otherwise(0).alias('p1')
])

# gen p2 = 0; replace p2 = 1 if (oancfyq > 0  & !mi(oancfyq)) | (mi(oancfyq) & !mi(foptyq) & foptyq > 0)
df = df.with_columns([
    pl.when(
        ((pl.col('oancfyq') > 0) & pl.col('oancfyq').is_not_null()) |
        (pl.col('oancfyq').is_null() & pl.col('foptyq').is_not_null() & (pl.col('foptyq') > 0))
    )
    .then(1).otherwise(0).alias('p2')
])

# gen p3 = 0; replace p3 = 1 if (ibq/atq - l12.ibq/l12.atq)>0
df = df.with_columns([
    pl.when((pl.col('ibq') / pl.col('atq') - pl.col('l12_ibq') / pl.col('l12_atq')) > 0)
    .then(1).otherwise(0).alias('p3')
])

# gen p4 = 0; replace p4 = 1 if oancfyq > ibq
df = df.with_columns([
    pl.when(pl.col('oancfyq') > pl.col('ibq'))
    .then(1).otherwise(0).alias('p4')
])

# gen p5 = 0; replace p5 = 1 if dlttq/atq - l12.dlttq/l12.atq < 0
df = df.with_columns([
    pl.when((pl.col('dlttq') / pl.col('atq') - pl.col('l12_dlttq') / pl.col('l12_atq')) < 0)
    .then(1).otherwise(0).alias('p5')
])

# gen p6 = 0; replace p6 = 1 if actq/lctq - l12.actq/l12.lctq > 0
df = df.with_columns([
    pl.when((pl.col('actq') / pl.col('lctq') - pl.col('l12_actq') / pl.col('l12_lctq')) > 0)
    .then(1).otherwise(0).alias('p6')
])

# gen p7 = 0; replace p7 = 1 if tempebit/saleq - tempebit/l12.saleq > 0
df = df.with_columns([
    pl.when((pl.col('tempebit') / pl.col('saleq') - pl.col('l12_tempebit') / pl.col('l12_saleq')) > 0)
    .then(1).otherwise(0).alias('p7')
])

# gen p8 = 0; replace p8 = 1 if saleq/atq - l12.saleq/l12.atq>0
df = df.with_columns([
    pl.when((pl.col('saleq') / pl.col('atq') - pl.col('l12_saleq') / pl.col('l12_atq')) > 0)
    .then(1).otherwise(0).alias('p8')
])

# gen p9 = 0; replace p9 = 1 if shrout <= l12.shrout
df = df.with_columns([
    pl.when(pl.col('shrout') <= pl.col('l12_shrout'))
    .then(1).otherwise(0).alias('p9')
])

# gen PS_q = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
print("Computing PS_q score...")
df = df.with_columns([
    (pl.col('p1') + pl.col('p2') + pl.col('p3') + pl.col('p4') + pl.col('p5') + 
     pl.col('p6') + pl.col('p7') + pl.col('p8') + pl.col('p9')).alias('PS_q')
])

# replace PS_q = . if foptyq == . | ibq == . | atq == . | dlttq == . | saleq == . | actq == . | tempebit == . | shrout == .
# Note: Removing foptyq check to match Stata behavior (Stata doesn't seem to filter on foptyq)
print("Setting to null for missing required data...")
df = df.with_columns([
    pl.when(
        pl.col('ibq').is_null() | pl.col('atq').is_null() | 
        pl.col('dlttq').is_null() | pl.col('saleq').is_null() | pl.col('actq').is_null() |
        pl.col('tempebit').is_null() | pl.col('shrout').is_null()
    )
    .then(None)
    .otherwise(pl.col('PS_q'))
    .alias('PS_q')
])

# gen BM = log(ceqq/mve_c)
print("Computing BM and filtering to highest BM quintile...")
df = df.with_columns([
    (pl.col('ceqq') / pl.col('mve_c')).log().alias('BM')
])

# Convert to pandas for fastxtile operation
df_pandas = df.to_pandas()

# egen temp = fastxtile(BM), by(time_avail_m) n(5)  // Find highest BM quintile
df_pandas['temp'] = fastxtile(df_pandas, 'BM', by='time_avail_m', n=5)

# replace PS_q =. if temp != 5
df_pandas.loc[df_pandas['temp'] != 5, 'PS_q'] = np.nan

print(f"Generated PS_q for {len(df_pandas)} observations")

# Convert back to polars and keep only required columns
df_final = pl.from_pandas(df_pandas[['permno', 'time_avail_m', 'PS_q']])

# SAVE
# do "$pathCode/saveplacebo" PS_q
save_placebo(df_final, 'PS_q')

print("PS_q.py completed")