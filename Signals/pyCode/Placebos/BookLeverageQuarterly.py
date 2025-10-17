# ABOUTME: BookLeverageQuarterly.py - calculates book leverage placebo (quarterly)
# ABOUTME: Python equivalent of BookLeverageQuarterly.do, translates line-by-line from Stata code

"""
BookLeverageQuarterly.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, txditcq, seqq, ceqq, pstkq, atq, ltq columns

Outputs:
    - BookLeverageQuarterly.csv: permno, yyyymm, BookLeverageQuarterly columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/BookLeverageQuarterly.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting BookLeverageQuarterly.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(txditcq seqq ceqq pstkq atq ltq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'txditcq', 'seqq', 'ceqq', 'pstkq', 'atq', 'ltq'])

# Apply forward-fill logic to match Stata's handling of missing quarterly data
print("Applying forward-fill for missing quarterly values...")
qcomp = apply_quarterly_fill_to_compustat(qcomp, quarterly_columns=['txditcq', 'seqq', 'ceqq', 'pstkq', 'atq', 'ltq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# replace txditcq = 0 if mi(txditcq)
print("Replacing missing txditcq with 0...")
df = df.with_columns(
    pl.col('txditcq').fill_null(0).alias('txditcq')
)

# gen tempSE = seqq
# replace tempSE = ceqq + pstkq if mi(tempSE)
# replace tempSE = atq - ltq if mi(tempSE)
print("Computing tempSE with conditional logic...")
df = df.with_columns(
    pl.when(pl.col('seqq').is_not_null())
    .then(pl.col('seqq'))
    .when(pl.col('ceqq').is_not_null() & pl.col('pstkq').is_not_null())
    .then(pl.col('ceqq') + pl.col('pstkq'))
    .when(pl.col('atq').is_not_null() & pl.col('ltq').is_not_null())
    .then(pl.col('atq') - pl.col('ltq'))
    .otherwise(None)
    .alias('tempSE')
)

# gen BookLeverageQuarterly = atq/(tempSE + txditcq - pstkq)
print("Computing BookLeverageQuarterly...")
df = df.with_columns(
    (pl.col('atq') / (pl.col('tempSE') + pl.col('txditcq') - pl.col('pstkq'))).alias('BookLeverageQuarterly')
)

print(f"Generated BookLeverageQuarterly for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'BookLeverageQuarterly'])

# SAVE
# do "$pathCode/saveplacebo" BookLeverageQuarterly
save_placebo(df_final, 'BookLeverageQuarterly')

print("BookLeverageQuarterly.py completed")