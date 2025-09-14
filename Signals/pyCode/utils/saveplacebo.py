# ABOUTME: Save utilities for placebo signals in standardized format
# ABOUTME: Saves data as CSV files in pyData/Placebos/ with standard columns: permno, yyyymm, signal_value

import pandas as pd
import numpy as np
import os

def save_placebo(df, signal_name):
    """
    Save placebo signal data to CSV in standardized format.
    
    Parameters:
    -----------
    df : pd.DataFrame or pl.DataFrame
        DataFrame containing permno, time_avail_m, and signal columns
    signal_name : str
        Name of the signal column and output file
    
    Output format:
    - permno: integer
    - yyyymm: integer (YYYYMM format)  
    - signal_value: float
    """
    
    # Convert polars to pandas if needed
    if hasattr(df, 'to_pandas'):
        df = df.to_pandas()
    
    # Ensure we have the required columns
    if 'permno' not in df.columns:
        raise ValueError("DataFrame must contain 'permno' column")
    if 'time_avail_m' not in df.columns:
        raise ValueError("DataFrame must contain 'time_avail_m' column") 
    if signal_name not in df.columns:
        raise ValueError(f"DataFrame must contain '{signal_name}' column")
    
    # Create output dataframe with standard format
    output_df = df[['permno', 'time_avail_m', signal_name]].copy()
    
    # Remove rows where signal is missing
    output_df = output_df.dropna(subset=[signal_name])
    
    # Convert time_avail_m to yyyymm format
    if pd.api.types.is_datetime64_any_dtype(output_df['time_avail_m']):
        output_df['yyyymm'] = output_df['time_avail_m'].dt.year * 100 + output_df['time_avail_m'].dt.month
    else:
        # Assume already in period format, extract year and month
        output_df['yyyymm'] = output_df['time_avail_m'].apply(lambda x: x.year * 100 + x.month if pd.notna(x) else np.nan)
    
    # Create final output with standardized columns
    final_df = pd.DataFrame({
        'permno': output_df['permno'].astype(int),
        'yyyymm': output_df['yyyymm'].astype(int),
        signal_name: output_df[signal_name]
    })
    
    # Sort by permno and yyyymm
    final_df = final_df.sort_values(['permno', 'yyyymm'])
    
    # Ensure output directory exists
    output_dir = '../pyData/Placebos'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_file = f'{output_dir}/{signal_name}.csv'
    final_df.to_csv(output_file, index=False)
    
    print(f"Saved {len(final_df)} observations to {output_file}")
    
    return final_df