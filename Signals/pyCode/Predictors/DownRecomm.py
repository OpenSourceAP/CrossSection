# ABOUTME: DownRecomm.py - computes earnings forecast downgrade indicator (Barber et al. 2001 JF Table 3C)
# ABOUTME: Binary indicator for decreased mean analyst earnings forecasts using IBES data

# Computes binary indicator for analyst recommendation downgrades
# Input: IBES recommendation data and master security table
# Output: Binary signal for recommendation improvements

import pandas as pd
import numpy as np

# Load IBES recommendation data with required columns
df = pd.read_parquet('../pyData/Intermediate/IBES_Recommendations.parquet', 
                     columns=['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd'])

# Aggregate analyst-firm-month recommendations
# First aggregation: get last non-missing recommendation per analyst
def last_non_missing(series):
    non_missing = series.dropna()
    return non_missing.iloc[-1] if len(non_missing) > 0 else np.nan

df = df.groupby(['tickerIBES', 'amaskcd', 'time_avail_m'])['ireccd'].apply(last_non_missing).reset_index()

# Second aggregation: compute mean recommendation across analysts
df = df.groupby(['tickerIBES', 'time_avail_m'], as_index=False)['ireccd'].mean()

# Create downgrade indicator based on month-over-month changes
# Sort data by firm and time for lag calculations
df = df.sort_values(['tickerIBES', 'time_avail_m'])

# Generate 1-month lagged recommendation
df['ireccd_lag'] = df.groupby('tickerIBES')['ireccd'].shift(1)

# Identify recommendation improvements (higher values = better recommendations)
df['DownRecomm'] = ((df['ireccd'] > df['ireccd_lag']) & (df['ireccd_lag'].notna())).astype(int)

# Add security identifiers by merging with master table
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                columns=['permno', 'tickerIBES', 'time_avail_m'])

# Inner join preserves only firms with both IBES and CRSP data
df = df.merge(signal_master, on=['tickerIBES', 'time_avail_m'], how='inner')

# Select output columns
result = df[['permno', 'time_avail_m', 'DownRecomm']].copy()

# Convert date to YYYYMM integer format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Format final output
result = result[['permno', 'yyyymm', 'DownRecomm']]

# Ensure integer data types
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/DownRecomm.csv', index=False)

print(f"DownRecomm predictor created with {len(result)} observations")