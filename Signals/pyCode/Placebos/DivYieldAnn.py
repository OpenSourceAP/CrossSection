# ABOUTME: DivYieldAnn.py - calculates annual dividend yield placebo
# ABOUTME: Python equivalent of DivYieldAnn.do, translates line-by-line from Stata code

"""
DivYieldAnn.py

Inputs:
    - CRSPdistributions.parquet: permno, exdt, divamt columns
    - SignalMasterTable.parquet: permno, time_avail_m, mve_c, prc columns

Outputs:
    - DivYieldAnn.csv: permno, yyyymm, DivYieldAnn columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/DivYieldAnn.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting DivYieldAnn.py")

# PREP DISTRIBUTIONS DATA
# use "$pathDataIntermediate/CRSPdistributions", clear
print("Loading CRSPdistributions...")
crsp_dist = pl.read_parquet("../pyData/Intermediate/CRSPdistributions.parquet")
crsp_dist = crsp_dist.select(['permno', 'exdt', 'divamt'])

print(f"After loading distributions: {len(crsp_dist)} rows")

# gen time_avail_m = mofd(exdt)
print("Converting exdt to time_avail_m...")
crsp_dist = crsp_dist.with_columns(
    pl.col('exdt').dt.truncate('1mo').alias('time_avail_m')
)

# drop if time_avail_m == . | divamt == .
print("Filtering for non-null dates and divamt...")
crsp_dist = crsp_dist.filter(
    pl.col('time_avail_m').is_not_null() & pl.col('divamt').is_not_null()
)

print(f"After filtering: {len(crsp_dist)} rows")

# gcollapse (sum) divamt, by(permno time_avail_m)
print("Collapsing dividends by permno-time_avail_m...")
tempdivamt = crsp_dist.group_by(['permno', 'time_avail_m']).agg(
    pl.col('divamt').sum()
)

print(f"After collapse: {len(tempdivamt)} rows")

# DATA LOAD
# use permno time_avail_m mve_c prc using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'time_avail_m', 'mve_c', 'prc'])

print(f"After loading SignalMasterTable: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(divamt)
print("Merging with dividend data...")
df = df.join(tempdivamt, on=['permno', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for rolling operations...")
df = df.sort(['permno', 'time_avail_m'])

# replace divamt = 0 if divamt ==.
print("Replacing missing divamt with 0...")
df = df.with_columns(pl.col('divamt').fill_null(0))

# Convert to pandas for rolling window operations
df_pd = df.to_pandas()

# asrol divamt, gen(divann) by(permno) stat(sum) window(time_avail_m 12) min(6)
print("Computing rolling 12-month dividend sum...")
df_pd = df_pd.set_index(['permno', 'time_avail_m']).sort_index()
df_pd['divann'] = df_pd.groupby('permno')['divamt'].rolling(window=12, min_periods=6).sum().reset_index(level=0, drop=True)
df_pd = df_pd.reset_index()

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen DivYieldAnn = divann/abs(prc)
print("Computing DivYieldAnn...")
df = df.with_columns(
    (pl.col('divann') / pl.col('prc').abs()).alias('DivYieldAnn')
)

print(f"Generated DivYieldAnn for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'DivYieldAnn'])

# SAVE
# do "$pathCode/saveplacebo" DivYieldAnn
save_placebo(df_final, 'DivYieldAnn')

print("DivYieldAnn.py completed")