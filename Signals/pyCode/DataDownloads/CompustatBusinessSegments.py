# ABOUTME: Downloads and processes Compustat business segment data from WRDS
# ABOUTME: Converts data types and applies column standardization to match expected format
"""
Inputs:
- compseg.wrds_segmerged (WRDS database)

Outputs:
- ../pyData/Intermediate/CompustatSegments.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/CompustatBusinessSegments.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("CompustatBusinessSegments")

print("=" * 60, flush=True)
print("🏢 CompustatBusinessSegments.py - Business Segment Data", flush=True)
print("=" * 60, flush=True)

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain segment sales and industry classifications for measuring company diversification.
QUERY = """
SELECT a.gvkey, a.datadate, a.stype, a.sid, a.sales, a.srcdate, a.naicsh, a.sics1, a.snms
FROM compseg.wrds_segmerged as a
"""

# Add row limit for debugging if configured
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

segments_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(segments_data)} business segment records")

# Make company and industry identifiers numeric, treating invalid values as missing.
segments_data['gvkey'] = pd.to_numeric(segments_data['gvkey'], errors='coerce')
segments_data['sics1'] = pd.to_numeric(segments_data['sics1'], errors='coerce')
segments_data['naicsh'] = pd.to_numeric(segments_data['naicsh'], errors='coerce')

# Preserve both report and source dates for selecting segment information over time.
segments_data['datadate'] = pd.to_datetime(segments_data['datadate'])
segments_data['srcdate'] = pd.to_datetime(segments_data['srcdate'])

# Represent absent segment names consistently as empty text.
segments_data['snms'] = segments_data['snms'].fillna('')

# Save segment-level sales and classifications for downstream signals.
segments_data.to_parquet("../pyData/Intermediate/CompustatSegments.parquet")

print(f"Compustat Business Segments data saved with {len(segments_data)} records")

print("\nSegment types:")
print(segments_data['stype'].value_counts())

print("\nDate range:")
print(f"  {segments_data['datadate'].min().strftime('%Y-%m-%d')} to {segments_data['datadate'].max().strftime('%Y-%m-%d')}")

print(f"\nUnique companies: {segments_data['gvkey'].nunique()}")

print("\nSample data:", flush=True)
print(segments_data.head(), flush=True)
print("=" * 60, flush=True)
print("✅ CompustatBusinessSegments.py completed successfully", flush=True)
print("=" * 60, flush=True)
