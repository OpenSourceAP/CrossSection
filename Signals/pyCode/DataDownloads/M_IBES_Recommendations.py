#!/usr/bin/env python3
"""
IBES Recommendations data download script - Python equivalent of M_IBES_Recommendations.do

Downloads IBES analyst recommendations from WRDS.
Recommendation codes: 1=Strong Buy, 2=Buy, 3=Hold, 4=Underperform, 5=Sell

Reference: https://www.tilburguniversity.edu/sites/default/files/download/IBESonWRDS_2.pdf
Note: This data only begins in 1993, while some studies use Zack's going back to 1985
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
)

QUERY = """
SELECT a.ticker, a.estimid, a.ereccd, a.etext, a.ireccd, a.itext, a.emaskcd, 
       a.amaskcd, a.anndats, actdats
FROM ibes.recddet as a
WHERE a.usfirm = '1'
"""

rec_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(rec_data)} IBES recommendation records")

# Ensure directories exist
os.makedirs("../Data/Intermediate", exist_ok=True)

# Convert ireccd to numeric and drop missing values
rec_data['ireccd'] = pd.to_numeric(rec_data['ireccd'], errors='coerce')
initial_count = len(rec_data)
rec_data = rec_data.dropna(subset=['ireccd'])
print(f"Removed {initial_count - len(rec_data)} records with missing ireccd")

# Clean up and rename
rec_data = rec_data.rename(columns={'ticker': 'tickerIBES'})

# Convert anndats to datetime and create time_avail_m
rec_data['anndats'] = pd.to_datetime(rec_data['anndats'])
rec_data['time_avail_m'] = rec_data['anndats'].dt.to_period('M')

# Reorder columns to put important stuff first
columns_order = ['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd'] + \
                [col for col in rec_data.columns if col not in ['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd']]
rec_data = rec_data[columns_order]

# Save the data
rec_data.to_pickle("../Data/Intermediate/IBES_Recommendations.pkl")

print(f"IBES Recommendations data saved with {len(rec_data)} records")

# Show summary statistics
print("\nRecommendation distribution:")
rec_counts = rec_data['ireccd'].value_counts().sort_index()
rec_labels = {1: 'Strong Buy', 2: 'Buy', 3: 'Hold', 4: 'Underperform', 5: 'Sell'}
for code, count in rec_counts.items():
    label = rec_labels.get(int(code), f'Unknown ({int(code)})')
    print(f"  {int(code)} ({label}): {count:,}")

# Show date range
print(f"\nDate range: {rec_data['time_avail_m'].min()} to {rec_data['time_avail_m'].max()}")

# Sample data
print("\nSample data:")
print(rec_data[['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd']].head())