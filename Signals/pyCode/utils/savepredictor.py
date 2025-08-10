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
import polars as pl
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
    
    # Convert to polars if pandas DataFrame is passed
    if isinstance(df, pd.DataFrame):
        df_save = pl.from_pandas(df)
    else:
        df_save = df.clone()
    
    # Clean up - drop if predictor value is missing (equivalent to: drop if `1' == .)
    df_save = df_save.filter(pl.col(predictor_name).is_not_null())
    
    # Convert time_avail_m to yyyymm format (replicating Stata date conversion)
    # gen yyyymm = year(dofm(time_avail_m))*100 + month(dofm(time_avail_m))
    # Check if time_avail_m is datetime or integer
    if df_save['time_avail_m'].dtype == pl.Datetime:
        df_save = df_save.with_columns(
            (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("yyyymm")
        )
    elif str(df_save['time_avail_m'].dtype).startswith('Date'):
        # Handle Date type (not Datetime)
        df_save = df_save.with_columns(
            (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("yyyymm")
        )
    else:
        # Already in yyyymm integer format, just rename
        df_save = df_save.with_columns(
            pl.col("time_avail_m").alias("yyyymm")
        )
    
    # Keep only required columns and set order: permno yyyymm predictor_name
    df_save = df_save.select(['permno', 'yyyymm', predictor_name])
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as CSV (main output format per updated requirements)
    output_file = output_path / f"{predictor_name}.csv"
    df_save.write_csv(output_file)
    
    print(f"Saved {len(df_save)} rows to {output_file}")