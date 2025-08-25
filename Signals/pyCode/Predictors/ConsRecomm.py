# ABOUTME: ConsRecomm predictor - calculates consensus recommendation
# ABOUTME: Run: python3 pyCode/Predictors/ConsRecomm.py

"""
ConsRecomm Predictor

Consensus recommendation calculation using IBES data.

Inputs:
- IBES_Recommendations.parquet (tickerIBES, amaskcd, anndats, time_avail_m, ireccd)
- SignalMasterTable.parquet (permno, time_avail_m, tickerIBES)

Outputs:
- ConsRecomm.csv (permno, yyyymm, ConsRecomm)

This predictor calculates:
1. Collapse IBES recommendations to firm-month level
2. ConsRecomm = 1 if ireccd > 3 and not missing
3. ConsRecomm = 0 if ireccd <= 1.5
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting ConsRecomm predictor...")
    
    # PREP IBES DATA
    print("Loading IBES Recommendations data...")
    ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_Recommendations.parquet', 
                             columns=['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd'])
    
    print(f"Loaded {len(ibes_df):,} IBES recommendations observations")
    
    # Collapse down to firm-month level
    # gcollapse (lastnm) ireccd, by(tickerIBES amaskcd time_avail_m)
    # Sort by time to get last non-missing value
    ibes_df = ibes_df.sort_values(['tickerIBES', 'amaskcd', 'time_avail_m', 'anndats'])
    ibes_df = ibes_df.groupby(['tickerIBES', 'amaskcd', 'time_avail_m'])['ireccd'].last().reset_index()
    
    print(f"After first collapse: {len(ibes_df):,} observations")
    
    # gcollapse (mean) ireccd, by(tickerIBES time_avail_m)
    ibes_df = ibes_df.groupby(['tickerIBES', 'time_avail_m'])['ireccd'].mean().reset_index()
    
    print(f"After second collapse: {len(ibes_df):,} observations")
    
    # Define signal - match Stata logic exactly:
    # gen ConsRecomm = 1 if ireccd > 3 & ireccd < .
    # replace ConsRecomm = 0 if ireccd <= 1.5
    ibes_df['ConsRecomm'] = np.nan
    ibes_df.loc[(ibes_df['ireccd'] > 3) & ibes_df['ireccd'].notna(), 'ConsRecomm'] = 1
    ibes_df.loc[ibes_df['ireccd'] <= 1.5, 'ConsRecomm'] = 0
    
    print(f"Generated ConsRecomm values for {ibes_df['ConsRecomm'].notna().sum():,} observations")
    
    # Add permno
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                   columns=['permno', 'time_avail_m', 'tickerIBES'])
    
    print(f"Loaded {len(signal_master):,} SignalMasterTable observations")
    
    # Merge with SignalMasterTable (Stata uses 1:m merge)
    print("Merging data...")
    # The Stata merge is: merge 1:m tickerIBES time_avail_m using SignalMasterTable
    # This means one IBES record can match multiple permnos
    df = pd.merge(ibes_df, signal_master, on=['tickerIBES', 'time_avail_m'], how='inner')
    
    print(f"After merging: {len(df):,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['ireccd'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ConsRecomm')
    
    print("ConsRecomm predictor completed successfully!")

if __name__ == "__main__":
    main()