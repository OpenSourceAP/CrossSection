# ABOUTME: Downloads IBES EPS estimates (adjusted for splits) with actuals joined from statsum_epsus and actpsum_epsus
# ABOUTME: Processes data to monthly frequency, removes missing estimates, and applies column standardization
"""
Inputs:
- ibes.statsum_epsus (EPS summary statistics)
- ibes.actpsum_epsus (actual price and shares data)

Outputs:
- ../pyData/Intermediate/IBES_EPS_Adj.parquet

How to run: python3 IBESEPSAdjusted.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.fpi, a.ticker, a.statpers, a.fpedats, a.anndats_act
    , a.meanest, a.actual, a.medest, a.stdev, a.numest
    , b.prdays, b.price, b.shout
FROM ibes.statsum_epsus as a left join ibes.actpsum_epsus as b
on a.ticker = b.ticker and a.statpers = b.statpers
"""

if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

ibes_adj = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(ibes_adj)} IBES EPS adjusted records")


ibes_adj['statpers'] = pd.to_datetime(ibes_adj['statpers'])
ibes_adj['time_avail_m'] = ibes_adj['statpers'].dt.to_period('M').dt.to_timestamp()
ibes_adj['time_avail_m'] = pd.to_datetime(ibes_adj['time_avail_m'])

ibes_adj['fpedats'] = pd.to_datetime(ibes_adj['fpedats'])
ibes_adj['anndats_act'] = pd.to_datetime(ibes_adj['anndats_act'])
ibes_adj['prdays'] = pd.to_datetime(ibes_adj['prdays'])

ibes_adj = ibes_adj.rename(columns={'ticker': 'tickerIBES'})

initial_count = len(ibes_adj)
ibes_adj = ibes_adj.dropna(subset=['meanest'])
print(f"Removed {initial_count - len(ibes_adj)} records with missing meanest")

ibes_adj = ibes_adj.sort_values(['tickerIBES', 'fpi', 'time_avail_m', 'statpers'])
ibes_adj = ibes_adj.drop_duplicates(['tickerIBES', 'fpi', 'time_avail_m'], keep='last')

print(f"After keeping last obs per month: {len(ibes_adj)} records")

ibes_adj.to_parquet("../pyData/Intermediate/IBES_EPS_Adj.parquet", index=False)

print(f"IBES EPS Adjusted data saved with {len(ibes_adj)} records")
print(f"Date range: {ibes_adj['time_avail_m'].min()} to {ibes_adj['time_avail_m'].max()}")

print("\nSample data:")
print(ibes_adj.head())
