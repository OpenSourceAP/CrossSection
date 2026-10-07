"""Restore legacy share/exchange codes from CIZ classifications.

How to run: imported by CRSPMonthly.py.
Inputs: dataframe with CIZ share/issuer and exchange/trading fields.
Outputs: float64 share/exchange series matching the existing download schema.
Rules: WRDS CIZ-to-SIZ macro, January 2026, referenced in monthly_mapping.md.
Default75/99 classifications follow that macro and are reported in comparisons.
"""

import numpy as np
import pandas as pd

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


def legacy_share_codes(data):
    return pd.Series([SHARE_CODES.get(tuple(row),75) for row in data[SHARE_COLUMNS].itertuples(index=False,name=None)],index=data.index,dtype='float64')


def legacy_exchange_codes(data):
    exchange=data.primaryexch
    regular=data.conditionaltype.eq('RW')
    active=data.tradingstatusflg.eq('A')
    out=pd.Series(99.0,index=data.index)
    mapped=exchange.map({'N':1,'A':2,'Q':3,'R':4,'B':5,'I':6})
    mask=regular & active & mapped.notna()
    out.loc[mask]=mapped.loc[mask]
    main=exchange.isin(['N','A','Q'])
    out.loc[main & regular & data.tradingstatusflg.eq('H')]=-2
    out.loc[main & regular & data.tradingstatusflg.eq('S')]=-1
    when_issued=data.conditionaltype.eq('NW') | (exchange.eq('N') & data.conditionaltype.eq('WI'))
    mask=main & active & when_issued
    out.loc[mask]=exchange.loc[mask].map({'N':31,'A':32,'Q':33})
    out.loc[exchange.eq('X') & data.conditionaltype.eq('NT')]=0
    return out.astype('float64')
