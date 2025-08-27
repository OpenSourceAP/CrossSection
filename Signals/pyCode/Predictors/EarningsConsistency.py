# ABOUTME: Translates EarningsConsistency.do from Stata to Python
# ABOUTME: Calculates earnings consistency measure based on standardized earnings changes

# How to run: python3 EarningsConsistency.py
# Inputs: ../pyData/Intermediate/m_aCompustat.parquet
# Outputs: ../pyData/Predictors/EarningsConsistency.csv

import pandas as pd
import numpy as np

# set path for utils
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.stata_replication import stata_multi_lag

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'epspx'])

# SIGNAL CONSTRUCTION
# Sort data (equivalent to xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Generate earnings growth (called temp in Stata)
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'epspx', [12, 24], prefix='l', fill_gaps=True)
df = df.assign(
    egrowth = lambda x: (x['epspx'] - x['l12_epspx']) / (0.5 * (abs(x['l12_epspx']) + abs(x['l24_epspx'])))
)

# replace infs (from division by zero) with nans
df['egrowth'] = df['egrowth'].replace([np.inf, -np.inf], np.nan)

# Generate earnings consistency = the mean earnings growth from 48 months ago to now, with some exceptions
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'egrowth', [12, 24, 36, 48], prefix='l', fill_gaps=True)
temp_cols = ['egrowth', 'l12_egrowth', 'l24_egrowth', 'l36_egrowth', 'l48_egrowth']
df['EarningsConsistency'] = df[temp_cols].mean(axis=1,skipna=True) # important to skipna=True

# exceptions: ignore the following settings
df = df.assign(
    exception=lambda x: (
        (
            x["epspx"].isna()
            | x["l12_epspx"].isna()  # missing earnings this year or last
        )
        | (abs(x["epspx"] / x["l12_epspx"]) > 6)  # absurdly high growth
        | (
            (x["egrowth"] > 0)
            & (x["l12_egrowth"] < 0)
            & x["egrowth"].notna()  # sign change this year
        )
        | (
            (x["egrowth"] < 0)
            & ((x["l12_egrowth"] > 0) | x["l12_egrowth"].isna())
            & x["egrowth"].notna()  # sign change this year
        )
    ) # end lambda
)
df.loc[df["exception"], "EarningsConsistency"] = np.nan

# Save the predictor
save_predictor(df, 'EarningsConsistency')