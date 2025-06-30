# ABOUTME: Downloads NBER patent data and calculates patent counts and citation metrics
# ABOUTME: Pure Python implementation - translated from R script logic

import pandas as pd
import numpy as np
import requests
import zipfile
import tempfile
import os
import logging
from io import BytesIO
from itertools import product

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_and_extract_dta(url, filename):
    """Download a ZIP file and extract the specified DTA file"""
    logger.info(f"Downloading {url}")
    
    response = requests.get(url, timeout=300)
    response.raise_for_status()
    
    # Extract DTA file from ZIP
    with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
        with zip_file.open(filename) as dta_file:
            # Read DTA file directly from ZIP
            return pd.read_stata(BytesIO(dta_file.read()), preserve_dtypes=False)

def main():
    """Main function that implements patent citation processing in pure Python"""
    
    logger.info("Starting Patent Citations processing with pure Python implementation...")
    
    # Ensure output directory exists
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    
    # Download the three datasets from NBER
    logger.info("Downloading NBER patent datasets...")
    
    try:
        # Download 1: dynass.dta (company-gvkey mapping)
        dynass = download_and_extract_dta(
            "http://www.nber.org/~jbessen/dynass.dta.zip", 
            "dynass.dta"
        )
        logger.info(f"Downloaded dynass: {len(dynass):,} rows")
        
        # Download 2: cite76_06.dta (citation data)
        cite76_06 = download_and_extract_dta(
            "http://www.nber.org/~jbessen/cite76_06.dta.zip", 
            "cite76_06.dta"
        )
        logger.info(f"Downloaded cite76_06: {len(cite76_06):,} rows")
        
        # Download 3: pat76_06_assg.dta (patent assignment data)
        pat76_06_assg = download_and_extract_dta(
            "http://www.nber.org/~jbessen/pat76_06_assg.dta.zip", 
            "pat76_06_assg.dta"
        )
        logger.info(f"Downloaded pat76_06_assg: {len(pat76_06_assg):,} rows")
        
    except Exception as e:
        logger.error(f"Error downloading data: {str(e)}")
        raise
    
    # Number of patents (equivalent to df_npat in R)
    logger.info("Processing patent counts...")
    
    # Count patents by company and year
    df_npat = (pat76_06_assg
               .groupby(['pdpass', 'gyear'], as_index=False)
               .size()
               .rename(columns={'size': 'npat'}))
    
    # Join with dynass to get gvkey mappings
    df_npat = df_npat.merge(dynass, on='pdpass', how='left')
    
    # Initialize gvkey column
    df_npat['gvkey'] = ""
    
    # Time-dependent gvkey mapping (equivalent to R's case_when)
    conditions = [
        (df_npat['gyear'] >= df_npat['begyr1']) & (df_npat['gyear'] <= df_npat['endyr1']),
        (df_npat['gyear'] >= df_npat['begyr2']) & (df_npat['gyear'] <= df_npat['endyr2']),
        (df_npat['gyear'] >= df_npat['begyr3']) & (df_npat['gyear'] <= df_npat['endyr3']),
        (df_npat['gyear'] >= df_npat['begyr4']) & (df_npat['gyear'] <= df_npat['endyr4']),
        (df_npat['gyear'] >= df_npat['begyr5']) & (df_npat['gyear'] <= df_npat['endyr5'])
    ]
    
    choices = [
        df_npat['gvkey1'],
        df_npat['gvkey2'], 
        df_npat['gvkey3'],
        df_npat['gvkey4'],
        df_npat['gvkey5']
    ]
    
    df_npat['gvkey'] = np.select(conditions, choices, default="")
    
    # Convert data types and filter - ensure integer types to match R exactly
    df_npat['year'] = pd.to_numeric(df_npat['gyear'], errors='coerce').astype('Int64')
    df_npat['gvkey'] = pd.to_numeric(df_npat['gvkey'], errors='coerce').astype('Int64')
    df_npat['pdpass'] = df_npat['pdpass'].astype('Int64')
    
    # Filter out empty gvkeys and select final columns
    df_npat = (df_npat[df_npat['gvkey'].notna()]
               [['pdpass', 'gvkey', 'year', 'npat']]
               .drop_duplicates())
    
    logger.info(f"Created patent counts: {len(df_npat):,} rows")
    
    # Number of patent citations (equivalent to df_cite, df_scale in R)
    logger.info("Processing patent citations...")
    
    # Create citation matching table
    df_cite_match = (pat76_06_assg[pat76_06_assg['pdpass'] != ""]
                     [['patent', 'pdpass', 'gyear', 'cat', 'subcat']])
    
    # Match citing and cited patents (double merge)
    df_cite = cite76_06.merge(
        df_cite_match, 
        left_on='cited', 
        right_on='patent', 
        how='left',
        suffixes=('', '.x')
    ).merge(
        df_cite_match,
        left_on='citing',
        right_on='patent',
        how='left', 
        suffixes=('.x', '.y')
    )
    
    # Convert citation data types to integers to match R exactly  
    df_cite['pdpass.x'] = pd.to_numeric(df_cite['pdpass.x'], errors='coerce').astype('Int64')
    df_cite['pdpass.y'] = pd.to_numeric(df_cite['pdpass.y'], errors='coerce').astype('Int64')
    df_cite['gyear.x'] = pd.to_numeric(df_cite['gyear.x'], errors='coerce').astype('Int64')
    df_cite['gyear.y'] = pd.to_numeric(df_cite['gyear.y'], errors='coerce').astype('Int64')
    
    # Filter for valid companies and years (exact R logic)
    df_cite = df_cite[
        (df_cite['pdpass.x'].notna()) & 
        (df_cite['pdpass.y'].notna()) & 
        (df_cite['gyear.x'].notna()) & 
        (df_cite['gyear.y'].notna())
    ].copy()
    
    # Calculate time difference and filter to 5 years
    df_cite['gdiff'] = df_cite['gyear.y'] - df_cite['gyear.x']
    df_cite = df_cite[df_cite['gdiff'] <= 5]
    
    # Remove unnecessary column
    df_cite = df_cite.drop(columns=['ncites7606'], errors='ignore')
    
    logger.info(f"Created citation data: {len(df_cite):,} rows")
    
    # Scale citations by subcategory (equivalent to df_scale in R)
    logger.info("Scaling citations by subcategory...")
    
    # Join npat with citations - exact R logic with consistent data types
    df_scale = df_npat.merge(
        df_cite,
        left_on=['pdpass', 'year'],
        right_on=['pdpass.x', 'gyear.y'],
        how='left'
    )
    
    # Filter for valid citations (cited != "")
    df_scale = df_scale[df_scale['cited'].notna() & (df_scale['cited'] != "")]
    
    # Select relevant columns
    df_scale = df_scale[['pdpass', 'gvkey', 'year', 'gyear.x', 'subcat.x']]
    
    # Count citations by group (equivalent to R's summarise(ncites = n()))
    df_scale = (df_scale.groupby(['pdpass', 'gvkey', 'year', 'gyear.x', 'subcat.x'], as_index=False)
                .size()
                .rename(columns={'size': 'ncites'}))
    
    # Calculate scaled citations using transform to replicate R's mutate behavior exactly (na.rm = TRUE)
    df_scale['citscale'] = (df_scale.groupby(['year', 'gyear.x', 'subcat.x'])['ncites']
                           .transform(lambda x: x / x.mean(skipna=True)))
    
    # Sum scaled citations by gvkey and year (equivalent to R's final summarise with na.rm = TRUE)
    # Note: pandas groupby.sum() already skips NaN values by default
    df_scale = (df_scale.groupby(['gvkey', 'year'])['citscale']
                .sum()
                .reset_index()
                .rename(columns={'citscale': 'ncitscale'}))
    
    logger.info(f"Created scaled citations: {len(df_scale):,} rows")
    
    # Merge patent counts and scaled citations
    logger.info("Merging patents and citations...")
    
    # First aggregate npat by gvkey/year to remove duplicates
    df_patents = (df_npat.groupby(['gvkey', 'year'])['npat']
                  .sum()
                  .reset_index())
    
    # Merge with scaled citations
    df_patents = df_patents.merge(df_scale, on=['gvkey', 'year'], how='left')
    
    logger.info(f"Merged data: {len(df_patents):,} rows")
    
    # Expand to balanced panel
    logger.info("Creating balanced panel...")
    
    # Get all unique gvkeys and years
    all_gvkeys = sorted(df_patents['gvkey'].unique())
    all_years = list(range(int(df_patents['year'].min()), int(df_patents['year'].max()) + 1))
    
    # Create full grid
    full_grid = pd.DataFrame(list(product(all_gvkeys, all_years)), 
                            columns=['gvkey', 'year'])
    
    # Merge with actual data
    df_patents = full_grid.merge(df_patents, on=['gvkey', 'year'], how='left')
    
    # Fill missing values with 0
    df_patents['npat'] = df_patents['npat'].fillna(0.0)
    df_patents['ncitscale'] = df_patents['ncitscale'].fillna(0.0)
    
    logger.info(f"Balanced panel: {len(df_patents):,} rows")
    
    # Final data type conversion
    df_patents['gvkey'] = df_patents['gvkey'].astype('Int64')
    df_patents['year'] = df_patents['year'].astype('Int64') 
    df_patents['npat'] = df_patents['npat'].astype(float)
    df_patents['ncitscale'] = df_patents['ncitscale'].astype(float)
    
    # Save to parquet
    output_path = "../pyData/Intermediate/PatentDataProcessed.parquet"
    df_patents.to_parquet(output_path, index=False)
    
    logger.info(f"Successfully saved {len(df_patents):,} rows to {output_path}")
    logger.info("Patent Citations processing completed successfully!")
    
    # Show sample data
    logger.info("Sample data:")
    logger.info(df_patents.head().to_string())
    
    # Show summary statistics
    logger.info("Summary statistics:")
    for col in ['npat', 'ncitscale']:
        series_data = df_patents[col].dropna()
        if len(series_data) > 0:
            logger.info(f"{col}: mean={series_data.mean():.6f}, std={series_data.std():.6f}, count={len(series_data)}")
    
    return df_patents

if __name__ == "__main__":
    main()