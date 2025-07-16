# ABOUTME: ChEQ predictor - calculates sustainable growth (change in equity)
# ABOUTME: Run: python3 pyCode/Predictors/ChEQ.py

"""
ChEQ Predictor

Sustainable growth calculation: ceq/l12.ceq (current equity / 12-month lagged equity)

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, ceq)

Outputs:
- ChEQ.csv (permno, yyyymm, ChEQ)

This predictor calculates sustainable growth as the ratio of current equity 
to equity from 12 months ago, but only for positive values.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting ChEQ predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                        columns=['gvkey', 'permno', 'time_avail_m', 'ceq'])
    
    print(f"Loaded {len(df):,} Compustat observations")
    
    # Deduplicate by permno time_avail_m (equivalent to bysort permno time_avail_m: keep if _n == 1)
    df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChEQ signal...")
    
    # Sort by permno and time_avail_m (equivalent to xtset permno time_avail_m)
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 12-month lag of ceq
    df['l12_ceq'] = df.groupby('permno')['ceq'].shift(12)
    
    # Calculate ChEQ = ceq/l12.ceq if ceq >0 & l12.ceq >0
    # Only calculate for positive values, otherwise set to missing
    df['ChEQ'] = np.where(
        (df['ceq'] > 0) & (df['l12_ceq'] > 0),
        df['ceq'] / df['l12_ceq'],
        np.nan
    )
    
    print(f"Generated ChEQ values for {df['ChEQ'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['l12_ceq'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChEQ')
    
    print("ChEQ predictor completed successfully!")

if __name__ == "__main__":
    main()