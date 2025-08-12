# ABOUTME: Translates FirmAgeMom.do to create firm age-momentum interaction predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/FirmAgeMom.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet  
# Output: ../pyData/Predictors/FirmAgeMom.csv

import pandas as pd
import numpy as np
import polars as pl
from utils.savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile

# DATA LOAD
# use permno time_avail_m ret prc using "$pathDataIntermediate/SignalMasterTable", clear
df = pl.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df.select(['permno', 'time_avail_m', 'ret', 'prc'])

# SIGNAL CONSTRUCTION

# replace ret = 0 if mi(ret)
df = df.with_columns(
    pl.col('ret').fill_null(0)
)

# bys permno (time_avail_m): gen tempage = _n
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns(
    pl.col('permno').cum_count().over(['permno']).alias('tempage_initial')
)

# drop if abs(prc) < 5 | tempage < 12
df = df.filter(
    (pl.col('prc').abs() >= 5) & (pl.col('tempage_initial') >= 12)
)

# Recalculate tempage for remaining observations (this is what Stata effectively does)
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns(
    pl.col('permno').cum_count().over(['permno']).alias('tempage')
)

# gen FirmAgeMom = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
# Create lagged returns with proper time-aware lagging
# Stata's l.ret, l2.ret etc. require consecutive monthly data

# First, create time-aware lags by checking monthly continuity
for i in range(1, 6):
    col_name = f'ret_lag{i}'
    time_lag_col = f'time_lag{i}'
    
    # Create basic shift and time shift
    df = df.with_columns([
        pl.col('ret').shift(i).over(['permno']).alias(col_name),
        pl.col('time_avail_m').shift(i).over(['permno']).alias(time_lag_col)
    ])
    
    # Check if the time gap is exactly i months (30*i days approximately)
    # If not, set the lagged return to null
    expected_days = i * 30
    tolerance_days = 8  # Allow 8 days tolerance for month boundaries (months can be 28-31 days)
    
    df = df.with_columns(
        pl.when(
            (pl.col('time_avail_m') - pl.col(time_lag_col)).dt.total_days().abs() > (expected_days + tolerance_days)
        )
        .then(None)
        .otherwise(pl.col(col_name))
        .alias(col_name)
    )
    
    # Clean up the temporary time lag column
    df = df.drop(time_lag_col)

# Calculate momentum product
df = df.with_columns(
    ((1 + pl.col('ret_lag1')) * 
     (1 + pl.col('ret_lag2')) * 
     (1 + pl.col('ret_lag3')) * 
     (1 + pl.col('ret_lag4')) * 
     (1 + pl.col('ret_lag5')) - 1).alias('FirmAgeMom')
)

# egen temp = fastxtile(tempage), by(time_avail_m) n(5)  // Find bottom age quintile
# Create quintiles of firm age by time period (1=youngest, 5=oldest)
# Convert to pandas for fastxtile operation
df_pd = df.to_pandas()
df_pd['temp'] = fastxtile(df_pd, 'tempage', by='time_avail_m', n=5)
# Convert back to polars
df = pl.from_pandas(df_pd)

# replace FirmAgeMom =. if temp > 1 & temp !=.
# Set FirmAgeMom to null for firms not in bottom (youngest) quintile
df = df.with_columns(
    pl.when((pl.col('temp') > 1) & pl.col('temp').is_not_null())
    .then(None)
    .otherwise(pl.col('FirmAgeMom'))
    .alias('FirmAgeMom')
)

# SAVE
# do "$pathCode/savepredictor" FirmAgeMom
save_predictor(df, 'FirmAgeMom')

print("FirmAgeMom predictor completed")