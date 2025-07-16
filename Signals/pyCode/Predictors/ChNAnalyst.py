# ABOUTME: ChNAnalyst predictor - calculates decline in analyst coverage
# ABOUTME: Run: python3 pyCode/Predictors/ChNAnalyst.py

"""
ChNAnalyst Predictor

Change in number of analysts following company.

Inputs:
- IBES_EPS_Unadj.parquet (tickerIBES, time_avail_m, numest, statpers, fpedats)
- SignalMasterTable.parquet (permno, time_avail_m, tickerIBES, mve_c)

Outputs:
- ChNAnalyst.csv (permno, yyyymm, ChNAnalyst)

This predictor calculates:
1. Decline in analyst coverage (numest < l3.numest)
2. Only works in small firms (bottom 2 quintiles by market cap)
3. Excludes July-September 1987 observations
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def fastxtile(series, n_quantiles=5):
    """
    Python equivalent of Stata's fastxtile function using pd.qcut
    """
    try:
        # Handle -inf values by replacing them with NaN before quantile calculation
        series_clean = series.replace([np.inf, -np.inf], np.nan)
        return pd.qcut(series_clean, q=n_quantiles, labels=False, duplicates='drop') + 1
    except Exception:
        return pd.Series(np.nan, index=series.index)

def main():
    print("Starting ChNAnalyst predictor...")
    
    # Prep IBES data
    print("Loading IBES data...")
    ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
    
    # Keep only FPI == "1" (equivalent to keep if fpi == "1")
    ibes_df = ibes_df[ibes_df['fpi'] == "1"]
    
    # Set to last non-missing forecast in period that trade happens
    # gen tmp = 1 if fpedats != . & fpedats > statpers + 30
    # bys tickerIBES: replace meanest = meanest[_n-1] if mi(tmp) & fpedats == fpedats[_n-1]
    ibes_df = ibes_df.sort_values(['tickerIBES', 'time_avail_m'])
    ibes_df['tmp'] = np.where(
        ibes_df['fpedats'].notna() & (ibes_df['fpedats'] > ibes_df['statpers'] + pd.Timedelta(days=30)),
        1, 
        np.nan
    )
    
    # Create lag of meanest by tickerIBES
    ibes_df['l_meanest'] = ibes_df.groupby('tickerIBES')['meanest'].shift(1)
    ibes_df['l_fpedats'] = ibes_df.groupby('tickerIBES')['fpedats'].shift(1)
    
    # Replace meanest with lagged value when tmp is missing and fpedats equals lagged fpedats
    mask = ibes_df['tmp'].isna() & (ibes_df['fpedats'] == ibes_df['l_fpedats'])
    ibes_df.loc[mask, 'meanest'] = ibes_df.loc[mask, 'l_meanest']
    
    # Keep required columns
    ibes_df = ibes_df[['tickerIBES', 'time_avail_m', 'numest', 'statpers', 'fpedats']].copy()
    
    print(f"Loaded {len(ibes_df):,} IBES observations")
    
    # DATA LOAD
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                   columns=['permno', 'time_avail_m', 'tickerIBES', 'mve_c'])
    
    print(f"Loaded {len(signal_master):,} SignalMasterTable observations")
    
    # Merge data
    print("Merging data...")
    df = pd.merge(signal_master, ibes_df, on=['tickerIBES', 'time_avail_m'], how='left')
    
    print(f"After merging: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChNAnalyst signal...")
    
    # Sort by permno and time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 3-month lag of numest
    df['l3_numest'] = df.groupby('permno')['numest'].shift(3)
    
    # Generate ChNAnalyst signal
    # ChNAnalyst = 1 if numest < l3.numest & !mi(l3.numest)
    # ChNAnalyst = 0 if numest >= l3.numest & !mi(numest)
    df['ChNAnalyst'] = np.nan
    
    # Set to 1 if numest < l3.numest and l3.numest is not missing
    df.loc[
        (df['numest'] < df['l3_numest']) & df['l3_numest'].notna(), 
        'ChNAnalyst'
    ] = 1
    
    # Set to 0 if numest >= l3.numest and numest is not missing
    df.loc[
        (df['numest'] >= df['l3_numest']) & df['numest'].notna(), 
        'ChNAnalyst'
    ] = 0
    
    # Exclude July-September 1987 observations
    # replace ChNAnalyst = . if time_avail_m >= ym(1987,7) & time_avail_m <= ym(1987,9)
    july_1987 = pd.Timestamp('1987-07-01')
    sep_1987 = pd.Timestamp('1987-09-01')
    df.loc[
        (df['time_avail_m'] >= july_1987) & (df['time_avail_m'] <= sep_1987), 
        'ChNAnalyst'
    ] = np.nan
    
    # Only works in small firms (bottom 2 quintiles by market cap)
    # egen temp = fastxtile(mve_c), n(5)
    # keep if temp <= 2
    df['temp'] = fastxtile(df['mve_c'], n_quantiles=5)
    df = df[df['temp'] <= 2]
    
    print(f"After filtering for small firms: {len(df):,} observations")
    print(f"Generated ChNAnalyst values for {df['ChNAnalyst'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['l3_numest', 'temp'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChNAnalyst')
    
    print("ChNAnalyst predictor completed successfully!")

if __name__ == "__main__":
    main()