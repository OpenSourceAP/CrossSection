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
from sqlalchemy import create_engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()


# Load OptionMetrics linking data from WRDS database
print("Downloading OptionMetrics-CRSP linking data from WRDS...")

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Query WRDS database for OptionMetrics linking data
QUERY = """
SELECT secid, sdate, edate, permno, score
FROM wrdsapps_link_crsp_optionm.opcrsphist as a
WHERE permno is not null
"""

# Read linking data from WRDS
omlink = pd.read_sql_query(QUERY, engine)
print(f"Loaded {len(omlink)} OptionMetrics linking records from WRDS")

engine.dispose()

# Save raw linking table
omlink.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet", index=False)

print(f"OptionMetrics linking data saved with {len(omlink)} records")
print(f"Head: {omlink.head()}")