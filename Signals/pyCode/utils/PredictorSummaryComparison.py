#%%

import os
import numpy as np
import pandas as pd

RERUN_PORTFOLIOS = True

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#%%

# call RunPortfoliosExcerpt.R
if RERUN_PORTFOLIOS:
    print(' Xxx ======= Rerunning PortfoliosExcerpt.R ======= Xxx ')
    print(' This will take ~10 minutes')
    os.system('Rscript RunPortfoliosExcerpt.R')
else:
    print(' Xxx ======= Not rerunning PortfoliosExcerpt.R ======= Xxx ')
    print(' Are you sure this is what you want? (y/n)')
    answer = input()
    if answer != 'y':
        print(' Consider opening utils/PredictorSummaryComparison.py and setting RERUN_PORTFOLIOS = True')
        input("Press Enter to continue, Ctrl-C to exit...")
        raise Exception('Exiting...')


#%%
# Read in the new Predictor portfolios summary   
sumnew = pd.read_excel('../../../Portfolios/Data/Portfolios/PredictorSummary.xlsx')

# Read in the old version
sumold = pd.read_excel('../../DocsForClaude/PredictorSummary2024.xlsx')

# keep select columns
cols = ['signalname','tstat','rbar','vol','T','Nlong','Nshort']

sumold = sumold[cols]
sumnew = sumnew[cols]

# Read in signaldoc
signaldoc0 = pd.read_csv('../../DocsForClaude/SignalDoc-Copy.csv')

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
    ).round(2)

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

# save
tstat_display.to_csv('../../Logs/PredictorSummaryComparison.csv', index=False)
# %%
