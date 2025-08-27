#%%

# debug
import os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
print('debug')
print(os.getcwd())


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
from utils.savepredictor import save_predictor
from utils.stata_replication import stata_multi_lag, stata_ineq_pd, fill_date_gaps

# DATA LOAD
# Load m_aCompustat data
compustat_df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                               columns=['permno', 'time_avail_m', 'fopt', 'oancf', 'ib', 'at', 'dltt', 'act', 'lct', 'txt', 'xint', 'sale', 'ceq'])

# Merge with SignalMasterTable
signal_df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                           columns=['permno', 'time_avail_m', 'mve_c'])
df = compustat_df.merge(signal_df, on=['permno', 'time_avail_m'], how='inner')

# Merge with monthlyCRSP
crsp_df = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet", 
                         columns=['permno', 'time_avail_m', 'shrout'])
df = df.merge(crsp_df, on=['permno', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Replace fopt with oancf if fopt is missing
df['fopt'] = df['fopt'].fillna(df['oancf'])

# Create tempebit before lag creation (needed for accurate comparison)
df['tempebit'] = df['ib'] + df['txt'] + df['xint']

# Create 12-month lags for required variables using stata_multi_lag
df = fill_date_gaps(df, 'permno', 'time_avail_m') # fill gaps first for efficiency
lag_vars = ['ib', 'at', 'dltt', 'act', 'lct', 'sale', 'shrout']
for var in lag_vars:
    df = stata_multi_lag(df, 'permno', 'time_avail_m', var, [12], prefix='l', fill_gaps=False)

# Calculate individual Piotroski components
# p1: Positive net income
df['p1'] = 0
df.loc[stata_ineq_pd(df['ib'], ">", 0), 'p1'] = 1

# p2: Positive operating cash flow
df['p2'] = 0
df.loc[stata_ineq_pd(df['fopt'], ">", 0), 'p2'] = 1

# p3: Improvement in ROA
df['p3'] = 0
condition = stata_ineq_pd(df['ib']/df['at'] - df['l12_ib']/df['l12_at'], ">", 0)
df.loc[condition, 'p3'] = 1

# p4: Cash flow exceeds net income
df['p4'] = 0
df.loc[stata_ineq_pd(df['fopt'] - df['ib'], ">", 0), 'p4'] = 1

# p5: Reduction in leverage
df['p5'] = 0
condition = stata_ineq_pd(df['dltt']/df['at'] - df['l12_dltt']/df['l12_at'], "<", 0)
df.loc[condition, 'p5'] = 1

# p6: Improvement in current ratio
df['p6'] = 0
condition = stata_ineq_pd(df['act']/df['lct'] - df['l12_act']/df['l12_lct'], ">", 0)
df.loc[condition, 'p6'] = 1

# p7: Improvement in gross margin - exact Stata replication (tempebit/sale - tempebit/l12.sale)
df['p7'] = 0
condition = stata_ineq_pd(df['tempebit']/df['sale'] - df['tempebit']/df['l12_sale'], ">", 0)
df.loc[condition, 'p7'] = 1

# p8: Improvement in asset turnover
df['p8'] = 0
condition = stata_ineq_pd(df['sale']/df['at'] - df['l12_sale']/df['l12_at'], ">", 0)
df.loc[condition, 'p8'] = 1

# p9: No increase in shares outstanding
df['p9'] = 0
condition = stata_ineq_pd(df['shrout'], "<=", df['l12_shrout'])
df.loc[condition, 'p9'] = 1


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

# save
save_predictor(df, 'PS')

#%% debug

# read in stata csv
stata0 = pd.read_csv('../Data/Predictors/PS.csv').rename(columns={'PS': 'stata'})

# merge on to df
testdat = df.copy()
testdat = testdat.assign(
    yyyymm = lambda x: (x['time_avail_m'].dt.year * 100 + x['time_avail_m'].dt.month).astype(int)
)
testdat = testdat.merge(stata0, on=['permno', 'yyyymm'], how='left').assign(
    diff = lambda x: abs(x['PS'] - x['stata'])
)

#%% debug

print(f'rows with large differences out of {len(testdat)} rows')
print(
    testdat[['permno', 'yyyymm', 'PS', 'stata', 'diff']].query(
        'diff > 0'
    ).sort_values('diff', ascending=False)
)

"""
         permno  yyyymm   PS  stata  diff
2144821   77790  199904  6.0    8.0   2.0
2144812   77790  199807  5.0    7.0   2.0
2144820   77790  199903  6.0    8.0   2.0
"""

# from stata details we can see
# permno 77790, yyyymm 199904: all ps are 1 except p5

#%% debug

print(
    testdat[
        ['permno', 'yyyymm'] 
        + ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'PS']
    ].query('permno == 77790 & yyyymm == 199904')
)

# p6 and p7 are zero, unlike stata.

#%% debug

print('check on p6')

print(
    testdat[
        ['permno', 'yyyymm']
        + ['p6','act','lct','l12_act','l12_lct']
    ].query('permno == 77790 & yyyymm == 199904')
)

# it's a division by zero issue. l12_lct is zero, making the test -Inf > 0. in python, this is false. in stata, I guess this is true?

#%% debug

print('check on p7')

print(
    testdat[
        ['permno', 'yyyymm']
        + ['p7','tempebit','sale','l12_sale']
    ].query('permno == 77790 & yyyymm == 199904')
)

# also a division by zero issue.
