# ABOUTME: Python wrapper for Patent Citations using original R script
# ABOUTME: Calls R script then handles post-processing and saves as Parquet

import subprocess
import pandas as pd
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function that calls R script and handles post-processing"""
    
    logger.info("Starting Patent Citations processing using R script...")
    
    # Ensure output directory exists
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    
    # Get the project root path (parent of pyCode)
    project_root = str(Path().absolute().parent)
    
    # Call the R script
    logger.info("Calling R script...")
    r_script_path = "DataDownloads/ZIR_Patents.R"
    
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
    
    # Read the R script output (DTA format)
    logger.info("Reading R script output...")
    r_output_path = "../pyData/Intermediate/PatentDataProcessed.dta"
    
    if not os.path.exists(r_output_path):
        raise FileNotFoundError(f"R script output file not found at {r_output_path}")
    
    # Read DTA file using pandas - ensure we get a DataFrame
    patent_data = pd.read_stata(r_output_path, preserve_dtypes=False)
    if not isinstance(patent_data, pd.DataFrame):
        # If it's a StataReader, convert to DataFrame
        patent_data = patent_data.read()
    logger.info(f"Loaded R script output: {len(patent_data):,} rows")
    
    # Basic data processing to ensure consistency
    logger.info("Processing patent data...")
    
    # Ensure proper data types
    if 'gvkey' in patent_data.columns:
        patent_data['gvkey'] = patent_data['gvkey'].astype('Int64')
    if 'year' in patent_data.columns:
        patent_data['year'] = patent_data['year'].astype('Int64')
    if 'npat' in patent_data.columns:
        patent_data['npat'] = patent_data['npat'].astype(float)
    if 'ncitscale' in patent_data.columns:
        patent_data['ncitscale'] = patent_data['ncitscale'].astype(float)
    
    # Handle missing values consistently
    fillna_dict = {}
    if 'npat' in patent_data.columns:
        fillna_dict['npat'] = 0.0
    if 'ncitscale' in patent_data.columns:
        fillna_dict['ncitscale'] = 0.0
    
    if fillna_dict:
        patent_data = patent_data.fillna(fillna_dict)
    
    logger.info(f"After processing: {len(patent_data):,} rows")
    
    # Save to parquet
    output_path = "../pyData/Intermediate/PatentDataProcessed.parquet"
    patent_data.to_parquet(output_path, index=False)
    
    logger.info(f"Successfully saved {len(patent_data):,} rows to {output_path}")
    logger.info("Patent Citations processing completed successfully!")
    
    # Show sample data
    logger.info("Sample data:")
    logger.info(patent_data.head().to_string())
    
    # Show summary statistics
    logger.info("Summary statistics:")
    for col in ['npat', 'ncitscale']:
        if col in patent_data.columns:
            series_data = patent_data[col].dropna()
            if len(series_data) > 0:
                logger.info(f"{col}: mean={series_data.mean():.6f}, std={series_data.std():.6f}, count={len(series_data)}")
    
    return patent_data

if __name__ == "__main__":
    main()