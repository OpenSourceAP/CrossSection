#%%

# ABOUTME: Converts many OptionMetrics datasets into cleaned pyData/Intermediate/*.parquet files
# ABOUTME: OptionMetrics datasets come from ZH1_OptionVolume.py and PrepScripts/OptionMetricsProcessing.R
"""
Usage:
    python3 DataDownloads/ZH2_OptionMetricsCleaning.py

Outputs:
    - pyData/Intermediate/OptionMetricsVolSurf.parquet
    - pyData/Intermediate/OptionMetricsXZZ.parquet
    - pyData/Intermediate/OptionMetricsBH.parquet
"""

import os
import pandas as pd
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

print("Processing OptionMetrics data...")

# Create output directory
os.makedirs("../pyData/Intermediate", exist_ok=True)

# tbc: OptionMetricsVolume cleaning

# Process OptionMetrics Volatility Surface data
print("Processing OptionMetricsVolSurf...")
vol_surf_data = pd.read_csv("../pyData/Prep/OptionMetricsVolSurf.csv")

# convert time_avail_m to first of the month 
# (we use the convention that time_avail_m represents a monthly date, and use 
# the first as an arbitrary day of the month)
vol_surf_data['time_avail_m'] = pd.to_datetime(vol_surf_data['time_avail_m']).dt.to_period('M').dt.to_timestamp()
vol_surf_data = standardize_columns(vol_surf_data, "OptionMetricsVolSurf")
vol_surf_data.to_parquet("../pyData/Intermediate/OptionMetricsVolSurf.parquet", index=False)
print(f"Saved OptionMetricsVolSurf: {len(vol_surf_data)} records")

# Process OptionMetrics XZZ data
print("Processing OptionMetricsXZZ...")
xzz_data = pd.read_csv("../pyData/Prep/OptionMetricsXZZ.csv")
xzz_data = xzz_data.rename(columns={'Skew1': 'skew1'})
xzz_data['time_avail_m'] = pd.to_datetime(xzz_data['time_avail_m']).dt.to_period('M').dt.to_timestamp()
xzz_data = standardize_columns(xzz_data, "OptionMetricsXZZ")
xzz_data.to_parquet("../pyData/Intermediate/OptionMetricsXZZ.parquet", index=False)
print(f"Saved OptionMetricsXZZ: {len(xzz_data)} records")

# Process Bali-Hovakimian (2009) implied volatility data
print("Processing OptionMetricsBH...")
bh_data = pd.read_csv("../pyData/Prep/bali_hovak_imp_vol.csv")
bh_data['time_avail_m'] = pd.to_datetime(bh_data['date']).dt.to_period('M').dt.to_timestamp()
bh_data = standardize_columns(bh_data, "OptionMetricsBH")
bh_data.to_parquet("../pyData/Intermediate/OptionMetricsBH.parquet", index=False)
print(f"Saved OptionMetricsBH: {len(bh_data)} records")

print("OptionMetrics data processing completed successfully.")