#!/usr/bin/env python3
"""
CIQ Credit Ratings data download script - Python equivalent of X2_CIQCreditRatings.do

Downloads CIQ credit ratings from entity, instrument, and security ratings tables.
Extends coverage beyond Compustat ratings which end in 2017.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def download_ciq_ratings(query_type, conn):
    """Download one type of CIQ ratings"""
    if query_type == "entity":
        query = """
        SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.entity_id
        FROM ciq.wrds_erating a
        LEFT JOIN ciq.ratings_ids b
        ON a.entity_id = b.entity_id
        WHERE b.gvkey IS NOT NULL
        AND a.ratingdate >= '1970-01-01'
        """
        fill_cols = {'instrument_id': '', 'security_id': ''}
        
    elif query_type == "instrument":
        query = """
        SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.instrument_id
        FROM ciq.wrds_irating a
        LEFT JOIN ciq.ratings_ids b
        ON a.instrument_id = b.instrument_id
        WHERE b.gvkey IS NOT NULL
        AND a.ratingdate >= '1970-01-01'
        """
        fill_cols = {'entity_id': '', 'security_id': ''}
        
    else:  # security
        query = """
        SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.security_id
        FROM ciq.wrds_srating a
        LEFT JOIN ciq.ratings_ids b
        ON a.security_id = b.security_id
        WHERE b.gvkey IS NOT NULL
        AND a.ratingdate >= '1970-01-01'
        """
        fill_cols = {'entity_id': '', 'instrument_id': ''}
    
    try:
        data = pd.read_sql_query(query, conn)
        print(f"Downloaded {len(data)} {query_type} rating records")
        
        # Fill in missing columns
        for col, val in fill_cols.items():
            data[col] = val
            
        return data
    except Exception as e:
        print(f"Error downloading {query_type} ratings: {e}")
        return pd.DataFrame()

def main():
    """Main function to download and process CIQ credit ratings"""
    print("Downloading CIQ Credit Ratings...")
    
    conn = psycopg2.connect(
        host="wrds-pgdata.wharton.upenn.edu",
        port=9737,
        database="wrds",
        user=os.getenv("WRDS_USERNAME"),
        password=os.getenv("WRDS_PASSWORD")
    )
    
    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    
    # Download all three types of ratings
    entity_ratings = download_ciq_ratings("entity", conn)
    instrument_ratings = download_ciq_ratings("instrument", conn)
    security_ratings = download_ciq_ratings("security", conn)
    
    conn.close()
    
    # Combine all ratings
    all_ratings = []
    if not entity_ratings.empty:
        all_ratings.append(entity_ratings)
    if not instrument_ratings.empty:
        all_ratings.append(instrument_ratings)
    if not security_ratings.empty:
        all_ratings.append(security_ratings)
    
    if not all_ratings:
        print("No CIQ rating data downloaded")
        return
    
    combined_ratings = pd.concat(all_ratings, ignore_index=True)
    print(f"Combined {len(combined_ratings)} total rating records")
    
    # Drop "Not Rated" actions
    if 'ratingactionword' in combined_ratings.columns:
        initial_count = len(combined_ratings)
        combined_ratings = combined_ratings[combined_ratings['ratingactionword'] != 'Not Rated']
        print(f"Removed {initial_count - len(combined_ratings)} 'Not Rated' records")
    
    # Rank the sources (entity=1, instrument=2, security=3)
    combined_ratings['source'] = 3  # default
    combined_ratings.loc[combined_ratings['entity_id'].notna() & (combined_ratings['entity_id'] != ''), 'source'] = 1
    combined_ratings.loc[combined_ratings['instrument_id'].notna() & (combined_ratings['instrument_id'] != ''), 'source'] = 2
    
    # For each gvkey-ratingdate-ratingtime, keep the best source
    combined_ratings = combined_ratings.sort_values(['gvkey', 'ratingdate', 'ratingtime', 'source'])
    combined_ratings = combined_ratings.drop_duplicates(['gvkey', 'ratingdate', 'ratingtime'], keep='first')
    print(f"After removing time duplicates: {len(combined_ratings)} records")
    
    # Add time_avail_m
    combined_ratings['ratingdate'] = pd.to_datetime(combined_ratings['ratingdate'])
    combined_ratings['time_avail_m'] = combined_ratings['ratingdate'].dt.to_period('M')
    
    # For each gvkey-time_avail_m, keep last rating (by date and time)
    combined_ratings = combined_ratings.sort_values(['gvkey', 'time_avail_m', 'ratingdate', 'ratingtime'])
    combined_ratings = combined_ratings.drop_duplicates(['gvkey', 'time_avail_m'], keep='last')
    print(f"After keeping last rating per month: {len(combined_ratings)} records")
    
    # Convert gvkey to numeric
    combined_ratings['gvkey'] = pd.to_numeric(combined_ratings['gvkey'], errors='coerce')
    
    # Save the data
    combined_ratings.to_pickle("../pyData/Intermediate/m_CIQ_creditratings.pkl")
    
    print(f"CIQ Credit Ratings data saved with {len(combined_ratings)} records")
    print(f"Date range: {combined_ratings['time_avail_m'].min()} to {combined_ratings['time_avail_m'].max()}")
    
    # Show source distribution
    print("\nSource distribution:")
    source_dist = combined_ratings['source'].value_counts().sort_index()
    source_labels = {1: 'Entity', 2: 'Instrument', 3: 'Security'}
    for source, count in source_dist.items():
        label = source_labels.get(source, f'Unknown ({source})')
        print(f"  {source} ({label}): {count:,}")
    
    print("\nSample data:")
    print(combined_ratings[['gvkey', 'time_avail_m', 'currentratingsymbol', 'source']].head())

if __name__ == "__main__":
    main()