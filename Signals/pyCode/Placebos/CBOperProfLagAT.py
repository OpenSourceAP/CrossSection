# ABOUTME: CBOperProfLagAT.py - calculates cash-based operating profitability placebo (annual)
# ABOUTME: Python equivalent of CBOperProfLagAT.do, translates line-by-line from Stata code

"""
CBOperProfLagAT.py

Inputs:
    - m_aCompustat.parquet: permno, time_avail_m, revt, cogs, xsga, xrd, rect, invt, xpp, drc, drlt, ap, xacc, at, ceq columns
    - SignalMasterTable.parquet: permno, time_avail_m, mve_permco, sicCRSP, shrcd columns

Outputs:
    - CBOperProfLagAT.csv: permno, yyyymm, CBOperProfLagAT columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/CBOperProfLagAT.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

print("Starting CBOperProfLagAT.py")

# DATA LOAD
# use permno time_avail_m revt cogs xsga xrd rect invt xpp drc drlt ap xacc at ceq using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['permno', 'time_avail_m', 'revt', 'cogs', 'xsga', 'xrd', 'rect', 'invt', 'xpp', 'drc', 'drlt', 'ap', 'xacc', 'at', 'ceq'])

print(f"After loading m_aCompustat: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_permco sicCRSP shrcd)
print("Loading SignalMasterTable...")
signal_df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_df = signal_df.select(['permno', 'time_avail_m', 'mve_permco', 'sicCRSP', 'shrcd'])

print("Merging with SignalMasterTable...")
df = df.join(signal_df, on=['permno', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# foreach v of varlist revt cogs xsga xrd rect invt xpp drc drlt ap xacc {
#     replace `v' = 0 if mi(`v')
# }
print("Replacing missing values with 0...")
vars_to_fill = ['revt', 'cogs', 'xsga', 'xrd', 'rect', 'invt', 'xpp', 'drc', 'drlt', 'ap', 'xacc']
for var in vars_to_fill:
    df = df.with_columns(pl.col(var).fill_null(0))

# Convert to pandas for stata_multi_lag
df_pd = df.to_pandas()

# Create 12-month lags using stata_multi_lag
print("Computing 12-month lags using stata_multi_lag...")
lag_vars = ['rect', 'invt', 'xpp', 'drc', 'drlt', 'ap', 'xacc', 'at']
for var in lag_vars:
    df_pd = stata_multi_lag(df_pd, 'permno', 'time_avail_m', var, [12], freq='M', prefix='l')

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen CBOperProfLagAT = (revt - cogs - (xsga - xrd)) - (rect - l12.rect) - (invt - l12.invt) - (xpp - l12.xpp) + (drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)
print("Computing CBOperProfLagAT...")
df = df.with_columns(
    ((pl.col('revt') - pl.col('cogs') - (pl.col('xsga') - pl.col('xrd'))) -
     (pl.col('rect') - pl.col('l12_rect')) -
     (pl.col('invt') - pl.col('l12_invt')) -
     (pl.col('xpp') - pl.col('l12_xpp')) +
     (pl.col('drc') + pl.col('drlt') - pl.col('l12_drc') - pl.col('l12_drlt')) +
     (pl.col('ap') - pl.col('l12_ap')) +
     (pl.col('xacc') - pl.col('l12_xacc'))).alias('CBOperProfLagAT')
)

# replace CBOperProfLagAT = CBOperProfLagAT/l12.at
print("Dividing by lagged at...")
df = df.with_columns(
    (pl.col('CBOperProfLagAT') / pl.col('l12_at')).alias('CBOperProfLagAT')
)

# gen BM = log(ceq/mve_permco)
print("Computing BM...")
df = df.with_columns(
    (pl.col('ceq') / pl.col('mve_permco')).log().alias('BM')
)

# replace CBOperProfLagAT = . if shrcd > 11 | mi(mve_permco) | mi(BM) | mi(at) | (sicCRSP >= 6000 & sicCRSP < 7000)
print("Applying filters...")
df = df.with_columns(
    pl.when((pl.col('shrcd') > 11) | pl.col('mve_permco').is_null() | pl.col('BM').is_null() | 
            pl.col('at').is_null() | ((pl.col('sicCRSP') >= 6000) & (pl.col('sicCRSP') < 7000)))
    .then(None)
    .otherwise(pl.col('CBOperProfLagAT'))
    .alias('CBOperProfLagAT')
)

print(f"Generated CBOperProfLagAT for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'CBOperProfLagAT'])

# SAVE
# do "$pathCode/saveplacebo" CBOperProfLagAT
save_placebo(df_final, 'CBOperProfLagAT')

print("CBOperProfLagAT.py completed")