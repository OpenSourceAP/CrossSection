#!/usr/bin/env python3
"""
ABOUTME: CRSP Distributions data download script with YAML-based column standardization
ABOUTME: Python equivalent of H_CRSPDistributions.do using YAML schema

Downloads CRSP distributions data (dividends, splits, etc.)
http://www.crsp.org/products/documentation/distribution-codes
"""

import os
import sys
import yaml
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("💰 H_CRSPDistributions.py - CRSP Dividends & Distributions", flush=True)
print("=" * 60, flush=True)

load_dotenv()


def yaml_standardize_columns(df, dataset_name="CRSPdistributions"):
    """
    Standardize DataFrame columns using YAML schema instead of DTA files.

    Args:
        df (pandas.DataFrame): Input DataFrame to standardize
        dataset_name (str): Name of dataset in YAML schema

    Returns:
        pandas.DataFrame: DataFrame with standardized columns
    """
    # Load YAML schema
    yaml_path = os.path.join(os.path.dirname(__file__),
                             "../utils/column_schemas.yaml")

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            schemas = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading YAML schema: {e}")
        return df

    if dataset_name not in schemas:
        print(f"❌ Dataset '{dataset_name}' not found in YAML schema")
        return df

    schema = schemas[dataset_name]
    target_columns = schema['columns']
    special_handling = schema.get('special_handling', {})

    print(f"{dataset_name}: Starting YAML-based column standardization")

    df_standardized = df.copy()

    # Remove unwanted columns based on patterns
    remove_patterns = special_handling.get('remove_patterns', [])
    unwanted_cols = []

    for pattern in remove_patterns:
        if pattern == '__index_level_*':
            # Find columns starting with '__index_level_'
            unwanted_cols.extend([col for col in df_standardized.columns
                                  if col.startswith('__index_level_')])
        elif pattern == 'index':
            # Find exact 'index' column
            if 'index' in df_standardized.columns:
                unwanted_cols.append('index')

    if unwanted_cols:
        print(f"{dataset_name}: Removing unwanted columns: {unwanted_cols}")
        df_standardized = df_standardized.drop(columns=unwanted_cols)

    # Check for missing columns
    missing_cols = [col for col in target_columns
                    if col not in df_standardized.columns]
    if missing_cols:
        print(f"{dataset_name}: Adding missing columns: {missing_cols}")
        for col in missing_cols:
            df_standardized[col] = np.nan

    # Check for extra columns
    extra_cols = [col for col in df_standardized.columns
                  if col not in target_columns]
    if extra_cols:
        print(f"{dataset_name}: Removing extra columns: {extra_cols}")
        df_standardized = df_standardized.drop(columns=extra_cols)

    # Reorder columns to match target order
    try:
        df_standardized = df_standardized[target_columns]
        print(f"{dataset_name}: Column order standardized successfully "
              "using YAML schema")
    except KeyError as e:
        print(f"{dataset_name}: Error reordering columns: {e}")
        return df

    return df_standardized


# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:"
    f"{os.getenv('WRDS_PASSWORD')}"
    "@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT d.permno, d.divamt, d.distcd, d.facshr, d.rcrddt, d.exdt, d.paydt
FROM crsp.msedist as d
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

dist_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

print(f"Downloaded {len(dist_data)} distribution records")

# Replicate Stata's exact duplicate removal logic:
# "bysort permno distcd paydt: keep if _n == 1"
# This means: sort by permno distcd paydt, then keep first record in each group
initial_count = len(dist_data)

# Sort first (this is what bysort does), then remove duplicates
# Stata's "bysort permno distcd paydt" sorts by exactly these 3 columns
# For tied records, Stata may use the original dataset order as tie-breaker
# We need to replicate this by using a stable sort that preserves original
# order for ties
dist_data = dist_data.sort_values(['permno', 'distcd', 'paydt'],
                                  kind='stable').reset_index(drop=True)
dist_data = dist_data.drop_duplicates(subset=['permno', 'distcd', 'paydt'],
                                      keep='first')
duplicates_removed = initial_count - len(dist_data)

if duplicates_removed > 0:
    print(f"Removed {duplicates_removed} duplicate records")

# For convenience, extract components of distribution code
# IMPORTANT: In Stata, the tostring distcd happens AFTER deduplication
# So we need to work with the numeric distcd for digit extraction
# Convert distcd to string and extract individual digits
dist_data['distcd_str'] = (dist_data['distcd'].astype(str)
                           .str.zfill(4))  # Pad with zeros to ensure 4 digits

# Extract each digit as separate columns
dist_data['cd1'] = pd.to_numeric(dist_data['distcd_str'].str[0],
                                 errors='coerce')
dist_data['cd2'] = pd.to_numeric(dist_data['distcd_str'].str[1],
                                 errors='coerce')
dist_data['cd3'] = pd.to_numeric(dist_data['distcd_str'].str[2],
                                 errors='coerce')
dist_data['cd4'] = pd.to_numeric(dist_data['distcd_str'].str[3],
                                 errors='coerce')

# Drop the temporary string column
dist_data = dist_data.drop('distcd_str', axis=1)

# Convert date columns to datetime format to match Stata expectations
date_columns = ['rcrddt', 'exdt', 'paydt']
for col in date_columns:
    if col in dist_data.columns:
        dist_data[col] = pd.to_datetime(dist_data[col])

# YAML-based column standardization (replaces standardize_against_dta)
dist_data = yaml_standardize_columns(dist_data, "CRSPdistributions")

# Save the data
dist_data.to_parquet("../pyData/Intermediate/CRSPdistributions.parquet")

print(f"CRSP Distributions data saved with {len(dist_data)} records",
      flush=True)

# Show sample of distribution codes
print("\nSample distribution codes:", flush=True)
sample_codes = dist_data['distcd'].value_counts().head(10)
print(sample_codes, flush=True)
print("=" * 60, flush=True)
print("✅ H_CRSPDistributions.py completed successfully", flush=True)
print("=" * 60, flush=True)