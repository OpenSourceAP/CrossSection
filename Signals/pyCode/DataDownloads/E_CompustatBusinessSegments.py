#!/usr/bin/env python3
"""
Compustat Business Segments data download script - Python equivalent of E_CompustatBusinessSegments.do

Downloads Compustat business segment data from the WRDS merged segments file.
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
SELECT a.gvkey, a.datadate, a.stype, a.sid, a.sales, a.srcdate, a.naicsh, a.sics1, a.snms
FROM compseg.wrds_segmerged as a
"""

segments_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(segments_data)} business segment records")

# Ensure directories exist
os.makedirs("../Data/Intermediate", exist_ok=True)

# Convert columns to numeric (equivalent to destring gvkey sics1 naicsh, replace)
segments_data['gvkey'] = pd.to_numeric(segments_data['gvkey'], errors='coerce')
segments_data['sics1'] = pd.to_numeric(segments_data['sics1'], errors='coerce')
segments_data['naicsh'] = pd.to_numeric(segments_data['naicsh'], errors='coerce')

# Save the data
segments_data.to_pickle("../Data/Intermediate/CompustatSegments.pkl")

print(f"Compustat Business Segments data saved with {len(segments_data)} records")

# Show summary statistics
print(f"\nSegment types:")
if 'stype' in segments_data.columns:
    print(segments_data['stype'].value_counts())

print(f"\nDate range:")
if 'datadate' in segments_data.columns:
    segments_data['datadate'] = pd.to_datetime(segments_data['datadate'])
    print(f"  {segments_data['datadate'].min().strftime('%Y-%m-%d')} to {segments_data['datadate'].max().strftime('%Y-%m-%d')}")

print(f"\nUnique companies: {segments_data['gvkey'].nunique()}")

# Sample data
print("\nSample data:")
print(segments_data.head())