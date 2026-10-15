# ABOUTME: Downloads native CRSP CIZ monthly stocks and prepares monthly stock outputs.
"""Run: python3 Signals/pyCode/DataDownloads/CRSPMonthly.py with the project venv.

Inputs: crsp.msf_v2, crsp.stksecurityinfohist and crsp.stkdelists.
Native monthly returns preserve source precision;
ret_b4_dl inverts the delisting return in month-end delisting months and is missing
for mid-month delistings, as in v1 (Docs/CRSP-v2-Migration.md).
The unused legacy bidlo/askhi columns are omitted. DEBUG_MODE selects all 1981
stock months; production uses full history. Cumulative factors are native.
Outputs: OPENAP_DATA_ROOT/Intermediate/monthlyCRSP.parquet (default Signals/pyData).
Mapping/compatibility decisions: Signals/tests/crsp_v2/monthly_mapping.md.
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_ROOT
from utils.debug_mode import log_selection, sql_date_window
from utils.wrds_connection import get_wrds_engine

(DATA_ROOT / 'Intermediate').mkdir(parents=True, exist_ok=True)


# WRDS CIZ-to-SIZ share classifications; see monthly_mapping.md.
SHARE_COLUMNS = ['sharetype', 'securitytype', 'securitysubtype', 'usincflg', 'issuertype']
SHARE_CODES = {
    ('NS','EQTY','COM','Y','ACOR'):10, ('NS','EQTY','COM','Y','CORP'):11,
    ('NS','EQTY','COM','N','CORP'):12, ('NS','FUND','CEF','Y','ACOR'):14,
    ('NS','FUND','CEF','N','ACOR'):15, ('NS','EQTY','COM','Y','REIT'):18,
    ('CE','EQTY','COM','Y','ACOR'):20, ('CE','EQTY','COM','Y','CORP'):21,
    ('NS','DERV','ATR','Y','ACOR'):23, ('CE','FUND','CEF','Y','ACOR'):24,
    ('AD','EQTY','COM','N','ACOR'):30, ('AD','EQTY','COM','N','CORP'):31,
    ('SB','EQTY','COM','Y','ACOR'):40, ('SB','EQTY','COM','Y','CORP'):41,
    ('SB','EQTY','COM','N','CORP'):42, ('SB','FUND','CEF','Y','ACOR'):44,
    ('SB','EQTY','COM','Y','REIT'):48, ('UG','EQTY','COM','Y','ACOR'):70,
    ('UG','EQTY','COM','Y','CORP'):71, ('UG','EQTY','COM','N','CORP'):72,
    ('NS','FUND','ETF','Y','ACOR'):73, ('UG','FUND','ETV','Y','ACOR'):74,
}


def restore_pre_delisting_returns(monthly, delist):
    """Rebuild v1-style returns before delisting; rules in Docs/CRSP-v2-Migration.md."""
    if delist.permno.duplicated().any():
        raise ValueError('CIZ delisting events have duplicate PERMNOs; resolve the event identity.')
    known = monthly.mthdelflg.isin(['N', 'G', 'M', 'A', 'P', 'V'])
    if not known.all():
        raise ValueError(f'Unknown CIZ monthly delisting flags: {monthly.loc[~known, "mthdelflg"].unique()}')
    includes_delisting = monthly.mthdelflg.isin(['A', 'P', 'V'])
    if monthly.loc[includes_delisting, 'permno'].duplicated().any():
        raise ValueError('A PERMNO has several delisting-inclusive months; resolve the event month.')
    # Match each event to its flagged month, which can differ from the DelistingDt month.
    monthly = monthly.merge(delist[['permno', 'delret']], on='permno', how='left', validate='many_to_one')
    if monthly.loc[includes_delisting, 'delret'].isna().any():
        raise ValueError('Delisting-inclusive months lack a CIZ delisting return.')
    # V1 monthly returns are missing when a delisting month has no month-end price.
    month_end = pd.to_datetime(monthly.mthprcdt).eq(pd.to_datetime(monthly.date))
    monthly['ret_b4_dl'] = monthly.ret
    monthly.loc[monthly.mthdelflg.ne('N') & ~month_end, 'ret_b4_dl'] = np.nan
    invert = includes_delisting & month_end
    monthly.loc[invert, 'ret_b4_dl'] = np.where(
        monthly.loc[invert, 'delret'].gt(-1),
        (1 + monthly.loc[invert, 'ret']) / (1 + monthly.loc[invert, 'delret']) - 1,
        np.nan,
    )
    print(f'Pre-delisting returns: {invert.sum():,} month-end inverses; '
          f'{(monthly.mthdelflg.ne("N") & ~month_end).sum():,} mid-month delistings left missing', flush=True)
    return monthly.drop(columns='delret')


log_selection('CRSPMonthly')
engine=get_wrds_engine()
predicate,params=sql_date_window('a.mthcaldt','monthly')
query=f"""
SELECT a.permno, a.permco, a.mthcaldt AS date, a.mthret AS ret, a.mthretx AS retx,
       a.mthvol AS vol, a.shrout, a.mthprc, a.mthprcflg, a.mthprcdt, a.mthdelflg, a.mthcumfacshr AS cfacshr,
       a.ticker, a.sharetype, a.securitytype, a.securitysubtype, a.usincflg,
       a.issuertype, a.primaryexch, a.conditionaltype, a.tradingstatusflg,
       b.shareclass, b.siccd
