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

How to run: from Signals/pyCode, run python3 DataDownloads/CIQCreditRatings.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("CIQCreditRatings")

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Download CIQ credit ratings data from WRDS
print("Downloading CIQ Credit Ratings...")
print("Warning: this can take ~5 minutes to run.")

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds",
    connect_args={
        "connect_timeout": 30,  # 30 second connection timeout
        "options": "-c statement_timeout=300000"  # 5 minute query timeout
    }
)

os.makedirs("../pyData/Intermediate", exist_ok=True)

# Obtain company-level ratings, the preferred source for each company-date.
print("Downloading entity ratings...")
entity_query = """
SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.entity_id
FROM ciq.wrds_erating a
LEFT JOIN ciq.ratings_ids b
ON a.entity_id = b.entity_id
WHERE b.gvkey IS NOT NULL
AND a.ratingdate >= '1970-01-01'
"""

if DEBUG_MODE:
    entity_query += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting entity query to {DEBUG_ROWS} rows")

try:
    start_time = time.time()
    entity_ratings = pd.read_sql_query(entity_query, engine)
    print(f"Downloaded {len(entity_ratings)} entity rating records in {time.time() - start_time:.1f} seconds")

    # Give all rating sources the same identifier fields before combining them.
    entity_ratings['instrument_id'] = ''
    entity_ratings['security_id'] = ''

except Exception as e:
    print(f"Error downloading entity ratings: {e}")

# Obtain instrument ratings to cover dates without a company-level rating.
print("Downloading instrument ratings...")
instrument_query = """
SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.instrument_id
FROM ciq.wrds_irating a
LEFT JOIN ciq.ratings_ids b
ON a.instrument_id = b.instrument_id
WHERE b.gvkey IS NOT NULL
AND a.ratingdate >= '1970-01-01'
"""

if DEBUG_MODE:
    instrument_query += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting instrument query to {DEBUG_ROWS} rows")

try:
    start_time = time.time()
    instrument_ratings = pd.read_sql_query(instrument_query, engine)
    print(f"Downloaded {len(instrument_ratings)} instrument rating records in {time.time() - start_time:.1f} seconds")

    # Give all rating sources the same identifier fields before combining them.
    instrument_ratings['entity_id'] = ''
    instrument_ratings['security_id'] = ''

except Exception as e:
    print(f"Error downloading instrument ratings: {e}")

# Obtain security ratings as the final source of company-date coverage.
print("Downloading security ratings...")
security_query = """
SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.security_id
FROM ciq.wrds_srating a
LEFT JOIN ciq.ratings_ids b
ON a.security_id = b.security_id
WHERE b.gvkey IS NOT NULL
AND a.ratingdate >= '1970-01-01'
"""

if DEBUG_MODE:
    security_query += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting security query to {DEBUG_ROWS} rows")

try:
    start_time = time.time()
    security_ratings = pd.read_sql_query(security_query, engine)
    print(f"Downloaded {len(security_ratings)} security rating records in {time.time() - start_time:.1f} seconds")

    # Give all rating sources the same identifier fields before combining them.
    security_ratings['entity_id'] = ''
    security_ratings['instrument_id'] = ''

except Exception as e:
    print(f"Error downloading security ratings: {e}")

engine.dispose()

# Put all rating sources on the same scale, with larger values indicating better credit.
rating_map = {
    "D": 1,
    "C": 2,
    "CC": 3,
    "CCC-": 4,
    "CCC": 5,
    "CCC+": 6,
    "B-": 7,
    "B": 8,
    "B+": 9,
    "BB-": 10,
    "BB": 11,
    "BB+": 12,
    "BBB-": 13,
    "BBB": 14,
    "BBB+": 15,
    "A-": 16,
    "A": 17,
    "A+": 18,
    "AA-": 19,
    "AA": 20,
    "AA+": 21,
    "AAA": 22
}


def collapse_ratings(df: pd.DataFrame, source_id: int) -> pd.DataFrame:
    """Provide one average rating and any-downgrade indicator per company-date."""
    ratings = df.copy()

    # Put ratings on a common scale; missing or unrecognized symbols receive code 0.
    ratings['currentratingnum'] = ratings['currentratingsymbol'].map(rating_map).fillna(0)
    ratings['anydowngrade'] = (ratings['ratingactionword'] == 'Downgrade').astype(int)

    # Average all ratings from this source and retain any downgrade on the date.
    company_date_groups = ratings.groupby(['gvkey', 'ratingdate'], as_index=False)
    daily_ratings = company_date_groups.agg(
        currentratingnum=('currentratingnum', 'mean'),
        anydowngrade=('anydowngrade', 'max'),
    )
    daily_ratings['source'] = source_id
    return daily_ratings


# Summarize each source separately before choosing company-date coverage.
entity_agg = collapse_ratings(entity_ratings, source_id=1)
instrument_agg = collapse_ratings(instrument_ratings, source_id=2)
security_agg = collapse_ratings(security_ratings, source_id=3)

# Bring together the alternative sources for each company-date.
ratings_agg = pd.concat([entity_agg, instrument_agg, security_agg], ignore_index=True)

# Keep one source per company-date, preferring entity, then instrument, then security ratings.
ratings = ratings_agg.sort_values(['gvkey', 'ratingdate', 'source'])
ratings = ratings.drop_duplicates(subset=['gvkey', 'ratingdate'], keep='first')
print(f"After removing date duplicates: {len(ratings)} records")

# Save company-date ratings and downgrade indicators for downstream signals.
ratings.to_parquet("../pyData/Intermediate/m_CIQ_creditratings.parquet", index=False)

print(f"CIQ Credit Ratings data saved with {len(ratings)} records")
print(f"Date range: {ratings['ratingdate'].min()} to {ratings['ratingdate'].max()}")

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
