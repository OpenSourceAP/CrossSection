# ABOUTME: iomom_supp predictor - Input-Output supplier momentum
# ABOUTME: Run: python3 pyCode/Predictors/iomom_supp.py

"""
iomom_supp Predictor - Input-Output Supplier Momentum

This predictor extracts supplier momentum from pre-computed Input-Output momentum data.
The heavy computation is done in R (ZJR_InputOutputMomentum.R), and this script
simply extracts the relevant column and merges with the signal master table.

Inputs:
- SignalMasterTable.parquet (permno, gvkey, time_avail_m)
- InputOutputMomentumProcessed.parquet (gvkey, time_avail_m, retmatchsupplier)

Outputs:
- iomom_supp.csv (permno, yyyymm, iomom_supp)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting iomom_supp predictor...")
    
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
    # gen iomom_supp = retmatchsupplier
    df['iomom_supp'] = df['retmatchsupplier']
    
    # keep if iomom_supp != .
    df = df.dropna(subset=['iomom_supp'])
    print(f"After dropping missing iomom_supp: {len(df):,} observations")
    
    # Keep only needed columns for save
    df = df[['permno', 'time_avail_m', 'iomom_supp']].copy()
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'iomom_supp')
    
    print("iomom_supp predictor completed successfully!")

if __name__ == "__main__":
    main()