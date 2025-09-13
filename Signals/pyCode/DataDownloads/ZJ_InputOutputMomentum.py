# ABOUTME: Python wrapper for Input-Output Momentum calculation using R script
# ABOUTME: Calls R script for momentum calculations then applies Stata post-processing and saves as Parquet
"""
Inputs:
- DataDownloads/ZJR_InputOutputMomentum.R (R script)
- ../pyData/Intermediate/InputOutputMomentum_R.csv (R script output)

Outputs:
- ../pyData/Intermediate/InputOutputMomentumProcessed.parquet

How to run: python3 ZJ_InputOutputMomentum.py
"""

import subprocess
import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.column_standardizer_yaml import standardize_columns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():

    logger.info("Starting InputOutputMomentum processing using R script...")

    # Create output directory
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Get project root path for R script
    project_root = str(Path().absolute().parent)

    # Execute R script for momentum calculations
    logger.info("Calling R script...")
    r_script_path = "DataDownloads/ZJR_InputOutputMomentum.R"

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

    final_output = iomom_wide[expected_cols].copy()

    # Convert gvkey to Int64 for consistency
    final_output['gvkey'] = final_output['gvkey'].astype('Int64')

    # Apply column standardization and save to parquet
    output_path = "../pyData/Intermediate/InputOutputMomentumProcessed.parquet"
    final_output = standardize_columns(final_output, 'InputOutputMomentumProcessed')
    final_output.to_parquet(output_path, index=False)

    logger.info(f"Successfully saved {len(final_output):,} rows to {output_path}")
    logger.info("InputOutputMomentum processing completed successfully!")

    # Display sample and summary statistics
    logger.info("Sample data:")
    logger.info(final_output.head().to_string())

    logger.info("Summary statistics:")
    for col in ['retmatchcustomer', 'retmatchsupplier']:
        if col in final_output.columns:
            series_data = final_output[col].dropna()
            if len(series_data) > 0:
                logger.info(f"{col}: mean={series_data.mean():.6f}, std={series_data.std():.6f}, count={len(series_data)}")

    return final_output

if __name__ == "__main__":
    main()