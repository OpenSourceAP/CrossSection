# ABOUTME: Downloads IBES EPS estimates (unadjusted for splits) from WRDS, focusing on key forecast periods
# ABOUTME: Processes and standardizes IBES data, keeping last observation per ticker/period combination
"""
Inputs:
- WRDS database: ibes.statsumu_epsus (IBES summary statistics for unadjusted EPS estimates)

Outputs:
- ../pyData/Intermediate/IBES_EPS_Unadj.parquet

How to run: python3 IBESEPSUnadjusted.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

# Create database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Download IBES EPS estimates for specific forecast periods
# FPI codes: 0=long-term growth, 1=next year, 2=year after, 6=current quarter
QUERY = """
SELECT a.ticker, a.statpers, a.measure, a.fpi, a.numest, a.medest,
       a.meanest, a.stdev, a.fpedats
FROM ibes.statsumu_epsus as a
WHERE a.fpi = '0' or a.fpi = '1' or a.fpi = '2' or a.fpi = '6'
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

ibes_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(ibes_data)} IBES EPS records")


# Process date variables and prepare linking variables
ibes_data['statpers'] = pd.to_datetime(ibes_data['statpers'])
ibes_data['time_avail_m'] = ibes_data['statpers'].dt.to_period('M').dt.to_timestamp()
ibes_data['time_avail_m'] = pd.to_datetime(ibes_data['time_avail_m'])

# Convert forecast period end dates to datetime
ibes_data['fpedats'] = pd.to_datetime(ibes_data['fpedats'])

# Rename ticker to match IBES convention
ibes_data = ibes_data.rename(columns={'ticker': 'tickerIBES'})

# Remove unnecessary measure column
ibes_data = ibes_data.drop('measure', axis=1)

# Clean data by removing missing estimates and keeping latest monthly observations
initial_count = len(ibes_data)
ibes_data = ibes_data.dropna(subset=['meanest'])
print(f"Removed {initial_count - len(ibes_data)} records with missing meanest")

# Keep only the latest estimate for each ticker/forecast period/month combination
ibes_data = ibes_data.sort_values(['tickerIBES', 'fpi', 'time_avail_m', 'statpers'])
ibes_data = ibes_data.drop_duplicates(['tickerIBES', 'fpi', 'time_avail_m'], keep='last')

print(f"After keeping last obs per month: {len(ibes_data)} records")

# Save final dataset
ibes_data.to_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet", index=False)

print(f"IBES EPS Unadjusted data saved with {len(ibes_data)} records")

# Display summary statistics and data preview
print("\nRecords by FPI (Forecast Period Indicator):")
fpi_counts = ibes_data['fpi'].value_counts().sort_index()
print(fpi_counts)

print(f"\nDate range: {ibes_data['time_avail_m'].min()} to {ibes_data['time_avail_m'].max()}")

print("\nSample data:")
print(ibes_data.head())
