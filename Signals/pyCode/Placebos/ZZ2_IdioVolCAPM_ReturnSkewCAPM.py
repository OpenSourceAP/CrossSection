# ABOUTME: ZZ2_IdioVolCAPM_ReturnSkewCAPM.py - calculates CAPM idiosyncratic volatility and skewness placebos
# ABOUTME: Python equivalent of ZZ2_IdioVolCAPM_ReturnSkewCAPM.do, translates line-by-line from Stata code

import pandas as pd
import numpy as np
import polars as pl
import sys
import os
from scipy.stats import skew

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_regress import asreg

print("Starting ZZ2_IdioVolCAPM_ReturnSkewCAPM.py")

# DATA LOAD
# use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
print("Loading dailyCRSP...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")

# merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
print("Loading dailyFF...")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")

print("Merging with dailyFF...")
# keep(match) means inner join
df = daily_crsp.join(daily_ff, on='time_d', how='inner')

print(f"After merge: {len(df)} rows")

# replace ret = ret - rf
print("Computing excess returns...")
df = df.with_columns([
    (pl.col('ret') - pl.col('rf')).alias('ret')
])

# drop rf
df = df.drop('rf')

# SIGNAL CONSTRUCTION
# sort permno time_d
print("Sorting by permno time_d...")
df = df.sort(['permno', 'time_d'])

# create time_avail_m that is just the year-month of each year-day
# gen time_avail_m = mofd(time_d)
print("Creating time_avail_m...")
df = df.with_columns([
    pl.col('time_d').dt.truncate('1mo').alias('time_avail_m')
])

# Convert to pandas for asreg processing
print("Converting to pandas for asreg processing...")
df_pandas = df.to_pandas()

# get CAPM residuals within each month
# bys permno time_avail_m: asreg ret mktrf, fit
print("Running CAPM regressions by permno-month using asreg...")
df_pandas = asreg(
    df_pandas, 
    y='ret', 
    X='mktrf',
    by=['permno', 'time_avail_m'], 
    min_obs=3,  # Reduce minimum to match Stata behavior
    add_constant=True
)

print(f"After asreg: {len(df_pandas)} rows")

# collapse into second and third moments
# gcollapse (sd) IdioVolCAPM = _residuals (skewness) ReturnSkewCAPM = _residuals, by(permno time_avail_m)
print("Calculating moments of residuals...")

# Filter to observations that have valid residuals
df_with_residuals = df_pandas[df_pandas['_residuals'].notna()].copy()
print(f"Observations with valid residuals: {len(df_with_residuals)}")

# Group by permno-month and calculate moments
results = []
groups = df_with_residuals.groupby(['permno', 'time_avail_m'])

print(f"Processing {len(groups):,} permno-month groups for moment calculation...")

for (permno, time_avail_m), group in groups:
    residuals = group['_residuals'].values
    
    # Calculate standard deviation and skewness
    if len(residuals) >= 1:  # At least 1 observation for std
        idio_vol = np.std(residuals, ddof=1) if len(residuals) > 1 else 0.0
        
        # For skewness, need at least 3 observations
        if len(residuals) >= 3:
            try:
                return_skew = skew(residuals, nan_policy='omit')
                # Handle NaN skewness by setting to 0 or keeping as NaN based on Stata behavior
                if np.isnan(return_skew):
                    return_skew = 0.0  # Or could be NaN depending on Stata handling
            except:
                return_skew = 0.0
        else:
            return_skew = np.nan if len(residuals) < 3 else 0.0
        
        results.append({
            'permno': int(permno),
            'time_avail_m': time_avail_m,
            'IdioVolCAPM': idio_vol,
            'ReturnSkewCAPM': return_skew
        })

# Convert results to DataFrames
if len(results) > 0:
    results_df = pd.DataFrame(results)
    
    # Create separate DataFrames for each placebo
    df_vol = pl.from_pandas(results_df[['permno', 'time_avail_m', 'IdioVolCAPM']])
    df_skew = pl.from_pandas(results_df[['permno', 'time_avail_m', 'ReturnSkewCAPM']])
    
else:
    print("ERROR: No results generated!")
    # Create empty DataFrames
    df_vol = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime),
        'IdioVolCAPM': pl.Series([], dtype=pl.Float64)
    })
    
    df_skew = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime),
        'ReturnSkewCAPM': pl.Series([], dtype=pl.Float64)
    })

print(f"Generated {len(results):,} total results")

# SAVE
# do "$pathCode/saveplacebo" IdioVolCAPM
save_placebo(df_vol, 'IdioVolCAPM')
# do "$pathCode/saveplacebo" ReturnSkewCAPM  
save_placebo(df_skew, 'ReturnSkewCAPM')

print(f"Generated {len(df_vol):,} IdioVolCAPM observations")
print(f"Generated {len(df_skew):,} ReturnSkewCAPM observations")
print("ZZ2_IdioVolCAPM_ReturnSkewCAPM.py completed")