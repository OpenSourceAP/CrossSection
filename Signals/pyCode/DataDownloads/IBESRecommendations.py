# ABOUTME: Downloads IBES analyst recommendations data from WRDS with recommendation codes 1-5
# ABOUTME: Processes announcement dates and creates monthly time availability for recommendation tracking
"""
Inputs:
- ibes.recddet from WRDS (US firms only)

Outputs:
- ../pyData/Intermediate/IBES_Recommendations.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/IBESRecommendations.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("IBESRecommendations")

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain analyst recommendation events for the US-firm sample.
QUERY = """
SELECT a.ticker, a.estimid, a.ereccd, a.etext, a.ireccd, a.itext, a.emaskcd,
       a.amaskcd, a.anndats, actdats
FROM ibes.recddet as a
WHERE a.usfirm = '1'
"""

# Add row limit for debugging if configured
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

rec_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(rec_data)} IBES recommendation records")

# Retain recommendation events with a usable numeric recommendation code.
rec_data['ireccd'] = pd.to_numeric(rec_data['ireccd'], errors='coerce')
initial_count = len(rec_data)
rec_data = rec_data.dropna(subset=['ireccd'])
print(f"Removed {initial_count - len(rec_data)} records with missing ireccd")

# Distinguish IBES tickers from identifiers supplied by other datasets.
rec_data = rec_data.rename(columns={'ticker': 'tickerIBES'})

# Preserve announcement and activation dates for timing recommendation events.
rec_data['anndats'] = pd.to_datetime(rec_data['anndats'])
rec_data['actdats'] = pd.to_datetime(rec_data['actdats'])

# Represent absent source recommendation codes consistently as empty text.
rec_data['ereccd'] = rec_data['ereccd'].fillna('')

# Assign each recommendation to its announcement month for monthly signal calculations.
rec_data['time_avail_m'] = rec_data['anndats'].dt.to_period('M').dt.to_timestamp()
rec_data['time_avail_m'] = pd.to_datetime(rec_data['time_avail_m'])

# Put linking identifiers, event dates, and the recommendation measure first in the saved data.
key_columns = ['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd']
other_columns = [col for col in rec_data.columns if col not in key_columns]
columns_order = key_columns + other_columns
rec_data = rec_data[columns_order]

# Save recommendation events with monthly linking dates for downstream signals.
rec_data.to_parquet("../pyData/Intermediate/IBES_Recommendations.parquet", index=False)

print(f"IBES Recommendations data saved with {len(rec_data)} records")

print("\nRecommendation distribution:")
rec_counts = rec_data['ireccd'].value_counts().sort_index()
rec_labels = {1: 'Strong Buy', 2: 'Buy', 3: 'Hold', 4: 'Underperform', 5: 'Sell'}
for code, count in rec_counts.items():
    label = rec_labels.get(int(code), f'Unknown ({int(code)})')
    print(f"  {int(code)} ({label}): {count:,}")

print(f"\nDate range: {rec_data['time_avail_m'].min()} to {rec_data['time_avail_m'].max()}")

print("\nSample data:")
print(rec_data[['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd']].head())
