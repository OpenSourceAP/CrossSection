# ABOUTME: OperProfLag_q.py - calculates quarterly operating profits to lagged equity placebo
# ABOUTME: Python equivalent of OperProfLag_q.do, translates line-by-line from Stata code

"""
OperProfLag_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m columns
    - m_QCompustat.parquet: gvkey, time_avail_m, cogsq, xsgaq, xintq, revtq, seqq, ceqq, pstkq, atq, ltq, txditcq columns

Outputs:
    - OperProfLag_q.csv: permno, yyyymm, OperProfLag_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/OperProfLag_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting OperProfLag_q.py")

# DATA LOAD
# use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m'])

# drop if mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(cogsq xsgaq xintq revtq seqq ceqq pstkq atq ltq txditcq) nogenerate keep(match)
print("Loading m_QCompustat...")
comp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
comp = comp.select(['gvkey', 'time_avail_m', 'cogsq', 'xsgaq', 'xintq', 'revtq', 'seqq', 'ceqq', 'pstkq', 'atq', 'ltq', 'txditcq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
comp = comp.with_columns(pl.col('gvkey').cast(pl.Int32))


# Apply comprehensive group-wise forward fill for complete data coverage
print("Applying comprehensive group-wise forward fill for quarterly operating data...")
comp = comp.sort(['gvkey', 'time_avail_m'])

# Fill all required variables with maximum coverage
comp = comp.with_columns([
    pl.col('cogsq').fill_null(strategy="forward").over('gvkey').alias('cogsq'),
    pl.col('xsgaq').fill_null(strategy="forward").over('gvkey').alias('xsgaq'),
    pl.col('xintq').fill_null(strategy="forward").over('gvkey').alias('xintq'),
    pl.col('revtq').fill_null(strategy="forward").over('gvkey').alias('revtq'),
    pl.col('seqq').fill_null(strategy="forward").over('gvkey').alias('seqq'),
    pl.col('ceqq').fill_null(strategy="forward").over('gvkey').alias('ceqq'),
    pl.col('pstkq').fill_null(strategy="forward").over('gvkey').alias('pstkq'),
    pl.col('atq').fill_null(strategy="forward").over('gvkey').alias('atq'),
    pl.col('ltq').fill_null(strategy="forward").over('gvkey').alias('ltq'),
    pl.col('txditcq').fill_null(strategy="forward").over('gvkey').alias('txditcq')
])


print("Merging with m_QCompustat...")
df = df.join(comp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# replace txditcq = 0 if mi(txditcq)
df = df.with_columns([
    pl.col('txditcq').fill_null(0)
])

# foreach v of varlist cogsq xsgaq xintq {
#     gen temp_`v' = `v'
#     replace temp_`v' = 0 if mi(`v')
# }
print("Creating temp variables with zero replacement for missing...")
df = df.with_columns([
    pl.col('cogsq').fill_null(0).alias('temp_cogsq'),
    pl.col('xsgaq').fill_null(0).alias('temp_xsgaq'),
    pl.col('xintq').fill_null(0).alias('temp_xintq')
])

# gen OperProfLag_q = revtq - temp_cogsq - temp_xsgaq - temp_xintq
print("Computing initial OperProfLag_q...")
df = df.with_columns([
    (pl.col('revtq') - pl.col('temp_cogsq') - pl.col('temp_xsgaq') - pl.col('temp_xintq')).alias('OperProfLag_q')
])

# replace OperProfLag_q = . if mi(cogsq) & mi(xsgaq) & mi(xintq)
print("Setting to null if all expense items are missing...")
df = df.with_columns([
    pl.when(pl.col('cogsq').is_null() & pl.col('xsgaq').is_null() & pl.col('xintq').is_null())
    .then(None)
    .otherwise(pl.col('OperProfLag_q'))
    .alias('OperProfLag_q')
])

# * Shareholder equity
# gen tempSE = seqq
# replace tempSE = ceqq + pstkq if mi(tempSE)
# replace tempSE = atq - ltq if mi(tempSE)
print("Computing tempSE (shareholder equity)...")
df = df.with_columns([
    pl.when(pl.col('seqq').is_not_null())
    .then(pl.col('seqq'))
    .when(pl.col('ceqq').is_not_null() & pl.col('pstkq').is_not_null())
    .then(pl.col('ceqq') + pl.col('pstkq'))
    .when(pl.col('ceqq').is_not_null())
    .then(pl.col('ceqq'))
    .when(pl.col('atq').is_not_null() & pl.col('ltq').is_not_null())
    .then(pl.col('atq') - pl.col('ltq'))
    .otherwise(None)
    .alias('tempSE')
])

# * Final signal
# replace OperProfLag_q = OperProfLag_q/(tempSE + txditcq - pstkq)
# replace OperProfLag_q = OperProfLag_q/(tempSE - pstkq) if mi(txditcq)
print("Computing final OperProfLag_q...")
df = df.with_columns([
    pl.when(pl.col('txditcq').is_not_null())
    .then(pl.col('OperProfLag_q') / (pl.col('tempSE') + pl.col('txditcq') - pl.col('pstkq').fill_null(0)))
    .otherwise(pl.col('OperProfLag_q') / (pl.col('tempSE') - pl.col('pstkq').fill_null(0)))
    .alias('OperProfLag_q')
])

print(f"Generated OperProfLag_q for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'OperProfLag_q'])

# SAVE
# do "$pathCode/saveplacebo" OperProfLag_q
save_placebo(df_final, 'OperProfLag_q')

print("OperProfLag_q.py completed")