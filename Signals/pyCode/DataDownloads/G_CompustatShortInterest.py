#!/usr/bin/env python3
"""
Compustat Short Interest data download script - Python equivalent of G_CompustatShortInterest.do

Downloads short interest data with monthly aggregation.
Data reported bi-weekly with 4-day lag; using mid-month observation for real-time availability.
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
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM comp.sec_shortint as a
"""

si_data = pd.read_sql_query(QUERY, conn)
conn.close()

print("Downloaded {len(si_data)} short interest records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Create monthly time variable
si_data['datadate'] = pd.to_datetime(si_data['datadate'])
si_data['time_avail_m'] = si_data['datadate'].dt.to_period('M')

# Collapse to monthly data using first non-missing values
# (equivalent to gcollapse (firstnm) shortint shortintadj, by(gvkey time_avail_m))
# Using mid-month observation for real-time availability
def first_non_missing(series):
    """Return first non-missing value"""
    non_missing = series.dropna()
    return non_missing.iloc[0] if len(non_missing) > 0 else None

monthly_si = si_data.groupby(['gvkey', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing
}).reset_index()

print("After monthly aggregation: {len(monthly_si)} records")

# Convert gvkey to numeric
monthly_si['gvkey'] = pd.to_numeric(monthly_si['gvkey'], errors='coerce')

# Save the data
monthly_si.to_pickle("../pyData/Intermediate/monthlyShortInterest.pkl")

print("Monthly Short Interest data saved with {len(monthly_si)} records")

# Show summary statistics
print("Date range: {monthly_si['time_avail_m'].min()} to {monthly_si['time_avail_m'].max()}")
print("Unique companies: {monthly_si['gvkey'].nunique()}")

print("\nSample data:")
print(monthly_si.head())

# Show missing data summary
print("\nMissing data:")
print("shortint: {monthly_si['shortint'].isna().sum()} missing")
print("shortintadj: {monthly_si['shortintadj'].isna().sum()} missing")
