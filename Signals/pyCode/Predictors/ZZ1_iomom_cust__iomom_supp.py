# ABOUTME: Calculates customer and supplier momentum following Menzly and Ozbas 2010 Table 2 (1) r_customer,t-1 and r_supplier,t-1
# ABOUTME: Run: python3 pyCode/Predictors/ZZ1_iomom_cust__iomom_supp.py

"""
ZZ1_iomom_cust__iomom_supp Predictor - Input-Output Customer and Supplier Momentum

This predictor runs the R script for Input-Output momentum calculations, processes the results,
and extracts both customer and supplier momentum signals.

Inputs:
- Predictors/ZZ1_iomom_cust__iomom_supp.R (R script)
- SignalMasterTable.parquet (permno, gvkey, time_avail_m)

Outputs:
- iomom_cust.csv (permno, yyyymm, iomom_cust)
- iomom_supp.csv (permno, yyyymm, iomom_supp)
"""

import subprocess
import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path
import sys

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Starting iomom_cust and iomom_supp predictors...")

# STEP 1: RUN R SCRIPT FOR INPUT-OUTPUT MOMENTUM CALCULATIONS
logger.info("Starting InputOutputMomentum processing using R script...")

# Create output directory
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Get project root path for R script
project_root = str(Path().absolute().parent)

# Execute R script for momentum calculations
logger.info("Calling R script...")
r_script_path = "Predictors/ZZ1_iomom_cust__iomom_supp.R"

try:
    result = subprocess.run([
        "Rscript", r_script_path, project_root
    ], capture_output=True, text=True, timeout=1800)

    if result.returncode != 0:
        logger.error(f"R script failed with return code {result.returncode}")
        logger.error(f"STDERR: {result.stderr}")
        logger.error(f"STDOUT: {result.stdout}")
        raise RuntimeError(f"R script execution failed: {result.stderr}")

    logger.info("R script completed successfully")
    if result.stdout:
        logger.info(f"R output: {result.stdout}")

except subprocess.TimeoutExpired:
    logger.error("R script timed out after 30 minutes")
    raise
except Exception as e:
    logger.error(f"Error running R script: {str(e)}")
    raise

# STEP 2: LOAD AND PROCESS R SCRIPT OUTPUT
# Load R script output
logger.info("Reading R script output...")
r_output_path = "../pyData/Intermediate/InputOutputMomentum_R.csv"

if not os.path.exists(r_output_path):
    raise FileNotFoundError(f"R script output file not found at {r_output_path}")

iomom = pd.read_csv(r_output_path)
logger.info(f"Loaded R script output: {len(iomom):,} rows")

# Apply Stata-style post-processing
logger.info("Applying Stata post-processing...")

# Create monthly time variable from year_avail and month_avail
temp_df = iomom[['year_avail', 'month_avail']].copy()
temp_df['year'] = temp_df['year_avail'].astype(int)
temp_df['month'] = temp_df['month_avail'].astype(int)
temp_df['day'] = 1
iomom['time_avail_m'] = pd.to_datetime(temp_df[['year', 'month', 'day']])

logger.info(f"After time_avail_m creation: {len(iomom):,} rows")

# Collapse data by averaging retmatch and portind within gvkey-time_avail_m-type groups
iomom_collapsed = iomom.groupby(['gvkey', 'time_avail_m', 'type']).agg({
    'retmatch': 'mean',
    'portind': 'mean'
}).reset_index()

logger.info(f"After collapse: {len(iomom_collapsed):,} rows")

# Reshape from long to wide format by type (customer/supplier)
iomom_wide = iomom_collapsed.pivot_table(
    index=['gvkey', 'time_avail_m'],
    columns='type',
    values=['retmatch', 'portind'],
    fill_value=np.nan
).reset_index()

logger.info(f"After pivot to wide: {len(iomom_wide):,} rows")

# Flatten column names to match Stata reshape wide convention
iomom_wide.columns = [f'{col[0]}{col[1]}' if col[1] else col[0] for col in iomom_wide.columns]

# Ensure all expected columns exist
expected_cols = ['gvkey', 'time_avail_m', 'retmatchcustomer', 'portindcustomer', 'retmatchsupplier', 'portindsupplier']
for col in expected_cols:
    if col not in iomom_wide.columns:
        logger.warning(f"Missing expected column: {col}")
        iomom_wide[col] = np.nan

final_iomom = iomom_wide[expected_cols].copy()

# Convert gvkey to Int64 for consistency
final_iomom['gvkey'] = final_iomom['gvkey'].astype('Int64')

# Save to parquet
output_path = "../pyData/Intermediate/InputOutputMomentumProcessed.parquet"
final_iomom.to_parquet(output_path, index=False)

logger.info(f"Successfully saved {len(final_iomom):,} rows to {output_path}")
logger.info("InputOutputMomentum processing completed successfully!")

# Display sample and summary statistics
logger.info("Sample data:")
logger.info(final_iomom.head().to_string())

logger.info("Summary statistics:")
for col in ['retmatchcustomer', 'retmatchsupplier']:
    if col in final_iomom.columns:
        series_data = final_iomom[col].dropna()
        if len(series_data) > 0:
            logger.info(f"{col}: mean={series_data.mean():.6f}, std={series_data.std():.6f}, count={len(series_data)}")

# STEP 3: LOAD SIGNAL MASTER TABLE AND MERGE
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                               columns=['permno', 'gvkey', 'time_avail_m'])

# Drop observations with missing gvkey
signal_master = signal_master.dropna(subset=['gvkey'])
print(f"Loaded {len(signal_master):,} observations with gvkey")

# Use the processed iomom data
iomom_df = final_iomom
print(f"Using {len(iomom_df):,} InputOutputMomentum observations")

# STEP 4: MERGE AND CREATE PREDICTORS
# Merge with InputOutputMomentumProcessed data on gvkey and time_avail_m
print("Merging with InputOutputMomentumProcessed...")
df = pd.merge(signal_master, iomom_df, on=['gvkey', 'time_avail_m'], how='left')
print(f"After merge: {len(df):,} observations")

# SIGNAL CONSTRUCTION - Customer Momentum
# Set customer momentum variable from retmatchcustomer column
df['iomom_cust'] = df['retmatchcustomer']

# Keep only observations with valid customer momentum values for saving
df_cust = df.dropna(subset=['iomom_cust'])
print(f"After dropping missing iomom_cust: {len(df_cust):,} observations")

# Keep only needed columns for customer momentum save
df_cust = df_cust[['permno', 'time_avail_m', 'iomom_cust']].copy()

# SAVE Customer Momentum
print("Saving iomom_cust predictor...")
save_predictor(df_cust, 'iomom_cust')

# SIGNAL CONSTRUCTION - Supplier Momentum
# Set supplier momentum variable from retmatchsupplier column
df['iomom_supp'] = df['retmatchsupplier']

# Keep only observations with valid supplier momentum values for saving
df_supp = df.dropna(subset=['iomom_supp'])
print(f"After dropping missing iomom_supp: {len(df_supp):,} observations")

# Keep only needed columns for supplier momentum save
df_supp = df_supp[['permno', 'time_avail_m', 'iomom_supp']].copy()

# SAVE Supplier Momentum
print("Saving iomom_supp predictor...")
save_predictor(df_supp, 'iomom_supp')

print("iomom_cust and iomom_supp predictors completed successfully!")