FROM crsp.msf_v2 AS a
LEFT JOIN crsp.stksecurityinfohist AS b
  ON a.permno=b.permno
 AND b.secinfostartdt <= COALESCE(a.mthprcdt,a.mthcaldt)
 AND COALESCE(a.mthprcdt,a.mthcaldt) <= b.secinfoenddt
WHERE {predicate}
"""
crsp_data=pd.read_sql_query(query,engine,params=params)
crsp_data['time_avail_m']=pd.to_datetime(crsp_data['date']).dt.to_period('M').dt.to_timestamp()
keys=['permno','time_avail_m']
if crsp_data.duplicated(keys).any():
    raise ValueError('CIZ monthly/name join has duplicate security-month keys; resolve the intervals.')

# Full delisting history: events are matched to flagged months by PERMNO.
delist=pd.read_sql_query("SELECT permno, delret FROM crsp.stkdelists",engine)
engine.dispose()
crsp_data=restore_pre_delisting_returns(crsp_data,delist)

crsp_data[['permno','permco']]=crsp_data[['permno','permco']].astype('Int64')
crsp_data['prc']=np.where(crsp_data.mthprcflg.eq('BA'),-crsp_data.mthprc,crsp_data.mthprc)
# Restore the legacy numeric classifications using WRDS's CIZ-to-SIZ rules.
crsp_data['shrcd'] = pd.Series(
    [SHARE_CODES.get(tuple(row), 75)
     for row in crsp_data[SHARE_COLUMNS].itertuples(index=False, name=None)],
    index=crsp_data.index, dtype='float64',
)
exchange = crsp_data.primaryexch
regular = crsp_data.conditionaltype.eq('RW')
active = crsp_data.tradingstatusflg.eq('A')
exchange_codes = pd.Series(99.0, index=crsp_data.index)
mapped = exchange.map({'N': 1, 'A': 2, 'Q': 3, 'R': 4, 'B': 5, 'I': 6})
mask = regular & active & mapped.notna()
exchange_codes.loc[mask] = mapped.loc[mask]
main = exchange.isin(['N', 'A', 'Q'])
exchange_codes.loc[main & regular & crsp_data.tradingstatusflg.eq('H')] = -2
exchange_codes.loc[main & regular & crsp_data.tradingstatusflg.eq('S')] = -1
when_issued = (crsp_data.conditionaltype.eq('NW')
               | (exchange.eq('N') & crsp_data.conditionaltype.eq('WI')))
mask = main & active & when_issued
exchange_codes.loc[mask] = exchange.loc[mask].map({'N': 31, 'A': 32, 'Q': 33})
exchange_codes.loc[exchange.eq('X') & crsp_data.conditionaltype.eq('NT')] = 0
crsp_data['exchcd'] = exchange_codes
crsp_data['ticker']=crsp_data.ticker.fillna('')
crsp_data['shrcls']=crsp_data.shareclass.replace('NCS','').fillna('')
crsp_data['sicCRSP']=pd.to_numeric(crsp_data.siccd,errors='coerce').astype('float64')
crsp_data['sic2D']=pd.to_numeric(crsp_data.sicCRSP.astype(str).str[:2],errors='coerce')
crsp_data['shrout']=crsp_data.shrout/1000
crsp_data['vol']=crsp_data.vol/1000000
crsp_data['mve_c']=crsp_data.shrout*crsp_data.prc.abs()
company=(crsp_data.dropna(subset='permco').groupby(['permco','time_avail_m'],as_index=False)
         .mve_c.sum(min_count=1).rename(columns={'mve_c':'mve_permco'}))
crsp_data=crsp_data.merge(company,on=['permco','time_avail_m'],how='left',validate='many_to_one')
columns=['permno','permco','ret','retx','vol','shrout','prc','cfacshr',
         'shrcd','exchcd','ticker','shrcls','sicCRSP','sic2D','time_avail_m','ret_b4_dl','mve_c','mve_permco']
crsp_data=crsp_data[columns]
crsp_data.to_parquet(DATA_ROOT / 'Intermediate/monthlyCRSP.parquet',index=False)
print(f'CRSP CIZ monthly saved: {len(crsp_data):,} rows; {crsp_data.time_avail_m.min()} to {crsp_data.time_avail_m.max()}',flush=True)
