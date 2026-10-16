# ABOUTME: Downloads native CRSP CIZ monthly stocks and prepares monthly stock outputs.
"""Run: python3 Signals/pyCode/DataDownloads/CRSPMonthly.py with the project venv.

Inputs: crsp.msf_v2, crsp.stksecurityinfohist and crsp.stkdelists.
Prepares monthly stock data for downstream signals, preserving native return
precision and providing legacy classifications and market equity measures.
Also provides returns before delisting, keeping these missing for mid-month
delistings under the legacy convention (Docs/CRSP-v2-Migration.md).
DEBUG_MODE selects all 1981 stock months; production uses full history.
Outputs: OPENAP_DATA_ROOT/Intermediate/monthlyCRSP.parquet (default Signals/pyData).
The output uses native cumulative share factors and omits the unused legacy
bidlo/askhi columns.
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


# Recover the legacy share codes used by downstream stock-sample filters.
# Classification rules follow WRDS; see monthly_mapping.md.
SHARE_COLUMNS = ['sharetype', 'securitytype', 'securitysubtype', 'usincflg', 'issuertype']
SHARE_CODES = {
    ('NS', 'EQTY', 'COM', 'Y', 'ACOR'): 10,
    ('NS', 'EQTY', 'COM', 'Y', 'CORP'): 11,
    ('NS', 'EQTY', 'COM', 'N', 'CORP'): 12,
    ('NS', 'FUND', 'CEF', 'Y', 'ACOR'): 14,
    ('NS', 'FUND', 'CEF', 'N', 'ACOR'): 15,
    ('NS', 'EQTY', 'COM', 'Y', 'REIT'): 18,
    ('CE', 'EQTY', 'COM', 'Y', 'ACOR'): 20,
    ('CE', 'EQTY', 'COM', 'Y', 'CORP'): 21,
    ('NS', 'DERV', 'ATR', 'Y', 'ACOR'): 23,
    ('CE', 'FUND', 'CEF', 'Y', 'ACOR'): 24,
    ('AD', 'EQTY', 'COM', 'N', 'ACOR'): 30,
    ('AD', 'EQTY', 'COM', 'N', 'CORP'): 31,
    ('SB', 'EQTY', 'COM', 'Y', 'ACOR'): 40,
    ('SB', 'EQTY', 'COM', 'Y', 'CORP'): 41,
    ('SB', 'EQTY', 'COM', 'N', 'CORP'): 42,
    ('SB', 'FUND', 'CEF', 'Y', 'ACOR'): 44,
    ('SB', 'EQTY', 'COM', 'Y', 'REIT'): 48,
    ('UG', 'EQTY', 'COM', 'Y', 'ACOR'): 70,
    ('UG', 'EQTY', 'COM', 'Y', 'CORP'): 71,
    ('UG', 'EQTY', 'COM', 'N', 'CORP'): 72,
    ('NS', 'FUND', 'ETF', 'Y', 'ACOR'): 73,
    ('UG', 'FUND', 'ETV', 'Y', 'ACOR'): 74,
}


def legacy_exchange_codes(monthly):
    """Recover legacy exchange codes for downstream sample selection.

    Distinguish ordinary trading from halted, suspended, and when-issued trading.
    Unclassified combinations retain code 99. Rules follow WRDS; see monthly_mapping.md.
    """
    exchange = monthly['primaryexch']
    condition = monthly['conditionaltype']
    trading_status = monthly['tradingstatusflg']

    is_regular_way = condition == 'RW'
    is_active = trading_status == 'A'
    is_major_exchange = exchange.isin(['N', 'A', 'Q'])  # NYSE, AMEX, NASDAQ

    codes = pd.Series(99.0, index=monthly.index)

    # Identify the listing exchange for securities in ordinary active trading.
    regular_exchange_codes = exchange.map({
        'N': 1, 'A': 2, 'Q': 3, 'R': 4, 'B': 5, 'I': 6,
    })
    is_regular_active = is_regular_way & is_active & regular_exchange_codes.notna()
    codes.loc[is_regular_active] = regular_exchange_codes.loc[is_regular_active]

    # Give halted and suspended securities their legacy status codes.
    is_halted = is_major_exchange & is_regular_way & (trading_status == 'H')
    is_suspended = is_major_exchange & is_regular_way & (trading_status == 'S')
    codes.loc[is_halted] = -2
    codes.loc[is_suspended] = -1

    # Keep when-issued securities distinct from ordinary active listings.
    is_when_issued = (condition == 'NW') | ((exchange == 'N') & (condition == 'WI'))
    is_active_when_issued = is_major_exchange & is_active & is_when_issued
    when_issued_codes = exchange.map({'N': 31, 'A': 32, 'Q': 33})
    codes.loc[is_active_when_issued] = when_issued_codes.loc[is_active_when_issued]

    # Apply WRDS's legacy code 0 to securities reported as X/NT.
    is_x_nt = (exchange == 'X') & (condition == 'NT')
    codes.loc[is_x_nt] = 0
    return codes


def restore_pre_delisting_returns(monthly, delist):
    """Provide monthly returns excluding the delisting return.

    Returns retain native CIZ dividend reinvestment. Keep the legacy missing-value
    rule for delisting months without a month-end price; also leave returns
    missing when removing a -100% delisting return is impossible.
    Rules: Docs/CRSP-v2-Migration.md.
    """
    # Require an unambiguous delisting event and supported flags before adjusting returns.
    if delist['permno'].duplicated().any():
        raise ValueError('CIZ delisting events have duplicate PERMNOs; resolve the event identity.')
    has_known_flag = monthly['mthdelflg'].isin(['N', 'G', 'M', 'A', 'P', 'V'])
    if not has_known_flag.all():
        unknown_flags = monthly.loc[~has_known_flag, 'mthdelflg'].unique()
        raise ValueError(f'Unknown CIZ monthly delisting flags: {unknown_flags}')
    includes_delisting = monthly['mthdelflg'].isin(['A', 'P', 'V'])
    if monthly.loc[includes_delisting, 'permno'].duplicated().any():
        raise ValueError('A PERMNO has several delisting-inclusive months; resolve the event month.')
    # Attach the delisting return needed to remove its contribution to monthly returns.
    monthly = monthly.merge(
        delist[['permno', 'delret']],
        on='permno',
        how='left',
        validate='many_to_one',
    )
    if monthly.loc[includes_delisting, 'delret'].isna().any():
        raise ValueError('Delisting-inclusive months lack a CIZ delisting return.')
    # In delisting months without a month-end price, keep pre-delisting returns
    # missing, as in the legacy data.
    has_month_end_price = pd.to_datetime(monthly['mthprcdt']) == pd.to_datetime(monthly['date'])
    is_mid_month_delisting = (monthly['mthdelflg'] != 'N') & ~has_month_end_price
    monthly['ret_b4_dl'] = monthly['ret']
    monthly.loc[is_mid_month_delisting, 'ret_b4_dl'] = np.nan

    # Remove the delisting return from eligible months to recover the return before delisting.
    should_invert = includes_delisting & has_month_end_price
    monthly.loc[should_invert, 'ret_b4_dl'] = np.where(
        monthly.loc[should_invert, 'delret'] > -1,
        (1 + monthly.loc[should_invert, 'ret']) / (1 + monthly.loc[should_invert, 'delret']) - 1,
        np.nan,
    )
    print(
        f'Pre-delisting returns: {should_invert.sum():,} month-end inverses; '
        f'{is_mid_month_delisting.sum():,} mid-month delistings left missing',
        flush=True,
    )
    return monthly.drop(columns='delret')


# Download monthly stock data with share-class and industry information as of
# the last price date, so stocks that delist mid-month keep their descriptors.
log_selection('CRSPMonthly')
engine = get_wrds_engine()
predicate, params = sql_date_window('a.mthcaldt', 'monthly')
query = f"""
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
crsp_data = pd.read_sql_query(query, engine, params=params)
crsp_data['time_avail_m'] = pd.to_datetime(crsp_data['date']).dt.to_period('M').dt.to_timestamp()
keys = ['permno', 'time_avail_m']
if crsp_data.duplicated(keys).any():
    raise ValueError('CIZ monthly/name join has duplicate security-month keys; resolve the intervals.')

