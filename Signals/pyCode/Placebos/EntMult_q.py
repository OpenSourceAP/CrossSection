# ABOUTME: EntMult_q.py - calculates enterprise multiple placebo (quarterly)
# ABOUTME: Python equivalent of EntMult_q.do, translates line-by-line from Stata code

"""
EntMult_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, dlttq, dlcq, pstkq, cheq, oibdpq, ceqq columns

Outputs:
    - EntMult_q.csv: permno, yyyymm, EntMult_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/EntMult_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting EntMult_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dlttq dlcq pstkq che oibdpq ceqq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'dlttq', 'dlcq', 'pstkq', 'cheq', 'oibdpq', 'ceqq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

# Remove forward-fill to match Stata behavior exactly
# print("Applying forward-fill for missing quarterly values...")
# qcomp = apply_quarterly_fill_to_compustat(qcomp, quarterly_columns=['dlttq', 'dlcq', 'pstkq', 'cheq', 'oibdpq', 'ceqq'])

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen EntMult_q = (mve_c + dlttq + dlcq + pstkq - cheq)/oibdpq
print("Computing EntMult_q...")
df = df.with_columns(
    ((pl.col('mve_c') + pl.col('dlttq') + pl.col('dlcq') + pl.col('pstkq') - pl.col('cheq')) / pl.col('oibdpq')).alias('EntMult_q')
)

# replace EntMult_q = . if ceqq < 0 | oibdpq < 0
print("Applying conditional filter...")
df = df.with_columns(
    pl.when((pl.col('ceqq') < 0) | (pl.col('oibdpq') < 0))
    .then(None)
    .otherwise(pl.col('EntMult_q'))
    .alias('EntMult_q')
)

print(f"Generated EntMult_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'EntMult_q'])

# SAVE
# do "$pathCode/saveplacebo" EntMult_q
save_placebo(df_final, 'EntMult_q')

print("EntMult_q.py completed")