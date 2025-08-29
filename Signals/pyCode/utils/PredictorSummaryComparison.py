#%%

import os
import numpy as np
import pandas as pd

RERUN_PORTFOLIOS = True

#%%

# call RunPortfoliosExcerpt.R
if RERUN_PORTFOLIOS:
    os.system('Rscript RunPortfoliosExcerpt.R')


#%%
# Read in the new Predictor portfolios summary   
sumnew = pd.read_excel('../../../Portfolios/Data/Portfolios/PredictorSummary.xlsx')

# Read in the old version
sumold = pd.read_excel('../DocsForClaude/PredictorSummary2024.xlsx')

# keep select columns
cols = ['signalname','tstat','rbar','vol','T','Nlong','Nshort']

sumold = sumold[cols]
sumnew = sumnew[cols]

# Read in signaldoc
signaldoc0 = pd.read_csv('../DocsForClaude/SignalDoc-Copy.csv')

signaldoc = signaldoc0[
    ['Acronym','T-Stat', 'Test in OP']
].rename(columns={'Acronym': 'signalname', 'T-Stat': 'tstat_op'})
signaldoc['tstat_op'] = signaldoc['tstat_op'].round(2)
signaldoc = signaldoc.sort_values('tstat_op', ascending=False)



#%%

# convert to long and merge

id_cols = ['signalname']

# Melt to long format
sumold_long = sumold.melt(
    id_vars=id_cols,
    var_name='metric',
    value_name='old'
)

sumnew_long = sumnew.melt(
    id_vars=id_cols, 
    var_name='metric', 
    value_name='new'
)

both = pd.merge(sumold_long, sumnew_long, on=id_cols + ['metric'], how='outer')\
    .assign(
        diff = lambda x: x['new'] - x['old']
    ).assign(
        diff = lambda x: x['diff'].fillna(np.inf)
    )

# focus on tstat
tstat = both[both['metric'] == 'tstat'].merge(signaldoc, on='signalname', how='left')

#%%

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 20)

print('signals with diff(tstat) > 0.1')
tstat_display = tstat.copy()
if 'Test in OP' in tstat_display.columns:
    tstat_display['Test in OP'] = tstat_display['Test in OP'].astype(str).str[:12]
print(
    tstat_display.sort_values(
        by='diff', key=lambda x: abs(x), ascending=False
    ).query('abs(diff) > 0.1')
)

#%%

signallist = [
    "AbnormalAccruals", "RIO_Volatility", "BetaFP", "TrendFactor", "RDAbility", "ResidualMomentum", "ReturnSkew3F", "CitationsRD", "MomOffSeason11YrPlus", "MomOffSeason06YrPlus", "PriceDelayRsq", "DivSeason", "RDAbility"
]

print(
    tstat.query('signalname.isin(@signallist)')\
        .assign(_order=lambda df: df['signalname'].map({k: i for i, k in enumerate(signallist)}))\
        .sort_values('_order').drop(columns=['_order'])
)

