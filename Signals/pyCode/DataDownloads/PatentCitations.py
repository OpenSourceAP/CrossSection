# ABOUTME: Downloads NBER patent data and calculates patent counts and citation metrics by gvkey-year
# ABOUTME: Creates balanced panel with patent counts (npat) and scaled citations (ncitscale) for 1976-2006
"""
Inputs:
- NBER patent datasets (downloaded automatically):
  * dynass.dta (company-gvkey mapping)
  * cite76_06.dta (citation data)
  * pat76_06_assg.dta (patent assignment data)

Outputs:
- ../pyData/Intermediate/PatentDataProcessed.parquet

How to run: python3 PatentCitations.py
"""

import pandas as pd
import numpy as np
import requests
import zipfile
import logging
from io import BytesIO
from itertools import product

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting Patent Citations processing with pure Python implementation...")

# Download the three datasets from NBER
logger.info("Downloading NBER patent datasets...")

# Download company-gvkey mapping table
logger.info("Downloading http://www.nber.org/~jbessen/dynass.dta.zip")
response = requests.get("http://www.nber.org/~jbessen/dynass.dta.zip", timeout=300)
response.raise_for_status()
with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
    with zip_file.open("dynass.dta") as dta_file:
        dynass = pd.read_stata(BytesIO(dta_file.read()), preserve_dtypes=False)
logger.info(f"Downloaded dynass: {len(dynass):,} rows")

# Download citation data
logger.info("Downloading http://www.nber.org/~jbessen/cite76_06.dta.zip")
response = requests.get("http://www.nber.org/~jbessen/cite76_06.dta.zip", timeout=300)
response.raise_for_status()
with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
    with zip_file.open("cite76_06.dta") as dta_file:
        cite76_06 = pd.read_stata(BytesIO(dta_file.read()), preserve_dtypes=False)
logger.info(f"Downloaded cite76_06: {len(cite76_06):,} rows")

# Download patent assignment data
logger.info("Downloading http://www.nber.org/~jbessen/pat76_06_assg.dta.zip")
response = requests.get("http://www.nber.org/~jbessen/pat76_06_assg.dta.zip", timeout=300)
response.raise_for_status()
with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
    with zip_file.open("pat76_06_assg.dta") as dta_file:
        pat76_06_assg = pd.read_stata(BytesIO(dta_file.read()), preserve_dtypes=False)
logger.info(f"Downloaded pat76_06_assg: {len(pat76_06_assg):,} rows")
# Count patents by company and year
logger.info("Processing patent counts...")

# Count patents by company (pdpass) and year
df_npat = (pat76_06_assg
           .groupby(['pdpass', 'gyear'], as_index=False)
           .size()
           .rename(columns={'size': 'npat'}))

# Join with company-gvkey mapping table
df_npat = df_npat.merge(dynass, on='pdpass', how='left')

# Map pdpass to gvkey based on time period (companies can have different gvkeys over time)
df_npat['gvkey'] = ""

# Time-dependent gvkey mapping using multiple time periods
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

# Convert to proper data types and clean data
df_npat['year'] = pd.to_numeric(df_npat['gyear'], errors='coerce').astype('Int64')
df_npat['gvkey'] = pd.to_numeric(df_npat['gvkey'], errors='coerce').astype('Int64')
df_npat['pdpass'] = df_npat['pdpass'].astype('Int64')

# Keep only valid gvkeys and select final columns
df_npat = (df_npat[df_npat['gvkey'].notna()]
           [['pdpass', 'gvkey', 'year', 'npat']]
           .drop_duplicates())

logger.info(f"Created patent counts: {len(df_npat):,} rows")

# Process patent citations
logger.info("Processing patent citations...")

# Create lookup table for patent-company mapping
df_cite_match = (pat76_06_assg[pat76_06_assg['pdpass'] != ""]
                 [['patent', 'pdpass', 'gyear', 'cat', 'subcat']])

# Join citation data with company info for both citing and cited patents
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

# Convert to proper data types
df_cite['pdpass.x'] = pd.to_numeric(df_cite['pdpass.x'], errors='coerce').astype('Int64')
df_cite['pdpass.y'] = pd.to_numeric(df_cite['pdpass.y'], errors='coerce').astype('Int64')
df_cite['gyear.x'] = pd.to_numeric(df_cite['gyear.x'], errors='coerce').astype('Int64')
df_cite['gyear.y'] = pd.to_numeric(df_cite['gyear.y'], errors='coerce').astype('Int64')

