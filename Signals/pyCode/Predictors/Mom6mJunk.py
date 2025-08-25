#%%

# ABOUTME: Translates Code/Predictors/Mom6mJunk.do to calculate 6-month momentum for junk stocks
# ABOUTME: Creates junk stock momentum signal using CIQ and SP credit ratings with forward fill

"""
This script calculates 6-month momentum for junk-rated stocks (credit rating <= 14).

How to run:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/Mom6mJunk.py

Inputs:
    - ../pyData/Intermediate/m_CIQ_creditratings.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet  
    - ../pyData/Intermediate/m_SP_creditratings.parquet

Outputs:
    - ../pyData/Predictors/Mom6mJunk.csv (permno, yyyymm, Mom6mJunk)
"""

import pandas as pd
import numpy as np
import os
import sys
# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor
from stata_replication import stata_multi_lag


#%%
# ==== Import and clean data ====

# CIQ ratings
ciq_raw = pd.read_parquet("../pyData/Intermediate/m_CIQ_creditratings.parquet",
                             columns=['gvkey', 'ratingdate', 'source', 'currentratingnum'])

# clean up formats and names
ciq_raw['gvkey'] = ciq_raw['gvkey'].astype(np.int64)
ciq_raw['ratingdate'] = pd.to_datetime(ciq_raw['ratingdate'])
ciq_raw.rename(columns={'currentratingnum': 'ratingciq'}, inplace=True)

# keep most recent rating each month
ciq_raw.sort_values(['gvkey', 'ratingdate'], inplace=True)
ciq_raw['time_avail_m'] = ciq_raw['ratingdate'].dt.to_period('M').dt.start_time
ciq_raw = ciq_raw.drop_duplicates(subset=['gvkey', 'time_avail_m'], keep='last')

# SP ratings
# (this is already deduplicated)
sp_raw = pd.read_parquet("../pyData/Intermediate/m_SP_creditratings.parquet")
sp_raw.rename(columns={'credrat': 'ratingsp'}, inplace=True)

# SignalMasterTable
df_raw = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet",
                     columns=['gvkey', 'permno', 'time_avail_m', 'ret'])

#%%
# ==== Merge and Process Credit Ratings ====

# use SP ratings by default, CIQ as fallback
df = df_raw.copy()

# ac: Mom6mJunk.do has `drop if gvkey == .` but I'm not sure it makes sense! 
df.query('gvkey.notna()', inplace=True)

df = pd.merge(df, sp_raw, on=['gvkey', 'time_avail_m'], how='left')
print(f"left join with sp ratings, nrow = {len(df)}")

df = pd.merge(df, ciq_raw, on=['gvkey', 'time_avail_m'], how='left') 
print(f"left join with ciq ratings, nrow = {len(df)}")

# use sp by default (as in Avramov et al), CIQ otherwise
df['credrat'] = df['ratingsp'].fillna(df['ratingciq'])


#%%
# ==== Fill in date gaps and forward fill missing values ====
# replicate Stata: xtset permno time_avail_m; tsfill
# ac: the fill date gaps is only needed because we drop missing gvkey above


# get all permno and time_avail_m
permno_list = df['permno'].unique()
ym_list = df['time_avail_m'].unique() # let's make this cleaner

# 're-index' the df to make a balanced panel with lots of missing values
full_idx = pd.MultiIndex.from_product([permno_list, ym_list], names=['permno', 'time_avail_m'])
df_balanced = df.set_index(['permno', 'time_avail_m']).reindex(full_idx).reset_index()\
    .sort_values(['permno', 'time_avail_m'])

# keep only the observations that are within the range of the original df
ym_ranges = df.groupby('permno')['time_avail_m'].agg(ym_min='min', ym_max='max').reset_index()
df_balanced = df_balanced.merge(ym_ranges, on='permno', how='left')
df_balanced.query('time_avail_m >= ym_min & time_avail_m <= ym_max', inplace=True)

# finally, fill credrat with most recent rating
df.sort_values(['permno', 'time_avail_m'], inplace=True)
df['credrat'] = df.groupby('permno')['credrat'].ffill()

#%%

# ==== SIGNAL CONSTRUCTION ====

# Set index for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# Replace missing returns with 0 
# ac: this interacts with the missing gvkey drop above
df.loc[df['ret'].isna(), 'ret'] = 0

# Calculate 6-month momentum using stata_multi_lag for calendar validation
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5])

# Calculate 6-month momentum (geometric return)
df['Mom6m'] = ((1 + df['ret_lag1']) * 
               (1 + df['ret_lag2']) * 
               (1 + df['ret_lag3']) * 
               (1 + df['ret_lag4']) * 
               (1 + df['ret_lag5'])) - 1

# Create Mom6mJunk for junk stocks (rating <= 14 and > 0)
# set missing to +Inf, following stata rules
df['credrat'] = df['credrat'].fillna(np.inf)
df['Mom6mJunk'] = np.where((df['credrat'] <= 14) & (df['credrat'] > 0), df['Mom6m'], np.nan)

# SAVE 
# note: save_predictor drops missing values for Mom6mJunk
save_predictor(df, 'Mom6mJunk')


print(f"Mom6mJunk saved with {len(df)} observations")

