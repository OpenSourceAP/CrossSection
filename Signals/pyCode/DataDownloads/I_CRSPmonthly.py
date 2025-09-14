# ABOUTME: Downloads CRSP monthly stock data with company names and delisting information
# ABOUTME: Processes returns incorporating delisting returns and computes market value of equity
"""
Inputs:
- crsp.msf (CRSP monthly stock file)
- crsp.msenames (CRSP stock names)
- crsp.msedelist (CRSP delisting information)

Outputs:
- ../pyData/Intermediate/monthlyCRSP.parquet

How to run: python3 I_CRSPmonthly.py
"""

import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("📊 I_CRSPmonthly.py - CRSP Monthly Stock Data", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Set up database connection to WRDS
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# SQL query to get CRSP monthly data with company names and delisting info
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

# Download data from WRDS
crsp_data = pd.read_sql_query(QUERY, engine)
engine.dispose()


# Handle missing string values to match Stata behavior (empty strings instead of NaN)
string_columns = ['ticker', 'shrcls']
for col in string_columns:
    crsp_data[col] = crsp_data[col].fillna('')

# Process SIC codes: rename siccd to sicCRSP and create 2-digit SIC
crsp_data['sicCRSP'] = crsp_data['siccd']
crsp_data['sic2D'] = crsp_data['sicCRSP'].astype(str).str[:2]
crsp_data['sic2D'] = pd.to_numeric(crsp_data['sic2D'], errors='coerce')
crsp_data['sicCRSP'] = pd.to_numeric(crsp_data['sicCRSP'], errors='coerce')
crsp_data = crsp_data.drop('siccd', axis=1)

# Convert date to monthly timestamp (equivalent to Stata's mofd function)
crsp_data['date'] = pd.to_datetime(crsp_data['date'])
crsp_data['time_avail_m'] = crsp_data['date'].dt.to_period('M').dt.to_timestamp()
crsp_data = crsp_data.drop('date', axis=1)

# Preserve original returns before delisting adjustment
crsp_data['ret_b4_dl'] = crsp_data['ret']

# Process delisting returns with exchange-specific defaults
mask1 = (crsp_data['dlret'].isna() &
         ((crsp_data['dlstcd'] == 500) |
          ((crsp_data['dlstcd'] >= 520) & (crsp_data['dlstcd'] <= 584))) &
         ((crsp_data['exchcd'] == 1) | (crsp_data['exchcd'] == 2)))
crsp_data.loc[mask1, 'dlret'] = -0.35

mask2 = (crsp_data['dlret'].isna() &
         ((crsp_data['dlstcd'] == 500) |
          ((crsp_data['dlstcd'] >= 520) & (crsp_data['dlstcd'] <= 584))) &
         (crsp_data['exchcd'] == 3))
crsp_data.loc[mask2, 'dlret'] = -0.55

crsp_data.loc[(crsp_data['dlret'] < -1) & crsp_data['dlret'].notna(), 'dlret'] = -1
crsp_data['dlret'] = crsp_data['dlret'].fillna(0)

# Incorporate delisting returns into main returns
crsp_data['ret'] = (1 + crsp_data['ret']) * (1 + crsp_data['dlret']) - 1
mask3 = crsp_data['ret'].isna() & (crsp_data['dlret'] != 0)
crsp_data.loc[mask3, 'ret'] = crsp_data.loc[mask3, 'dlret']

# Convert units and compute market value of equity
crsp_data['shrout'] = crsp_data['shrout'] / 1000
crsp_data['vol'] = crsp_data['vol'] / 10000
crsp_data['mve_c'] = crsp_data['shrout'] * np.abs(crsp_data['prc'])

# Clean up unnecessary columns
crsp_data = crsp_data.drop(['dlret', 'dlstcd', 'permco'], axis=1)

# Save final dataset
crsp_data.to_parquet("../pyData/Intermediate/monthlyCRSP.parquet", index=False)

print(f"CRSP Monthly data downloaded with {len(crsp_data)} records", flush=True)
print(f"Date range: {crsp_data['time_avail_m'].min()} to {crsp_data['time_avail_m'].max()}", flush=True)
print("=" * 60, flush=True)
print("✅ I_CRSPmonthly.py completed successfully", flush=True)
print("=" * 60, flush=True)
