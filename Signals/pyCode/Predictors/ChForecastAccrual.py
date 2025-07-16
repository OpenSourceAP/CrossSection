# ABOUTME: ChForecastAccrual predictor - calculates change in forecast and accrual
# ABOUTME: Run: python3 pyCode/Predictors/ChForecastAccrual.py

"""
ChForecastAccrual Predictor

Change in forecast and accrual calculation using IBES data.

Inputs:
- IBES_EPS_Unadj.parquet (tickerIBES, time_avail_m, meanest, fpi)
- m_aCompustat.parquet (permno, time_avail_m, act, che, lct, dlc, txp, at)
- SignalMasterTable.parquet (permno, time_avail_m, tickerIBES)

Outputs:
- ChForecastAccrual.csv (permno, yyyymm, ChForecastAccrual)

This predictor calculates:
1. Accruals-based filter (exclude bottom decile)
2. Forecast revision indicator (1 if forecast increased, 0 if decreased)
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
    print("Starting ChForecastAccrual predictor...")
    
    # Prep IBES data
    print("Loading IBES data...")
    ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
    
    # Keep only FPI == "1" (equivalent to keep if fpi == "1")
    ibes_df = ibes_df[ibes_df['fpi'] == "1"]
    ibes_df = ibes_df[['tickerIBES', 'time_avail_m', 'meanest']].copy()
    
    print(f"Loaded {len(ibes_df):,} IBES observations")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                                 columns=['permno', 'time_avail_m', 'act', 'che', 'lct', 'dlc', 'txp', 'at'])
    
    # Deduplicate by permno time_avail_m
    compustat_df = compustat_df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"Loaded {len(compustat_df):,} Compustat observations")
    
    # Load SignalMasterTable
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                   columns=['permno', 'time_avail_m', 'tickerIBES'])
    
    print(f"Loaded {len(signal_master):,} SignalMasterTable observations")
    
    # Merge data
    print("Merging data...")
    df = pd.merge(compustat_df, signal_master, on=['permno', 'time_avail_m'], how='left')
    df = pd.merge(df, ibes_df, on=['tickerIBES', 'time_avail_m'], how='left')
    
    print(f"After merging: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChForecastAccrual signal...")
    
    # Sort by permno and time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 12-month lags for accruals calculation
    lag_cols = ['act', 'che', 'lct', 'dlc', 'txp', 'at']
    for col in lag_cols:
        df[f'l12_{col}'] = df.groupby('permno')[col].shift(12)
    
    # Calculate accruals: tempAccruals = ((act - l12.act) - (che - l12.che) - ((lct - l12.lct) - (dlc - l12.dlc) - (txp - l12.txp))) / ((at + l12.at)/2)
    df['accruals_numerator'] = (
        (df['act'] - df['l12_act']) - (df['che'] - df['l12_che']) - 
        ((df['lct'] - df['l12_lct']) - (df['dlc'] - df['l12_dlc']) - (df['txp'] - df['l12_txp']))
    )
    df['avg_assets'] = (df['at'] + df['l12_at']) / 2
    
    # Calculate tempAccruals with domain-aware missing handling
    df['tempAccruals'] = np.where(
        df['avg_assets'] == 0,
        np.nan,
        np.where(
            df['accruals_numerator'].isna() & df['avg_assets'].isna(),
            1.0,
            df['accruals_numerator'] / df['avg_assets']
        )
    )
    
    # Calculate tempsort (accruals decile by time_avail_m)
    df['tempsort'] = df.groupby('time_avail_m')['tempAccruals'].transform(lambda x: fastxtile(x, 2))
    
    # Create lag of meanest
    df['l_meanest'] = df.groupby('permno')['meanest'].shift(1)
    
    # Calculate ChForecastAccrual
    # 1 if meanest > l.meanest & !mi(meanest) & !mi(l.meanest)
    # 0 if meanest < l.meanest & !mi(meanest) & !mi(l.meanest)
    # . otherwise
    df['ChForecastAccrual'] = np.nan
    
    # Conditions for non-missing values
    valid_mask = df['meanest'].notna() & df['l_meanest'].notna()
    
    # Set to 1 if forecast increased
    df.loc[valid_mask & (df['meanest'] > df['l_meanest']), 'ChForecastAccrual'] = 1
    
    # Set to 0 if forecast decreased
    df.loc[valid_mask & (df['meanest'] < df['l_meanest']), 'ChForecastAccrual'] = 0
    
    # Set to missing if in bottom accruals decile (tempsort == 1)
    df.loc[df['tempsort'] == 1, 'ChForecastAccrual'] = np.nan
    
    print(f"Generated ChForecastAccrual values for {df['ChForecastAccrual'].notna().sum():,} observations")
    
    # Clean up temporary columns
    temp_cols = [f'l12_{col}' for col in lag_cols] + ['accruals_numerator', 'avg_assets', 'tempAccruals', 'tempsort', 'l_meanest']
    df = df.drop(columns=temp_cols)
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChForecastAccrual')
    
    print("ChForecastAccrual predictor completed successfully!")

if __name__ == "__main__":
    main()