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

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_ROOT
from utils.debug_mode import log_selection
from utils.wrds_connection import get_wrds_engine

(DATA_ROOT / 'Intermediate').mkdir(parents=True, exist_ok=True)

log_selection("OptionMetricsCRSPLink")
load_dotenv()

print("Downloading OptionMetrics-CRSP linking data from WRDS...")

# Obtain the stock links, validity dates, and match scores needed to join option data.
QUERY = """
SELECT secid, sdate, edate, permno, score
FROM wrdsapps_link_crsp_optionm.opcrsphist as a
WHERE permno is not null
"""

engine = get_wrds_engine()
try:
    omlink = pd.read_sql_query(QUERY, engine)
finally:
    engine.dispose()
print(f"Loaded {len(omlink)} OptionMetrics linking records from WRDS")

# Reject missing or repeated link identities before downstream option-stock joins.
key = ["secid", "permno", "sdate"]
if omlink[key].isna().any().any():
    raise ValueError(f"OptionMetrics-CRSP link has null key values: {key}")
duplicate_count = int(omlink.duplicated(key, keep=False).sum())
if duplicate_count:
    raise ValueError(
        f"OptionMetrics-CRSP link has {duplicate_count} rows with duplicate {key} keys"
    )

# Save validated option-stock link histories with their original dates and match scores.
omlink.to_parquet(DATA_ROOT / 'Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet', index=False)

print(f"OptionMetrics linking data saved with {len(omlink)} records")
print(f"Head: {omlink.head()}")
