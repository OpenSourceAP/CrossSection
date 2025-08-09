# ABOUTME: Translates FirmAgeMom.do to create firm age-momentum interaction predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/FirmAgeMom.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet  
# Output: ../pyData/Predictors/FirmAgeMom.csv

import pandas as pd
import numpy as np
import polars as pl
from utils.savepredictor import save_predictor

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
    pl.col('permno').cum_count().over(['permno']).alias('tempage')
)

# drop if abs(prc) < 5 | tempage < 12
df = df.filter(
    (pl.col('prc').abs() >= 5) & (pl.col('tempage') >= 12)
)

# gen FirmAgeMom = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
# Create lagged returns (l.ret, l2.ret, l3.ret, l4.ret, l5.ret)
for i in range(1, 6):
    col_name = f'ret_lag{i}'
    df = df.with_columns(
        pl.col('ret').shift(i).over(['permno']).alias(col_name)
    )

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
df = df.with_columns(
    pl.col('tempage').qcut(5, labels=['1', '2', '3', '4', '5'], allow_duplicates=True).over('time_avail_m').alias('temp')
)

# replace FirmAgeMom =. if temp > 1 & temp !=.
# Set FirmAgeMom to null for firms not in bottom (youngest) quintile
df = df.with_columns(
    pl.when((pl.col('temp') != '1') & pl.col('temp').is_not_null())
    .then(None)
    .otherwise(pl.col('FirmAgeMom'))
    .alias('FirmAgeMom')
)

# SAVE
# do "$pathCode/savepredictor" FirmAgeMom
save_predictor(df, 'FirmAgeMom')

print("FirmAgeMom predictor completed")