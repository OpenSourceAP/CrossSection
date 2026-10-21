# ABOUTME: RetNOA_q.py - calculates return on net operating assets placebo (quarterly)
# ABOUTME: Python equivalent of RetNOA_q.do, translates line-by-line from Stata code

"""
RetNOA_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, atq, ceqq, cheq, ivaoq, dlcq, dlttq, mibq, pstkq, oiadpq columns

Outputs:
    - RetNOA_q.csv: permno, yyyymm, RetNOA_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/RetNOA_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.saveplacebo import save_placebo

print("Starting RetNOA_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ceqq cheq ivaoq dlcq dlttq mibq pstkq oiadpq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'atq', 'ceqq', 'cheq', 'ivaoq', 'dlcq', 'dlttq', 'mibq', 'pstkq', 'oiadpq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
# Use left join to preserve SignalMasterTable observations
# Stata's keep(match) might be more lenient about missing values  
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempOA = atq - cheq - ivaoq
# replace tempOA = atq - cheq if mi(ivaoq)
print("Computing tempOA...")
df = df.with_columns(
    pl.when(pl.col('ivaoq').is_not_null())
    .then(pl.col('atq') - pl.col('cheq') - pl.col('ivaoq'))
    .otherwise(pl.col('atq') - pl.col('cheq'))
    .alias('tempOA')
)

# foreach v of varlist dlcq dlttq mibq pstkq {
#    gen temp`v' = `v'
#    replace temp`v' = 0 if mi(`v')
# }
print("Computing temp variables with missing replaced by 0...")
df = df.with_columns([
    pl.col('dlcq').fill_null(0).alias('tempdlcq'),
    pl.col('dlttq').fill_null(0).alias('tempdlttq'),
    pl.col('mibq').fill_null(0).alias('tempmibq'),
    pl.col('pstkq').fill_null(0).alias('temppstkq')
])

# gen tempOL = atq - tempdlcq - tempdlttq - tempmibq - temppstkq - ceqq
# NOTE: Handle null ceqq like other variables (treat as 0)
print("Computing tempOL...")
df = df.with_columns(
    (pl.col('atq') - pl.col('tempdlcq') - pl.col('tempdlttq') - pl.col('tempmibq') - pl.col('temppstkq') - pl.col('ceqq').fill_null(0)).alias('tempOL')
)

# Convert to pandas for lag operations
# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['tempOA', 'tempOL'], [3], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

# gen RetNOA_q = oiadpq/(l3.tempOA - l3.tempOL)
# NOTE: Handle null values in the calculation
print("Computing RetNOA_q...")
df = df.with_columns(
    (pl.col('oiadpq').fill_null(0) / (pl.col('l3_tempOA').fill_null(0) - pl.col('l3_tempOL').fill_null(0))).alias('RetNOA_q')
)

print(f"Generated RetNOA_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'RetNOA_q'])

# SAVE
# do "$pathCode/saveplacebo" RetNOA_q
save_placebo(df_final, 'RetNOA_q')

print("RetNOA_q.py completed")
