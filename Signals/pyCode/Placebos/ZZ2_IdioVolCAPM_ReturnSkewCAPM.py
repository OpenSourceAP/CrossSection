# ABOUTME: ZZ2_IdioVolCAPM_ReturnSkewCAPM_fixed.py - Chunked processing for CAPM idiosyncratic volatility and skewness
# ABOUTME: Efficient implementation using chunked daily data processing to handle 107M+ rows

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

print("Starting ZZ2_IdioVolCAPM_ReturnSkewCAPM.py (CHUNKED PROCESSING)")

# Load daily Fama-French factors first (small dataset)
print("Loading daily Fama-French factors...")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
print(f"Loaded {len(daily_ff):,} daily FF rows")

# Process daily CRSP in chunks to handle 107M+ rows
print("Loading daily CRSP in chunks...")
chunk_size = 5000000  # 5M rows per chunk
results = []

# Read CRSP data in chunks
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
total_rows = len(daily_crsp)
print(f"Total daily CRSP rows: {total_rows:,}")

# Process in chunks
n_chunks = (total_rows + chunk_size - 1) // chunk_size
print(f"Processing in {n_chunks} chunks of {chunk_size:,} rows each")

for chunk_i in range(n_chunks):
    start_idx = chunk_i * chunk_size
    end_idx = min((chunk_i + 1) * chunk_size, total_rows)
    
    print(f"\nProcessing chunk {chunk_i + 1}/{n_chunks} (rows {start_idx:,} to {end_idx:,})")
    
    # Get chunk of daily CRSP data
    chunk = daily_crsp.slice(start_idx, end_idx - start_idx)
    print(f"  Chunk size: {len(chunk):,} rows")
    
    # Merge with Fama-French factors
    chunk = chunk.join(daily_ff, on='time_d', how='inner')
    
    if len(chunk) == 0:
        print(f"  No data after FF merge, skipping chunk")
        continue
    
    # Calculate excess returns
    chunk = chunk.with_columns([
        (pl.col('ret') - pl.col('rf')).alias('ret_excess')
    ])
    
    # Create monthly time variable
    chunk = chunk.with_columns([
        pl.col('time_d').dt.truncate('1mo').alias('time_avail_m')
    ])
    
    # Convert to pandas for regression processing
    chunk_pandas = chunk.select(['permno', 'time_avail_m', 'ret_excess', 'mktrf']).to_pandas()
    chunk_pandas = chunk_pandas.dropna()
    
    if len(chunk_pandas) == 0:
        print(f"  No data after cleaning, skipping chunk")
        continue
    
    # Group by permno-month and run regressions
    chunk_results = []
    groups = chunk_pandas.groupby(['permno', 'time_avail_m'])
    
    print(f"  Processing {len(groups):,} permno-month groups...")
    
    for (permno, time_avail_m), group in groups:
        # Need at least 10 observations for meaningful regression
        if len(group) >= 10:
            try:
                y = group['ret_excess'].values
                X = group['mktrf'].values.reshape(-1, 1)
                
                # Run CAPM regression
                reg = LinearRegression().fit(X, y)
                residuals = y - reg.predict(X)
                
                # Calculate standard deviation and skewness of residuals
                if len(residuals) >= 3:
                    idio_vol = np.std(residuals, ddof=1)
                    return_skew = skew(residuals)
                    
                    chunk_results.append({
                        'permno': int(permno),
                        'time_avail_m': time_avail_m,
                        'IdioVolCAPM': idio_vol,
                        'ReturnSkewCAPM': return_skew
                    })
            except:
                # Skip groups with regression issues
                pass
    
    print(f"  Generated {len(chunk_results):,} results from chunk")
    results.extend(chunk_results)

print(f"\nCompleted processing all chunks: {len(results):,} total results")

# Convert results to DataFrames
if len(results) > 0:
    results_df = pd.DataFrame(results)
    
    # Create separate DataFrames for each placebo
    df_vol = pl.from_pandas(results_df[['permno', 'time_avail_m', 'IdioVolCAPM']])
    df_skew = pl.from_pandas(results_df[['permno', 'time_avail_m', 'ReturnSkewCAPM']])
    
else:
    print("ERROR: No results generated!")
    # Create empty DataFrames rather than placeholders
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

# SAVE
save_placebo(df_vol, 'IdioVolCAPM')
save_placebo(df_skew, 'ReturnSkewCAPM')

print(f"Generated {len(df_vol):,} IdioVolCAPM observations")
print(f"Generated {len(df_skew):,} ReturnSkewCAPM observations")
print("ZZ2_IdioVolCAPM_ReturnSkewCAPM.py completed")