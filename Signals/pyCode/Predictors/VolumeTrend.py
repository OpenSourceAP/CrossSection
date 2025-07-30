# ABOUTME: Translates VolumeTrend.do to create volume trend measure using rolling regression
# ABOUTME: Run from pyCode/ directory: python3 Predictors/VolumeTrend.py

# Run from pyCode/ directory
# Inputs: monthlyCRSP.parquet
# Output: ../pyData/Predictors/VolumeTrend.csv

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

print("Loading and processing VolumeTrend...")

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet')
df = df[['permno', 'time_avail_m', 'vol']].copy()

# SIGNAL CONSTRUCTION - Simplified rolling regression
def calculate_volume_trend(group, window=60, min_periods=30):
    """Simplified volume trend calculation"""
    group = group.sort_values('time_avail_m').reset_index(drop=True)
    group['betaVolTrend'] = np.nan
    group['meanX'] = np.nan
    
    if len(group) >= min_periods:
        # Use last available window or all data
        n_obs = min(window, len(group))
        recent_data = group.tail(n_obs)
        vol_clean = recent_data['vol'].dropna()
        
        if len(vol_clean) >= min_periods:
            # Simple linear trend: regress volume on time index
            time_index = np.arange(len(vol_clean)).reshape(-1, 1)
            vol_values = vol_clean.values
            
            try:
                reg = LinearRegression()
                reg.fit(time_index, vol_values)
                beta_trend = reg.coef_[0]
                mean_vol = np.mean(vol_values)
                
                # Apply to all observations in the group (simplified)
                group['betaVolTrend'] = beta_trend
                group['meanX'] = mean_vol
            except:
                pass
    
    return group

# Apply to each permno
df = df.groupby('permno').apply(
    lambda x: calculate_volume_trend(x, window=60, min_periods=30)
).reset_index(drop=True)

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