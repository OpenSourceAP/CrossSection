# ABOUTME: pchsaleinv.py - calculates change in sales to inventory placebo
# ABOUTME: Python equivalent of pchsaleinv.do, translates line-by-line from Stata code

"""
pchsaleinv.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, invt columns.

Outputs:
    - ../pyData/Placebos/pchsaleinv.csv: permno, yyyymm (time_avail_m), pchsaleinv columns.

How to run:
    cd Signals/pyCode
    source .venv/bin/activate
    python3 Placebos/pchsaleinv.py

Example:
    python3 Placebos/pchsaleinv.py
"""

import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

print("Starting pchsaleinv.py")

# DATA LOAD
# use gvkey permno time_avail_m sale invt using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'invt'])

print(f"After loading m_aCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen pchsaleinv = ( (sale/invt)-(l12.sale/l12.invt) ) / (l12.sale/l12.invt)
print("Computing 12-month lags using stata_multi_lag...")
df = stata_multi_lag(
    df,
    group_col='permno',
    time_col='time_avail_m',
    value_col=['sale', 'invt'],
    lag_list=[12],
    freq='M',
    prefix='l',
)

print("Computing pchsaleinv...")
# Calculate the components with proper null handling
df = df.with_columns([
    # Current sale-to-inventory ratio
    pl.when(pl.col('invt') == 0)
    .then(None)
    .otherwise(pl.col('sale') / pl.col('invt'))
    .alias('saleinv_current'),
    # Lagged sale-to-inventory ratio
    pl.when(pl.col('l12_invt') == 0)
    .then(None)
    .otherwise(pl.col('l12_sale') / pl.col('l12_invt'))
    .alias('saleinv_lagged')
])

# Calculate pchsaleinv = (saleinv_current - saleinv_lagged) / saleinv_lagged
df = df.with_columns(
    pl.when(pl.col('saleinv_lagged') == 0)
    .then(None)
    .otherwise((pl.col('saleinv_current') - pl.col('saleinv_lagged')) / pl.col('saleinv_lagged'))
    .alias('pchsaleinv')
)

print(f"Generated pchsaleinv for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'pchsaleinv'])

# SAVE
# do "$pathCode/saveplacebo" pchsaleinv
save_placebo(df_final, 'pchsaleinv')

print("pchsaleinv.py completed")
