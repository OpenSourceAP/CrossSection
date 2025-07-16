# ABOUTME: CompositeDebtIssuance predictor - calculates composite debt issuance
# ABOUTME: Run: python3 pyCode/Predictors/CompositeDebtIssuance.py

"""
CompositeDebtIssuance Predictor

Composite debt issuance calculation.

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, dltt, dlc)

Outputs:
- CompositeDebtIssuance.csv (permno, yyyymm, CompositeDebtIssuance)

This predictor calculates:
1. Total debt = dltt + dlc
2. Composite debt issuance = log(tempBD/l60.tempBD)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting CompositeDebtIssuance predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                        columns=['gvkey', 'permno', 'time_avail_m', 'dltt', 'dlc'])
    
    print(f"Loaded {len(df):,} Compustat observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing CompositeDebtIssuance signal...")
    
    # Deduplicate by permno time_avail_m
    df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {len(df):,} observations")
    
    # Sort by permno and time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate total debt
    df['tempBD'] = df['dltt'] + df['dlc']
    
    # Create 60-month lag
    df['l60_tempBD'] = df.groupby('permno')['tempBD'].shift(60)
    
    # Calculate composite debt issuance
    # CompositeDebtIssuance = log(tempBD/l60.tempBD)
    df['CompositeDebtIssuance'] = np.where(
        df['l60_tempBD'] == 0,
        np.nan,
        np.where(
            (df['tempBD'] / df['l60_tempBD']).isna() & df['l60_tempBD'].isna(),
            1.0,
            np.log(df['tempBD'] / df['l60_tempBD'])
        )
    )
    
    print(f"Generated CompositeDebtIssuance values for {df['CompositeDebtIssuance'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['tempBD', 'l60_tempBD'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'CompositeDebtIssuance')
    
    print("CompositeDebtIssuance predictor completed successfully!")

if __name__ == "__main__":
    main()