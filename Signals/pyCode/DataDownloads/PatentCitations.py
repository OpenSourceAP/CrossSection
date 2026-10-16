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

How to run: from Signals/pyCode, run python3 DataDownloads/PatentCitations.py

Use the project Python environment at /opt/venv/projects/openap.
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

# Obtain patent ownership histories and citation links for company innovation measures.
logger.info("Downloading NBER patent datasets...")

# Obtain historical company identifiers so patents can be linked to Compustat firms.
logger.info("Downloading http://www.nber.org/~jbessen/dynass.dta.zip")
response = requests.get("http://www.nber.org/~jbessen/dynass.dta.zip", timeout=300)
response.raise_for_status()
with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
    with zip_file.open("dynass.dta") as dta_file:
        dynass = pd.read_stata(BytesIO(dta_file.read()), preserve_dtypes=False)
logger.info(f"Downloaded dynass: {len(dynass):,} rows")

# Obtain links between citing and cited patents to measure subsequent patent impact.
logger.info("Downloading http://www.nber.org/~jbessen/cite76_06.dta.zip")
response = requests.get("http://www.nber.org/~jbessen/cite76_06.dta.zip", timeout=300)
response.raise_for_status()
with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
    with zip_file.open("cite76_06.dta") as dta_file:
        cite76_06 = pd.read_stata(BytesIO(dta_file.read()), preserve_dtypes=False)
logger.info(f"Downloaded cite76_06: {len(cite76_06):,} rows")

# Obtain patent ownership, grant years, and technology classifications.
logger.info("Downloading http://www.nber.org/~jbessen/pat76_06_assg.dta.zip")
response = requests.get("http://www.nber.org/~jbessen/pat76_06_assg.dta.zip", timeout=300)
response.raise_for_status()
with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
    with zip_file.open("pat76_06_assg.dta") as dta_file:
        pat76_06_assg = pd.read_stata(BytesIO(dta_file.read()), preserve_dtypes=False)
logger.info(f"Downloaded pat76_06_assg: {len(pat76_06_assg):,} rows")

logger.info("Processing patent counts...")

# Measure annual patent output for each source company identifier.
company_year_groups = pat76_06_assg.groupby(['pdpass', 'gyear'], as_index=False)
df_npat = company_year_groups.size()
df_npat = df_npat.rename(columns={'size': 'npat'})

df_npat = df_npat.merge(dynass, on='pdpass', how='left')

# Match patents to the Compustat company identifier valid in their grant year.
df_npat['gvkey'] = ""

# Where mapping periods overlap, retain the first matching period.
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

# Standardize company identifiers and grant years for matching patent and citation records.
df_npat['year'] = pd.to_numeric(df_npat['gyear'], errors='coerce').astype('Int64')
df_npat['gvkey'] = pd.to_numeric(df_npat['gvkey'], errors='coerce').astype('Int64')
df_npat['pdpass'] = df_npat['pdpass'].astype('Int64')

# Retain unique patent counts that can be attributed to a Compustat company.
df_npat = df_npat[df_npat['gvkey'].notna()]
df_npat = df_npat[['pdpass', 'gvkey', 'year', 'npat']].drop_duplicates()

logger.info(f"Created patent counts: {len(df_npat):,} rows")

logger.info("Processing patent citations...")

# Associate each patent with its owner, grant year, and technology category.
has_company_identifier = pat76_06_assg['pdpass'] != ""
df_cite_match = pat76_06_assg[has_company_identifier]
df_cite_match = df_cite_match[['patent', 'pdpass', 'gyear', 'cat', 'subcat']]

# Identify the owners and grant years on both sides of each citation.
# The .x fields describe the cited patent; .y fields describe the citing patent.
df_cite = cite76_06.merge(
    df_cite_match,
    left_on='cited',
    right_on='patent',
    how='left',
    suffixes=('', '.x')
)
df_cite = df_cite.merge(
    df_cite_match,
    left_on='citing',
    right_on='patent',
    how='left',
    suffixes=('.x', '.y')
)

df_cite['pdpass.x'] = pd.to_numeric(df_cite['pdpass.x'], errors='coerce').astype('Int64')
df_cite['pdpass.y'] = pd.to_numeric(df_cite['pdpass.y'], errors='coerce').astype('Int64')
df_cite['gyear.x'] = pd.to_numeric(df_cite['gyear.x'], errors='coerce').astype('Int64')
df_cite['gyear.y'] = pd.to_numeric(df_cite['gyear.y'], errors='coerce').astype('Int64')

