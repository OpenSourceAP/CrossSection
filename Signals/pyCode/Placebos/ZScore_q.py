# ABOUTME: ZScore_q.py - calculates Altman Z-Score placebo (quarterly)
# ABOUTME: Python equivalent of ZScore_q.do, translates line-by-line from Stata code

"""
ZScore_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, sicCRSP, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, actq, lctq, atq, req, niq, xintq, txtq, ltq, revtq columns

Outputs:
    - ZScore_q.csv: permno, yyyymm, ZScore_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZScore_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting ZScore_q.py")

# DATA LOAD
# use permno gvkey time_avail_m sicCRSP mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'sicCRSP', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(actq lctq atq req atq niq xintq txtq ltq revtq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'actq', 'lctq', 'atq', 'req', 'niq', 'xintq', 'txtq', 'ltq', 'revtq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Applying forward-fill for missing quarterly values...")
qcomp = apply_quarterly_fill_to_compustat(qcomp, quarterly_columns=['actq', 'lctq', 'atq', 'req', 'niq', 'xintq', 'txtq', 'ltq', 'revtq'])

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen ZScore_q = 1.2*(actq - lctq)/atq + 1.4*(req/atq) + 3.3*(niq + xintq + txtq)/atq + .6*(mve_permco/ltq) + revtq/atq
print("Computing ZScore_q...")
df = df.with_columns(
    (1.2 * (pl.col('actq') - pl.col('lctq')) / pl.col('atq') + 
     1.4 * pl.col('req') / pl.col('atq') + 
     3.3 * (pl.col('niq') + pl.col('xintq') + pl.col('txtq')) / pl.col('atq') + 
     0.6 * pl.col('mve_permco') / pl.col('ltq') + 
     pl.col('revtq') / pl.col('atq')).alias('ZScore_q')
)

# replace ZScore_q = . if (sicCRSP >3999 & sicCRSP < 4999) | sicCRSP > 5999
print("Applying SIC filters...")
df = df.with_columns(
    pl.when(((pl.col('sicCRSP') > 3999) & (pl.col('sicCRSP') < 4999)) | (pl.col('sicCRSP') > 5999))
    .then(None)
    .otherwise(pl.col('ZScore_q'))
    .alias('ZScore_q')
)

print(f"Generated ZScore_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ZScore_q'])

# SAVE
# do "$pathCode/saveplacebo" ZScore_q
save_placebo(df_final, 'ZScore_q')

print("ZScore_q.py completed")