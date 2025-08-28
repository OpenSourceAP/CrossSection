# ABOUTME: OPLeverage.py - Operating Leverage predictor calculation
# ABOUTME: Translates Code/Predictors/OPLeverage.do to Python using polars

"""
OPLeverage.py

Operating Leverage predictor calculation - line-by-line translation of OPLeverage.do

Usage: python3 OPLeverage.py
Inputs: ../pyData/Intermediate/m_aCompustat.parquet
Outputs: ../pyData/Predictors/OPLeverage.csv

Operating Leverage = (tempxsga + cogs) / at
where tempxsga = 0 if xsga is missing, else xsga

Original Stata code:
use gvkey permno time_avail_m xsga cogs at using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempxsga = 0
replace tempxsga = xsga if xsga !=.
gen OPLeverage = (tempxsga + cogs)/at
label var OPLeverage "Operating Leverage"
do "$pathCode/savepredictor" OPLeverage
"""

import polars as pl
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

# DATA LOAD - equivalent to: use gvkey permno time_avail_m xsga cogs at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat data...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")

# Select only the columns we need (matching Stata command exactly)
df = df.select(['gvkey', 'permno', 'time_avail_m', 'xsga', 'cogs', 'at'])

print(f"Loaded {len(df)} observations")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
# In our case, there are no duplicates, but we replicate the logic anyway
df = df.group_by(['permno', 'time_avail_m']).first()
print(f"After removing duplicates: {len(df)} observations")

# xtset permno time_avail_m - not needed in Python, just documentation

# gen tempxsga = 0
# replace tempxsga = xsga if xsga !=.
df = df.with_columns([
    pl.when(pl.col('xsga').is_null()).then(0).otherwise(pl.col('xsga')).alias('tempxsga')
])

# gen OPLeverage = (tempxsga + cogs)/at
df = df.with_columns([
    ((pl.col('tempxsga') + pl.col('cogs')) / pl.col('at')).alias('OPLeverage')
])

print(f"Calculated OPLeverage for {df.filter(pl.col('OPLeverage').is_not_null()).count()} observations")

# SAVE - equivalent to: do "$pathCode/savepredictor" OPLeverage  
save_predictor(df, 'OPLeverage')

print("OPLeverage predictor completed successfully")