# ABOUTME: NetDebtPrice_q.py - calculates net debt to price ratio placebo (quarterly)
# ABOUTME: Python equivalent of NetDebtPrice_q.do, translates line-by-line from Stata code

"""
NetDebtPrice_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, dlttq, dlcq, pstkq, cheq, atq, ibq, ceqq columns
    - m_aCompustat.parquet: gvkey, time_avail_m, sic, ceq, csho, prcc_f columns

Outputs:
    - NetDebtPrice_q.csv: permno, yyyymm, NetDebtPrice_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/NetDebtPrice_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting NetDebtPrice_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dlttq dlcq pstkq cheq atq ibq ceqq) nogenerate keep(master match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'dlttq', 'dlcq', 'pstkq', 'cheq', 'atq', 'ibq', 'ceqq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
# Use left join to preserve SignalMasterTable observations
# Stata's keep(match) might be more lenient about missing values
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge with m_QCompustat: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(match) nogenerate keepusing(sic ceq csho prcc_f)
print("Loading m_aCompustat...")
acomp = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
acomp = acomp.select(['gvkey', 'time_avail_m', 'sic', 'ceq', 'csho', 'prcc_f'])
acomp = acomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_aCompustat...")
df = df.join(acomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge with m_aCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# destring sic, replace
print("Processing SIC codes...")
df = df.with_columns(
    pl.col('sic').cast(pl.Float64, strict=False)
)

# gen NetDebtPrice_q = ((dlttq + dlcq + pstkq) - cheq)/mve_c
print("Computing NetDebtPrice_q...")
df = df.with_columns(
    ((pl.col('dlttq') + pl.col('dlcq') + pl.col('pstkq')) - pl.col('cheq')).truediv(pl.col('mve_c')).alias('NetDebtPrice_q')
)

# replace NetDebtPrice_q = . if sic >= 6000 & sic <= 6999
print("Applying SIC filter (6000-6999)...")
df = df.with_columns(
    pl.when((pl.col('sic') >= 6000) & (pl.col('sic') <= 6999))
    .then(None)
    .otherwise(pl.col('NetDebtPrice_q'))
    .alias('NetDebtPrice_q')
)

# replace NetDebtPrice_q = . if mi(atq) | mi(ibq) | mi(csho) | mi(ceqq) | mi(prcc_f)
print("Applying missing value filters...")
df = df.with_columns(
    pl.when(pl.col('atq').is_null() | pl.col('ibq').is_null() | pl.col('csho').is_null() | 
            pl.col('ceqq').is_null() | pl.col('prcc_f').is_null())
    .then(None)
    .otherwise(pl.col('NetDebtPrice_q'))
    .alias('NetDebtPrice_q')
)

# * keep constant B/M, as in Table 4
# gen BM = log(ceq/mve_c)
print("Computing BM for quintile filtering...")
df = df.with_columns(
    (pl.col('ceq') / pl.col('mve_c')).log().alias('BM')
)

# Convert to pandas for quintile calculation
print("Converting to pandas for quintile calculation...")
df_pd = df.to_pandas()

# egen tempsort = fastxtile(BM), by(time_avail_m) n(5)
print("Computing BM quintiles by month...")
df_pd['tempsort'] = df_pd.groupby('time_avail_m')['BM'].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates='drop') + 1)

# Convert back to polars
df = pl.from_pandas(df_pd)

# replace NetDebtPrice_q = . if tempsort <= 2
print("Keeping only top 3 BM quintiles...")
df = df.with_columns(
    pl.when(pl.col('tempsort') <= 2)
    .then(None)
    .otherwise(pl.col('NetDebtPrice_q'))
    .alias('NetDebtPrice_q')
)

print(f"Generated NetDebtPrice_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'NetDebtPrice_q'])

# SAVE
# do "$pathCode/saveplacebo" NetDebtPrice_q
save_placebo(df_final, 'NetDebtPrice_q')

print("NetDebtPrice_q.py completed")