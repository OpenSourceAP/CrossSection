#!/usr/bin/env python3
"""
CIQ Credit Ratings data download script - Python equivalent of X2_CIQCreditRatings.do

Downloads CIQ credit ratings from entity, instrument, and security ratings tables.
Extends coverage beyond Compustat ratings which end in 2017.

this guy was hand-coded by andrew since the stata code needed significant improvements
"""

#%%
# setup

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine



load_dotenv()


"""Main function to download and process CIQ credit ratings"""
print("Downloading CIQ Credit Ratings...")
print("Warning: this can take ~5 minutes to run.")

# Create SQLAlchemy engine with timeouts
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds",
    connect_args={
        "connect_timeout": 30,  # 30 second connection timeout
        "options": "-c statement_timeout=300000"  # 5 minute query timeout
    }
)

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)


#%%

# Download entity ratings (like Stata's first query)
print("Downloading entity ratings...")
entity_query = """
SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.entity_id
FROM ciq.wrds_erating a
LEFT JOIN ciq.ratings_ids b
ON a.entity_id = b.entity_id
WHERE b.gvkey IS NOT NULL
AND a.ratingdate >= '1970-01-01'
"""

if MAX_ROWS_DL > 0:
    entity_query += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting entity query to {MAX_ROWS_DL} rows")

try:
    start_time = time.time()
    entity_ratings = pd.read_sql_query(entity_query, engine)
    print(f"Downloaded {len(entity_ratings)} entity rating records in {time.time() - start_time:.1f} seconds")
    
    # Fill in missing columns (like Stata's gen str6 commands)
    entity_ratings['instrument_id'] = ''
    entity_ratings['security_id'] = ''
        
except Exception as e:
    print(f"Error downloading entity ratings: {e}")


# Download instrument ratings (like Stata's second query)
print("Downloading instrument ratings...")
instrument_query = """
SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.instrument_id
FROM ciq.wrds_irating a
LEFT JOIN ciq.ratings_ids b
ON a.instrument_id = b.instrument_id
WHERE b.gvkey IS NOT NULL
AND a.ratingdate >= '1970-01-01'
"""

if MAX_ROWS_DL > 0:
    instrument_query += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting instrument query to {MAX_ROWS_DL} rows")

try:
    start_time = time.time()
    instrument_ratings = pd.read_sql_query(instrument_query, engine)
    print(f"Downloaded {len(instrument_ratings)} instrument rating records in {time.time() - start_time:.1f} seconds")
    
    # Fill in missing columns
    instrument_ratings['entity_id'] = ''
    instrument_ratings['security_id'] = ''
        
except Exception as e:
    print(f"Error downloading instrument ratings: {e}")

# Download security ratings (like Stata's third query)
print("Downloading security ratings...")
security_query = """
SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.security_id
FROM ciq.wrds_srating a
LEFT JOIN ciq.ratings_ids b
ON a.security_id = b.security_id
WHERE b.gvkey IS NOT NULL
AND a.ratingdate >= '1970-01-01'
"""

if MAX_ROWS_DL > 0:
    security_query += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting security query to {MAX_ROWS_DL} rows")

try:
    start_time = time.time()
    security_ratings = pd.read_sql_query(security_query, engine)
    print(f"Downloaded {len(security_ratings)} security rating records in {time.time() - start_time:.1f} seconds")
    
    # Fill in missing columns
    security_ratings['entity_id'] = ''
    security_ratings['instrument_id'] = ''
        
except Exception as e:
    print(f"Error downloading security ratings: {e}")

engine.dispose()

#%%
# clean and collapse (new, not in stata)

# define stuff for collapsing (taking means and maxes)
rating_map = {
    "D":   1,
    "C":   2,
    "CC":  3,
    "CCC-":4,
    "CCC": 5,
    "CCC+":6,
    "B-":  7,
    "B":   8,
    "B+":  9,
    "BB-":10,
    "BB": 11,
    "BB+":12,
    "BBB-":13,
    "BBB":14,
    "BBB+":15,
    "A-": 16,
    "A":  17,
    "A+": 18,
    "AA-":19,
    "AA": 20,
    "AA+":21,
    "AAA":22
}

def collapse_ratings(df: pd.DataFrame, source_id: int) -> pd.DataFrame:
    """
    • Map ratings to numbers (missing → 0)  
    • Flag downgrades as 0/1  
    • Collapse to (gvkey, ratingdate) with the desired aggregates  
    • Tag the provenance with `source_id`
    """
    return (
        df
        # 1️⃣ create helper columns
        .assign(
            currentratingnum=lambda d: d['currentratingsymbol']
                                          .map(rating_map)
                                          .fillna(0),
            anydowngrade   =lambda d: d['ratingactionword']
                                          .eq('Downgrade')
                                          .astype(int)
        )
        # 2️⃣ aggregate
        .groupby(['gvkey', 'ratingdate'], as_index=False)
        .agg(
            currentratingnum=('currentratingnum', 'mean'),
            anydowngrade   =('anydowngrade',   'max')
        )
        # 3️⃣ mark the source
        .assign(source=source_id)
    )

# --- run it for each table ----------------------------------------------------
entity_agg, instrument_agg, security_agg = [
    collapse_ratings(df, src)
    for df, src in zip(
        [entity_ratings, instrument_ratings, security_ratings],
        [1, 2, 3]       # ← your source codes
    )
]

# Concatenate
ratings_agg = pd.concat([entity_agg, instrument_agg, security_agg], ignore_index=True)

#%%
# finishing up

# For each gvkey-ratingdate, keep the best source 
ratings = ratings_agg.sort_values(['gvkey', 'ratingdate', 'source'])
ratings = ratings.drop_duplicates(subset=['gvkey', 'ratingdate'], keep='first')
print(f"After removing date duplicates: {len(ratings)} records")

# note: stata code converted to time_avail_m, but this led to some inconsistencies with the use of stale data. Mom6mJunk.do for example filled all missing ciq credit ratings with the most recent obs, but it did not do this for the S&P credit ratings. We should revisit this and CredRatDG. These are the only two signals that use this data.


# Save the data
# skip standardizing (does not make sense, we're ignoring stata)
ratings.to_parquet("../pyData/Intermediate/m_CIQ_creditratings.parquet", index=False)

print(f"CIQ Credit Ratings data saved with {len(ratings)} records")
print(f"Date range: {ratings['ratingdate'].min()} to {ratings['ratingdate'].max()}")

# Show source distribution
print("\nSource distribution:")
source_dist = ratings['source'].value_counts().sort_index()
source_labels = {1: 'Entity', 2: 'Instrument', 3: 'Security'}
for source, count in source_dist.items():
    if isinstance(source, (int, float)):
        source_int = int(source)
        label = source_labels.get(source_int, f'Unknown ({source})')
        print(f"  {source} ({label}): {count:,}")

print("\nSample data:")
print(ratings.head())

