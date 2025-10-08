# ABOUTME: ZZ2_IdioVolCAPM_ReturnSkewCAPM.py - calculates idiosyncratic volatility and skewness from CAPM
# ABOUTME: Python equivalent of ZZ2_IdioVolCAPM_ReturnSkewCAPM.do using daily CRSP and FF data

"""
ZZ2_IdioVolCAPM_ReturnSkewCAPM.py - CAPM Idiosyncratic Volatility and Return Skewness

Replicates the Stata implementation:
1. Loads daily CRSP returns and daily Fama-French factors 
2. Subtracts risk-free rate from returns
3. Runs monthly CAPM regressions: ret_excess = alpha + beta * mktrf + residual
4. Calculates standard deviation and skewness of residuals by permno-month

Inputs:
    - dailyCRSP.parquet: permno, time_d, ret columns
    - dailyFF.parquet: time_d, rf, mktrf columns

Outputs:
    - IdioVolCAPM.csv: permno, yyyymm, IdioVolCAPM columns
    - ReturnSkewCAPM.csv: permno, yyyymm, ReturnSkewCAPM columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ2_IdioVolCAPM_ReturnSkewCAPM.py
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

print("Starting ZZ2_IdioVolCAPM_ReturnSkewCAPM.py")

# DATA LOAD - replicate Stata lines 3-6
print("Loading daily CRSP data...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
print(f"Loaded {len(daily_crsp):,} daily CRSP rows")

print("Loading daily Fama-French factors...")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
print(f"Loaded {len(daily_ff):,} daily FF rows")

# Merge daily data - replicate Stata line 4
print("Merging CRSP with Fama-French factors...")
df = daily_crsp.join(daily_ff, on='time_d', how='inner')
print(f"After merge: {len(df):,} rows")

# Calculate excess returns - replicate Stata line 5
print("Calculating excess returns...")
df = df.with_columns([
    (pl.col('ret') - pl.col('rf')).alias('ret_excess')
])

# Create time_avail_m - replicate Stata lines 12-13
print("Creating monthly time variable...")
df = df.with_columns([
    pl.col('time_d').dt.truncate('1mo').alias('time_avail_m')
])

# Convert to pandas for regression processing
print("Converting to pandas for regression processing...")
df_pandas = df.select(['permno', 'time_avail_m', 'ret_excess', 'mktrf']).to_pandas()

# CAPM regressions by permno-month - replicate Stata line 16
print("Running monthly CAPM regressions...")
results = []
total_groups = len(df_pandas.groupby(['permno', 'time_avail_m']))
processed = 0

for (permno, time_avail_m), group in df_pandas.groupby(['permno', 'time_avail_m']):
    processed += 1
    if processed % 10000 == 0:
        print(f"  Processed {processed:,} / {total_groups:,} groups ({processed/total_groups*100:.1f}%)")
    
    # Need at least 10 observations for meaningful regression
    if len(group) >= 10 and group['mktrf'].notna().sum() >= 10 and group['ret_excess'].notna().sum() >= 10:
        y = group['ret_excess'].dropna()
        X = group['mktrf'].dropna()
        
        # Align y and X
        common_idx = y.index.intersection(X.index)
        if len(common_idx) >= 10:
            y_aligned = y.loc[common_idx]
            X_aligned = X.loc[common_idx].values.reshape(-1, 1)
            
            try:
                # Run CAPM regression: ret_excess = alpha + beta * mktrf + residual
                reg = LinearRegression().fit(X_aligned, y_aligned)
                residuals = y_aligned - reg.predict(X_aligned)
                
                # Calculate standard deviation and skewness of residuals
                if len(residuals) >= 3:  # Need at least 3 observations for skewness
                    idio_vol = np.std(residuals, ddof=1)  # Sample standard deviation
                    return_skew = skew(residuals)  # Skewness
                    
                    results.append({
                        'permno': int(permno),
                        'time_avail_m': time_avail_m,
                        'IdioVolCAPM': idio_vol,
                        'ReturnSkewCAPM': return_skew,
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
    df_vol = pl.from_pandas(results_df[['permno', 'time_avail_m', 'IdioVolCAPM']])
    df_skew = pl.from_pandas(results_df[['permno', 'time_avail_m', 'ReturnSkewCAPM']])
    
else:
    # Empty results
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

# SAVE - replicate Stata lines 26-27
save_placebo(df_vol, 'IdioVolCAPM')
save_placebo(df_skew, 'ReturnSkewCAPM')

print(f"Generated {len(df_vol):,} IdioVolCAPM observations")
print(f"Generated {len(df_skew):,} ReturnSkewCAPM observations")
print("ZZ2_IdioVolCAPM_ReturnSkewCAPM.py completed")