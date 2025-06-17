#!/usr/bin/env python3
"""
Monthly Fama-French factors download script - Python equivalent of P_Monthly_Fama-French.do

Downloads monthly Fama-French factors from WRDS.
"""

import os
import psycopg2
import pandas as pd
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
SELECT date, mktrf, smb, hml, rf, umd
FROM ff.factors_monthly
"""

ff_monthly = pd.read_sql_query(QUERY, conn)
conn.close()

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Convert date to monthly period (equivalent to gen time_avail_m = mofd(date))
ff_monthly['date'] = pd.to_datetime(ff_monthly['date'])
ff_monthly['time_avail_m'] = ff_monthly['date'].dt.to_period('M')

# Drop original date column
ff_monthly = ff_monthly.drop('date', axis=1)

# Save the data
ff_monthly.to_pickle("../pyData/Intermediate/monthlyFF.pkl")

print(f"Monthly Fama-French factors downloaded with {len(ff_monthly)} records")

# Show date range and sample data
print(f"Date range: {ff_monthly['time_avail_m'].min()} to {ff_monthly['time_avail_m'].max()}")
print("\nSample data:")
print(ff_monthly.head())