# Download delisting returns and restore pre-delisting monthly returns.
# Use the full event history so delisting adjustments are available for the selected months.
delist = pd.read_sql_query('SELECT permno, delret FROM crsp.stkdelists', engine)
engine.dispose()
crsp_data = restore_pre_delisting_returns(crsp_data, delist)

# Preserve security and company identifiers as whole numbers, allowing missing values.
crsp_data[['permno', 'permco']] = crsp_data[['permno', 'permco']].astype('Int64')

# Preserve the legacy distinction between closing prices and bid/ask averages:
# a negative price marks a bid/ask average.
is_bid_ask_average = crsp_data['mthprcflg'] == 'BA'
crsp_data['prc'] = np.where(is_bid_ask_average, -crsp_data['mthprc'], crsp_data['mthprc'])

# Recover share and exchange codes so downstream filters can use the legacy classifications.
share_classifications = crsp_data[SHARE_COLUMNS].itertuples(index=False, name=None)
crsp_data['shrcd'] = pd.Series(
    [SHARE_CODES.get(classification, 75) for classification in share_classifications],
    index=crsp_data.index,
    dtype='float64',
)
crsp_data['exchcd'] = legacy_exchange_codes(crsp_data)

# Represent missing tickers and absent share classes consistently as empty text.
crsp_data['ticker'] = crsp_data['ticker'].fillna('')
crsp_data['shrcls'] = crsp_data['shareclass'].replace('NCS', '').fillna('')

