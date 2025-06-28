#!/usr/bin/env python3
"""
Compustat Business Segments data download script - Python equivalent of E_CompustatBusinessSegments.do

Downloads Compustat business segment data from the WRDS merged segments file.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("🏢 E_CompustatBusinessSegments.py - Business Segment Data", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.gvkey, a.datadate, a.stype, a.sid, a.sales, a.srcdate, a.naicsh, a.sics1, a.snms
FROM compseg.wrds_segmerged as a
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

segments_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(segments_data)} business segment records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Convert columns to numeric (equivalent to destring gvkey sics1 naicsh, replace)
segments_data['gvkey'] = pd.to_numeric(segments_data['gvkey'], errors='coerce')
segments_data['sics1'] = pd.to_numeric(segments_data['sics1'], errors='coerce')
segments_data['naicsh'] = pd.to_numeric(segments_data['naicsh'], errors='coerce')

# Convert date columns to datetime format to match Stata output
segments_data['datadate'] = pd.to_datetime(segments_data['datadate'])
segments_data['srcdate'] = pd.to_datetime(segments_data['srcdate'])

# Apply IBES Pattern: Convert None/NaN to empty string for string columns (snms)
# This matches Stata's treatment of missing string values
segments_data['snms'] = segments_data['snms'].fillna('')

# Save the data
segments_data.to_parquet("../pyData/Intermediate/CompustatSegments.parquet")

print(f"Compustat Business Segments data saved with {len(segments_data)} records")

# Show summary statistics
print("\nSegment types:")
if 'stype' in segments_data.columns:
    print(segments_data['stype'].value_counts())

print("\nDate range:")
if 'datadate' in segments_data.columns:
    print(f"  {segments_data['datadate'].min().strftime('%Y-%m-%d')} to {segments_data['datadate'].max().strftime('%Y-%m-%d')}")

print(f"\nUnique companies: {segments_data['gvkey'].nunique()}")

# Sample data
print("\nSample data:", flush=True)
print(segments_data.head(), flush=True)
print("=" * 60, flush=True)
print("✅ E_CompustatBusinessSegments.py completed successfully", flush=True)
print("=" * 60, flush=True)
