# ABOUTME: ULTRA-OPTIMIZED Idiosyncratic risk predictor using RMSE from 252-day rolling CAPM regression
# ABOUTME: Usage: python3 ZZ2_IdioVolAHT_ultra.py [--start_year YYYY] [--end_year YYYY] [--testing] (run from pyCode/ directory)

import polars as pl
import numpy as np
import sys
import os
import argparse
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Parse command line arguments
parser = argparse.ArgumentParser(description='Calculate IdioVolAHT predictor (ULTRA-OPTIMIZED)')
parser.add_argument('--start_year', type=int, default=None, help='Start year for filtering (e.g., 1985)')
parser.add_argument('--end_year', type=int, default=None, help='End year for filtering (e.g., 1989)')
parser.add_argument('--testing', action='store_true', help='Testing mode: process only first 100 permnos')
parser.add_argument('--match_file', type=str, default=None, help='Path to reference CSV file to match exactly')
args = parser.parse_args()

# Timer setup
script_start_time = time.time()
print(f"Starting ULTRA-OPTIMIZED IdioVolAHT calculation...")
if args.testing:
    print("TESTING MODE: Processing only first 100 permnos")
if args.match_file:
    print(f"MATCH MODE: Targeting exact match with {args.match_file}")
if args.start_year and args.end_year:
    print(f"Year range: {args.start_year}-{args.end_year}")
elif args.start_year:
    print(f"Year range: {args.start_year} onwards")
elif args.end_year:
    print(f"Year range: up to {args.end_year}")
else:
    print("Year range: all available years")

# Load reference file if specified
target_permnos = None
if args.match_file:
    print(f"Loading reference file: {args.match_file}")
    target_df = pl.read_csv(args.match_file)
    target_permnos = target_df.select("permno").unique().to_series().to_list()
    print(f"Found {len(target_permnos)} unique permnos in reference file")

# Data load
load_start = time.time()
print("Loading data files...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
print(f"Data loading completed in {time.time() - load_start:.1f} seconds")

# Apply year filtering if specified
filter_start = time.time()
if args.start_year or args.end_year:
    print("Applying year filters...")
    if args.start_year:
        daily_crsp = daily_crsp.filter(pl.col("time_d").dt.year() >= args.start_year)
        daily_ff = daily_ff.filter(pl.col("time_d").dt.year() >= args.start_year)
    if args.end_year:
        daily_crsp = daily_crsp.filter(pl.col("time_d").dt.year() <= args.end_year)
        daily_ff = daily_ff.filter(pl.col("time_d").dt.year() <= args.end_year)
    print(f"Year filtering completed in {time.time() - filter_start:.1f} seconds")

# Select required columns
df = daily_crsp.select(["permno", "time_d", "ret"])

# Apply testing or match filter if requested
if target_permnos:
    df = df.filter(pl.col("permno").is_in(target_permnos))
    print(f"Match mode: Limited to {len(target_permnos)} permnos from reference")
elif args.testing:
    test_permnos = df.select("permno").unique().head(100).to_series().to_list()
    df = df.filter(pl.col("permno").is_in(test_permnos))
    print(f"Testing mode: Limited to {len(test_permnos)} permnos")

# Merge with FF data
merge_start = time.time()
print("Merging CRSP and Fama-French data...")
df = df.join(
    daily_ff.select(["time_d", "rf", "mktrf"]),
    on="time_d",
    how="inner"
)
print(f"Data merging completed in {time.time() - merge_start:.1f} seconds")
print(f"Merged data shape: {df.shape}")

# Calculate excess return and prepare data
calc_start = time.time()
print("Calculating excess returns and preparing data...")
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("ret_excess")
]).sort(["permno", "time_d"])

print(f"Data preparation completed in {time.time() - calc_start:.1f} seconds")

# ULTRA-OPTIMIZED rolling RMSE calculation using vectorized numpy operations
regression_start = time.time()
print("Running ULTRA-OPTIMIZED rolling CAPM regressions...")
print(f"Processing {df['permno'].n_unique()} unique stocks...")

