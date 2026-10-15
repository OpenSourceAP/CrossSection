# ABOUTME: Downloads daily Fama-French factors from WRDS
# ABOUTME: Processes and saves to parquet format for cross-section analysis
"""
Inputs:
- ff.factors_daily (WRDS database table)

Outputs:
- ../pyData/Intermediate/dailyFF.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/FamaFrenchDaily.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("FamaFrenchDaily")

print("=" * 60, flush=True)
print("📈 FamaFrenchDaily.py - Daily Fama-French Factors", flush=True)
print("=" * 60, flush=True)

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@"
    f"wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain market, size, value, momentum, and risk-free returns for daily factor models.
QUERY = """
SELECT date, mktrf, smb, hml, rf, umd
FROM ff.factors_daily
"""

# Add row limit for debugging if configured
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

ff_daily = pd.read_sql_query(QUERY, engine)

# Use the standard daily date field so factor observations can be joined to stock data.
ff_daily = ff_daily.rename(columns={'date': 'time_d'})

ff_daily['time_d'] = pd.to_datetime(ff_daily['time_d'])

# Save daily factors in the format used by downstream return calculations.
ff_daily.to_parquet("../pyData/Intermediate/dailyFF.parquet")

print(f"Daily Fama-French factors downloaded with {len(ff_daily)} records", flush=True)
print(f"Date range: {ff_daily['time_d'].min().strftime('%Y-%m-%d')} to {ff_daily['time_d'].max().strftime('%Y-%m-%d')}", flush=True)
print("\nSample data:", flush=True)
print(ff_daily.head(), flush=True)
print("=" * 60, flush=True)
print("✅ FamaFrenchDaily.py completed successfully", flush=True)
print("=" * 60, flush=True)
