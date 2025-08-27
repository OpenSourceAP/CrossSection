# ABOUTME: Creates Illiquidity predictor using Amihud illiquidity measure
# ABOUTME: Run: python3 Predictors/Illiquidity.py

"""
Illiquidity Predictor

Implements the Amihud illiquidity measure:
- Daily illiquidity = |return| / (|price| * volume)
- Monthly average of daily illiquidity
- 12-month rolling mean of monthly illiquidity

Inputs:
- ../pyData/Intermediate/dailyCRSP.parquet

Outputs:  
- ../pyData/Predictors/Illiquidity.csv
"""

import pandas as pd
import numpy as np

# DATA LOAD
print("Loading dailyCRSP data...")
df = pd.read_parquet('../pyData/Intermediate/dailyCRSP.parquet')

# SIGNAL CONSTRUCTION
print("Constructing Illiquidity signal...")

# Convert time_d to monthly time_avail_m (year * 100 + month format)
df['time_avail_m'] = df['time_d'].dt.year * 100 + df['time_d'].dt.month

# Calculate daily illiquidity measure
df['ill'] = np.abs(df['ret']) / (np.abs(df['prc']) * df['vol'])

# Handle division by zero and inf values
df['ill'] = df['ill'].replace([np.inf, -np.inf], np.nan)

# Monthly average of daily illiquidity
monthly_ill = df.groupby(['permno', 'time_avail_m'])['ill'].mean().reset_index()

# Sort for lag operations
monthly_ill = monthly_ill.sort_values(['permno', 'time_avail_m'])

# Calculate 12-month rolling mean using lags
monthly_ill['ill_lag1'] = monthly_ill.groupby('permno')['ill'].shift(1)
monthly_ill['ill_lag2'] = monthly_ill.groupby('permno')['ill'].shift(2)
monthly_ill['ill_lag3'] = monthly_ill.groupby('permno')['ill'].shift(3)
monthly_ill['ill_lag4'] = monthly_ill.groupby('permno')['ill'].shift(4)
monthly_ill['ill_lag5'] = monthly_ill.groupby('permno')['ill'].shift(5)
monthly_ill['ill_lag6'] = monthly_ill.groupby('permno')['ill'].shift(6)
monthly_ill['ill_lag7'] = monthly_ill.groupby('permno')['ill'].shift(7)
monthly_ill['ill_lag8'] = monthly_ill.groupby('permno')['ill'].shift(8)
monthly_ill['ill_lag9'] = monthly_ill.groupby('permno')['ill'].shift(9)
monthly_ill['ill_lag10'] = monthly_ill.groupby('permno')['ill'].shift(10)
monthly_ill['ill_lag11'] = monthly_ill.groupby('permno')['ill'].shift(11)

# Calculate 12-month rolling mean
# In Stata, the formula (ill + l.ill + ... + l11.ill)/12 requires ALL 12 values to be non-missing
# If ANY are missing, the result is missing. We need to replicate this exact behavior.
illiquidity_cols = ['ill', 'ill_lag1', 'ill_lag2', 'ill_lag3', 'ill_lag4', 'ill_lag5',
                   'ill_lag6', 'ill_lag7', 'ill_lag8', 'ill_lag9', 'ill_lag10', 'ill_lag11']

# Count non-missing values for each observation
monthly_ill['non_missing_count'] = monthly_ill[illiquidity_cols].count(axis=1)

# Calculate mean, but only if ALL 12 values are present (matching Stata's behavior)
monthly_ill['Illiquidity'] = np.where(
    monthly_ill['non_missing_count'] == 12,
    monthly_ill[illiquidity_cols].mean(axis=1),
    np.nan
)

# Prepare final output - rename time_avail_m to yyyymm for consistency
result = monthly_ill[['permno', 'time_avail_m', 'Illiquidity']].copy()
result = result.rename(columns={'time_avail_m': 'yyyymm'})

# Drop rows with missing Illiquidity values
result = result.dropna(subset=['Illiquidity'])

print(f"Final dataset shape: {result.shape}")
print("Sample of final data:")
print(result.head())

# SAVE
result.to_csv('../pyData/Predictors/Illiquidity.csv', index=False)
print("Saved to ../pyData/Predictors/Illiquidity.csv")