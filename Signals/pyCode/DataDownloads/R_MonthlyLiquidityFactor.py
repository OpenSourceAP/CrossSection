#!/usr/bin/env python3
"""
Monthly Liquidity Factor download script - Python equivalent of R_MonthlyLiquidityFactor.do

Downloads monthly liquidity factor (Pastor-Stambaugh) from WRDS.
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

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@"
    f"wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT date, ps_innov
FROM ff.liq_ps
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

liquidity_data = pd.read_sql_query(QUERY, engine)

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Convert date to monthly datetime (preserve as datetime64[ns] for parquet compatibility)
liquidity_data['date'] = pd.to_datetime(liquidity_data['date'])
# Keep as datetime64[ns] instead of Period to maintain type compatibility with DTA format
liquidity_data['time_avail_m'] = liquidity_data['date'].dt.to_period('M').dt.to_timestamp()

# Drop original date column
liquidity_data = liquidity_data.drop('date', axis=1)

# Save the data
liquidity_data.to_parquet("../pyData/Intermediate/monthlyLiquidity.parquet")

print(f"Monthly Liquidity Factor downloaded with {len(liquidity_data)} records")

# Show date range and sample data
print(f"Date range: {liquidity_data['time_avail_m'].min()} to {liquidity_data['time_avail_m'].max()}")
print("\nSample data:")
print(liquidity_data.head())

# Show summary statistics
print("\nLiquidity factor summary:")
print(f"Mean: {liquidity_data['ps_innov'].mean():.6f}")
print(f"Std: {liquidity_data['ps_innov'].std():.6f}")
