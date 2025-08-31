# %%
import os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

# ABOUTME: Volume Trend following Haugen and Baker 1996, Table 1, trading volume trend
# ABOUTME: calculates rolling coefficient from regressing monthly trading volume on linear time trend over 60-month window
"""
Usage:
    python3 Predictors/VolumeTrend.py

Inputs:
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, vol]

Outputs:
    - VolumeTrend.csv: CSV file with columns [permno, yyyymm, VolumeTrend]
    - VolumeTrend = rolling coefficient from regressing vol on time trend, scaled by 60-month average volume
    - Uses 60-month rolling window, requires at least 30 observations
"""

import polars as pl
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.asreg import asreg_collinear
from utils.asrol import asrol  
from utils.winsor2 import winsor2

print("Loading and processing VolumeTrend...")

# DATA LOAD
df = pl.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet',
                     columns=['permno', 'time_avail_m', 'vol'])

# SIGNAL CONSTRUCTION - Time-based rolling regression
print("Calculating time-based rolling regressions by permno...")

# Sort data first
df = df.sort(['permno', 'time_avail_m'])

# Convert time_avail_m to numeric form for regression (months since 1960-01, Stata format)
df = df.with_columns([
    ((pl.col('time_avail_m').dt.year() - 1960) * 12 + pl.col('time_avail_m').dt.month() - 1).alias('time_numeric')
])

# # Convert to pandas for asreg (which expects pandas DataFrames)
# df_pandas = df.to_pandas()

# # Run time-based rolling regression using asreg
# print("Running asreg for vol ~ time_numeric...")
# reg_results = asreg_collinear(
#     df_pandas,
#     y='vol',
#     X=['time_numeric'], 
#     by='permno',
#     time='time_avail_m',
#     window=60,  # 60-month window
#     min_obs=30,  # min(30) requirement
#     add_constant=True
# )

# # Merge regression results back with original data
# df_pandas = df_pandas.merge(reg_results[['_b_time_numeric']], left_index=True, right_index=True, how='left')
# df_pandas = df_pandas.rename(columns={'_b_time_numeric': 'betaVolTrend'})

# # Convert back to polars
# df = pl.from_pandas(df_pandas)

#%%
# Run time-based rolling regression using asreg_polars
print("Rolling window regressions of volume on time...")
df = df.with_columns(
    pl.col('vol').least_squares.rolling_ols(
        pl.col('time_numeric'),
        window_size=60,
        min_periods=30,
        mode='coefficients',
        add_intercept=True,
        null_policy='drop'
    ).over('permno').alias('coef')
).with_columns([
    pl.col('coef').struct.field('time_numeric').alias('betaVolTrend')
])


# Calculate rolling mean using asrol 
print("Calculating 60-month rolling mean of vol...")
df = asrol(
    df,
    group_col='permno',
    time_col='time_avail_m', 
    freq='1mo',
    window=60,
    value_col='vol',
    stat='mean',
    new_col_name='meanX',
    min_samples=30
)


# Calculate VolumeTrend
df = df.with_columns([
    (pl.col('betaVolTrend') / pl.col('meanX')).alias('VolumeTrend')
])

# Stata: winsor2 VolumeTrend, cut(1 99) replace trim
df = winsor2(df, ['VolumeTrend'], replace=True, trim=True, cuts=[1, 99])

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