# ABOUTME: Downloads CIQ credit ratings from entity, instrument, and security ratings tables
# ABOUTME: Aggregates ratings data by gvkey and date, mapping ratings to numeric scale and tracking downgrades
"""
Inputs:
- ciq.wrds_erating (entity ratings)
- ciq.wrds_irating (instrument ratings) 
- ciq.wrds_srating (security ratings)
- ciq.ratings_ids (linking table)

Outputs:
- ../pyData/Intermediate/m_CIQ_creditratings.parquet

How to run: python3 X2_CIQCreditRatings.py
"""

# Import libraries and setup environment

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

# Download CIQ credit ratings data from WRDS
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

# Download entity ratings from wrds_erating table
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
    
    # Fill in missing columns for consistency across rating types
    entity_ratings['instrument_id'] = ''
    entity_ratings['security_id'] = ''
        
except Exception as e:
    print(f"Error downloading entity ratings: {e}")

# Download instrument ratings from wrds_irating table
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
    
    # Fill in missing columns for consistency across rating types
    instrument_ratings['entity_id'] = ''
    instrument_ratings['security_id'] = ''
        
except Exception as e:
    print(f"Error downloading instrument ratings: {e}")

# Download security ratings from wrds_srating table
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
    
    # Fill in missing columns for consistency across rating types
    security_ratings['entity_id'] = ''
    security_ratings['instrument_id'] = ''
        
except Exception as e:
    print(f"Error downloading security ratings: {e}")

engine.dispose()

# Process and aggregate ratings data

# Define mapping from rating symbols to numeric values for aggregation
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
    return (
        df
        # Create helper columns: map ratings to numbers and flag downgrades
        .assign(
            currentratingnum=lambda d: d['currentratingsymbol']
                                          .map(rating_map)
                                          .fillna(0),
            anydowngrade   =lambda d: d['ratingactionword']
                                          .eq('Downgrade')
                                          .astype(int)
        )
        # Aggregate by gvkey and rating date
        .groupby(['gvkey', 'ratingdate'], as_index=False)
        .agg(
            currentratingnum=('currentratingnum', 'mean'),
            anydowngrade   =('anydowngrade',   'max')
        )
        # Tag with source identifier
        .assign(source=source_id)
    )

# Apply aggregation function to each rating table
entity_agg, instrument_agg, security_agg = [
    collapse_ratings(df, src)
    for df, src in zip(
        [entity_ratings, instrument_ratings, security_ratings],
        [1, 2, 3]       # Source codes: 1=Entity, 2=Instrument, 3=Security
    )
]

# Combine all rating sources
ratings_agg = pd.concat([entity_agg, instrument_agg, security_agg], ignore_index=True)

# Clean and finalize the data

# For each gvkey-ratingdate combination, keep the best source (entity=1 preferred over instrument=2 over security=3)
ratings = ratings_agg.sort_values(['gvkey', 'ratingdate', 'source'])
ratings = ratings.drop_duplicates(subset=['gvkey', 'ratingdate'], keep='first')
print(f"After removing date duplicates: {len(ratings)} records")

# Save the processed data
ratings.to_parquet("../pyData/Intermediate/m_CIQ_creditratings.parquet", index=False)

print(f"CIQ Credit Ratings data saved with {len(ratings)} records")
print(f"Date range: {ratings['ratingdate'].min()} to {ratings['ratingdate'].max()}")

# Display summary statistics
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

