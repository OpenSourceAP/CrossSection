# ABOUTME: Downloads S&P credit ratings from Compustat and converts text ratings to numerical scale
# ABOUTME: Creates time_avail_m monthly variable and saves gvkey-month level credit rating data
"""
Inputs:
- comp.adsprate (gvkey, datadate, splticrm)

Outputs:
- ../pyData/Intermediate/m_SP_creditratings.parquet

How to run: python3 SPCreditRatings.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

# Connect to WRDS database
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Download S&P credit ratings from Compustat
QUERY = """
SELECT gvkey, datadate, splticrm
FROM comp.adsprate
"""

if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

rating_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(rating_data)} credit rating records")

# Convert datadate to monthly time variable
rating_data['datadate'] = pd.to_datetime(rating_data['datadate'])
rating_data['time_avail_m'] = rating_data['datadate'].dt.to_period('M').dt.to_timestamp()
rating_data = rating_data.drop('datadate', axis=1)

# Rename column for easier reference
rating_data = rating_data.rename(columns={'splticrm': 'sp'})

# Define rating to numerical mapping (higher number = better rating)
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

# Convert text ratings to numerical scale
rating_data['credrat'] = rating_data['sp'].map(rating_map).fillna(0)
rating_data = rating_data.drop('sp', axis=1)

# Clean data types
rating_data['gvkey'] = pd.to_numeric(rating_data['gvkey'], errors='coerce')
rating_data['credrat'] = rating_data['credrat'].astype('int8')

# Save data
rating_data.to_parquet("../pyData/Intermediate/m_SP_creditratings.parquet")

print(f"S&P Credit Ratings data saved with {len(rating_data)} records")

# Display summary statistics
print(f"Date range: {rating_data['time_avail_m'].min()} to {rating_data['time_avail_m'].max()}")
print(f"Unique companies: {rating_data['gvkey'].nunique()}")

print("\nCredit rating distribution:")
rating_dist = rating_data['credrat'].value_counts().sort_index()
rating_labels = {v: k for k, v in rating_map.items()}
for rating_num, count in rating_dist.items():
    label = rating_labels.get(rating_num, f'Unknown ({rating_num})')
    print(f"  {rating_num} ({label}): {count:,}")

print("\nSample data:")
print(rating_data.head())
