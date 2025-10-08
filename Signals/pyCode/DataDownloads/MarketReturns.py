# ABOUTME: Downloads monthly equal- and value-weighted market returns from CRSP market summary index
# ABOUTME: Converts dates to monthly timestamp format and saves as standardized parquet file
"""
Inputs:
- crsp.msi (Market Summary Index)

Outputs:
- ../pyData/Intermediate/monthlyMarket.parquet

How to run: python3 MarketReturns.py
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

# Connect to WRDS database
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@"
    f"wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Query for market returns data
QUERY = """
SELECT date, vwretd, ewretd, usdval
FROM crsp.msi
"""

# Apply debug row limit if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Download market returns data
market_data = pd.read_sql_query(QUERY, engine)


# Convert date to monthly timestamp format
market_data['date'] = pd.to_datetime(market_data['date'])
market_data['time_avail_m'] = market_data['date'].dt.to_period('M').dt.to_timestamp()

# Remove original date column
market_data = market_data.drop('date', axis=1)

# Save data
market_data.to_parquet("../pyData/Intermediate/monthlyMarket.parquet")

# Display summary information
print(f"Monthly Market Returns downloaded with {len(market_data)} records")
print(f"Date range: {market_data['time_avail_m'].min()} to {market_data['time_avail_m'].max()}")
print("\nSample data:")
print(market_data.head())
print("\nSummary statistics:")
print(f"Value-weighted return - Mean: {market_data['vwretd'].mean():.4f}, Std: {market_data['vwretd'].std():.4f}")
print(f"Equal-weighted return - Mean: {market_data['ewretd'].mean():.4f}, Std: {market_data['ewretd'].std():.4f}")
