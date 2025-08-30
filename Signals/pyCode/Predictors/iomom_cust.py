# ABOUTME: Calculates customer momentum following Menzly and Ozbas 2010 Table 2 (1) r_customer,t-1
# ABOUTME: Run: python3 pyCode/Predictors/iomom_cust.py

"""
iomom_cust Predictor - Input-Output Customer Momentum

This predictor extracts customer momentum from pre-computed Input-Output momentum data.
The heavy computation is done in R (ZJR_InputOutputMomentum.R), and this script
simply extracts the relevant column and merges with the signal master table.

Inputs:
- SignalMasterTable.parquet (permno, gvkey, time_avail_m)
- InputOutputMomentumProcessed.parquet (gvkey, time_avail_m, retmatchcustomer)

Outputs:
- iomom_cust.csv (permno, yyyymm, iomom_cust)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting iomom_cust predictor...")

# DATA LOAD
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                               columns=['permno', 'gvkey', 'time_avail_m'])

# drop if gvkey ==.
signal_master = signal_master.dropna(subset=['gvkey'])
print(f"Loaded {len(signal_master):,} observations with gvkey")

print("Loading InputOutputMomentumProcessed...")
iomom_df = pd.read_parquet('../pyData/Intermediate/InputOutputMomentumProcessed.parquet')
print(f"Loaded {len(iomom_df):,} InputOutputMomentum observations")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/InputOutputMomentumProcessed", keep(master match) nogenerate
print("Merging with InputOutputMomentumProcessed...")
df = pd.merge(signal_master, iomom_df, on=['gvkey', 'time_avail_m'], how='left')
print(f"After merge: {len(df):,} observations")

# SIGNAL CONSTRUCTION
# gen iomom_cust = retmatchcustomer
df['iomom_cust'] = df['retmatchcustomer']

# keep if iomom_cust != .
df = df.dropna(subset=['iomom_cust'])
print(f"After dropping missing iomom_cust: {len(df):,} observations")

# Keep only needed columns for save
df = df[['permno', 'time_avail_m', 'iomom_cust']].copy()

# SAVE
print("Saving predictor...")
save_predictor(df, 'iomom_cust')

print("iomom_cust predictor completed successfully!")