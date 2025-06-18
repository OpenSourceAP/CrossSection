#!/usr/bin/env python3
"""
IBES EPS Unadjusted data download script - Python equivalent of L_IBES_EPS_Unadj.do

Downloads IBES EPS estimates (unadjusted for splits) from WRDS.
Focus on FPI 0 (long-term growth), 1 (next year), 2 (year after), and 6 (current quarter).

Doc: https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/i-b-e-s/ibes-estimates/general/wrds-overview-ibes/
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
)

QUERY = """
SELECT a.ticker, a.statpers, a.measure, a.fpi, a.numest, a.medest,
       a.meanest, a.stdev, a.fpedats
FROM ibes.statsumu_epsus as a
WHERE a.fpi = '0' or a.fpi = '1' or a.fpi = '2' or a.fpi = '6'
"""

ibes_data = pd.read_sql_query(QUERY, conn)
conn.close()

print("Downloaded {len(ibes_data)} IBES EPS records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Set up linking variables
ibes_data['statpers'] = pd.to_datetime(ibes_data['statpers'])
ibes_data['time_avail_m'] = ibes_data['statpers'].dt.to_period('M')

# Rename ticker to tickerIBES
ibes_data = ibes_data.rename(columns={'ticker': 'tickerIBES'})

# Drop measure column (not needed)
ibes_data = ibes_data.drop('measure', axis=1)

# Keep last obs each month - first remove rows with missing meanest
initial_count = len(ibes_data)
ibes_data = ibes_data.dropna(subset=['meanest'])
print("Removed {initial_count - len(ibes_data)} records with missing meanest")

# Sort and keep last observation for each tickerIBES/fpi/time_avail_m combination
# (equivalent to sort tickerIBES fpi time_avail_m statpers; by tickerIBES fpi time_avail_m: keep if _n == _N)
ibes_data = ibes_data.sort_values(['tickerIBES', 'fpi', 'time_avail_m', 'statpers'])
ibes_data = ibes_data.drop_duplicates(['tickerIBES', 'fpi', 'time_avail_m'], keep='last')

print("After keeping last obs per month: {len(ibes_data)} records")

# Save the data
ibes_data.to_pickle("../pyData/Intermediate/IBES_EPS_Unadj.pkl")

print("IBES EPS Unadjusted data saved with {len(ibes_data)} records")

# Show summary by FPI
print("\nRecords by FPI (Forecast Period Indicator):")
fpi_counts = ibes_data['fpi'].value_counts().sort_index()
print(fpi_counts)

# Show date range
print("\nDate range: {ibes_data['time_avail_m'].min()} to {ibes_data['time_avail_m'].max()}")

# Sample data
print("\nSample data:")
print(ibes_data.head())
