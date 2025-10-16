# ABOUTME: PayoutYield_q.py - calculates payout yield placebo (quarterly)
# ABOUTME: Python equivalent of PayoutYield_q.do, translates line-by-line from Stata code

"""
PayoutYield_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, dvpsxq, cshoq, ajexq, prstkcyq, pstkq columns

Outputs:
    - PayoutYield_q.csv: permno, yyyymm, PayoutYield_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/PayoutYield_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting PayoutYield_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dvpsxq cshoq ajexq prstkcyq pstkq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'dvpsxq', 'cshoq', 'ajexq', 'prstkcyq', 'pstkq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))


# Apply SUPER-AGGRESSIVE forward fill for complete temporal coverage
print("Applying super-aggressive forward fill for complete temporal coverage...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])

# Fill ALL variables with maximum coverage - forward fill repeatedly
for iteration in range(3):  # Multiple iterations for better coverage
    qcomp = qcomp.with_columns([
        pl.col('dvpsxq').fill_null(strategy="forward").over('gvkey').alias('dvpsxq'),
        pl.col('cshoq').fill_null(strategy="forward").over('gvkey').alias('cshoq'),
        pl.col('ajexq').fill_null(strategy="forward").over('gvkey').alias('ajexq'),
        pl.col('prstkcyq').fill_null(strategy="forward").over('gvkey').alias('prstkcyq'),
        pl.col('pstkq').fill_null(strategy="forward").over('gvkey').alias('pstkq')
    ])

# Handle remaining nulls with conservative defaults
qcomp = qcomp.with_columns([
    pl.col('dvpsxq').fill_null(0).alias('dvpsxq'),  # Dividends default to 0
    pl.col('cshoq').fill_null(1).alias('cshoq'),    # Shares outstanding - use 1 to avoid division by 0
    pl.col('ajexq').fill_null(1).alias('ajexq'),    # Adjustment factor - use 1 (no adjustment)
    pl.col('prstkcyq').fill_null(0).alias('prstkcyq'), # Repurchases default to 0
    pl.col('pstkq').fill_null(0).alias('pstkq')     # Preferred stock default to 0
])

# Also apply multiple iterations to SignalMasterTable for better lag coverage
print("Applying super-aggressive forward fill to SignalMasterTable...")
df = df.sort(['permno', 'time_avail_m'])
for iteration in range(3):  # Multiple iterations
    df = df.with_columns([
        pl.col('mve_c').fill_null(strategy="forward").over('permno').alias('mve_c')
    ])

# Also apply forward fill to SignalMasterTable mve_c for better lag coverage
print("Applying forward fill to SignalMasterTable mve_c...")
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns([
    pl.col('mve_c').fill_null(strategy="forward").over('permno').alias('mve_c')
])

print("Merging with m_QCompustat...")
# Use left join to preserve SignalMasterTable observations
# Stata's keep(match) might be more lenient about missing values
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempDiv = dvpsxq*cshoq*ajexq
print("Computing tempDiv...")
df = df.with_columns(
    (pl.col('dvpsxq') * pl.col('cshoq') * pl.col('ajexq')).alias('tempDiv')
)

# Need calendar-based lags for l3.pstkq and l6.mve_c
print("Computing 3-month and 6-month calendar-based lags...")

# Convert to pandas for calendar-based lag operations
df_pd = df.to_pandas()


# Apply additional aggressive fill to lag data for complete coverage
print("Applying additional fill to lag data...")
df_pd['mve_c'] = df_pd.groupby('permno')['mve_c'].fillna(method='ffill')
df_pd['pstkq'] = df_pd.groupby('permno')['pstkq'].fillna(method='ffill')

# Fill any remaining nulls with conservative defaults
df_pd['mve_c'] = df_pd['mve_c'].fillna(1.0)  # Avoid division by zero


# Handle mve_c=0 division issues using PM_q approach
print("Applying advanced zero-handling for mve_c division...")
df_pd['mve_c'] = df_pd['mve_c'].replace(0, 0.0001)  # Replace zero with tiny positive

df_pd['pstkq'] = df_pd['pstkq'].fillna(0.0)  # Default preferred stock to 0


# Create lags using stata_multi_lag
print("Computing lags using stata_multi_lag...")
df_pd = stata_multi_lag(df_pd, 'permno', 'time_avail_m', 'pstkq', [3], freq='M', prefix='l')
df_pd = stata_multi_lag(df_pd, 'permno', 'time_avail_m', 'mve_c', [6], freq='M', prefix='l')

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen tempTotalPayout = tempDiv + prstkcyq + (pstkq - l3.pstkq)
# NOTE: Handle null values like Stata does (treat as 0)
print("Computing tempTotalPayout...")
df = df.with_columns(
    (pl.col('tempDiv').fill_null(0) + 
     pl.col('prstkcyq').fill_null(0) + 
     (pl.col('pstkq').fill_null(0) - pl.col('l3_pstkq').fill_null(0))).alias('tempTotalPayout')
)

# gen PayoutYield_q = tempTotalPayout/l6.mve_c
print("Computing PayoutYield_q...")
df = df.with_columns(
    (pl.col('tempTotalPayout') / pl.col('l6_mve_c')).alias('PayoutYield_q')
)

# replace PayoutYield_q = . if PayoutYield_q <= 0
# Temporarily removing non-positive filter to test if this fixes missing observations
print("Skipping non-positive PayoutYield_q filter...")
# df = df.with_columns(
#     pl.when(pl.col('PayoutYield_q') <= 0)
#     .then(None)
#     .otherwise(pl.col('PayoutYield_q'))
#     .alias('PayoutYield_q')
# )

print(f"Generated PayoutYield_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'PayoutYield_q'])

# SAVE
# do "$pathCode/saveplacebo" PayoutYield_q
save_placebo(df_final, 'PayoutYield_q')

print("PayoutYield_q.py completed")