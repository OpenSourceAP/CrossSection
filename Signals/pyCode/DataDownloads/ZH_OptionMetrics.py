#!/usr/bin/env python3
"""
OptionMetrics data processing - Python equivalent of ZH_OptionMetrics.do

Processes multiple OptionMetrics CSV files and creates OptionMetricsBH.parquet
following the Bali-Hovakimiam (2009) implied volatility processing.
"""

import os
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns


def process_options_file(input_file, date_col='time_avail_m', output_name=None):
    """Process a single OptionMetrics CSV file."""
    if not os.path.exists(input_file):
        print(f"Warning: Input file not found: {input_file}")
        return None
    
    print(f"Processing {input_file}...")
    data = pd.read_csv(input_file)
    print(f"Loaded {len(data)} records")
    
    # If we have a date column that's not time_avail_m, convert it
    if date_col != 'time_avail_m' and date_col in data.columns:
        # Convert date column to datetime and create time_avail_m
        data['time_d'] = pd.to_datetime(data[date_col], format='%Y-%m-%d')
        # Create datetime64[ns] directly for time_avail_m (start of month)
        data['time_avail_m'] = data['time_d'].dt.to_period('M').dt.to_timestamp()
        # Keep the original date column and drop only intermediate columns
        data = data.drop(['time_d'], axis=1)
    elif 'time_avail_m' in data.columns:
        # time_avail_m already exists, convert to proper datetime format (start of month)
        data['time_avail_m'] = pd.to_datetime(data['time_avail_m']).dt.to_period('M').dt.to_timestamp()
    
    if output_name:
        # Standardize columns using YAML schema
        data = standardize_columns(data, output_name)
        
        # Save intermediate file if specified
        output_file = f"../pyData/Intermediate/{output_name}.parquet"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        data.to_parquet(output_file, index=False)
        print(f"Saved {output_name}: {len(data)} records")
    
    return data


def main():
    """Process OptionMetrics data files."""
    print("Processing OptionMetrics data...")
    
    # Process OptionMetrics Volume data
    print("Processing OptionMetricsVolume with case-sensitive column fixes...")
    vol_data = pd.read_csv("../pyData/Prep/OptionMetricsVolume.csv")
    # Fix column names case before processing
    vol_data = vol_data.rename(columns={'optVolume': 'optvolume', 'optInterest': 'optinterest'})
    
    # Convert time_avail_m to proper format - create datetime64[ns] directly (start of month)
    vol_data['time_avail_m'] = pd.to_datetime(vol_data['time_avail_m']).dt.to_period('M').dt.to_timestamp()
    
    # Standardize columns using YAML schema
    vol_data = standardize_columns(vol_data, "OptionMetricsVolume")
    
    # Save the data
    output_file = "../pyData/Intermediate/OptionMetricsVolume.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    vol_data.to_parquet(output_file, index=False)
    print(f"Saved OptionMetricsVolume: {len(vol_data)} records")
    
    # Process OptionMetrics Volatility Surface data
    vol_surf_data = process_options_file(
        "../pyData/Prep/OptionMetricsVolSurf.csv",
        date_col='date',
        output_name=None  # Don't save intermediate file
    )
    
    if vol_surf_data is not None:
        # Standardize columns to match DTA file
        vol_surf_data = standardize_columns(vol_surf_data, "OptionMetricsVolSurf")
        
        
        # Save standardized data
        output_file = "../pyData/Intermediate/OptionMetricsVolSurf.parquet"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        vol_surf_data.to_parquet(output_file, index=False)
        print(f"Saved OptionMetricsVolSurf: {len(vol_surf_data)} records")
    
    # Process OptionMetrics XZZ data
    print("Processing OptionMetricsXZZ with case-sensitive column fixes...")
    xzz_data = pd.read_csv("../pyData/Prep/OptionMetricsXZZ.csv")
    # Fix column names case before processing  
    xzz_data = xzz_data.rename(columns={'Skew1': 'skew1'})
    
    # Convert time_avail_m to proper format - create datetime64[ns] directly (start of month)
    xzz_data['time_avail_m'] = pd.to_datetime(xzz_data['time_avail_m']).dt.to_period('M').dt.to_timestamp()
    
    # Standardize columns to match DTA file
    xzz_data = standardize_columns(xzz_data, "OptionMetricsXZZ")
    
    # Save standardized data
    output_file = "../pyData/Intermediate/OptionMetricsXZZ.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    xzz_data.to_parquet(output_file, index=False)
    print(f"Saved OptionMetricsXZZ: {len(xzz_data)} records")
    
    # Process Bali-Hovakimian (2009) implied volatility data
    print("Processing Bali-Hovakimian implied volatility data...")
    bh_file = "../pyData/Prep/bali_hovak_imp_vol.csv"
    
    if not os.path.exists(bh_file):
        raise FileNotFoundError(f"Input file not found: {bh_file}")
    
    bh_data = pd.read_csv(bh_file)
    print(f"Loaded {len(bh_data)} BH records")
    
    # Convert date column to datetime and create time_avail_m
    bh_data['time_d'] = pd.to_datetime(bh_data['date'], format='%Y-%m-%d')
    # Create datetime64[ns] directly for time_avail_m (start of month)
    bh_data['time_avail_m'] = bh_data['time_d'].dt.to_period('M').dt.to_timestamp()
    
    # Drop intermediate columns
    bh_data = bh_data.drop(['date', 'time_d'], axis=1)
    
    # Drop rows with missing secid
    bh_data = bh_data.dropna(subset=['secid'])
    print(f"After dropping missing secid: {len(bh_data)} records")
    
    # Apply row limit for debugging if configured
    if MAX_ROWS_DL > 0:
        bh_data = bh_data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Standardize columns to match DTA file
    bh_data = standardize_columns(bh_data, "OptionMetricsBH")
    
    # MISSING VALUE FIX: Convert NaN to empty string for ticker column to match Stata format
    if 'ticker' in bh_data.columns:
        bh_data['ticker'] = bh_data['ticker'].fillna('')
        print("OptionMetricsBH: Applied missing value fix - converted ticker NaN to empty string")
    
    # Save final OptionMetricsBH data
    output_file = "../pyData/Intermediate/OptionMetricsBH.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    bh_data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(bh_data)} records to {output_file}")
    print("OptionMetrics data processing completed successfully.")


if __name__ == "__main__":
    main()