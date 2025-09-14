# ABOUTME: Downloads Pastor-Stambaugh monthly liquidity factor from WRDS French library
# ABOUTME: Creates time_avail_m variable for monthly liquidity data
"""
Inputs:
- ff.liq_ps table from WRDS (date, ps_innov columns)

Outputs:
- ../pyData/Intermediate/monthlyLiquidity.parquet

How to run: python3 R_MonthlyLiquidityFactor.py
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

# Query Pastor-Stambaugh liquidity factor data
QUERY = """
SELECT date, ps_innov
FROM ff.liq_ps
"""

if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Download liquidity factor data
liquidity_data = pd.read_sql_query(QUERY, engine)

# Convert date to monthly time_avail_m variable
liquidity_data['date'] = pd.to_datetime(liquidity_data['date'])
liquidity_data['time_avail_m'] = liquidity_data['date'].dt.to_period('M').dt.to_timestamp()

# Remove original date column
liquidity_data = liquidity_data.drop('date', axis=1)

# Save data
liquidity_data.to_parquet("../pyData/Intermediate/monthlyLiquidity.parquet")

# Display summary statistics
print(f"Monthly Liquidity Factor downloaded with {len(liquidity_data)} records")
print(f"Date range: {liquidity_data['time_avail_m'].min()} to {liquidity_data['time_avail_m'].max()}")
print("\nSample data:")
print(liquidity_data.head())
print("\nLiquidity factor summary:")
print(f"Mean: {liquidity_data['ps_innov'].mean():.6f}")
print(f"Std: {liquidity_data['ps_innov'].std():.6f}")
