# ABOUTME: Downloads monthly equal- and value-weighted market returns from CRSP CIZ indexes
# ABOUTME: Converts dates to monthly timestamps and saves a standardized parquet file
"""
Inputs:
- crsp.indmthseriesdata (CIZ monthly index series 1000200 and 1000201)

Outputs:
- OPENAP_DATA_ROOT/Intermediate/monthlyMarket.parquet

How to run: /opt/venv/projects/openap/bin/python3 Signals/pyCode/DataDownloads/MarketReturns.py
"""

import os
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.debug_mode import log_selection
from utils.wrds_connection import get_wrds_engine, release_wrds_engine
from utils.download_paths import intermediate_path

load_dotenv()

# CRSP's NYSE/NYSEMKT/Nasdaq/Arca market indexes. Monthly series retain these
# identifiers; other CIZ monthly index families may use daily INDNO + 400.
VALUE_WEIGHTED_INDNO = 1000200
EQUAL_WEIGHTED_INDNO = 1000201
QUERY = """
SELECT indno, mthcaldt, mthtotret, mthusdval
FROM crsp.indmthseriesdata
WHERE indno IN (1000200, 1000201)
ORDER BY indno, mthcaldt
"""

log_selection("MarketReturns")

# Download both complete index series, then require one observation per month.
engine = get_wrds_engine()
try:
    series = pd.read_sql_query(QUERY, engine)
finally:
    release_wrds_engine(engine)

series['time_avail_m'] = pd.to_datetime(series['mthcaldt']).dt.to_period('M').dt.to_timestamp()
if series[['indno', 'time_avail_m']].isna().any().any():
    raise ValueError('CIZ market index has a missing index identifier or month')
if series.duplicated(['indno', 'time_avail_m']).any():
    raise ValueError('CIZ market index has duplicate index-month rows')

vw = series.loc[series['indno'] == VALUE_WEIGHTED_INDNO,
                ['time_avail_m', 'mthtotret', 'mthusdval']].rename(
                    columns={'mthtotret': 'vwretd', 'mthusdval': 'usdval'})
ew = series.loc[series['indno'] == EQUAL_WEIGHTED_INDNO,
                ['time_avail_m', 'mthtotret']].rename(columns={'mthtotret': 'ewretd'})
if vw.empty or ew.empty:
    raise ValueError('One or both CIZ market index series are missing')
market_data = vw.merge(ew, on='time_avail_m', how='outer', validate='one_to_one', indicator=True)
if (market_data['_merge'] != 'both').any():
    raise ValueError('CIZ value- and equal-weighted index months do not match')
market_data = market_data[['vwretd', 'ewretd', 'usdval', 'time_avail_m']].sort_values(
    'time_avail_m').reset_index(drop=True)

# Save data
market_data.to_parquet(intermediate_path("monthlyMarket.parquet"))

# Display summary information
print(f"Monthly Market Returns downloaded with {len(market_data)} records")
print(f"Date range: {market_data['time_avail_m'].min()} to {market_data['time_avail_m'].max()}")
print("\nSample data:")
print(market_data.head())
print("\nSummary statistics:")
print(f"Value-weighted return - Mean: {market_data['vwretd'].mean():.4f}, Std: {market_data['vwretd'].std():.4f}")
print(f"Equal-weighted return - Mean: {market_data['ewretd'].mean():.4f}, Std: {market_data['ewretd'].std():.4f}")
