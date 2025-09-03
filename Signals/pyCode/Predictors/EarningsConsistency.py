# ABOUTME: Calculates earnings consistency following Alwathainani 2009 Table 11A CLG-CHG
# ABOUTME: Average earnings growth over previous 48 months with sign consistency filters
# 
# Inputs: ../pyData/Intermediate/m_aCompustat.parquet
# Outputs: ../pyData/Predictors/EarningsConsistency.csv
# How to run: python3 EarningsConsistency.py

import pandas as pd
import numpy as np

# set path for utils
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

print("Starting EarningsConsistency.py...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'epspx'])
print(f"Loaded data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Setting up panel data structure...")
# Sort data by permno and time for panel structure
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate earnings growth: (EPS - EPS_12m_ago) / average(abs(EPS_12m_ago), abs(EPS_24m_ago))
print("Creating lag variables for earnings...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'epspx', [12, 24], prefix='l')
df = df.assign(
    egrowth = lambda x: (x['epspx'] - x['l12_epspx']) / (0.5 * (abs(x['l12_epspx']) + abs(x['l24_epspx'])))
)

# Replace infinite values from division by zero with NaN
df['egrowth'] = df['egrowth'].replace([np.inf, -np.inf], np.nan)

# Calculate earnings consistency as mean of current and lagged earnings growth over 48 months
print("Creating additional lag variables for earnings growth...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'egrowth', [12, 24, 36, 48], prefix='l')
print("Calculating earnings consistency...")
temp_cols = ['egrowth', 'l12_egrowth', 'l24_egrowth', 'l36_egrowth', 'l48_egrowth']
df['EarningsConsistency'] = df[temp_cols].mean(axis=1,skipna=True)

# Apply exclusion filters: missing earnings, extreme growth (>600%), or sign changes
df = df.assign(
    exception=lambda x: (
        (
            x["epspx"].isna()
            | x["l12_epspx"].isna()  # missing earnings current or prior year
        )
        | (abs(x["epspx"] / x["l12_epspx"]) > 6)  # earnings growth exceeds 600%
        | (
            (x["egrowth"] > 0)
            & (x["l12_egrowth"] < 0)
            & x["egrowth"].notna()  # positive growth following negative growth
        )
        | (
            (x["egrowth"] < 0)
            & ((x["l12_egrowth"] > 0) | x["l12_egrowth"].isna())
            & x["egrowth"].notna()  # negative growth following positive/missing growth
        )
    ) # end lambda
)
df.loc[df["exception"], "EarningsConsistency"] = np.nan
print(f"Calculated EarningsConsistency for {df['EarningsConsistency'].notna().sum()} observations")

# Save the predictor
save_predictor(df, 'EarningsConsistency')
print("EarningsConsistency.py completed successfully")