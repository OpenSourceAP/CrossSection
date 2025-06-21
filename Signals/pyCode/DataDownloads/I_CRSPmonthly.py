#!/usr/bin/env python3
"""
CRSP Monthly data download script - Python equivalent of I_CRSPmonthly.do

Downloads CRSP monthly stock file (MSF) with company names and delisting info.
"""

import os
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv

print("=" * 60, flush=True)
print("📊 I_CRSPmonthly.py - CRSP Monthly Stock Data", flush=True)
print("=" * 60, flush=True)

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

crsp_data = pd.read_sql_query(QUERY, conn)
conn.close()

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Export for R processing (equivalent to CSV export in Stata)
crsp_data.to_csv("../pyData/Intermediate/mCRSP.csv", index=False)

# Make 2 digit SIC
crsp_data['sicCRSP'] = crsp_data['siccd']
crsp_data['sic2D'] = crsp_data['sicCRSP'].astype(str).str[:2]

# Convert back to numeric, handling non-numeric values
crsp_data['sic2D'] = pd.to_numeric(crsp_data['sic2D'], errors='coerce')
crsp_data['sicCRSP'] = pd.to_numeric(crsp_data['sicCRSP'], errors='coerce')

# Create monthly date (equivalent to Stata's mofd function)
crsp_data['date'] = pd.to_datetime(crsp_data['date'])
crsp_data['time_avail_m'] = crsp_data['date'].dt.to_period('M')

# Drop original date column
crsp_data = crsp_data.drop('date', axis=1)

# Incorporate delisting return
# Replace missing dlret with -0.35 for specific delisting codes on NYSE/AMEX
mask1 = (crsp_data['dlret'].isna() &
         ((crsp_data['dlstcd'] == 500) |
          ((crsp_data['dlstcd'] >= 520) & (crsp_data['dlstcd'] <= 584))) &
         ((crsp_data['exchcd'] == 1) | (crsp_data['exchcd'] == 2)))
crsp_data.loc[mask1, 'dlret'] = -0.35

# Replace missing dlret with -0.55 for NASDAQ (exchcd == 3)
mask2 = (crsp_data['dlret'].isna() &
         ((crsp_data['dlstcd'] == 500) |
          ((crsp_data['dlstcd'] >= 520) & (crsp_data['dlstcd'] <= 584))) &
         (crsp_data['exchcd'] == 3))
crsp_data.loc[mask2, 'dlret'] = -0.55

# Cap delisting return at -1
crsp_data.loc[(crsp_data['dlret'] < -1) & crsp_data['dlret'].notna(), 'dlret'] = -1

# Fill remaining missing dlret with 0
crsp_data['dlret'] = crsp_data['dlret'].fillna(0)

# Update returns to incorporate delisting returns
# Handle case where ret < -1 (updated in 2022 02)
crsp_data['ret'] = (1 + crsp_data['ret']) * (1 + crsp_data['dlret']) - 1

# Use dlret if ret is missing but dlret is not zero
mask3 = crsp_data['ret'].isna() & (crsp_data['dlret'] != 0)
crsp_data.loc[mask3, 'ret'] = crsp_data.loc[mask3, 'dlret']

# Compute market value of equity
# Converting units (shares in thousands, volume in ten-thousands)
crsp_data['shrout'] = crsp_data['shrout'] / 1000
crsp_data['vol'] = crsp_data['vol'] / 10000

# Market value = Common shares outstanding * |Price|
crsp_data['mve_c'] = crsp_data['shrout'] * np.abs(crsp_data['prc'])

# Housekeeping - drop columns
crsp_data = crsp_data.drop(['dlret', 'dlstcd', 'permco'], axis=1)

# Save the data
crsp_data.to_parquet("../pyData/Intermediate/monthlyCRSP.parquet")

print(f"CRSP Monthly data downloaded with {len(crsp_data)} records", flush=True)
print(f"Date range: {crsp_data['time_avail_m'].min()} to {crsp_data['time_avail_m'].max()}", flush=True)
print("=" * 60, flush=True)
print("✅ I_CRSPmonthly.py completed successfully", flush=True)
print("=" * 60, flush=True)