# Preserve numeric SIC codes and the legacy industry grouping used by signals.
# This legacy conversion does not restore leading zeros for codes below 1000.
crsp_data['sicCRSP'] = pd.to_numeric(crsp_data['siccd'], errors='coerce').astype('float64')
sic_first_two_digits = crsp_data['sicCRSP'].astype(str).str[:2]
crsp_data['sic2D'] = pd.to_numeric(sic_first_two_digits, errors='coerce')

# Express shares outstanding and trading volume in millions of shares.
# Source units are thousands of shares for shares outstanding, and shares for volume.
crsp_data['shrout'] = crsp_data['shrout'] / 1_000
crsp_data['vol'] = crsp_data['vol'] / 1_000_000

# Calculate each security's market equity in millions of dollars,
# treating bid/ask averages as positive prices for valuation.
crsp_data['mve_c'] = crsp_data['shrout'] * crsp_data['prc'].abs()

# Calculate total company market equity across its securities each month.
# Keep the total missing when no security has a usable market equity value.
company_month_keys = ['permco', 'time_avail_m']
securities_with_company = crsp_data.dropna(subset='permco')
company_groups = securities_with_company.groupby(company_month_keys, as_index=False)
company_market_equity = company_groups['mve_c'].sum(min_count=1)
company_market_equity = company_market_equity.rename(columns={'mve_c': 'mve_permco'})

# Give each security its company-wide market equity as well as its own valuation.
crsp_data = crsp_data.merge(
    company_market_equity,
    on=company_month_keys,
    how='left',
    validate='many_to_one',
)

# Save the monthly stock dataset in the format expected by downstream signals.
columns = [
    'permno', 'permco', 'ret', 'retx', 'vol', 'shrout', 'prc', 'cfacshr',
    'shrcd', 'exchcd', 'ticker', 'shrcls', 'sicCRSP', 'sic2D', 'time_avail_m',
    'ret_b4_dl', 'mve_c', 'mve_permco',
]
crsp_data = crsp_data[columns]
crsp_data.to_parquet(DATA_ROOT / 'Intermediate/monthlyCRSP.parquet', index=False)
print(
    f'CRSP CIZ monthly saved: {len(crsp_data):,} rows; '
    f'{crsp_data["time_avail_m"].min()} to {crsp_data["time_avail_m"].max()}',
    flush=True,
)
