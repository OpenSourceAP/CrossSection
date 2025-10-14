# ABOUTME: KZ_q.py - calculates Kaplan-Zingales financial constraints index placebo (quarterly)
# ABOUTME: Python equivalent of KZ_q.do, translates line-by-line from Stata code

"""
KZ_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, txdiq, ibq, dpq, atq, ceqq, dlcq, dlttq, cheq, dvy, ppentq columns

Outputs:
    - KZ_q.csv: permno, yyyymm, KZ_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/KZ_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting KZ_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(txdiq ibq dpq atq ceqq dlcq dlttq cheq dvy ppentq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'txdiq', 'ibq', 'dpq', 'atq', 'ceqq', 'dlcq', 'dlttq', 'cheq', 'dvy', 'ppentq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen tempTX = txdiq
# replace tempTX = 0 if mi(tempTX)
print("Processing tempTX...")
df = df.with_columns([
    pl.col('txdiq').alias('tempTX')
])

df = df.with_columns([
    pl.when(pl.col('tempTX').is_null())
    .then(0.0)
    .otherwise(pl.col('tempTX'))
    .alias('tempTX')
])

# gen KZ_q = -1.002* (ibq + dpq)/ppentq + .283*(atq + mve_c - ceqq - tempTX)/atq + 3.139*(dlcq + dlttq)/(dlcq + dlttq + ceqq) - 39.368*(dvy/ppentq) - 1.315*(cheq/ppentq)
print("Computing KZ_q index...")

# Build the KZ_q formula step by step
df = df.with_columns([
    # Term 1: -1.002 * (ibq + dpq)/ppentq
    (-1.002 * (pl.col('ibq') + pl.col('dpq')) / pl.col('ppentq')).alias('term1'),
    
    # Term 2: 0.283 * (atq + mve_c - ceqq - tempTX)/atq
    (0.283 * (pl.col('atq') + pl.col('mve_c') - pl.col('ceqq') - pl.col('tempTX')) / pl.col('atq')).alias('term2'),
    
    # Term 3: 3.139 * (dlcq + dlttq)/(dlcq + dlttq + ceqq)
    (3.139 * (pl.col('dlcq') + pl.col('dlttq')) / (pl.col('dlcq') + pl.col('dlttq') + pl.col('ceqq'))).alias('term3'),
    
    # Term 4: -39.368 * (dvy/ppentq)
    (-39.368 * pl.col('dvy') / pl.col('ppentq')).alias('term4'),
    
    # Term 5: -1.315 * (cheq/ppentq)
    (-1.315 * pl.col('cheq') / pl.col('ppentq')).alias('term5')
])

# Sum all terms to get KZ_q
df = df.with_columns([
    (pl.col('term1') + pl.col('term2') + pl.col('term3') + pl.col('term4') + pl.col('term5')).alias('KZ_q')
])

print(f"Generated KZ_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'KZ_q'])

# SAVE
# do "$pathCode/saveplacebo" KZ_q
save_placebo(df_final, 'KZ_q')

print("KZ_q.py completed")