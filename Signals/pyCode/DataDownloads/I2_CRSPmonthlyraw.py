# ABOUTME: Downloads CRSP monthly data WITHOUT delisting return adjustments for testing
# ABOUTME: Python equivalent of I2_CRSPmonthlyraw.do
# Inputs: CRSP database via WRDS
# Outputs: monthlyCRSPraw.parquet in ../pyData/Intermediate/
# Run: python DataDownloads/I2_CRSPmonthlyraw.py

import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.permno, a.permco, a.date, a.ret, a.retx, a.vol, a.shrout, a.prc, a.cfacshr, a.bidlo, a.askhi,
       b.shrcd, b.exchcd, b.siccd, b.ticker, b.shrcls,
       c.dlstcd, c.dlret
FROM crsp.msf as a
LEFT JOIN crsp.msenames as b
ON a.permno=b.permno AND b.namedt<=a.date AND a.date<=b.nameendt
LEFT JOIN crsp.msedelist as c
ON a.permno=c.permno AND date_trunc('month', a.date) = date_trunc('month', c.dlstdt)
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

crsp_raw = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(crsp_raw)} CRSP raw monthly records")


# Handle string columns that should be empty strings instead of NaN (to match Stata behavior)
# In Stata, missing string values appear as empty strings, not NaN
string_columns = ['ticker', 'shrcls']
for col in string_columns:
    if col in crsp_raw.columns:
        crsp_raw[col] = crsp_raw[col].fillna('')

# Make 2 digit SIC (rename siccd to sicCRSP like in Stata)
crsp_raw['sicCRSP'] = crsp_raw['siccd']
crsp_raw['sic2D'] = crsp_raw['sicCRSP'].astype(str).str[:2]

# Convert back to numeric, handling non-numeric values
crsp_raw['sic2D'] = pd.to_numeric(crsp_raw['sic2D'], errors='coerce')
crsp_raw['sicCRSP'] = pd.to_numeric(crsp_raw['sicCRSP'], errors='coerce')

# Drop original siccd column (equivalent to Stata's rename)
crsp_raw = crsp_raw.drop('siccd', axis=1)

# Create monthly date (equivalent to mofd function)
crsp_raw['date'] = pd.to_datetime(crsp_raw['date'])
# Convert to monthly timestamp to match Stata datetime format
crsp_raw['time_avail_m'] = crsp_raw['date'].dt.to_period('M').dt.to_timestamp()
# Ensure it's properly datetime64[ns] format
crsp_raw['time_avail_m'] = pd.to_datetime(crsp_raw['time_avail_m'])

# Drop original date column
crsp_raw = crsp_raw.drop('date', axis=1)

# Compute market value of equity
# Converting units (shares in thousands, volume in ten-thousands)
crsp_raw['shrout'] = crsp_raw['shrout'] / 1000
crsp_raw['vol'] = crsp_raw['vol'] / 10000

# Market value = Common shares outstanding * |Price|
crsp_raw['mve_c'] = crsp_raw['shrout'] * np.abs(crsp_raw['prc'])

# Housekeeping - drop columns (note: NOT processing delisting returns)
crsp_raw = crsp_raw.drop(['dlret', 'dlstcd', 'permco'], axis=1)


# Save processed data to parquet
crsp_raw.to_parquet("../pyData/Intermediate/monthlyCRSPraw.parquet")

print(f"CRSP Monthly Raw data saved with {len(crsp_raw)} records")
print(f"Date range: {crsp_raw['time_avail_m'].min()} to {crsp_raw['time_avail_m'].max()}")
print("Note: This is raw data WITHOUT delisting return adjustments")
