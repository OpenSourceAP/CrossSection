#!/usr/bin/env python3
"""
CRSP Monthly Raw data download script - Python equivalent of I2_CRSPmonthlyraw.do

Downloads CRSP monthly data WITHOUT delisting return adjustments for testing.
"""

import os
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
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

crsp_raw = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(crsp_raw)} CRSP raw monthly records")

# Ensure directories exist
os.makedirs("../Data/Intermediate", exist_ok=True)

# Make 2 digit SIC
crsp_raw['sicCRSP'] = crsp_raw['siccd']
crsp_raw['sic2D'] = crsp_raw['sicCRSP'].astype(str).str[:2]

# Convert back to numeric, handling non-numeric values
crsp_raw['sic2D'] = pd.to_numeric(crsp_raw['sic2D'], errors='coerce')
crsp_raw['sicCRSP'] = pd.to_numeric(crsp_raw['sicCRSP'], errors='coerce')

# Create monthly date (equivalent to mofd function)
crsp_raw['date'] = pd.to_datetime(crsp_raw['date'])
crsp_raw['time_avail_m'] = crsp_raw['date'].dt.to_period('M')

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

# Save the data
crsp_raw.to_pickle("../Data/Intermediate/monthlyCRSPraw.pkl")

print(f"CRSP Monthly Raw data saved with {len(crsp_raw)} records")
print(f"Date range: {crsp_raw['time_avail_m'].min()} to {crsp_raw['time_avail_m'].max()}")
print("Note: This is raw data WITHOUT delisting return adjustments")