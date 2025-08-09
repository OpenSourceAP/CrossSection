# ABOUTME: CompEquIss predictor - calculates composite equity issuance
# ABOUTME: Run: python3 pyCode/Predictors/CompEquIss.py

"""
CompEquIss Predictor

Line-by-line translation of CompEquIss.do

Run from pyCode/ directory:
python3 Predictors/CompEquIss.py

Inputs:
- SignalMasterTable.parquet (permno, time_avail_m, ret, mve_c)

Outputs:
- CompEquIss.csv (permno, yyyymm, CompEquIss)

Stata code translated:
1. use permno time_avail_m ret mve_c using "$pathDataIntermediate/SignalMasterTable", clear
2. bys permno (time_avail): gen tempIdx = 1 if _n == 1
3. bys permno (time_avail): replace tempIdx = (1 + ret)*l.tempIdx if _n > 1
4. gen tempBH = (tempIdx - l60.tempIdx)/l60.tempIdx
5. gen CompEquIss = log(mve_c/l60.mve_c) - tempBH
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting CompEquIss predictor...")
    
    # DATA LOAD
    # Stata: use permno time_avail_m ret mve_c using "$pathDataIntermediate/SignalMasterTable", clear
    print("Loading SignalMasterTable...")
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                        columns=['permno', 'time_avail_m', 'ret', 'mve_c'])
    
    print(f"Loaded {len(df):,} SignalMasterTable observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing CompEquIss signal...")
    
    # Data is already sorted by permno, time_avail_m (verified in debug script)
    
    # Stata: bys permno (time_avail): gen tempIdx = 1 if _n == 1
    # Stata: bys permno (time_avail): replace tempIdx = (1 + ret)*l.tempIdx if _n > 1
    # This creates a cumulative return index starting at 1 for each permno
    df['tempIdx'] = df.groupby('permno')['ret'].transform(lambda x: (1 + x).cumprod())
    
    # Stata: gen tempBH = (tempIdx - l60.tempIdx)/l60.tempIdx
    df['l60_tempIdx'] = df.groupby('permno')['tempIdx'].shift(60)
    df['tempBH'] = (df['tempIdx'] - df['l60_tempIdx']) / df['l60_tempIdx']
    
    # Stata: gen CompEquIss = log(mve_c/l60.mve_c) - tempBH
    df['l60_mve_c'] = df.groupby('permno')['mve_c'].shift(60)
    df['CompEquIss'] = np.log(df['mve_c'] / df['l60_mve_c']) - df['tempBH']
    
    print(f"Generated CompEquIss values for {df['CompEquIss'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['tempIdx', 'l60_tempIdx', 'tempBH', 'l60_mve_c'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'CompEquIss')
    
    print("CompEquIss predictor completed successfully!")

if __name__ == "__main__":
    main()