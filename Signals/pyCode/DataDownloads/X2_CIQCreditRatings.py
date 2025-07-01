#!/usr/bin/env python3
"""
CIQ Credit Ratings data download script - Python equivalent of X2_CIQCreditRatings.do

Downloads CIQ credit ratings from entity, instrument, and security ratings tables.
Extends coverage beyond Compustat ratings which end in 2017.
"""


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

def main():
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
    
    all_ratings = []
    
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
        
        if not entity_ratings.empty:
            all_ratings.append(entity_ratings)
            
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
        
        if not instrument_ratings.empty:
            all_ratings.append(instrument_ratings)
            
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
        
        if not security_ratings.empty:
            all_ratings.append(security_ratings)
            
    except Exception as e:
        print(f"Error downloading security ratings: {e}")
    
    engine.dispose()
    
    # Append all ratings (like Stata's append using commands)
    if not all_ratings:
        print("No CIQ rating data downloaded")
        return
    
    combined_ratings = pd.concat(all_ratings, ignore_index=True)
    print(f"Combined {len(combined_ratings)} total rating records")
    
    # Drop "Not Rated" actions (like Stata: drop if ratingaction == "Not Rated")
    if 'ratingactionword' in combined_ratings.columns:
        initial_count = len(combined_ratings)
        combined_ratings = combined_ratings[combined_ratings['ratingactionword'] != 'Not Rated']
        print(f"Removed {initial_count - len(combined_ratings)} 'Not Rated' records")
    
    # Rank the sources (like Stata's gen source logic)
    combined_ratings['source'] = 3  # default for security
    entity_mask = (combined_ratings['entity_id'].notna()) & (combined_ratings['entity_id'] != '')
    combined_ratings.loc[entity_mask, 'source'] = 1
    instrument_mask = (combined_ratings['instrument_id'].notna()) & (combined_ratings['instrument_id'] != '')
    combined_ratings.loc[instrument_mask, 'source'] = 2
    
    # For each gvkey-ratingdate-ratingtime, keep the best source (like Stata's dupcount logic)
    combined_ratings = combined_ratings.sort_values(['gvkey', 'ratingdate', 'ratingtime', 'source'])
    combined_ratings = combined_ratings.drop_duplicates(subset=['gvkey', 'ratingdate', 'ratingtime'], keep='first')
    print(f"After removing time duplicates: {len(combined_ratings)} records")
    
    # Add time_avail_m (like Stata's gen time_avail_m = mofd(ratingdate))
    combined_ratings['ratingdate'] = pd.to_datetime(combined_ratings['ratingdate'])
    combined_ratings['time_avail_m'] = combined_ratings['ratingdate'].dt.to_period('M').dt.to_timestamp()
    
    # Fix ratingtime format to match Stata (add dummy date 1960-01-01)
    if 'ratingtime' in combined_ratings.columns:
        dummy_date = pd.Timestamp('1960-01-01')
        combined_ratings['ratingtime'] = pd.to_datetime(combined_ratings['ratingtime'].astype(str), format='%H:%M:%S', errors='coerce')
        combined_ratings['ratingtime'] = combined_ratings['ratingtime'].apply(
            lambda x: dummy_date.replace(hour=x.hour, minute=x.minute, second=x.second) if pd.notna(x) else dummy_date
        )
        print("Applied ratingtime datetime conversion with dummy date 1960-01-01")
    
    # For each gvkey-time_avail_m, keep last rating by date and time (like Stata's gsort and dupcount)
    combined_ratings = combined_ratings.sort_values(['gvkey', 'time_avail_m', 'ratingdate', 'ratingtime'])
    combined_ratings = combined_ratings.drop_duplicates(subset=['gvkey', 'time_avail_m'], keep='last')
    print(f"After keeping last rating per month: {len(combined_ratings)} records")
    
    # Convert gvkey to numeric (like Stata's destring gvkey)
    combined_ratings['gvkey'] = pd.to_numeric(combined_ratings['gvkey'], errors='coerce')
    
    # Convert None/NaN to empty string for string columns (match Stata missing values)
    string_columns = ['ticker', 'ratingactionword', 'currentratingsymbol', 'entity_id', 'instrument_id', 'security_id']
    for col in string_columns:
        if col in combined_ratings.columns:
            combined_ratings[col] = combined_ratings[col].fillna('')
            combined_ratings[col] = combined_ratings[col].replace('None', '')
    
    # Save the data
    # Apply column standardization
    combined_ratings = standardize_columns(combined_ratings, 'm_CIQ_creditratings')
    combined_ratings.to_parquet("../pyData/Intermediate/m_CIQ_creditratings.parquet", index=False)
    
    print(f"CIQ Credit Ratings data saved with {len(combined_ratings)} records")
    print(f"Date range: {combined_ratings['time_avail_m'].min()} to {combined_ratings['time_avail_m'].max()}")
    
    # Show source distribution
    print("\nSource distribution:")
    source_dist = combined_ratings['source'].value_counts().sort_index()
    source_labels = {1: 'Entity', 2: 'Instrument', 3: 'Security'}
    for source, count in source_dist.items():
        if isinstance(source, (int, float)):
            source_int = int(source)
            label = source_labels.get(source_int, f'Unknown ({source})')
            print(f"  {source} ({label}): {count:,}")
    
    print("\nSample data:")
    print(combined_ratings[['gvkey', 'time_avail_m', 'currentratingsymbol', 'source']].head())

if __name__ == "__main__":
    main()