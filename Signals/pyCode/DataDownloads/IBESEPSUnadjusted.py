# ABOUTME: Downloads IBES EPS estimates (unadjusted for splits) from WRDS, focusing on key forecast periods
# ABOUTME: Processes and standardizes IBES data, keeping last observation per ticker/period combination
"""
Inputs:
- WRDS database: ibes.statsumu_epsus (IBES summary statistics for unadjusted EPS estimates)

Outputs:
- ../pyData/Intermediate/IBES_EPS_Unadj.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/IBESEPSUnadjusted.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("IBESEPSUnadjusted")

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain unadjusted EPS forecasts for the horizons used by downstream signals.
# Select the forecast horizons used by downstream signals: FPI 0, 1, 2, and 6.
QUERY = """
SELECT a.ticker, a.statpers, a.measure, a.fpi, a.numest, a.medest,
       a.meanest, a.stdev, a.fpedats
FROM ibes.statsumu_epsus as a
WHERE a.fpi = '0' or a.fpi = '1' or a.fpi = '2' or a.fpi = '6'
"""

# Add row limit for debugging if configured
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

ibes_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(ibes_data)} IBES EPS records")

# Align forecasts with their observation month for monthly analyst-data joins.
ibes_data['statpers'] = pd.to_datetime(ibes_data['statpers'])
ibes_data['time_avail_m'] = ibes_data['statpers'].dt.to_period('M').dt.to_timestamp()
ibes_data['time_avail_m'] = pd.to_datetime(ibes_data['time_avail_m'])

# Preserve the forecast-period end date for horizon-specific calculations.
ibes_data['fpedats'] = pd.to_datetime(ibes_data['fpedats'])

# Distinguish IBES tickers from identifiers supplied by other datasets.
ibes_data = ibes_data.rename(columns={'ticker': 'tickerIBES'})

ibes_data = ibes_data.drop('measure', axis=1)

# Exclude observations without a usable mean forecast.
initial_count = len(ibes_data)
ibes_data = ibes_data.dropna(subset=['meanest'])
print(f"Removed {initial_count - len(ibes_data)} records with missing meanest")

# Keep the latest forecast per ticker, forecast horizon, and month.
ibes_data = ibes_data.sort_values(['tickerIBES', 'fpi', 'time_avail_m', 'statpers'])
ibes_data = ibes_data.drop_duplicates(['tickerIBES', 'fpi', 'time_avail_m'], keep='last')

print(f"After keeping last obs per month: {len(ibes_data)} records")

# Save monthly unadjusted EPS forecasts for downstream signals.
ibes_data.to_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet", index=False)

print(f"IBES EPS Unadjusted data saved with {len(ibes_data)} records")

print("\nRecords by FPI (Forecast Period Indicator):")
fpi_counts = ibes_data['fpi'].value_counts().sort_index()
print(fpi_counts)

print(f"\nDate range: {ibes_data['time_avail_m'].min()} to {ibes_data['time_avail_m'].max()}")

print("\nSample data:")
print(ibes_data.head())
