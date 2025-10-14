# ABOUTME: OScore_q.py - calculates quarterly O-Score placebo
# ABOUTME: Python equivalent of OScore_q.do, translates line-by-line from Stata code

"""
OScore_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, sicCRSP, prc columns
    - m_QCompustat.parquet: gvkey, time_avail_m, foptyq, atq, ltq, actq, lctq, ibq, oancfyq columns
    - GNPdefl.parquet: time_avail_m, gnpdefl columns

Outputs:
    - OScore_q.csv: permno, yyyymm, OScore_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/OScore_q.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_fastxtile import fastxtile

print("Starting OScore_q.py")

# DATA LOAD
# use permno gvkey time_avail_m sicCRSP prc using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'sicCRSP', 'prc'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(foptyq atq ltq actq lctq ibq oancfyq) nogenerate keep(match)
print("Loading m_QCompustat...")
comp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
comp = comp.select(['gvkey', 'time_avail_m', 'foptyq', 'atq', 'ltq', 'actq', 'lctq', 'ibq', 'oancfyq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
comp = comp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(comp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge with QCompustat: {len(df)} rows")

# merge m:1 time_avail_m using "$pathDataIntermediate/GNPdefl", keep(match) nogenerate 
print("Loading GNPdefl...")
gnp = pl.read_parquet("../pyData/Intermediate/GNPdefl.parquet")
gnp = gnp.select(['time_avail_m', 'gnpdefl'])

print("Merging with GNPdefl...")
df = df.join(gnp, on=['time_avail_m'], how='inner')

print(f"After merge with GNPdefl: {len(df)} rows")

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

# Create 12-month lags needed for the formula
print("Computing 12-month lags...")
df = df.with_columns([
    pl.col('ibq').shift(12).over('permno').alias('l12_ibq')
])

# gen OScore_q = -1.32 - .407*log(atq/gnpdefl) + 6.03*(ltq/atq) - 1.43*( (actq - lctq)/atq) + ///
#     .076*(lctq/actq) - 1.72*(ltq>atq) - 2.37*(ibq/atq) - 1.83*(foptyq/ltq) + .285*(ibq + l12.ibq <0) - ///
#     .521*( (ibq - l12.ibq)/(abs(ibq) + abs(l12.ibq)) )
print("Computing OScore_q...")
df = df.with_columns([
    (
        -1.32 
        - 0.407 * (pl.col('atq') / pl.col('gnpdefl')).log()
        + 6.03 * pl.when(pl.col('atq') == 0)
                 .then(0)
                 .otherwise(pl.col('ltq') / pl.col('atq'))
        - 1.43 * pl.when(pl.col('atq') == 0)
                 .then(0)
                 .otherwise((pl.col('actq') - pl.col('lctq')) / pl.col('atq'))
        + 0.076 * pl.when(pl.col('actq') == 0)
                  .then(0)
                  .otherwise(pl.col('lctq') / pl.col('actq'))
        - 1.72 * (pl.col('ltq') > pl.col('atq')).cast(pl.Float64)
        - 2.37 * pl.when(pl.col('atq') == 0)
                 .then(0)
                 .otherwise(pl.col('ibq') / pl.col('atq'))
        - 1.83 * pl.when(pl.col('foptyq').is_null() | pl.col('ltq').is_null() | (pl.col('ltq') == 0))
                 .then(0)
                 .otherwise(pl.col('foptyq') / pl.col('ltq'))
        + 0.285 * pl.when(pl.col('l12_ibq').is_null())
                  .then((pl.col('ibq') < 0).cast(pl.Float64))
                  .otherwise(((pl.col('ibq') + pl.col('l12_ibq')) < 0).cast(pl.Float64))
        - 0.521 * pl.when(pl.col('l12_ibq').is_null())
                  .then(0)
                  .otherwise((pl.col('ibq') - pl.col('l12_ibq')) / (pl.col('ibq').abs() + pl.col('l12_ibq').abs()))
    ).alias('OScore_q')
])

# replace OScore_q = . if (sicCRSP > 3999 & sicCRSP < 5000) | sicCRSP > 5999 
print("Filtering out financial firms...")
df = df.with_columns([
    pl.when(((pl.col('sicCRSP') > 3999) & (pl.col('sicCRSP') < 5000)) | (pl.col('sicCRSP') > 5999))
    .then(None)
    .otherwise(pl.col('OScore_q'))
    .alias('OScore_q')
])

# Convert to pandas for fastxtile operation
print("Converting to pandas for fastxtile...")
df_pandas = df.to_pandas()

# Filter out infinite values before fastxtile (like Stata filters missing values)
print("Filtering out infinite OScore_q values...")
valid_mask = df_pandas['OScore_q'].notna() & np.isfinite(df_pandas['OScore_q'])
df_valid = df_pandas[valid_mask].copy()
print(f"Valid observations for fastxtile: {len(df_valid)} (filtered out {len(df_pandas) - len(df_valid)} infinite/null values)")

# * form LS following Tab 5  
# NOTE: Stata code has 'fastxtile(OScore)' but variable is 'OScore_q' - assuming this means OScore_q
# egen tempsort = fastxtile(OScore_q), by(time_avail_m) n(10)
print("Computing OScore deciles...")
df_valid['tempsort'] = fastxtile(df_valid, 'OScore_q', by='time_avail_m', n=10)

# replace OScore_q = .
# replace OScore_q = 1 if tempsort == 10  
# replace OScore_q = 0 if tempsort <= 7  & tempsort >= 1
print("Converting to binary signal...")
df_valid['OScore_q_new'] = np.nan
df_valid.loc[df_valid['tempsort'] == 10, 'OScore_q_new'] = 1
df_valid.loc[(df_valid['tempsort'] >= 1) & (df_valid['tempsort'] <= 7), 'OScore_q_new'] = 0

# Replace the original OScore_q with the new binary version
df_valid['OScore_q'] = df_valid['OScore_q_new']

print(f"Generated OScore_q for {len(df_valid)} observations")

# Convert back to polars and keep only required columns  
df_final = pl.from_pandas(df_valid[['permno', 'time_avail_m', 'OScore_q']])

# SAVE
# do "$pathCode/saveplacebo" OScore_q
save_placebo(df_final, 'OScore_q')

print("OScore_q.py completed")