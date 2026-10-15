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
from config import DATA_ROOT
from utils.debug_mode import log_selection
from utils.wrds_connection import get_wrds_engine

(DATA_ROOT / 'Intermediate').mkdir(parents=True, exist_ok=True)

load_dotenv()

# Select CRSP's broad NYSE/NYSEMKT/Nasdaq/Arca market benchmarks under both weighting schemes.
VALUE_WEIGHTED_INDNO = 1000200
EQUAL_WEIGHTED_INDNO = 1000201
QUERY = """
SELECT indno, mthcaldt, mthtotret, mthusdval
FROM crsp.indmthseriesdata
WHERE indno IN (1000200, 1000201)
ORDER BY indno, mthcaldt
"""

log_selection("MarketReturns")

# Obtain complete benchmark histories so stock returns can be compared with the market.
engine = get_wrds_engine()
try:
    series = pd.read_sql_query(QUERY, engine)
finally:
    engine.dispose()

# Require a unique month for each benchmark before combining the return series.
series['time_avail_m'] = pd.to_datetime(series['mthcaldt']).dt.to_period('M').dt.to_timestamp()
if series[['indno', 'time_avail_m']].isna().any().any():
    raise ValueError('CIZ market index has a missing index identifier or month')
if series.duplicated(['indno', 'time_avail_m']).any():
    raise ValueError('CIZ market index has duplicate index-month rows')

# Provide value-weighted returns and market value alongside equal-weighted returns.
value_weighted = series.loc[
    series['indno'] == VALUE_WEIGHTED_INDNO,
    ['time_avail_m', 'mthtotret', 'mthusdval'],
]
value_weighted = value_weighted.rename(columns={'mthtotret': 'vwretd', 'mthusdval': 'usdval'})
equal_weighted = series.loc[
    series['indno'] == EQUAL_WEIGHTED_INDNO,
    ['time_avail_m', 'mthtotret'],
]
equal_weighted = equal_weighted.rename(columns={'mthtotret': 'ewretd'})
if value_weighted.empty or equal_weighted.empty:
    raise ValueError('One or both CIZ market index series are missing')
# Require both benchmarks to cover the same months so weighting comparisons are consistent.
market_data = value_weighted.merge(
    equal_weighted, on='time_avail_m', how='outer', validate='one_to_one', indicator=True,
)
if (market_data['_merge'] != 'both').any():
    raise ValueError('CIZ value- and equal-weighted index months do not match')
market_data = market_data[['vwretd', 'ewretd', 'usdval', 'time_avail_m']]
market_data = market_data.sort_values('time_avail_m').reset_index(drop=True)

# Save monthly market benchmarks for downstream return calculations.
market_data.to_parquet(DATA_ROOT / 'Intermediate/monthlyMarket.parquet')

print(f"Monthly Market Returns downloaded with {len(market_data)} records")
print(f"Date range: {market_data['time_avail_m'].min()} to {market_data['time_avail_m'].max()}")
print("\nSample data:")
print(market_data.head())
print("\nSummary statistics:")
print(f"Value-weighted return - Mean: {market_data['vwretd'].mean():.4f}, Std: {market_data['vwretd'].std():.4f}")
print(f"Equal-weighted return - Mean: {market_data['ewretd'].mean():.4f}, Std: {market_data['ewretd'].std():.4f}")
