# ABOUTME: Downloads and processes Compustat business segment data from WRDS
# ABOUTME: Converts data types and applies column standardization to match expected format
"""
Inputs:
- compseg.wrds_segmerged (WRDS database)

Outputs:
- ../pyData/Intermediate/CompustatSegments.parquet

How to run: python3 E_CompustatBusinessSegments.py
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

# Load environment variables for database connection
load_dotenv()

# Create database connection to WRDS
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Define SQL query to extract business segment data
QUERY = """
SELECT a.gvkey, a.datadate, a.stype, a.sid, a.sales, a.srcdate, a.naicsh, a.sics1, a.snms
FROM compseg.wrds_segmerged as a
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Execute query and download data
segments_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(segments_data)} business segment records")


# Convert numeric columns from string to numeric format
segments_data['gvkey'] = pd.to_numeric(segments_data['gvkey'], errors='coerce')
segments_data['sics1'] = pd.to_numeric(segments_data['sics1'], errors='coerce')
segments_data['naicsh'] = pd.to_numeric(segments_data['naicsh'], errors='coerce')

# Convert date columns to datetime format
segments_data['datadate'] = pd.to_datetime(segments_data['datadate'])
segments_data['srcdate'] = pd.to_datetime(segments_data['srcdate'])

# Handle missing string values by converting NaN to empty strings
segments_data['snms'] = segments_data['snms'].fillna('')

# Save data
segments_data.to_parquet("../pyData/Intermediate/CompustatSegments.parquet")

print(f"Compustat Business Segments data saved with {len(segments_data)} records")

# Display summary statistics and sample data
print("\nSegment types:")
print(segments_data['stype'].value_counts())

print("\nDate range:")
print(f"  {segments_data['datadate'].min().strftime('%Y-%m-%d')} to {segments_data['datadate'].max().strftime('%Y-%m-%d')}")

print(f"\nUnique companies: {segments_data['gvkey'].nunique()}")

print("\nSample data:", flush=True)
print(segments_data.head(), flush=True)
print("=" * 60, flush=True)
print("✅ E_CompustatBusinessSegments.py completed successfully", flush=True)
print("=" * 60, flush=True)