# Keep only valid citations with both companies identified
df_cite = df_cite[
    (df_cite['pdpass.x'].notna()) &
    (df_cite['pdpass.y'].notna()) &
    (df_cite['gyear.x'].notna()) &
    (df_cite['gyear.y'].notna())
].copy()

# Filter citations to within 5 years of cited patent
df_cite['gdiff'] = df_cite['gyear.y'] - df_cite['gyear.x']
df_cite = df_cite[df_cite['gdiff'] <= 5]

# Clean up unnecessary columns
df_cite = df_cite.drop(columns=['ncites7606'], errors='ignore')

logger.info(f"Created citation data: {len(df_cite):,} rows")

# Scale citations by subcategory and year
logger.info("Scaling citations by subcategory...")

# Join patent counts with citation data
df_scale = df_npat.merge(
    df_cite,
    left_on=['pdpass', 'year'],
    right_on=['pdpass.x', 'gyear.y'],
    how='left'
)

# Keep only valid citations
df_scale = df_scale[df_scale['cited'].notna() & (df_scale['cited'] != "")]

# Select columns needed for scaling calculation
df_scale = df_scale[['pdpass', 'gvkey', 'year', 'gyear.x', 'subcat.x']]

# Count citations by company-year-subcategory groups
df_scale = (df_scale.groupby(['pdpass', 'gvkey', 'year', 'gyear.x', 'subcat.x'], as_index=False)
            .size()
            .rename(columns={'size': 'ncites'}))

# Scale citations by dividing by mean citations in same year/subcategory
df_scale['citscale'] = (df_scale.groupby(['year', 'gyear.x', 'subcat.x'])['ncites']
                       .transform(lambda x: x / x.mean(skipna=True)))

# Sum scaled citations by gvkey-year
df_scale = (df_scale.groupby(['gvkey', 'year'])['citscale']
            .sum()
            .reset_index()
            .rename(columns={'citscale': 'ncitscale'}))

logger.info(f"Created scaled citations: {len(df_scale):,} rows")

# Combine patent counts and scaled citations
logger.info("Merging patents and citations...")

# Aggregate patent counts by gvkey-year
df_patents = (df_npat.groupby(['gvkey', 'year'])['npat']
              .sum()
              .reset_index())

# Add scaled citations
df_patents = df_patents.merge(df_scale, on=['gvkey', 'year'], how='left')

logger.info(f"Merged data: {len(df_patents):,} rows")

# Create balanced panel with all gvkey-year combinations
logger.info("Creating balanced panel...")

# Get all unique gvkeys and years in the data
all_gvkeys = sorted(df_patents['gvkey'].unique())
all_years = list(range(int(df_patents['year'].min()), int(df_patents['year'].max()) + 1))

# Create full grid of all possible gvkey-year combinations
full_grid = pd.DataFrame(list(product(all_gvkeys, all_years)),
                        columns=['gvkey', 'year'])

# Merge actual data with full grid
df_patents = full_grid.merge(df_patents, on=['gvkey', 'year'], how='left')

# Fill missing values with zero
df_patents['npat'] = df_patents['npat'].fillna(0.0)
df_patents['ncitscale'] = df_patents['ncitscale'].fillna(0.0)

logger.info(f"Balanced panel: {len(df_patents):,} rows")

# Set final data types
df_patents['gvkey'] = df_patents['gvkey'].astype('Int64')
df_patents['year'] = df_patents['year'].astype('Int64')
df_patents['npat'] = df_patents['npat'].astype(float)
df_patents['ncitscale'] = df_patents['ncitscale'].astype(float)

# Save to parquet
output_path = "../pyData/Intermediate/PatentDataProcessed.parquet"
df_patents.to_parquet(output_path, index=False)

logger.info(f"Successfully saved {len(df_patents):,} rows to {output_path}")
logger.info("Patent Citations processing completed successfully!")

# Display sample data and summary statistics
logger.info("Sample data:")
logger.info(df_patents.head().to_string())

logger.info("Summary statistics:")
for col in ['npat', 'ncitscale']:
    series_data = df_patents[col].dropna()
    if len(series_data) > 0:
        logger.info(f"{col}: mean={series_data.mean():.6f}, std={series_data.std():.6f}, count={len(series_data)}")