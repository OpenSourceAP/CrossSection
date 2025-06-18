#!/usr/bin/env python3
"""
S&P Credit Ratings data download script - Python equivalent of X_SPCreditRatings.do

Downloads S&P credit ratings and converts to numerical scale.
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
SELECT gvkey, datadate, splticrm
FROM comp.adsprate
"""

rating_data = pd.read_sql_query(QUERY, conn)
conn.close()

print("Downloaded {len(rating_data)} credit rating records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Create monthly time variable
rating_data['datadate'] = pd.to_datetime(rating_data['datadate'])
rating_data['time_avail_m'] = rating_data['datadate'].dt.to_period('M')
rating_data = rating_data.drop('datadate', axis=1)

# Rename splticrm to sp for easier reference
rating_data = rating_data.rename(columns={'splticrm': 'sp'})

# Create numerical rating (higher number = better rating)
rating_map = {
    'D': 1,
    'C': 2,
    'CC': 3,
    'CCC-': 4,
    'CCC': 5,
    'CCC+': 6,
    'B-': 7,
    'B': 8,
    'B+': 9,
    'BB-': 10,
    'BB': 11,
    'BB+': 12,
    'BBB-': 13,
    'BBB': 14,
    'BBB+': 15,
    'A-': 16,
    'A': 17,
    'A+': 18,
    'AA-': 19,
    'AA': 20,
    'AA+': 21,
    'AAA': 22
}

# Apply rating mapping
rating_data['credrat'] = rating_data['sp'].map(rating_map).fillna(0)

# Drop sp column
rating_data = rating_data.drop('sp', axis=1)

# Convert gvkey to numeric
rating_data['gvkey'] = pd.to_numeric(rating_data['gvkey'], errors='coerce')

# Save the data
rating_data.to_pickle("../pyData/Intermediate/m_SP_creditratings.pkl")

print("S&P Credit Ratings data saved with {len(rating_data)} records")

# Show summary statistics
print("Date range: {rating_data['time_avail_m'].min()} to {rating_data['time_avail_m'].max()}")
print("Unique companies: {rating_data['gvkey'].nunique()}")

print("\nCredit rating distribution:")
rating_dist = rating_data['credrat'].value_counts().sort_index()
rating_labels = {v: k for k, v in rating_map.items()}
for rating_num, count in rating_dist.items():
    label = rating_labels.get(rating_num, 'Unknown ({rating_num})')
    print("  {rating_num} ({label}): {count:,}")

print("\nSample data:")
print(rating_data.head())
