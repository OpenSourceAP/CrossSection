# ABOUTME: DivYield.py - calculates dividend yield placebo (current)
# ABOUTME: Python equivalent of DivYield.do, translates line-by-line from Stata code

"""
DivYield.py

Inputs:
    - CRSPdistributions.parquet: permno, exdt, divamt columns
    - SignalMasterTable.parquet: permno, time_avail_m, mve_c, prc columns

Outputs:
    - DivYield.csv: permno, yyyymm, DivYield columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/DivYield.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting DivYield.py")

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
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen temp = divamt
# replace temp = 0 if divamt ==.
print("Computing temp...")
df = df.with_columns(
    pl.col('divamt').fill_null(0).alias('temp')
)

# Convert to pandas for lag operations (need many lags: l1 through l11)
df_pd = df.to_pandas()

# Create lags for temp
print("Computing multiple lags...")
for lag_months in range(1, 12):  # l1 through l11
    df_pd[f'time_lag{lag_months}'] = df_pd['time_avail_m'] - pd.DateOffset(months=lag_months)
    
    # Create lag data
    lag_data = df_pd[['permno', 'time_avail_m', 'temp']].copy()
    lag_data.columns = ['permno', f'time_lag{lag_months}', f'l{lag_months}_temp']
    
    # Merge lag data
    df_pd = df_pd.merge(lag_data, on=['permno', f'time_lag{lag_months}'], how='left')

# Drop lag date columns
lag_columns = [f'time_lag{i}' for i in range(1, 12)]
df_pd = df_pd.drop(columns=lag_columns)

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen tempdy = 4*max(temp, l1.temp, l2.temp)/abs(prc)
print("Computing tempdy...")
df = df.with_columns(
    (4 * pl.max_horizontal(['temp', 'l1_temp', 'l2_temp']) / pl.col('prc').abs()).alias('tempdy')
)

# Complex conditional for tempdypos - replace tempdypos = . if multiple conditions
# Fixed: In Stata, missing values in conditions evaluate to FALSE, not TRUE
# We need to explicitly check for non-null values before applying <= 0 conditions
print("Computing tempdypos...")
df = df.with_columns(
    pl.when(
        # Condition 1: All three values must be non-null AND <= 0
        ((pl.col('temp').is_not_null() & (pl.col('temp') <= 0)) & 
         (pl.col('l1_temp').is_not_null() & (pl.col('l1_temp') <= 0)) & 
         (pl.col('l2_temp').is_not_null() & (pl.col('l2_temp') <= 0))) |
        # Condition 2: All three values must be non-null AND <= 0
        ((pl.col('l3_temp').is_not_null() & (pl.col('l3_temp') <= 0)) & 
         (pl.col('l4_temp').is_not_null() & (pl.col('l4_temp') <= 0)) & 
         (pl.col('l5_temp').is_not_null() & (pl.col('l5_temp') <= 0))) |
        # Condition 3: All three values must be non-null AND <= 0
        ((pl.col('l6_temp').is_not_null() & (pl.col('l6_temp') <= 0)) & 
         (pl.col('l7_temp').is_not_null() & (pl.col('l7_temp') <= 0)) & 
         (pl.col('l8_temp').is_not_null() & (pl.col('l8_temp') <= 0))) |
        # Condition 4: All three values must be non-null AND <= 0
        ((pl.col('l9_temp').is_not_null() & (pl.col('l9_temp') <= 0)) & 
         (pl.col('l10_temp').is_not_null() & (pl.col('l10_temp') <= 0)) & 
         (pl.col('l11_temp').is_not_null() & (pl.col('l11_temp') <= 0)))
    )
    .then(None)
    .otherwise(pl.col('tempdy'))
    .alias('tempdypos')
)

# gen DivYield = tempdypos
print("Setting DivYield...")
df = df.with_columns(pl.col('tempdypos').alias('DivYield'))

# Convert to pandas for fastxtile
df_pd = df.to_pandas()

# egen tempsize = fastxtile(mve_c), by(time_avail_m) n(4)
print("Computing size quintiles...")
df_pd['tempsize'] = df_pd.groupby('time_avail_m')['mve_c'].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates='drop') + 1)

# Convert back to polars
df = pl.from_pandas(df_pd)

# replace DivYield = . if tempsize >= 3
print("Filtering by size...")
df = df.with_columns(
    pl.when(pl.col('tempsize') >= 3)
    .then(None)
    .otherwise(pl.col('DivYield'))
    .alias('DivYield')
)

print(f"Generated DivYield for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'DivYield'])

# SAVE
# do "$pathCode/saveplacebo" DivYield
save_placebo(df_final, 'DivYield')

print("DivYield.py completed")