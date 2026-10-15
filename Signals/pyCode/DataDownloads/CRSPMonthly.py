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
from utils.crsp_v2_codes import legacy_exchange_codes, legacy_share_codes
from utils.debug_mode import log_selection, sql_date_window
from utils.download_paths import intermediate_path
from utils.wrds_connection import get_wrds_engine, release_wrds_engine


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
release_wrds_engine(engine)
crsp_data=restore_pre_delisting_returns(crsp_data,delist)

crsp_data[['permno','permco']]=crsp_data[['permno','permco']].astype('Int64')
crsp_data['prc']=np.where(crsp_data.mthprcflg.eq('BA'),-crsp_data.mthprc,crsp_data.mthprc)
crsp_data['shrcd']=legacy_share_codes(crsp_data)
crsp_data['exchcd']=legacy_exchange_codes(crsp_data)
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
crsp_data.to_parquet(intermediate_path('monthlyCRSP.parquet'),index=False)
print(f'CRSP CIZ monthly saved: {len(crsp_data):,} rows; {crsp_data.time_avail_m.min()} to {crsp_data.time_avail_m.max()}',flush=True)
