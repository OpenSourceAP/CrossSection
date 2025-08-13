#%%

import sys
import os
import pandas as pd
import polars as pl
import statsmodels.formula.api as smf


os.getcwd()

#%%

name = 'PredictedFE'

stata = pd.read_csv(f'../Data/Predictors/{name}.csv')\
    .rename(columns={'PredictedFE': 'stata'})
python = pd.read_csv(f'../pyData/Predictors/{name}.csv')\
    .rename(columns={'PredictedFE': 'python'})

both = pd.merge(stata, python, on=['permno', 'yyyymm'], how='outer')\
    .assign(diff = lambda x: x['python'] - x['stata'])

#%%

sd_stata = both['stata'].std()
both['diff_std'] = both['diff'] / sd_stata

both.describe()

#%%

model = smf.ols('python ~ stata', data=both)
result = model.fit()
result.summary()

#%%



