# ABOUTME: Calculates customer and supplier momentum following Menzly and Ozbas 2010 Table 2 (1)
# ABOUTME: Run: python3 pyCode/Predictors/ZZ1_iomom_cust__iomom_supp.py

"""
ZZ1_iomom_cust__iomom_supp Predictor - Consolidated Input-Output Momentum

This script combines the functionality of:
1. DataDownloads/ZJ_InputOutputMomentum.py - Runs R script and processes data
2. Predictors/iomom_cust.py - Extracts customer momentum
3. Predictors/iomom_supp.py - Extracts supplier momentum

The heavy computation is done in R (ZZ1_iomom_cust__iomom_supp.R), then this script
processes the output and creates both predictor files.

Inputs:
- SignalMasterTable.parquet (permno, gvkey, time_avail_m)
- R script output: InputOutputMomentum_R.csv

Outputs:
- InputOutputMomentumProcessed.parquet (intermediate)
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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.column_standardizer_yaml import standardize_columns
from utils.save_standardized import save_predictor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_r_script_and_process():
    """Run R script and process the output to create intermediate data"""
    
    logger.info("Starting InputOutputMomentum processing using R script...")
    
    # Ensure output directory exists
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    
    # Get the project root path (parent of pyCode)
    project_root = str(Path().absolute().parent)
    
    # Call the R script
    logger.info("Calling R script...")
    r_script_path = "Predictors/ZZ1_iomom_cust__iomom_supp.R"
    
    try:
        # Run R script with project root as argument
        result = subprocess.run([
            "Rscript", r_script_path, project_root
        ], capture_output=True, text=True, timeout=1800)  # 30 minute timeout
        
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
    
    # Read the R script output
    logger.info("Reading R script output...")
    r_output_path = "../pyData/Intermediate/InputOutputMomentum_R.csv"
    
    if not os.path.exists(r_output_path):
        raise FileNotFoundError(f"R script output file not found at {r_output_path}")
    
    iomom = pd.read_csv(r_output_path)
    logger.info(f"Loaded R script output: {len(iomom):,} rows")
    
    # Stata post-processing following ZJ_InputOutputMomentum.do
    logger.info("Applying Stata post-processing...")
    
    # gen time_avail_m = ym(year_avail, month_avail)
    temp_df = iomom[['year_avail', 'month_avail']].copy()
    temp_df['year'] = temp_df['year_avail'].astype(int)
    temp_df['month'] = temp_df['month_avail'].astype(int)
    temp_df['day'] = 1
    iomom['time_avail_m'] = pd.to_datetime(temp_df[['year', 'month', 'day']])
    
    logger.info(f"After time_avail_m creation: {len(iomom):,} rows")
    
    # gcollapse (mean) retmatch portind, by(gvkey time_avail_m type)
    iomom_collapsed = iomom.groupby(['gvkey', 'time_avail_m', 'type']).agg({
        'retmatch': 'mean',
        'portind': 'mean'
    }).reset_index()
    
    logger.info(f"After collapse: {len(iomom_collapsed):,} rows")
    
    # reshape wide retmatch portind, i(gvkey time_avail_m) j(type) string
    iomom_wide = iomom_collapsed.pivot_table(
        index=['gvkey', 'time_avail_m'],
        columns='type',
        values=['retmatch', 'portind'],
        fill_value=np.nan
    ).reset_index()
    
    logger.info(f"After pivot to wide: {len(iomom_wide):,} rows")
    
    # Flatten column names - matches Stata's reshape wide naming convention
    iomom_wide.columns = [f'{col[0]}{col[1]}' if col[1] else col[0] for col in iomom_wide.columns]
    
    # Ensure we have expected columns (matching Stata output)
    expected_cols = ['gvkey', 'time_avail_m', 'retmatchcustomer', 'portindcustomer', 'retmatchsupplier', 'portindsupplier']
    for col in expected_cols:
        if col not in iomom_wide.columns:
            logger.warning(f"Missing expected column: {col}")
            iomom_wide[col] = np.nan
    
    final_output = iomom_wide[expected_cols].copy()
    
    # Convert gvkey to Int64 for consistency with other datasets
    final_output['gvkey'] = final_output['gvkey'].astype('Int64')
    
    # Save intermediate parquet
    output_path = "../pyData/Intermediate/InputOutputMomentumProcessed.parquet"
    # Apply column standardization
    final_output = standardize_columns(final_output, 'InputOutputMomentumProcessed')
    final_output.to_parquet(output_path, index=False)
    
    logger.info(f"Successfully saved {len(final_output):,} rows to {output_path}")
    
    # Show summary statistics
    logger.info("Summary statistics for intermediate data:")
    for col in ['retmatchcustomer', 'retmatchsupplier']:
        if col in final_output.columns:
            series_data = final_output[col].dropna()
            if len(series_data) > 0:
                logger.info(f"{col}: mean={series_data.mean():.6f}, std={series_data.std():.6f}, count={len(series_data)}")
    
    return final_output

def create_iomom_cust():
    """Create customer momentum predictor"""
    
    print("Starting iomom_cust predictor...")
    
    # DATA LOAD
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                                   columns=['permno', 'gvkey', 'time_avail_m'])
    
    # Drop observations with missing gvkey
    signal_master = signal_master.dropna(subset=['gvkey'])
    print(f"Loaded {len(signal_master):,} observations with gvkey")
    
    print("Loading InputOutputMomentumProcessed...")
    iomom_df = pd.read_parquet('../pyData/Intermediate/InputOutputMomentumProcessed.parquet')
    print(f"Loaded {len(iomom_df):,} InputOutputMomentum observations")
    
    # Merge with InputOutputMomentumProcessed data on gvkey and time_avail_m
    print("Merging with InputOutputMomentumProcessed...")
    df = pd.merge(signal_master, iomom_df, on=['gvkey', 'time_avail_m'], how='left')
    print(f"After merge: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    # Set customer momentum variable from retmatchcustomer column
    df['iomom_cust'] = df['retmatchcustomer']
    
    # Keep only observations with valid customer momentum values
    df = df.dropna(subset=['iomom_cust'])
    print(f"After dropping missing iomom_cust: {len(df):,} observations")
    
    # Keep only needed columns for save
    df = df[['permno', 'time_avail_m', 'iomom_cust']].copy()
    
    # SAVE
    print("Saving iomom_cust predictor...")
    save_predictor(df, 'iomom_cust')
    
    print("iomom_cust predictor completed successfully!")
    return len(df)

def create_iomom_supp():
    """Create supplier momentum predictor"""
    
    print("Starting iomom_supp predictor...")
    
    # DATA LOAD
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                                   columns=['permno', 'gvkey', 'time_avail_m'])
    
    # Drop observations with missing gvkey
    signal_master = signal_master.dropna(subset=['gvkey'])
    print(f"Loaded {len(signal_master):,} observations with gvkey")
    
    print("Loading InputOutputMomentumProcessed...")
    iomom_df = pd.read_parquet('../pyData/Intermediate/InputOutputMomentumProcessed.parquet')
    print(f"Loaded {len(iomom_df):,} InputOutputMomentum observations")
    
    # Merge with InputOutputMomentumProcessed data on gvkey and time_avail_m
    print("Merging with InputOutputMomentumProcessed...")
    df = pd.merge(signal_master, iomom_df, on=['gvkey', 'time_avail_m'], how='left')
    print(f"After merge: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    # Set supplier momentum variable from retmatchsupplier column
    df['iomom_supp'] = df['retmatchsupplier']
    
    # Keep only observations with valid supplier momentum values
    df = df.dropna(subset=['iomom_supp'])
    print(f"After dropping missing iomom_supp: {len(df):,} observations")
    
    # Keep only needed columns for save
    df = df[['permno', 'time_avail_m', 'iomom_supp']].copy()
    
    # SAVE
    print("Saving iomom_supp predictor...")
    save_predictor(df, 'iomom_supp')
    
    print("iomom_supp predictor completed successfully!")
    return len(df)

def main():
    """Main function that orchestrates the entire process"""
    
    logger.info("="*80)
    logger.info("Starting consolidated ZZ1_iomom_cust__iomom_supp predictor")
    logger.info("="*80)
    
    # Step 1: Run R script and process intermediate data
    run_r_script_and_process()
    
    # Step 2: Create customer momentum predictor
    logger.info("\n" + "="*80)
    logger.info("Creating customer momentum predictor")
    logger.info("="*80)
    cust_count = create_iomom_cust()
    
    # Step 3: Create supplier momentum predictor
    logger.info("\n" + "="*80)
    logger.info("Creating supplier momentum predictor")
    logger.info("="*80)
    supp_count = create_iomom_supp()
    
    # Final summary
    logger.info("\n" + "="*80)
    logger.info("CONSOLIDATED SCRIPT COMPLETED SUCCESSFULLY!")
    logger.info(f"Created iomom_cust.csv with {cust_count:,} observations")
    logger.info(f"Created iomom_supp.csv with {supp_count:,} observations")
    logger.info("="*80)

if __name__ == "__main__":
    main()