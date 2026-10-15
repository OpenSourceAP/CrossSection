# ABOUTME: Downloads monthly Fama-French factors from WRDS including market, size, value and momentum factors
# ABOUTME: Processes date column and applies column standardization for consistency with other datasets
"""
Inputs:
- ff.factors_monthly (WRDS database)

Outputs:
- ../pyData/Intermediate/monthlyFF.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/FamaFrenchMonthly.py

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

DEBUG_ROWS = get_debug_row_limit("FamaFrenchMonthly")

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@"
    f"wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain market, size, value, momentum, and risk-free returns for monthly factor models.
QUERY = """
SELECT date, mktrf, smb, hml, rf, umd
FROM ff.factors_monthly
"""

# Apply row limit if in debug mode
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

ff_monthly = pd.read_sql_query(QUERY, engine)

# Align factor observations with the monthly calendar used by signals.
ff_monthly['date'] = pd.to_datetime(ff_monthly['date'])
ff_monthly['time_avail_m'] = ff_monthly['date'].dt.to_period('M').dt.to_timestamp()

ff_monthly = ff_monthly.drop('date', axis=1)

# Save monthly factors for downstream return calculations.
ff_monthly.to_parquet("../pyData/Intermediate/monthlyFF.parquet")

print(f"Monthly Fama-French factors downloaded with {len(ff_monthly)} records")
print(f"Date range: {ff_monthly['time_avail_m'].min()} to {ff_monthly['time_avail_m'].max()}")
print("\nSample data:")
print(ff_monthly.head())
