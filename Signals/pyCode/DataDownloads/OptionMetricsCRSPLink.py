# ABOUTME: Downloads raw OptionMetrics-CRSP linking data from WRDS
# ABOUTME: Saves the raw linking table without any processing
"""
Inputs:
- wrdsapps_link_crsp_optionm.opcrsphist (WRDS database)

Outputs:
- ../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet

How to run: python3 OptionMetricsCRSPLink.py
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

engine = get_wrds_engine()

# Query WRDS database for OptionMetrics linking data
QUERY = """
SELECT secid, sdate, edate, permno, score
FROM wrdsapps_link_crsp_optionm.opcrsphist as a
WHERE permno is not null
"""

# Read linking data from WRDS
omlink = pd.read_sql_query(QUERY, engine)
print(f"Loaded {len(omlink)} OptionMetrics linking records from WRDS")

release_wrds_engine(engine)

# Save raw linking table
omlink.to_parquet(intermediate_path("OPTIONMETRICSCRSPLinkingTable.parquet"), index=False)

print(f"OptionMetrics linking data saved with {len(omlink)} records")
print(f"Head: {omlink.head()}")