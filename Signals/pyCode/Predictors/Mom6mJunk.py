# ABOUTME: Translates Mom6mJunk.do to calculate 6-month momentum for junk stocks
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom6mJunk.py

# Run from pyCode/ directory  
# Inputs: SignalMasterTable.parquet, m_CIQ_creditratings.parquet, m_SP_creditratings.parquet
# Output: ../pyData/Predictors/Mom6mJunk.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.stata_replication import stata_multi_lag
from utils.savepredictor import save_predictor

# Clean CIQ ratings
df_ciq = pd.read_parquet('../pyData/Intermediate/m_CIQ_creditratings.parquet')

# remove suffixes
df_ciq['currentratingsymbol'] = df_ciq['currentratingsymbol'].str.replace('pi', '')
df_ciq['currentratingsymbol'] = df_ciq['currentratingsymbol'].str.replace('q', '')
df_ciq['currentratingsymbol'] = df_ciq['currentratingsymbol'].str.replace(' prelim', '')

# Create numerical rating (for ease of comparison with CredRatDG)
df_ciq['credratciq'] = 0
df_ciq.loc[df_ciq['currentratingsymbol'] == 'D', 'credratciq'] = 1
df_ciq.loc[df_ciq['currentratingsymbol'] == 'C', 'credratciq'] = 2
df_ciq.loc[df_ciq['currentratingsymbol'] == 'CC', 'credratciq'] = 3
df_ciq.loc[df_ciq['currentratingsymbol'] == 'CCC-', 'credratciq'] = 4
df_ciq.loc[df_ciq['currentratingsymbol'] == 'CCC', 'credratciq'] = 5
df_ciq.loc[df_ciq['currentratingsymbol'] == 'CCC+', 'credratciq'] = 6
df_ciq.loc[df_ciq['currentratingsymbol'] == 'B-', 'credratciq'] = 7
df_ciq.loc[df_ciq['currentratingsymbol'] == 'B', 'credratciq'] = 8
df_ciq.loc[df_ciq['currentratingsymbol'] == 'B+', 'credratciq'] = 9
df_ciq.loc[df_ciq['currentratingsymbol'] == 'BB-', 'credratciq'] = 10
df_ciq.loc[df_ciq['currentratingsymbol'] == 'BB', 'credratciq'] = 11
df_ciq.loc[df_ciq['currentratingsymbol'] == 'BB+', 'credratciq'] = 12
df_ciq.loc[df_ciq['currentratingsymbol'] == 'BBB-', 'credratciq'] = 13
df_ciq.loc[df_ciq['currentratingsymbol'] == 'BBB', 'credratciq'] = 14
df_ciq.loc[df_ciq['currentratingsymbol'] == 'BBB+', 'credratciq'] = 15
df_ciq.loc[df_ciq['currentratingsymbol'] == 'A-', 'credratciq'] = 16
df_ciq.loc[df_ciq['currentratingsymbol'] == 'A', 'credratciq'] = 17
df_ciq.loc[df_ciq['currentratingsymbol'] == 'A+', 'credratciq'] = 18
df_ciq.loc[df_ciq['currentratingsymbol'] == 'AA-', 'credratciq'] = 19
df_ciq.loc[df_ciq['currentratingsymbol'] == 'AA', 'credratciq'] = 20
df_ciq.loc[df_ciq['currentratingsymbol'] == 'AA+', 'credratciq'] = 21
df_ciq.loc[df_ciq['currentratingsymbol'] == 'AAA', 'credratciq'] = 22

df_ciq = df_ciq[['gvkey', 'time_avail_m', 'credratciq']].copy()

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'ret']].copy()
# drop if gvkey ==.
df = df[df['gvkey'].notna()]
# merge 1:1 gvkey time_avail_m using m_SP_creditratings
df_sp = pd.read_parquet('../pyData/Intermediate/m_SP_creditratings.parquet')
df = df.merge(df_sp, on=['gvkey', 'time_avail_m'], how='left')
# merge 1:1 gvkey time_avail_m using temp_ciq_rat
df = df.merge(df_ciq, on=['gvkey', 'time_avail_m'], how='left')

# fill missing credratciq with most recent 
# xtset permno time_avail_m; tsfill
df = df.sort_values(['permno', 'time_avail_m'])

# Get all permno-time combinations that exist in the data range for tsfill
df_ranges = df.groupby('permno')['time_avail_m'].agg(['min', 'max']).reset_index()
df_ranges.columns = ['permno', 'time_min', 'time_max']

# Create all time periods for each permno
all_times = df['time_avail_m'].unique()
df_full = []
for _, row in df_ranges.iterrows():
    permno = row['permno']
    time_range = [t for t in all_times if row['time_min'] <= t <= row['time_max']]
    df_permno = pd.DataFrame({'permno': permno, 'time_avail_m': time_range})
    df_full.append(df_permno)

df_full = pd.concat(df_full, ignore_index=True)
df = df_full.merge(df, on=['permno', 'time_avail_m'], how='left')
df = df.sort_values(['permno', 'time_avail_m'])

# foreach v of varlist credratciq { replace `v' = `v'[_n-1] if permno == permno[_n-1] & mi(`v') }
df['credratciq'] = df.groupby('permno')['credratciq'].ffill()

# coalecse credit ratings: replace credrat = credratciq if credrat == .
df['credrat'] = df['credrat'].fillna(df['credratciq'])

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)
# gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5])
df['Mom6m'] = ((1 + df['ret_lag1']) * 
               (1 + df['ret_lag2']) * 
               (1 + df['ret_lag3']) * 
               (1 + df['ret_lag4']) * 
               (1 + df['ret_lag5'])) - 1
# gen Mom6mJunk = Mom6m if ( credrat <= 14 & credrat > 0 )
df['Mom6mJunk'] = np.where((df['credrat'] <= 14) & (df['credrat'] > 0), df['Mom6m'], np.nan)

# SAVE
save_predictor(df, 'Mom6mJunk')