# Require known owners and grant years on both sides before attributing citation impact.
has_both_companies_and_years = (
    (df_cite['pdpass.x'].notna()) &
    (df_cite['pdpass.y'].notna()) &
    (df_cite['gyear.x'].notna()) &
    (df_cite['gyear.y'].notna())
)
df_cite = df_cite[has_both_companies_and_years].copy()

# Retain citations whose citing grant year is at most five years after the cited grant year.
df_cite['gdiff'] = df_cite['gyear.y'] - df_cite['gyear.x']
df_cite = df_cite[df_cite['gdiff'] <= 5]

df_cite = df_cite.drop(columns=['ncites7606'], errors='ignore')

logger.info(f"Created citation data: {len(df_cite):,} rows")

# Normalize citation impact for differences across technology and grant-year cohorts.
logger.info("Scaling citations by subcategory...")

# Attribute received citations to the cited patent's owner in the citing patent's grant year.
df_scale = df_npat.merge(
    df_cite,
    left_on=['pdpass', 'year'],
    right_on=['pdpass.x', 'gyear.y'],
    how='left'
)

# Exclude company-year entries without a citation to count.
df_scale = df_scale[df_scale['cited'].notna() & (df_scale['cited'] != "")]

df_scale = df_scale[['pdpass', 'gvkey', 'year', 'gyear.x', 'subcat.x']]

# Count company citations within each citing-year, cited-year, and technology cohort.
citation_group_keys = ['pdpass', 'gvkey', 'year', 'gyear.x', 'subcat.x']
citation_groups = df_scale.groupby(citation_group_keys, as_index=False)
df_scale = citation_groups.size()
del citation_groups
df_scale = df_scale.rename(columns={'size': 'ncites'})

# Express citation counts relative to the average company count in the same cohort.
cohort_keys = ['year', 'gyear.x', 'subcat.x']
cohort_citation_counts = df_scale.groupby(cohort_keys)['ncites']
df_scale['citscale'] = cohort_citation_counts.transform(
    lambda counts: counts / counts.mean(skipna=True)
)

# Combine cohort-adjusted citation impact into one company-year measure.
company_year_citations = df_scale.groupby(['gvkey', 'year'])['citscale'].sum()
df_scale = company_year_citations.reset_index()
df_scale = df_scale.rename(columns={'citscale': 'ncitscale'})

logger.info(f"Created scaled citations: {len(df_scale):,} rows")

logger.info("Merging patents and citations...")

# Combine source company identifiers into total patents per Compustat company-year.
company_year_patents = df_npat.groupby(['gvkey', 'year'])['npat'].sum()
df_patents = company_year_patents.reset_index()

# Provide patent output and citation impact together for each company-year.
df_patents = df_patents.merge(df_scale, on=['gvkey', 'year'], how='left')

logger.info(f"Merged data: {len(df_patents):,} rows")

# Include every observed company across the dataset's full year range.
logger.info("Creating balanced panel...")

all_gvkeys = sorted(df_patents['gvkey'].unique())
all_years = list(range(int(df_patents['year'].min()), int(df_patents['year'].max()) + 1))

full_grid = pd.DataFrame(list(product(all_gvkeys, all_years)),
                        columns=['gvkey', 'year'])

df_patents = full_grid.merge(df_patents, on=['gvkey', 'year'], how='left')

# Represent company-years without recorded patent activity or citation impact as zero.
df_patents['npat'] = df_patents['npat'].fillna(0.0)
df_patents['ncitscale'] = df_patents['ncitscale'].fillna(0.0)

logger.info(f"Balanced panel: {len(df_patents):,} rows")

# Keep identifiers and counts compatible with the downstream company-year panel.
df_patents['gvkey'] = df_patents['gvkey'].astype('Int64')
df_patents['year'] = df_patents['year'].astype('Int64')
df_patents['npat'] = df_patents['npat'].astype(float)
df_patents['ncitscale'] = df_patents['ncitscale'].astype(float)

# Save annual patent output and normalized citation impact for downstream signals.
output_path = "../pyData/Intermediate/PatentDataProcessed.parquet"
df_patents.to_parquet(output_path, index=False)

logger.info(f"Successfully saved {len(df_patents):,} rows to {output_path}")
logger.info("Patent Citations processing completed successfully!")

logger.info("Sample data:")
logger.info(df_patents.head().to_string())

logger.info("Summary statistics:")
for col in ['npat', 'ncitscale']:
    series_data = df_patents[col].dropna()
    if len(series_data) > 0:
        logger.info(f"{col}: mean={series_data.mean():.6f}, std={series_data.std():.6f}, count={len(series_data)}")
