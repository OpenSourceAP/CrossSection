# ABOUTME: Translates CitationsRD.do to create R&D citations ratio predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/CitationsRD.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_aCompustat.parquet, PatentDataProcessed.parquet, monthlyCRSP.parquet  
# Output: ../pyData/Predictors/CitationsRD.csv

import pandas as pd
import numpy as np
import polars as pl
import sys
import os
sys.path.append('.')
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import stata_multi_lag, stata_quantile
from utils.savepredictor import save_predictor

# Helper for polars column references
cc = pl.col

def asrol_custom(
    df: pl.DataFrame, 
    group_col: str, 
    date_col: str, 
    value_col: str, 
    stat: str = 'mean',
    window: str = '12mo', 
    min_obs: int = 1,
    require_prev_obs: bool = False,
    ) -> pl.DataFrame:
    """
    hand built polars asrol that 
      - constructs windows based a date duration
      - replaces with na if there are not enough observations in the window
    input: polars dataframe
    output: polars dataframe with a new column
    requires_prev_obs seems like it helps fit in a minority of cases, but in most cases it actually hurts. I left it in here for documentation to say we tried to match the stata 
    """

    # grab the stat function
    stat_dict = {'mean': pl.mean, 'std': pl.std, 'min': pl.min, 'max': pl.max, 'sum': pl.sum}
    stat_fun = stat_dict[stat]

    # First, add previous observation information to the original dataframe if require_prev_obs is True
    df_with_prev = df.sort(pl.col([group_col, date_col]))
    if require_prev_obs:
        df_with_prev = df_with_prev.with_columns([
            # Add columns for previous observation check
            pl.col(date_col).shift(1).over(group_col).alias('prev_date'),
            pl.col(value_col).shift(1).over(group_col).alias('prev_value')
        ]).with_columns([
            # Check if previous date is exactly 1 month before (accounting for varying month lengths)
            (((pl.col('prev_date') + pl.duration(days=31)) >= pl.col(date_col)) &
            ((pl.col('prev_date') + pl.duration(days=27)) <= pl.col(date_col)) &
            pl.col('prev_value').is_not_null()).alias('has_valid_prev_obs')
        ])

    df_addition = df_with_prev.with_columns(
        pl.col([group_col, date_col]).set_sorted()
    ).rolling(index_column=date_col, period=window, group_by=group_col).agg(
        [
            pl.last(value_col).alias(f'{value_col}_last'),
            stat_fun(value_col).alias(f'{value_col}_{stat}'),
            pl.count(value_col).alias(f'{value_col}_obs')
        ] + ([pl.last('has_valid_prev_obs').alias('has_valid_prev_obs')] if require_prev_obs else [])
    )
    
    # Apply the final condition based on min_obs and require_prev_obs
    if require_prev_obs:
        df_addition = df_addition.with_columns(
            pl.when(
                (cc(f'{value_col}_obs') >= min_obs) & cc('has_valid_prev_obs')
            ).then(cc(f'{value_col}_{stat}'))
            .otherwise(pl.lit(None))
            .alias(f'{value_col}_{stat}')
        )
    else:
        df_addition = df_addition.with_columns(
            pl.when(
                cc(f'{value_col}_obs') >= min_obs
            ).then(cc(f'{value_col}_{stat}'))
            .otherwise(pl.lit(None))
            .alias(f'{value_col}_{stat}')
        )

    return df.join(
        df_addition.select([group_col, date_col, f'{value_col}_{stat}']),
        on=[group_col, date_col],
        how='left',
        coalesce=True
    )

# DATA LOAD with early filtering for performance
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()

# OPTIMIZATION: Filter to post-1970 data early to reduce memory usage
df = df[df['time_avail_m'] >= '1970-01']  # Need extra history for lags
print(f"After early date filter: {df.shape}")

# Generate year from time_avail_m
df['year'] = df['time_avail_m'].dt.year

# Merge with Compustat annual data (also filtered early)
print("Loading and merging Compustat...")
compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
compustat = compustat[compustat['time_avail_m'] >= '1970-01']  # Match filtering

df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
print(f"After Compustat merge: {df.shape}")

# Drop if gvkey is missing (early filtering)
df = df.dropna(subset=['gvkey'])
print(f"After dropping missing gvkey: {df.shape}")

# Patent citation dataset
print("Loading and merging patent data...")
patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
patent = patent[['gvkey', 'year', 'ncitscale']].copy()

