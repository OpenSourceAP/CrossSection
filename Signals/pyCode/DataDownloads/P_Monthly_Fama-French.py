#!/usr/bin/env python3
"""
Monthly Fama-French factors download script - Python equivalent of P_Monthly_Fama-French.do

Downloads monthly Fama-French factors from WRDS.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@"
    f"wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT date, mktrf, smb, hml, rf, umd
FROM ff.factors_monthly
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

ff_monthly = pd.read_sql_query(QUERY, engine)

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Convert date to monthly datetime (preserve as datetime64[ns] for parquet compatibility)
ff_monthly['date'] = pd.to_datetime(ff_monthly['date'])
# Keep as datetime64[ns] instead of Period to maintain type compatibility with DTA format
ff_monthly['time_avail_m'] = ff_monthly['date'].dt.to_period('M').dt.to_timestamp()

# Drop original date column
ff_monthly = ff_monthly.drop('date', axis=1)

# Apply column standardization
ff_monthly = standardize_columns(ff_monthly, 'monthlyFF')
# Save the data
ff_monthly.to_parquet("../pyData/Intermediate/monthlyFF.parquet")

print(f"Monthly Fama-French factors downloaded with {len(ff_monthly)} records")

# Show date range and sample data
print(f"Date range: {ff_monthly['time_avail_m'].min()} to {ff_monthly['time_avail_m'].max()}")
print("\nSample data:")
print(ff_monthly.head())
