# ABOUTME: Calculates customer and supplier momentum following Menzly and Ozbas 2010 Table 2 (1) r_customer,t-1 and r_supplier,t-1
# ABOUTME: Run: python3 pyCode/Predictors/ZZ1_iomom_cust__iomom_supp.py

"""
ZZ1_iomom_cust__iomom_supp Predictor - Input-Output Customer and Supplier Momentum

This predictor extracts both customer and supplier momentum from pre-computed Input-Output momentum data.
The heavy computation is done in R (ZJR_InputOutputMomentum.R), and this script
simply extracts the relevant columns and merges with the signal master table.

Inputs:
- SignalMasterTable.parquet (permno, gvkey, time_avail_m)
- InputOutputMomentumProcessed.parquet (gvkey, time_avail_m, retmatchcustomer, retmatchsupplier)

Outputs:
- iomom_cust.csv (permno, yyyymm, iomom_cust)
- iomom_supp.csv (permno, yyyymm, iomom_supp)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting iomom_cust and iomom_supp predictors...")

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

# SIGNAL CONSTRUCTION - Customer Momentum
# Set customer momentum variable from retmatchcustomer column
df['iomom_cust'] = df['retmatchcustomer']

# Keep only observations with valid customer momentum values for saving
df_cust = df.dropna(subset=['iomom_cust'])
print(f"After dropping missing iomom_cust: {len(df_cust):,} observations")

# Keep only needed columns for customer momentum save
df_cust = df_cust[['permno', 'time_avail_m', 'iomom_cust']].copy()

# SAVE Customer Momentum
print("Saving iomom_cust predictor...")
save_predictor(df_cust, 'iomom_cust')

# SIGNAL CONSTRUCTION - Supplier Momentum
# Set supplier momentum variable from retmatchsupplier column
df['iomom_supp'] = df['retmatchsupplier']

# Keep only observations with valid supplier momentum values for saving
df_supp = df.dropna(subset=['iomom_supp'])
print(f"After dropping missing iomom_supp: {len(df_supp):,} observations")

# Keep only needed columns for supplier momentum save
df_supp = df_supp[['permno', 'time_avail_m', 'iomom_supp']].copy()

# SAVE Supplier Momentum
print("Saving iomom_supp predictor...")
save_predictor(df_supp, 'iomom_supp')

print("iomom_cust and iomom_supp predictors completed successfully!")