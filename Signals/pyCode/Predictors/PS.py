#%%

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')

# ABOUTME: PS.py - calculates Piotroski F-score (within highest BM quintile)
# ABOUTME: Nine-factor profitability, efficiency, and leverage score restricted to highest book-to-market quintile

"""
PS predictor calculation (Piotroski F-score)

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/PS.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, fopt, oancf, ib, at, dltt, act, lct, txt, xint, sale, ceq)
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c)
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, shrout)

Outputs:
    - ../pyData/Predictors/PS.csv (permno, yyyymm, PS)
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.stata_fastxtile import fastxtile
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag, fill_date_gaps

print("Starting PS.py...")

# DATA LOAD
print("Loading m_aCompustat data...")
# Load m_aCompustat data
compustat_df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                               columns=['permno', 'time_avail_m', 'fopt', 'oancf', 'ib', 'at', 'dltt', 'act', 'lct', 'txt', 'xint', 'sale', 'ceq'])

# Merge with SignalMasterTable
print("Merging with SignalMasterTable...")
signal_df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                           columns=['permno', 'time_avail_m', 'mve_c'])
df = compustat_df.merge(signal_df, on=['permno', 'time_avail_m'], how='inner')

# Merge with monthlyCRSP
crsp_df = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet", 
                         columns=['permno', 'time_avail_m', 'shrout'])
df = df.merge(crsp_df, on=['permno', 'time_avail_m'], how='inner')

print(f"Loaded and merged data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Setting up panel data structure and calculating Piotroski score...")
# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Replace fopt with oancf if fopt is missing
df['fopt'] = df['fopt'].fillna(df['oancf'])

# Create tempebit before lag creation (needed for accurate comparison)
df['tempebit'] = df['ib'] + df['txt'] + df['xint']

# Create 12-month lags for required variables using stata_multi_lag
df = fill_date_gaps(df, 'permno', 'time_avail_m', '1mo') # fill gaps first for efficiency
lag_vars = ['ib', 'at', 'dltt', 'act', 'lct', 'sale', 'shrout']
for var in lag_vars:
    df = stata_multi_lag(df, 'permno', 'time_avail_m', var, [12], prefix='l', fill_gaps=False)

# to replicate stata, we need to do some painful handling of 
#   1: division by zero
#   2: inequality tests with missing values
# These interact in a ridiculous way here
# Do we want to replicate all this? I'm not sure.
# But let's do it for now. Let's prove this point.
# My point is that I can effing do this.

# The logic here is likely specific to the Piotroski score. So the function is internal.

def handle_stata_edges(
    metric: pd.Series
):
    """    
    This function handles division by zero and missing values for inequality tests
    example: df['metric'] = handle_stata_edges(df['ib']/df['at'] - df['l12_ib']/df['l12_at'])
    output: 
        - pd.Series of 0s and 1s
    """

    # in python, we get infs from division by zero. stata forces these to nan
    metric = metric.replace([np.inf, -np.inf], np.nan)

    # in stata, for some crazy reason nan is treated as inf in inequality tests
    metric = metric.replace(np.nan, np.inf)

    return metric

    
# Calculate individual Piotroski components
# p1: Positive net income
metric = handle_stata_edges(df['ib'])
df['p1'] = 0
df.loc[metric > 0, 'p1'] = 1

# p2: Positive operating cash flow
df['p2'] = 0
metric = handle_stata_edges(df['fopt'])
df.loc[metric > 0, 'p2'] = 1

# p3: Improvement in ROA
df['p3'] = 0
metric = handle_stata_edges(df['ib']/df['at'] - df['l12_ib']/df['l12_at'])
df.loc[metric > 0, 'p3'] = 1

# p4: Cash flow exceeds net income
df['p4'] = 0
metric = handle_stata_edges(df['fopt'] - df['ib'])
df.loc[metric > 0, 'p4'] = 1

# p5: Reduction in leverage
df['p5'] = 0
metric = handle_stata_edges(df['dltt']/df['at'] - df['l12_dltt']/df['l12_at'])
df.loc[metric < 0, 'p5'] = 1

# p6: Improvement in current ratio
df['p6'] = 0
metric = handle_stata_edges(df['act']/df['lct'] - df['l12_act']/df['l12_lct'])
df.loc[metric > 0, 'p6'] = 1

# p7: Improvement in gross margin - exact Stata replication (tempebit/sale - tempebit/l12.sale)
df['p7'] = 0
metric = handle_stata_edges(df['tempebit']/df['sale'] - df['tempebit']/df['l12_sale'])
df.loc[metric > 0, 'p7'] = 1

# p8: Improvement in asset turnover
df['p8'] = 0
metric = handle_stata_edges(df['sale']/df['at'] - df['l12_sale']/df['l12_at'])
df.loc[metric > 0, 'p8'] = 1

# p9: No increase in shares outstanding
df['p9'] = 0
metric = handle_stata_edges(df['l12_shrout'] - df['shrout']) # we want that if l12_shrout is missing, this evaluate sto true, to replicate the stata shrout <= l12.shrout test
df.loc[metric >= 0, 'p9'] = 1

# Sum all components
df['PS'] = df['p1'] + df['p2'] + df['p3'] + df['p4'] + df['p5'] + df['p6'] + df['p7'] + df['p8'] + df['p9']

# Set PS to missing if any required variables are missing
df.loc[(df['fopt'].isna()) | (df['ib'].isna()) | (df['at'].isna()) | (df['dltt'].isna()) | 
       (df['sale'].isna()) | (df['act'].isna()) | (df['tempebit'].isna()) | (df['shrout'].isna()), 'PS'] = np.nan

# Restrict to highest BM quintile
df = (
    df.assign(
        ceq = lambda x: np.where(x['ceq'] > 0, x['ceq'], np.nan)
    ).assign(
        BM = lambda x: np.log(x['ceq'] / x['mve_c'])
    )
)
df['BM_quintile'] = fastxtile(df, 'BM', by='time_avail_m', n=5)
df.loc[(df['BM_quintile'] != 5), 'PS'] = np.nan

print(f"Calculated PS for {df['PS'].notna().sum()} observations")
# save
save_predictor(df, 'PS')
print("PS.py completed successfully")

#%%

