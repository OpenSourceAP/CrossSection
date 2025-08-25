# ABOUTME: OperProfLag.py - calculates operating profits to lagged equity placebo
# ABOUTME: Python equivalent of OperProfLag.do, translates line-by-line from Stata code

"""
OperProfLag.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_aCompustat.parquet: gvkey, time_avail_m, revt, cogs, xsga, xint, ceq columns

Outputs:
    - OperProfLag.csv: permno, yyyymm, OperProfLag columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/OperProfLag.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.stata_fastxtile import fastxtile

print("Starting OperProfLag.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# drop if mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(revt cogs xsga xint ceq) nogenerate keep(match)
print("Loading m_aCompustat...")
comp = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
comp = comp.select(['gvkey', 'time_avail_m', 'revt', 'cogs', 'xsga', 'xint', 'ceq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
comp = comp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_aCompustat...")
df = df.join(comp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# Sort for lag calculation
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempprof = (revt - cogs - xsga - xint)/l12.ceq
print("Computing tempprof with 12-month lag...")
df = df.with_columns([
    pl.col('ceq').shift(12).over('permno').alias('l12_ceq')
])

df = df.with_columns([
    ((pl.col('revt') - pl.col('cogs') - pl.col('xsga') - pl.col('xint')) / pl.col('l12_ceq')).alias('tempprof')
])

# Convert to pandas for fastxtile operation
print("Converting to pandas for fastxtile...")
df_pandas = df.to_pandas()

# egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(3)
print("Computing size terciles...")
df_pandas['tempsizeq'] = fastxtile(df_pandas, 'mve_c', by='time_avail_m', n=3)

# replace tempprof = . if tempsizeq == 1
print("Filtering out smallest size tercile...")
df_pandas.loc[df_pandas['tempsizeq'] == 1, 'tempprof'] = None

# gen OperProfLag = tempprof
df_pandas['OperProfLag'] = df_pandas['tempprof']

print(f"Generated OperProfLag for {len(df_pandas)} observations")

# Convert back to polars and keep only required columns
df_final = pl.from_pandas(df_pandas[['permno', 'time_avail_m', 'OperProfLag']])

# SAVE
# do "$pathCode/saveplacebo" OperProfLag
save_placebo(df_final, 'OperProfLag')

print("OperProfLag.py completed")