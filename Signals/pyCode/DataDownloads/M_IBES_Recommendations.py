# ABOUTME: Downloads IBES analyst recommendations data from WRDS with recommendation codes 1-5
# ABOUTME: Processes announcement dates and creates monthly time availability for recommendation tracking
"""
Inputs:
- ibes.recddet from WRDS (US firms only)

Outputs:
- ../pyData/Intermediate/IBES_Recommendations.parquet

How to run: python3 M_IBES_Recommendations.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

# Connect to WRDS database
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Query IBES recommendation detail data for US firms only
QUERY = """
SELECT a.ticker, a.estimid, a.ereccd, a.etext, a.ireccd, a.itext, a.emaskcd,
       a.amaskcd, a.anndats, actdats
FROM ibes.recddet as a
WHERE a.usfirm = '1'
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Download recommendation data
rec_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(rec_data)} IBES recommendation records")

# Clean recommendation codes - convert to numeric and drop missing values
rec_data['ireccd'] = pd.to_numeric(rec_data['ireccd'], errors='coerce')
initial_count = len(rec_data)
rec_data = rec_data.dropna(subset=['ireccd'])
print(f"Removed {initial_count - len(rec_data)} records with missing ireccd")

# Rename ticker column to distinguish from other ticker fields
rec_data = rec_data.rename(columns={'ticker': 'tickerIBES'})

# Convert date columns to datetime format
rec_data['anndats'] = pd.to_datetime(rec_data['anndats'])
rec_data['actdats'] = pd.to_datetime(rec_data['actdats'])

# Fill missing earnings recommendation codes with empty strings
rec_data['ereccd'] = rec_data['ereccd'].fillna('')

# Create monthly time availability variable from announcement date
rec_data['time_avail_m'] = rec_data['anndats'].dt.to_period('M').dt.to_timestamp()
rec_data['time_avail_m'] = pd.to_datetime(rec_data['time_avail_m'])

# Reorder columns with key variables first
columns_order = ['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd'] + \
                [col for col in rec_data.columns if col not in ['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd']]
rec_data = rec_data[columns_order]

# Save data
rec_data.to_parquet("../pyData/Intermediate/IBES_Recommendations.parquet", index=False)

print(f"IBES Recommendations data saved with {len(rec_data)} records")

# Display recommendation code distribution
print("\nRecommendation distribution:")
rec_counts = rec_data['ireccd'].value_counts().sort_index()
rec_labels = {1: 'Strong Buy', 2: 'Buy', 3: 'Hold', 4: 'Underperform', 5: 'Sell'}
for code, count in rec_counts.items():
    label = rec_labels.get(int(code), f'Unknown ({int(code)})')
    print(f"  {int(code)} ({label}): {count:,}")

# Display data date range and sample
print(f"\nDate range: {rec_data['time_avail_m'].min()} to {rec_data['time_avail_m'].max()}")

# Sample data
print("\nSample data:")
print(rec_data[['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd']].head())
