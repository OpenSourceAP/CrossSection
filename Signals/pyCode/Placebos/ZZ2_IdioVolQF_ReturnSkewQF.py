# ABOUTME: ZZ2_IdioVolQF_ReturnSkewQF.py - calculates Q-factor idiosyncratic volatility and skewness
# ABOUTME: Python equivalent of ZZ2_IdioVolQF_ReturnSkewQF.do using daily CRSP and Q-factor data

"""
ZZ2_IdioVolQF_ReturnSkewQF.py - Q-Factor Idiosyncratic Volatility and Return Skewness

Replicates the Stata implementation:
1. Loads daily CRSP returns and daily Q-factor data
2. Subtracts Q-factor risk-free rate from returns
3. Runs monthly Q-factor regressions: ret_excess = alpha + beta1*r_mkt + beta2*r_me + beta3*r_ia + beta4*r_roe + residual
4. Calculates standard deviation and skewness of residuals by permno-month

Inputs:
    - dailyCRSP.parquet: permno, time_d, ret columns
    - d_qfactor.parquet: time_d, r_f_qfac, r_mkt_qfac, r_me_qfac, r_ia_qfac, r_roe_qfac columns

Outputs:
    - IdioVolQF.csv: permno, yyyymm, IdioVolQF columns
    - ReturnSkewQF.csv: permno, yyyymm, ReturnSkewQF columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ2_IdioVolQF_ReturnSkewQF.py
"""

import pandas as pd
import numpy as np
import polars as pl
import sys
import os
from sklearn.linear_model import LinearRegression
from scipy.stats import skew

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ZZ2_IdioVolQF_ReturnSkewQF.py")

# DATA LOAD - replicate Stata lines 3-6
print("Loading daily CRSP data...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
print(f"Loaded {len(daily_crsp):,} daily CRSP rows")

print("Loading daily Q-factor data...")
try:
    daily_qf = pl.read_parquet("../pyData/Intermediate/d_qfactor.parquet")
    print(f"Loaded {len(daily_qf):,} daily Q-factor rows")
except:
    print("WARNING: d_qfactor.parquet not found, creating empty results")
    df_vol = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime),
        'IdioVolQF': pl.Series([], dtype=pl.Float64)
    })
    
    df_skew = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime),
        'ReturnSkewQF': pl.Series([], dtype=pl.Float64)
    })
    
    save_placebo(df_vol, 'IdioVolQF')
    save_placebo(df_skew, 'ReturnSkewQF')
    print("Generated 0 observations (missing Q-factor data)")
    print("ZZ2_IdioVolQF_ReturnSkewQF.py completed (NO DATA)")
    exit()

# Merge daily data - replicate Stata line 4
print("Merging CRSP with Q-factor data...")
df = daily_crsp.join(daily_qf, on='time_d', how='left')  # Keep master match
print(f"After merge: {len(df):,} rows")

# Calculate excess returns - replicate Stata line 5
print("Calculating excess returns...")
df = df.with_columns([
    (pl.col('ret') - pl.col('r_f_qfac')).alias('ret_excess')
])

# Create time_avail_m - replicate Stata lines 12-13
print("Creating monthly time variable...")
df = df.with_columns([
    pl.col('time_d').dt.truncate('1mo').alias('time_avail_m')
])

# Convert to pandas for regression processing
print("Converting to pandas for regression processing...")
df_pandas = df.select([
    'permno', 'time_avail_m', 'ret_excess', 
    'r_mkt_qfac', 'r_me_qfac', 'r_ia_qfac', 'r_roe_qfac'
]).to_pandas()

# Filter out rows with missing factor data
df_pandas = df_pandas.dropna(subset=['r_mkt_qfac', 'r_me_qfac', 'r_ia_qfac', 'r_roe_qfac'])
print(f"After removing missing factor data: {len(df_pandas):,} rows")

# Q-factor regressions by permno-month - replicate Stata line 16
print("Running monthly Q-factor regressions...")
results = []
total_groups = len(df_pandas.groupby(['permno', 'time_avail_m']))
processed = 0

for (permno, time_avail_m), group in df_pandas.groupby(['permno', 'time_avail_m']):
    processed += 1
    if processed % 10000 == 0:
        print(f"  Processed {processed:,} / {total_groups:,} groups ({processed/total_groups*100:.1f}%)")
    
    # Need at least 10 observations for meaningful 4-factor regression
    if len(group) >= 10:
        # Drop any remaining NaNs
        group_clean = group.dropna(subset=['ret_excess', 'r_mkt_qfac', 'r_me_qfac', 'r_ia_qfac', 'r_roe_qfac'])
        
        if len(group_clean) >= 10:
            try:
                # Prepare regression data
                y = group_clean['ret_excess'].values
                X = group_clean[['r_mkt_qfac', 'r_me_qfac', 'r_ia_qfac', 'r_roe_qfac']].values
                
                # Run Q-factor regression: ret_excess = alpha + beta1*r_mkt + beta2*r_me + beta3*r_ia + beta4*r_roe + residual
                reg = LinearRegression().fit(X, y)
                residuals = y - reg.predict(X)
                
                # Calculate standard deviation and skewness of residuals
                if len(residuals) >= 3:  # Need at least 3 observations for skewness
                    idio_vol = np.std(residuals, ddof=1)  # Sample standard deviation
                    return_skew = skew(residuals)  # Skewness
                    
                    results.append({
                        'permno': int(permno),
                        'time_avail_m': time_avail_m,
                        'IdioVolQF': idio_vol,
                        'ReturnSkewQF': return_skew,
                        'n_obs': len(residuals)
                    })
            except Exception as e:
                # Skip groups with regression issues
                pass

print(f"\nCompleted regressions: {len(results):,} permno-month groups")

# Convert results to DataFrames
if len(results) > 0:
    results_df = pd.DataFrame(results)
    
    # Create separate DataFrames for each placebo
    df_vol = pl.from_pandas(results_df[['permno', 'time_avail_m', 'IdioVolQF']])
    df_skew = pl.from_pandas(results_df[['permno', 'time_avail_m', 'ReturnSkewQF']])
    
else:
    # Empty results
    df_vol = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime),
        'IdioVolQF': pl.Series([], dtype=pl.Float64)
    })
    
    df_skew = pl.DataFrame({
        'permno': pl.Series([], dtype=pl.Int64),
        'time_avail_m': pl.Series([], dtype=pl.Datetime),
        'ReturnSkewQF': pl.Series([], dtype=pl.Float64)
    })

# SAVE - replicate Stata lines 27-28
save_placebo(df_vol, 'IdioVolQF')
save_placebo(df_skew, 'ReturnSkewQF')

print(f"Generated {len(df_vol):,} IdioVolQF observations")
print(f"Generated {len(df_skew):,} ReturnSkewQF observations")
print("ZZ2_IdioVolQF_ReturnSkewQF.py completed")