df = df.merge(patent, on=['gvkey', 'year'], how='left')
print(f"After patent merge: {df.shape}")

# Set panel structure and create calendar-based lags (to match Stata l6/l24 behavior)
print("Creating calendar-based lags...")
df = df.sort_values(['permno', 'time_avail_m'])

# Create calendar-based lags using standardized stata_multi_lag
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ncitscale', [6], freq='M')
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'xrd', [24], freq='M')

# Rename lag columns and fill missing with 0 to match original behavior
df['ncitscale'] = df['ncitscale_lag6'].fillna(0)
df['xrd_lag'] = df['xrd_lag24'].fillna(0)

# Clean up lag columns
df = df.drop(columns=['ncitscale_lag6', 'xrd_lag24'])
print(f"After creating lags: {df.shape}")

# Form portfolios only in June AFTER creating lags
print("Filtering to June observations...")
df = df[df['time_avail_m'] >= '1975-01']  # >= ym(1975,1)
df = df[df['time_avail_m'].dt.month == 6]  # month(dofm(time_avail_m)) == 6 (June)

print(f"After June filter: {df.shape}")

# Calendar-based rolling sums using asrol_custom (polars-based)
# Stata: asrol xrd_lag, window(time_avail_m 48) stat(sum) 
print("Creating calendar-based rolling sums...")

# Convert to polars for asrol_custom operations
df_pl = pl.from_pandas(df)

print("  Computing 48-month calendar rolling XRD sums...")
# asrol xrd_lag, window(time_avail_m 48) stat(sum) by(permno)
df_pl = asrol_custom(df_pl, 'permno', 'time_avail_m', 'xrd_lag', 'sum', '1470d', 1).rename({'xrd_lag_sum': 'sum_xrd'})

print("  Computing 48-month calendar rolling citation sums...")
# asrol ncitscale, window(time_avail_m 48) stat(sum) by(permno)  
df_pl = asrol_custom(df_pl, 'permno', 'time_avail_m', 'ncitscale', 'sum', '1470d', 1).rename({'ncitscale_sum': 'sum_ncit'})

# Convert back to pandas
df = df_pl.to_pandas()

# Create temporary CitationsRD signal
df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)

# Filter
# bysort gvkey (time_avail_m): drop if _n <= 2
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

# Drop financial firms
df = df.assign(sicCRSP = lambda x: x['sicCRSP'].fillna(np.inf)) # make sicCRSP Inf if missing, to match Stata
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]

# Drop if ceq < 0 (match Stata exactly: keeps NaN values)
df = df[~(df['ceq'] < 0)]

# == Double independent sort ==

# Size categories using NYSE breakpoints
print("Creating size categories...")

# Calculate NYSE median for each time period
nyse_medians = df[df['exchcd'] == 1].groupby('time_avail_m')['mve_c'].apply(
    lambda x: stata_quantile(x, 0.5)
).reset_index()
nyse_medians.columns = ['time_avail_m', 'nyse_median']

# Merge medians back to main dataset
df = df.merge(nyse_medians, on='time_avail_m', how='left')

# Create size categories: 1 if <= NYSE median, 2 if > NYSE median
df['sizecat'] = np.where(df['mve_c'] <= df['nyse_median'], 1, 2)

# Clean up
df = df.drop(columns=['nyse_median'])

# Main category using fastxtile logic exactly like Stata
print("Creating CitationsRD tercile categories...")

# Stata: egen maincat = fastxtile(tempCitationsRD), by(time_avail_m) n(3)
# fastxtile creates equal-sized groups based on VALID (non-missing) observations
df['maincat'] = fastxtile(df, 'tempCitationsRD', by='time_avail_m', n=3)

# Create CitationsRD signal: 1 if small & high, 0 if small & low  
df['CitationsRD'] = np.nan
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0

# OPTIMIZED: Expand back to monthly using more efficient approach
print("Expanding to monthly observations...")

# Keep only necessary columns for expansion to reduce memory usage
keep_cols = ['permno', 'gvkey', 'time_avail_m', 'CitationsRD']
df_slim = df[keep_cols].copy()

# Use list comprehension with pre-allocated DataFrames
df_expanded = pd.concat([
    df_slim.assign(time_avail_m=df_slim['time_avail_m'] + pd.DateOffset(months=i))
    for i in range(12)
], ignore_index=True)

df = df_expanded.sort_values(['gvkey', 'time_avail_m'])

# SAVE
save_predictor(df, 'CitationsRD')
