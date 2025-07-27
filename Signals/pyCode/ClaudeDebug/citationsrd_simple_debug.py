# ABOUTME: Simple debug of CitationsRD to find why 161k observations are missing
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_simple_debug.py

import pandas as pd
import numpy as np

def debug_citationsrd_basic_filtering():
    """Debug the basic filtering steps to see where observations are lost"""
    
    print("=== CitationsRD Basic Filtering Debug ===")
    
    # From my earlier debug, I saw only 0 observations get CitationsRD = 1
    # This suggests no small companies are getting assigned to the top tercile
    # Let me focus on that specific issue
    
    print("Loading and processing data through size categorization...")
    
    # Quick path to the problem area
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    df = df[df['time_avail_m'] >= '1970-01']
    df['year'] = df['time_avail_m'].dt.year
    
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
    compustat = compustat[compustat['time_avail_m'] >= '1970-01']
    
    df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
    df = df.dropna(subset=['gvkey'])
    
    patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
    patent = patent[['gvkey', 'year', 'ncitscale']].copy()
    df = df.merge(patent, on=['gvkey', 'year'], how='left')
    
    # Create lags
    df = df.sort_values(['permno', 'time_avail_m'])
    df['temp'] = df.groupby('permno')['ncitscale'].shift(6)
    df['temp'] = df['temp'].fillna(0)
    df['ncitscale'] = df['temp']
    df = df.drop(columns=['temp'])
    
    df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)
    df['xrd_lag'] = df['xrd_lag'].fillna(0)
    
    # June filter
    df = df[df['time_avail_m'] >= '1975-01']
    df = df[df['time_avail_m'].dt.month == 6]
    
    # Rolling sums
    df = df.sort_values(['permno', 'time_avail_m'])
    df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    
    # Create signal
    df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)
    
    # Filters
    df = df.sort_values(['gvkey', 'time_avail_m'])
    df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
    df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
    df = df[df['ceq'] >= 0]
    
    print(f"After all filters, before categorization: {len(df):,} observations")
    print(f"Non-null tempCitationsRD: {df['tempCitationsRD'].notna().sum():,}")
    
    # Focus on one specific time period to debug
    target_date = pd.to_datetime('2017-06-01')
    df_sample = df[df['time_avail_m'] == target_date].copy()
    
    print(f"\nFocusing on {target_date.strftime('%Y-%m')}...")
    print(f"Total observations: {len(df_sample):,}")
    print(f"Non-null tempCitationsRD: {df_sample['tempCitationsRD'].notna().sum():,}")
    
    if len(df_sample) > 0:
        # Size categorization
        nyse_stocks = df_sample[df_sample['exchcd'] == 1]
        print(f"NYSE stocks: {len(nyse_stocks):,}")
        
        if len(nyse_stocks) > 0:
            median_mve = nyse_stocks['mve_c'].median()
            df_sample['sizecat'] = np.where(df_sample['mve_c'] <= median_mve, 1, 2)
            
            small_count = (df_sample['sizecat'] == 1).sum()
            large_count = (df_sample['sizecat'] == 2).sum()
            
            print(f"Size categories - Small: {small_count:,}, Large: {large_count:,}")
            print(f"Median cutoff: {median_mve:.2f}")
            
            # Tercile categorization - this is where the issue might be
            try:
                df_sample['maincat'] = pd.qcut(df_sample['tempCitationsRD'], q=3, labels=False, duplicates='drop') + 1
                
                tercile_counts = df_sample['maincat'].value_counts().sort_index()
                print(f"Tercile distribution: {tercile_counts.to_dict()}")
                
                # Check the critical combination: small & high tercile
                small_high = ((df_sample['sizecat'] == 1) & (df_sample['maincat'] == 3)).sum()
                small_low = ((df_sample['sizecat'] == 1) & (df_sample['maincat'] == 1)).sum()
                
                print(f"Small & High tercile (CitationsRD=1): {small_high:,}")
                print(f"Small & Low tercile (CitationsRD=0): {small_low:,}")
                
                if small_high == 0:
                    print("\n*** PROBLEM FOUND: No small companies in high tercile! ***")
                    
                    # Check if small companies have any valid tempCitationsRD values
                    small_companies = df_sample[df_sample['sizecat'] == 1]
                    small_with_signal = small_companies['tempCitationsRD'].notna().sum()
                    
                    print(f"Small companies with valid tempCitationsRD: {small_with_signal:,}")
                    
                    if small_with_signal == 0:
                        print("Issue: Small companies have no valid tempCitationsRD values")
                        
                        # Check why
                        small_with_xrd = (small_companies['sum_xrd'] > 0).sum()
                        print(f"Small companies with sum_xrd > 0: {small_with_xrd:,}")
                        
                        if small_with_xrd == 0:
                            print("Root cause: Small companies have no R&D expenditure (sum_xrd = 0)")
                        else:
                            print("Other issue with signal creation")
                    else:
                        print("Issue: Small companies with valid signals not getting into high tercile")
                        
                        # Show distribution of tempCitationsRD for small vs large companies
                        small_signal_stats = small_companies['tempCitationsRD'].describe()
                        large_companies = df_sample[df_sample['sizecat'] == 2]
                        large_signal_stats = large_companies['tempCitationsRD'].describe()
                        
                        print("\nSignal distribution:")
                        print("Small companies:")
                        print(small_signal_stats)
                        print("\nLarge companies:")
                        print(large_signal_stats)
                
            except Exception as e:
                print(f"Tercile creation failed: {e}")
                
                # Check why qcut failed
                signal_values = df_sample['tempCitationsRD'].dropna()
                unique_values = len(signal_values.unique())
                print(f"Unique tempCitationsRD values: {unique_values}")
                
                if unique_values < 3:
                    print("Issue: Not enough unique values for terciles")

if __name__ == "__main__":
    debug_citationsrd_basic_filtering()