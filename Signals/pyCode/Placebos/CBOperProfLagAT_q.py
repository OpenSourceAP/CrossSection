# ABOUTME: CBOperProfLagAT_q.py - calculates cash-based operating profitability placebo (quarterly)
# ABOUTME: Python equivalent of CBOperProfLagAT_q.do, translates line-by-line from Stata code

"""
CBOperProfLagAT_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c, shrcd, sicCRSP columns
    - m_aCompustat.parquet: permno, time_avail_m, ceq columns
    - m_QCompustat.parquet: gvkey, time_avail_m, atq, revtq, cogsq, xsgaq, xrdq, rectq, invtq, drcq, drltq, apq, xaccq columns

Outputs:
    - CBOperProfLagAT_q.csv: permno, yyyymm, CBOperProfLagAT_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/CBOperProfLagAT_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting CBOperProfLagAT_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c shrcd sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c', 'shrcd', 'sicCRSP'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(ceq) keep(master match) nogenerate
print("Loading m_aCompustat...")
acomp = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
acomp = acomp.select(['permno', 'time_avail_m', 'ceq'])

print("Merging with m_aCompustat...")
df = df.join(acomp, on=['permno', 'time_avail_m'], how='left')

print(f"After merge with m_aCompustat: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq revtq cogsq xsgaq xrdq rectq invtq drcq drltq apq xaccq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'atq', 'revtq', 'cogsq', 'xsgaq', 'xrdq', 'rectq', 'invtq', 'drcq', 'drltq', 'apq', 'xaccq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge with m_QCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# foreach v of varlist revtq cogsq xsgaq xrdq rectq invtq drcq drltq apq xaccq {
#     replace `v' = 0 if mi(`v')
# }
print("Replacing missing values with 0...")
vars_to_fill = ['revtq', 'cogsq', 'xsgaq', 'xrdq', 'rectq', 'invtq', 'drcq', 'drltq', 'apq', 'xaccq']
for var in vars_to_fill:
    df = df.with_columns(pl.col(var).fill_null(0))

# Convert to pandas for lag operations
df_pd = df.to_pandas()

# Create 3-month lag date
df_pd['time_lag3'] = df_pd['time_avail_m'] - pd.DateOffset(months=3)

# Create lag data for merging
lag_vars = ['rectq', 'invtq', 'drcq', 'drltq', 'apq', 'xaccq', 'atq']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag3'] + [f'l3_{var}' for var in lag_vars]

# Merge lag data
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag3'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd.drop(columns=['time_lag3']))

# gen CBOperProfLagAT_q = (revtq - cogsq - (xsgaq - xrdq)) - (rectq - l3.rectq) - (invtq - l3.invtq) + (drcq + drltq - l3.drcq - l3.drltq) + (apq - l3.apq) + (xaccq - l3.xaccq)
print("Computing CBOperProfLagAT_q...")
df = df.with_columns(
    ((pl.col('revtq') - pl.col('cogsq') - (pl.col('xsgaq') - pl.col('xrdq'))) -
     (pl.col('rectq') - pl.col('l3_rectq')) -
     (pl.col('invtq') - pl.col('l3_invtq')) +
     (pl.col('drcq') + pl.col('drltq') - pl.col('l3_drcq') - pl.col('l3_drltq')) +
     (pl.col('apq') - pl.col('l3_apq')) +
     (pl.col('xaccq') - pl.col('l3_xaccq'))).alias('CBOperProfLagAT_q')
)

# replace CBOperProfLagAT_q = CBOperProfLagAT_q/l3.atq
print("Dividing by lagged atq...")
df = df.with_columns(
    (pl.col('CBOperProfLagAT_q') / pl.col('l3_atq')).alias('CBOperProfLagAT_q')
)

# gen BM = log(ceq/mve_c)
print("Computing BM...")
df = df.with_columns(
    (pl.col('ceq') / pl.col('mve_c')).log().alias('BM')
)

# replace CBOperProfLagAT_q = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(atq) | (sicCRSP >= 6000 & sicCRSP < 7000)
print("Applying filters...")
df = df.with_columns(
    pl.when((pl.col('shrcd') > 11) | pl.col('mve_c').is_null() | pl.col('BM').is_null() | 
            pl.col('atq').is_null() | ((pl.col('sicCRSP') >= 6000) & (pl.col('sicCRSP') < 7000)))
    .then(None)
    .otherwise(pl.col('CBOperProfLagAT_q'))
    .alias('CBOperProfLagAT_q')
)

print(f"Generated CBOperProfLagAT_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'CBOperProfLagAT_q'])

# SAVE
# do "$pathCode/saveplacebo" CBOperProfLagAT_q
save_placebo(df_final, 'CBOperProfLagAT_q')

print("CBOperProfLagAT_q.py completed")