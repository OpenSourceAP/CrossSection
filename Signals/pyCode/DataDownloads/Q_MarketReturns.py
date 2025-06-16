#!/usr/bin/env python3
"""
Market Returns data download script - Python equivalent of Q_MarketReturns.do

Downloads monthly equal- and value-weighted market returns from CRSP.
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
SELECT date, vwretd, ewretd, usdval
FROM crsp.msi
"""

market_data = pd.read_sql_query(QUERY, conn)
conn.close()

# Ensure directories exist
os.makedirs("../Data/Intermediate", exist_ok=True)

# Convert date to monthly period (equivalent to gen time_avail_m = mofd(date))
market_data['date'] = pd.to_datetime(market_data['date'])
market_data['time_avail_m'] = market_data['date'].dt.to_period('M')

# Drop original date column
market_data = market_data.drop('date', axis=1)

# Save the data
market_data.to_pickle("../Data/Intermediate/monthlyMarket.pkl")

print(f"Monthly Market Returns downloaded with {len(market_data)} records")

# Show date range and sample data
print(f"Date range: {market_data['time_avail_m'].min()} to {market_data['time_avail_m'].max()}")
print("\nSample data:")
print(market_data.head())

# Show summary statistics
print(f"\nSummary statistics:")
print(f"Value-weighted return - Mean: {market_data['vwretd'].mean():.4f}, Std: {market_data['vwretd'].std():.4f}")
print(f"Equal-weighted return - Mean: {market_data['ewretd'].mean():.4f}, Std: {market_data['ewretd'].std():.4f}")