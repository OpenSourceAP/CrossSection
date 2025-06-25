#!/usr/bin/env python3
"""
Daily Fama-French factors download script - Python equivalent of O_Daily_Fama-French.do

Downloads daily Fama-French factors from WRDS.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("📈 O_Daily_Fama-French.py - Daily Fama-French Factors", flush=True)
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
SELECT date, mktrf, smb, hml, rf, umd
FROM ff.factors_daily
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

ff_daily = pd.read_sql_query(QUERY, conn)
conn.close()

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Rename date to time_d (equivalent to Stata rename)
ff_daily = ff_daily.rename(columns={'date': 'time_d'})

# Ensure time_d is datetime64[ns] to match DTA format (not date32[day])
ff_daily['time_d'] = pd.to_datetime(ff_daily['time_d'])

# Save the data
ff_daily.to_parquet("../pyData/Intermediate/dailyFF.parquet")

print(f"Daily Fama-French factors downloaded with {len(ff_daily)} records", flush=True)

# Show date range and sample data
print(f"Date range: {ff_daily['time_d'].min().strftime('%Y-%m-%d')} to {ff_daily['time_d'].max().strftime('%Y-%m-%d')}", flush=True)
print("\nSample data:", flush=True)
print(ff_daily.head(), flush=True)
print("=" * 60, flush=True)
print("✅ O_Daily_Fama-French.py completed successfully", flush=True)
print("=" * 60, flush=True)
