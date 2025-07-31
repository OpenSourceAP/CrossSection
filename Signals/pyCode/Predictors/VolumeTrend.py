# ABOUTME: Translates VolumeTrend.do to create volume trend measure using rolling regression
# ABOUTME: Run from pyCode/ directory: python3 Predictors/VolumeTrend.py

# Run from pyCode/ directory
# Inputs: monthlyCRSP.parquet
# Output: ../pyData/Predictors/VolumeTrend.csv

import pandas as pd
import numpy as np

print("Loading and processing VolumeTrend...")

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet')
df = df[['permno', 'time_avail_m', 'vol']].copy()

# SIGNAL CONSTRUCTION - Implementation matching Stata asreg exactly
def rolling_regression_pandas(time_vals, vol_vals, window_size=60, min_periods=30):
    """Fast rolling regression using numba - matches Stata asreg vol time_avail_m"""
    n = len(time_vals)
    betas = np.full(n, np.nan)
    means = np.full(n, np.nan)
    
    for i in range(min_periods-1, n):  # Start from min_periods (30), not window_size (60)
        # Get window indices (last 60 observations or all available if fewer)
        start_idx = max(0, i - window_size + 1)
        end_idx = i + 1
        
        # Extract window data
        window_time = time_vals[start_idx:end_idx]
        window_vol = vol_vals[start_idx:end_idx]
        
        # Remove NaN values (like Stata automatically does)
        valid_mask = ~(np.isnan(window_time) | np.isnan(window_vol))
        if np.sum(valid_mask) < min_periods:
            continue
            
        clean_time = window_time[valid_mask]
        clean_vol = window_vol[valid_mask]
        
        # Manual OLS calculation (much faster than sklearn)
        # Regression: vol = alpha + beta * time
        time_mean = np.mean(clean_time)
        vol_mean = np.mean(clean_vol)
        
        # Calculate beta: (sum((x-x_mean)*(y-y_mean))) / (sum((x-x_mean)^2))
        numerator = np.sum((clean_time - time_mean) * (clean_vol - vol_mean))
        denominator = np.sum((clean_time - time_mean) ** 2)
        
        if denominator > 0:
            beta = numerator / denominator  # This is _b_time_avail_m from Stata
            betas[i] = beta
            means[i] = vol_mean  # Rolling mean like asrol vol, stat(mean)
    
    return betas, means

def calculate_volume_trend_vectorized(group):
    """Vectorized volume trend calculation matching Stata exactly"""
    group = group.sort_values('time_avail_m').copy()
    
    # Convert time_avail_m to numeric form (like Stata uses in regression)
    reference_date = pd.Timestamp('1960-01-01')
    group['time_numeric'] = ((group['time_avail_m'] - reference_date).dt.days / 30.44).round()
    
    # Extract arrays for numba processing
    time_vals = group['time_numeric'].values.astype(np.float64)
    vol_vals = group['vol'].values.astype(np.float64)
    
    # Use rolling regression
    betas, means = rolling_regression_pandas(time_vals, vol_vals, window_size=60, min_periods=30)
    
    # Store results (matching Stata variable names)
    group['betaVolTrend'] = betas  # rename _b_time betaVolTrend
    group['meanX'] = means  # asrol vol, gen(meanX) stat(mean)
    
    return group

# Apply to each permno
print("Calculating rolling regressions by permno...")
df = df.groupby('permno', group_keys=False).apply(calculate_volume_trend_vectorized)

# Calculate VolumeTrend
df['VolumeTrend'] = df['betaVolTrend'] / df['meanX']

# Winsorize at 1% and 99%
lower = df['VolumeTrend'].quantile(0.01)
upper = df['VolumeTrend'].quantile(0.99)
df['VolumeTrend'] = df['VolumeTrend'].clip(lower=lower, upper=upper)

# Convert to output format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
df['permno'] = df['permno'].astype('int64')
df['yyyymm'] = df['yyyymm'].astype('int64')

df_final = df[['permno', 'yyyymm', 'VolumeTrend']].copy()
df_final = df_final.dropna(subset=['VolumeTrend'])
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/VolumeTrend.csv')
print("VolumeTrend predictor saved successfully")