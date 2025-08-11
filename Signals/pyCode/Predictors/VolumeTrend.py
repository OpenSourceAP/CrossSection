# ABOUTME: Translates VolumeTrend.do to create volume trend measure using time-based rolling regression
# ABOUTME: Run from pyCode/ directory: python3 Predictors/VolumeTrend.py

# Run from pyCode/ directory
# Inputs: monthlyCRSP.parquet
# Output: ../pyData/Predictors/VolumeTrend.csv

import polars as pl
import numpy as np

print("Loading and processing VolumeTrend...")

# DATA LOAD
df = pl.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet')
df = df.select(['permno', 'time_avail_m', 'vol'])

# SIGNAL CONSTRUCTION - Time-based rolling regression
print("Calculating time-based rolling regressions by permno...")

# Sort data first
df = df.sort(['permno', 'time_avail_m'])

# Convert time_avail_m to numeric form for regression (months since 1960-01, Stata format)
df = df.with_columns([
    ((pl.col('time_avail_m').dt.year() - 1960) * 12 + pl.col('time_avail_m').dt.month() - 1).alias('time_numeric')
])

def time_based_rolling_regression(group_df):
    """
    Implement time-based rolling regression matching Stata:
    asreg vol time_avail_m, window(time_av 60) min(30) by(permno)
    
    This uses a 60-month rolling window, not 60-observation window.
    """
    if len(group_df) == 0:
        return group_df.with_columns([
            pl.lit(None, dtype=pl.Float64).alias('betaVolTrend'),
            pl.lit(None, dtype=pl.Float64).alias('meanX')
        ])
    
    # Convert to numpy for efficient computation
    dates = group_df['time_avail_m'].to_numpy()
    time_numeric = group_df['time_numeric'].to_numpy() 
    vol = group_df['vol'].to_numpy()
    
    n = len(group_df)
    betaVolTrend = np.full(n, np.nan)
    meanX = np.full(n, np.nan)
    
    # For each observation, look back 60 months
    for i in range(n):
        current_date = dates[i]
        # Calculate 60 months ago (approximately 60 * 30.44 days)
        cutoff_date = current_date - np.timedelta64(60 * 30, 'D')  # 60 months * 30 days
        
        # Find observations within the 60-month window
        window_mask = (dates <= current_date) & (dates >= cutoff_date)
        window_indices = np.where(window_mask)[0]
        
        if len(window_indices) >= 30:  # min(30) requirement
            # Extract window data
            window_time = time_numeric[window_indices]
            window_vol = vol[window_indices]
            
            # Remove any NaN values
            valid_mask = ~(np.isnan(window_time) | np.isnan(window_vol))
            if np.sum(valid_mask) >= 30:
                clean_time = window_time[valid_mask]
                clean_vol = window_vol[valid_mask]
                
                # Simple linear regression: vol = alpha + beta * time_numeric
                n_obs = len(clean_time)
                sum_x = np.sum(clean_time)
                sum_y = np.sum(clean_vol)
                sum_xx = np.sum(clean_time * clean_time)
                sum_xy = np.sum(clean_time * clean_vol)
                
                # Calculate beta coefficient
                denominator = n_obs * sum_xx - sum_x * sum_x
                if abs(denominator) > 1e-10:  # Avoid division by very small numbers
                    beta = (n_obs * sum_xy - sum_x * sum_y) / denominator
                    betaVolTrend[i] = beta
                
                # Calculate rolling mean of vol
                meanX[i] = np.mean(clean_vol)
    
    # Add results to dataframe
    result = group_df.with_columns([
        pl.Series('betaVolTrend', betaVolTrend),
        pl.Series('meanX', meanX)
    ])
    
    return result

# Apply time-based rolling regression to each permno group
df = df.group_by('permno', maintain_order=True).map_groups(time_based_rolling_regression)

# Calculate VolumeTrend
df = df.with_columns([
    (pl.col('betaVolTrend') / pl.col('meanX')).alias('VolumeTrend')
])

# Winsorize at 1% and 99%
lower = df.select(pl.col('VolumeTrend').quantile(0.01)).item()
upper = df.select(pl.col('VolumeTrend').quantile(0.99)).item()
df = df.with_columns([
    pl.col('VolumeTrend').clip(lower_bound=lower, upper_bound=upper)
])

# Convert to output format
df = df.with_columns([
    (pl.col('time_avail_m').dt.year() * 100 + pl.col('time_avail_m').dt.month()).alias('yyyymm'),
    pl.col('permno').cast(pl.Int64),
])

df_final = df.select(['permno', 'yyyymm', 'VolumeTrend']).drop_nulls(subset=['VolumeTrend'])

# SAVE - Convert to pandas for CSV output with proper indexing
df_final_pandas = df_final.to_pandas().set_index(['permno', 'yyyymm'])
df_final_pandas.to_csv('../pyData/Predictors/VolumeTrend.csv')
print("VolumeTrend predictor saved successfully")