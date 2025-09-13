# ABOUTME: Downloads daily Fama-French factors from WRDS
# ABOUTME: Processes and saves to parquet format for cross-section analysis
"""
Inputs:
- ff.factors_daily (WRDS database table)

Outputs:
- ../pyData/Intermediate/dailyFF.parquet

How to run: python3 O_Daily_Fama-French.py
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

print("=" * 60, flush=True)
print("📈 O_Daily_Fama-French.py - Daily Fama-French Factors", flush=True)
print("=" * 60, flush=True)

# Load environment variables for WRDS credentials
load_dotenv()

# Create database connection to WRDS
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@"
    f"wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Define SQL query to get daily Fama-French factors
QUERY = """
SELECT date, mktrf, smb, hml, rf, umd
FROM ff.factors_daily
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Download daily Fama-French factors from WRDS
ff_daily = pd.read_sql_query(QUERY, engine)

# Create output directory if it doesn't exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Rename date column to time_d for consistency
ff_daily = ff_daily.rename(columns={'date': 'time_d'})

# Convert time_d to datetime format
ff_daily['time_d'] = pd.to_datetime(ff_daily['time_d'])

# Apply column standardization and save to parquet
ff_daily = standardize_columns(ff_daily, 'dailyFF')
ff_daily.to_parquet("../pyData/Intermediate/dailyFF.parquet")

# Print summary statistics
print(f"Daily Fama-French factors downloaded with {len(ff_daily)} records", flush=True)
print(f"Date range: {ff_daily['time_d'].min().strftime('%Y-%m-%d')} to {ff_daily['time_d'].max().strftime('%Y-%m-%d')}", flush=True)
print("\nSample data:", flush=True)
print(ff_daily.head(), flush=True)
print("=" * 60, flush=True)
print("✅ O_Daily_Fama-French.py completed successfully", flush=True)
print("=" * 60, flush=True)
