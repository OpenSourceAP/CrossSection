# ABOUTME: saveplacebo.py - saves placebo data in standardized CSV format 
# ABOUTME: Python equivalent of savepredictor.do for placebos, simplified to only save CSV files

"""
saveplacebo.py

Usage:
    from utils.saveplacebo import save_placebo
    save_placebo(df, 'PlaceboName')

Inputs:
    - df: DataFrame with columns [permno, time_avail_m, placebo_name]
    - placebo_name: Name of the placebo column
    - output_dir: Output directory path (default: ../pyData/Placebos)

Outputs:
    - CSV file in pyData/Placebos/ with columns [permno, yyyymm, placebo_name]
    - Drops rows with missing placebo values
    - Converts time_avail_m to yyyymm format
"""

import pandas as pd
import polars as pl
from pathlib import Path


def save_placebo(df, placebo_name, output_dir="../pyData/Placebos"):
    """
    Saves placebo data in CSV format - Python equivalent of savepredictor.do for placebos
    Simplified version that only saves CSV (no DTA/parquet options)
    
    Args:
        df: DataFrame with columns [permno, time_avail_m, placebo_name]
        placebo_name: Name of the placebo column
        output_dir: Output directory path
    """
    
    print(f"saving {placebo_name}")
    
    # Convert to polars if pandas DataFrame is passed
    if isinstance(df, pd.DataFrame):
        df_save = pl.from_pandas(df)
    else:
        df_save = df.clone()
    
    # Clean up - drop if placebo value is missing (equivalent to: drop if `1' == .)
    df_save = df_save.filter(pl.col(placebo_name).is_not_null())
    
    # Convert time_avail_m to yyyymm format (replicating Stata date conversion)
    # gen yyyymm = year(dofm(time_avail_m))*100 + month(dofm(time_avail_m))
    df_save = df_save.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("yyyymm")
    )
    
    # Keep only required columns and set order: permno yyyymm placebo_name
    df_save = df_save.select(['permno', 'yyyymm', placebo_name])
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as CSV (main output format per updated requirements)
    output_file = output_path / f"{placebo_name}.csv"
    df_save.write_csv(output_file)
    
    print(f"Saved {len(df_save)} rows to {output_file}")