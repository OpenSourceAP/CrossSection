# ABOUTME: Downloads monthly Fama-French factors from WRDS including market, size, value and momentum factors
# ABOUTME: Processes date column and applies column standardization for consistency with other datasets
"""
Inputs:
- ff.factors_monthly (WRDS database)

Outputs:
- ../pyData/Intermediate/monthlyFF.parquet

How to run: python3 FamaFrenchMonthly.py
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

# Create database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@"
    f"wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Define query for monthly Fama-French factors
QUERY = """
SELECT date, mktrf, smb, hml, rf, umd
FROM ff.factors_monthly
"""

# Apply row limit if in debug mode
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Download the data
ff_monthly = pd.read_sql_query(QUERY, engine)

# Process date column to create time_avail_m
ff_monthly['date'] = pd.to_datetime(ff_monthly['date'])
ff_monthly['time_avail_m'] = ff_monthly['date'].dt.to_period('M').dt.to_timestamp()

# Remove original date column
ff_monthly = ff_monthly.drop('date', axis=1)

# Save processed data
ff_monthly.to_parquet("../pyData/Intermediate/monthlyFF.parquet")

# Display processing results
print(f"Monthly Fama-French factors downloaded with {len(ff_monthly)} records")
print(f"Date range: {ff_monthly['time_avail_m'].min()} to {ff_monthly['time_avail_m'].max()}")
print("\nSample data:")
print(ff_monthly.head())
