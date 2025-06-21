#!/usr/bin/env python3
"""
Compustat Business Segments data download script - Python equivalent of E_CompustatBusinessSegments.do

Downloads Compustat business segment data from the WRDS merged segments file.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

print("=" * 60, flush=True)
print("🏢 E_CompustatBusinessSegments.py - Business Segment Data", flush=True)
print("=" * 60, flush=True)

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
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Convert columns to numeric (equivalent to destring gvkey sics1 naicsh, replace)
segments_data['gvkey'] = pd.to_numeric(segments_data['gvkey'], errors='coerce')
segments_data['sics1'] = pd.to_numeric(segments_data['sics1'], errors='coerce')
segments_data['naicsh'] = pd.to_numeric(segments_data['naicsh'], errors='coerce')

# Save the data
segments_data.to_parquet("../pyData/Intermediate/CompustatSegments.parquet")

print(f"Compustat Business Segments data saved with {len(segments_data)} records")

# Show summary statistics
print("\nSegment types:")
if 'stype' in segments_data.columns:
    print(segments_data['stype'].value_counts())

print("\nDate range:")
if 'datadate' in segments_data.columns:
    segments_data['datadate'] = pd.to_datetime(segments_data['datadate'])
    print("  {segments_data['datadate'].min().strftime('%Y-%m-%d')} to {segments_data['datadate'].max().strftime('%Y-%m-%d')}")

print("\nUnique companies: {segments_data['gvkey'].nunique()}")

# Sample data
print("\nSample data:", flush=True)
print(segments_data.head(), flush=True)
print("=" * 60, flush=True)
print("✅ E_CompustatBusinessSegments.py completed successfully", flush=True)
print("=" * 60, flush=True)
