# ABOUTME: Downloads the WRDS OptionMetrics-CRSP history link.
# ABOUTME: Checks its comparison key and saves the raw linking table.
"""
Inputs:
- wrdsapps_link_crsp_optionm.opcrsphist (WRDS database)
- OPENAP_DATA_ROOT (optional output root; defaults to Signals/pyData)

Outputs:
- <data root>/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet

How to run: from the project root, python3 Signals/pyCode/DataDownloads/OptionMetricsCRSPLink.py
The link source has no separate CIZ table; DEBUG_MODE still reads full history.
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.debug_mode import log_selection
from utils.wrds_connection import get_wrds_engine, release_wrds_engine
from utils.download_paths import intermediate_path

log_selection("OptionMetricsCRSPLink")
load_dotenv()


# Load OptionMetrics linking data from WRDS database
print("Downloading OptionMetrics-CRSP linking data from WRDS...")

# Query WRDS database for OptionMetrics linking data
QUERY = """
SELECT secid, sdate, edate, permno, score
FROM wrdsapps_link_crsp_optionm.opcrsphist as a
WHERE permno is not null
"""

# Read linking data from WRDS
engine = get_wrds_engine()
try:
    omlink = pd.read_sql_query(QUERY, engine)
finally:
    release_wrds_engine(engine)
print(f"Loaded {len(omlink)} OptionMetrics linking records from WRDS")

key = ["secid", "permno", "sdate"]
if omlink[key].isna().any().any():
    raise ValueError(f"OptionMetrics-CRSP link has null key values: {key}")
duplicate_count = int(omlink.duplicated(key, keep=False).sum())
if duplicate_count:
    raise ValueError(
        f"OptionMetrics-CRSP link has {duplicate_count} rows with duplicate {key} keys"
    )

# Save raw linking table
omlink.to_parquet(intermediate_path("OPTIONMETRICSCRSPLinkingTable.parquet"), index=False)

print(f"OptionMetrics linking data saved with {len(omlink)} records")
print(f"Head: {omlink.head()}")
