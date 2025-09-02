# ABOUTME: ZH1_OptionVolume.py downloads OptionMetricsVolume data from WRDS 
# ABOUTME: and makes pyData/Intermediate/OptionMetricsVolume.parquet
"""
Usage:
    python3 DataDownloads/ZH1_OptionVolume.py

Outputs:
    - pyData/Intermediate/OptionMetricsVolume.parquet

Philosphy is: Option volume is generally useful for working with the option data. So we download the whole thing and use it elsewhere. 
"""

import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

tic = time.time()
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.*
FROM optionm.opvold as a
where a.cp_flag != 'NaN'
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Read from WRDS database
print("Downloading option volume data from WRDS. Takes 5 to 10 minutes...")
opvold0 = pd.read_sql_query(QUERY, engine)

engine.dispose()

toc = time.time()
print(f"Time taken: {(toc - tic) / 60:.2f} minutes")

#%%

# enforce proper types
opvold = opvold0.copy()

opvold = standardize_columns(opvold, "OptionMetricsVolume")

# save to parquet
opvold.to_parquet("../pyData/Intermediate/OptionMetricsVolume.parquet", index=False)

print(f"Saved OptionMetricsVolume.parquet: {len(opvold)} records")