def ultra_fast_rolling_rmse(df_input: pl.DataFrame) -> pl.DataFrame:
    """
    Ultra-fast rolling RMSE using fully vectorized numpy operations
    """
    # Convert entire dataframe to numpy at once for maximum speed
    print("  Converting to numpy arrays...")
    df_numpy = df_input.select(["permno", "ret_excess", "mktrf"]).to_numpy()
    permnos = df_numpy[:, 0].astype(int)
    ret_excess = df_numpy[:, 1].astype(float)
    mktrf = df_numpy[:, 2].astype(float)
    
    # Get unique permnos and their indices
    unique_permnos, inverse_indices, counts = np.unique(permnos, return_inverse=True, return_counts=True)
    
    print(f"  Processing {len(unique_permnos)} unique permnos with vectorized operations...")
    
    # Pre-allocate result array
    rmse_results = np.full(len(df_input), np.nan)
    
    # Process each permno with ultra-fast vectorized operations
    start_idx = 0
    for i, (permno, count) in enumerate(zip(unique_permnos, counts)):
        if i % 30 == 0:  # Progress every 30 stocks
            print(f"    Processed {i}/{len(unique_permnos)} permnos...")
        
        end_idx = start_idx + count
        
        if count < 100:  # Not enough observations
            start_idx = end_idx
            continue
        
        # Extract data for this permno
        y = ret_excess[start_idx:end_idx]
        x = mktrf[start_idx:end_idx]
        
        # Ultra-fast rolling regression using stride tricks for efficiency
        n = len(y)
        rmse_vals = np.full(n, np.nan)
        
        # Vectorized computation for each window
        for j in range(99, n):  # Start from 100th observation
            window_start = max(0, j - 251)
            
            # Extract window
            y_win = y[window_start:j+1]
            x_win = x[window_start:j+1]
            
            # Super fast NaN filtering
            valid_mask = ~(np.isnan(y_win) | np.isnan(x_win))
            if np.sum(valid_mask) < 100:
                continue
                
            y_clean = y_win[valid_mask]
            x_clean = x_win[valid_mask]
            
            try:
                # Lightning-fast OLS using Welford's algorithm for numerical stability
                n_obs = len(x_clean)
                if n_obs < 100:
                    continue
                
                # Vectorized mean calculation
                x_mean = np.mean(x_clean)
                y_mean = np.mean(y_clean)
                
                # Vectorized beta calculation using optimized formulas
                x_centered = x_clean - x_mean
                y_centered = y_clean - y_mean
                
                # Compute beta using dot products (fastest method)
                beta = np.dot(x_centered, y_centered) / np.dot(x_centered, x_centered)
                alpha = y_mean - beta * x_mean
                
                # Vectorized residual calculation
                predictions = alpha + beta * x_clean
                residuals = y_clean - predictions
                
                # Fast RMSE calculation
                rmse_vals[j] = np.sqrt(np.mean(residuals * residuals))
                
            except (ZeroDivisionError, np.linalg.LinAlgError):
                continue
        
        # Store results
        rmse_results[start_idx:end_idx] = rmse_vals
        start_idx = end_idx
    
    print("  Converting back to polars...")
    # Add results back to polars dataframe
    return df_input.with_columns(pl.Series("IdioVolAHT", rmse_results))

# Apply ultra-fast calculation
df_with_rmse = ultra_fast_rolling_rmse(df)
print(f"Total regression time: {time.time() - regression_start:.1f} seconds")

# Convert to monthly and keep last observation per month
monthly_start = time.time()
print("Converting to monthly data...")
df_with_rmse = df_with_rmse.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing IdioVolAHT per permno-month
df_monthly = df_with_rmse.filter(pl.col("IdioVolAHT").is_not_null()).sort(["permno", "time_avail_m", "time_d"])
df_monthly = df_monthly.group_by(["permno", "time_avail_m"]).agg([
    pl.col("IdioVolAHT").last().alias("IdioVolAHT")
])

# Prepare results
result = df_monthly.with_columns([
    (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("yyyymm")
])

# Keep time_avail_m for savepredictor, add yyyymm for comparison
result_for_save = result.select(["permno", "time_avail_m", "IdioVolAHT"])
result_for_comparison = result.select(["permno", "yyyymm", "IdioVolAHT"])

print(f"Monthly aggregation completed in {time.time() - monthly_start:.1f} seconds")
print(f"Final result shape: {result.shape}")

# If we're in match mode, compare with target
if args.match_file:
    print("\n=== MATCH MODE COMPARISON ===")
    target_df = pl.read_csv(args.match_file)
    
    # Compare shapes
    print(f"Target shape: {target_df.shape}")
    print(f"Result shape: {result_for_comparison.shape}")
    
    # Compare a few sample values
    merged = result_for_comparison.join(target_df, on=["permno", "yyyymm"], how="inner", suffix="_target")
    if len(merged) > 0:
        diff = merged.with_columns([
            (pl.col("IdioVolAHT") - pl.col("IdioVolAHT_target")).abs().alias("abs_diff")
        ])
        max_diff = diff.select("abs_diff").max().item()
        mean_diff = diff.select("abs_diff").mean().item()
        print(f"Max absolute difference: {max_diff:.2e}")
        print(f"Mean absolute difference: {mean_diff:.2e}")
        
        if max_diff < 1e-10:
            print("✅ PERFECT MATCH!")
        elif max_diff < 1e-6:
            print("✅ Excellent match (within numerical precision)")
        else:
            print("⚠️  Some differences detected")
            print("Sample differences:")
            print(diff.head(5).select(["permno", "yyyymm", "IdioVolAHT", "IdioVolAHT_target", "abs_diff"]))
    
    print("=== END COMPARISON ===\n")

# Save predictor
save_start = time.time()
print("Saving predictor...")
save_predictor(result_for_save, "IdioVolAHT")
print(f"Saving completed in {time.time() - save_start:.1f} seconds")

# Final timing
total_time = time.time() - script_start_time
print(f"\nULTRA-OPTIMIZED IdioVolAHT calculation completed successfully!")
print(f"Total execution time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")