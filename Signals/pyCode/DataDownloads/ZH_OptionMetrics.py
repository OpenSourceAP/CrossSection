#!/usr/bin/env python3
"""
OptionMetrics data processing - Python equivalent of ZH_OptionMetrics.do

Processes multiple OptionMetrics CSV files and creates OptionMetricsBH.parquet
following the Bali-Hovakimiam (2009) implied volatility processing.
"""

import os
import pandas as pd


def process_options_file(input_file, date_col='time_avail_m', output_name=None):
    """Process a single OptionMetrics CSV file."""
    if not os.path.exists(input_file):
        print(f"Warning: Input file not found: {input_file}")
        return None
    
    print(f"Processing {input_file}...")
    data = pd.read_csv(input_file)
    print(f"Loaded {len(data)} records")
    
    # Convert date column to datetime and create time_avail_m
    data['time_d'] = pd.to_datetime(data[date_col], format='%Y-%m-%d')
    data['time_avail_m'] = data['time_d'].dt.to_period('M')
    
    # Drop intermediate columns
    data = data.drop([date_col, 'time_d'], axis=1)
    
    if output_name:
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
    process_options_file(
        "../Data/Prep/OptionMetricsVolume.csv",
        date_col='time_avail_m',
        output_name='OptionMetricsVolume'
    )
    
    # Process OptionMetrics Volatility Surface data
    vol_surf_data = process_options_file(
        "../Data/Prep/OptionMetricsVolSurf.csv",
        date_col='time_avail_m',
        output_name=None  # Don't save intermediate file
    )
    
    if vol_surf_data is not None:
        # Reorder columns as in Stata
        expected_cols = ['secid', 'days', 'delta', 'cp_flag', 'time_avail_m']
        vol_surf_cols = [col for col in expected_cols if col in vol_surf_data.columns]
        other_cols = [col for col in vol_surf_data.columns if col not in expected_cols]
        vol_surf_data = vol_surf_data[vol_surf_cols + other_cols]
        
        # Save reordered data
        output_file = "../pyData/Intermediate/OptionMetricsVolSurf.parquet"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        vol_surf_data.to_parquet(output_file, index=False)
        print(f"Saved OptionMetricsVolSurf: {len(vol_surf_data)} records")
    
    # Process OptionMetrics XZZ data
    xzz_data = process_options_file(
        "../Data/Prep/OptionMetricsXZZ.csv",
        date_col='time_avail_m',
        output_name=None  # Don't save intermediate file
    )
    
    if xzz_data is not None:
        # Reorder columns as in Stata
        expected_cols = ['secid', 'time_avail_m']
        xzz_cols = [col for col in expected_cols if col in xzz_data.columns]
        other_cols = [col for col in xzz_data.columns if col not in expected_cols]
        xzz_data = xzz_data[xzz_cols + other_cols]
        
        # Save reordered data
        output_file = "../pyData/Intermediate/OptionMetricsXZZ.parquet"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        xzz_data.to_parquet(output_file, index=False)
        print(f"Saved OptionMetricsXZZ: {len(xzz_data)} records")
    
    # Process Bali-Hovakimian (2009) implied volatility data
    print("Processing Bali-Hovakimian implied volatility data...")
    bh_file = "../Data/Prep/bali_hovak_imp_vol.csv"
    
    if not os.path.exists(bh_file):
        raise FileNotFoundError(f"Input file not found: {bh_file}")
    
    bh_data = pd.read_csv(bh_file)
    print(f"Loaded {len(bh_data)} BH records")
    
    # Convert date column to datetime and create time_avail_m
    bh_data['time_d'] = pd.to_datetime(bh_data['date'], format='%Y-%m-%d')
    bh_data['time_avail_m'] = bh_data['time_d'].dt.to_period('M')
    
    # Drop intermediate columns
    bh_data = bh_data.drop(['date', 'time_d'], axis=1)
    
    # Drop rows with missing secid
    bh_data = bh_data.dropna(subset=['secid'])
    print(f"After dropping missing secid: {len(bh_data)} records")
    
    # Reorder columns as in Stata
    expected_cols = ['secid', 'time_avail_m']
    bh_cols = [col for col in expected_cols if col in bh_data.columns]
    other_cols = [col for col in bh_data.columns if col not in expected_cols]
    bh_data = bh_data[bh_cols + other_cols]
    
    # Save final OptionMetricsBH data
    output_file = "../pyData/Intermediate/OptionMetricsBH.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    bh_data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(bh_data)} records to {output_file}")
    print("OptionMetrics data processing completed successfully.")


if __name__ == "__main__":
    main()