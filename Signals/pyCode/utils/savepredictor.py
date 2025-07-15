# ABOUTME: savepredictor.py - saves predictor data in standardized CSV format 
# ABOUTME: Python equivalent of savepredictor.do, simplified to only save CSV files

"""
savepredictor.py

Usage:
    from utils.savepredictor import save_predictor
    save_predictor(df, 'PredictorName')

Inputs:
    - df: DataFrame with columns [permno, time_avail_m, predictor_name]
    - predictor_name: Name of the predictor column
    - output_dir: Output directory path (default: ../pyData/Predictors)

Outputs:
    - CSV file in pyData/Predictors/ with columns [permno, yyyymm, predictor_name]
    - Drops rows with missing predictor values
    - Converts time_avail_m to yyyymm format
"""

import pandas as pd
from pathlib import Path


def save_predictor(df, predictor_name, output_dir="../pyData/Predictors"):
    """
    Saves predictor data in CSV format - Python equivalent of savepredictor.do
    Simplified version that only saves CSV (no DTA/parquet options)
    
    Args:
        df: DataFrame with columns [permno, time_avail_m, predictor_name]
        predictor_name: Name of the predictor column
        output_dir: Output directory path
    """
    
    print(f"saving {predictor_name}")
    
    # Create a copy to avoid modifying original data (equivalent to preserve/restore)
    df_save = df.copy()
    
    # Clean up - drop if predictor value is missing (equivalent to: drop if `1' == .)
    df_save = df_save.dropna(subset=[predictor_name])
    
    # Convert time_avail_m to yyyymm format (replicating Stata date conversion)
    # gen yyyymm = year(dofm(time_avail_m))*100 + month(dofm(time_avail_m))
    df_save['yyyymm'] = df_save['time_avail_m'].dt.year * 100 + df_save['time_avail_m'].dt.month
    
    # Keep only required columns and set order: permno yyyymm predictor_name
    df_save = df_save[['permno', 'yyyymm', predictor_name]].copy()
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as CSV (main output format per updated requirements)
    output_file = output_path / f"{predictor_name}.csv"
    df_save.to_csv(output_file, index=False)
    
    print(f"Saved {len(df_save)} rows to {output_file}")