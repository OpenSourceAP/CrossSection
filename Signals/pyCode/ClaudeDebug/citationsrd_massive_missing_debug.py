# ABOUTME: Debug massive missing observations in CitationsRD after size categorization fix
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_massive_missing_debug.py

import pandas as pd
import numpy as np

def debug_massive_missing():
    """Debug why CitationsRD went from 324 missing to 161,532 missing observations"""
    
    print("=== CitationsRD Massive Missing Debug ===")
    
    # Load the original test data to compare against
    print("Loading test data...")
    
    # Check what's happening with the size categorization
    # First, let's run through the current logic step by step
    
    # Load data exactly like the script
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    df = df[df['time_avail_m'] >= '1970-01']
    print(f"After early date filter: {df.shape}")
    
    # Generate year
    df['year'] = df['time_avail_m'].dt.year
    
    # Merge with Compustat
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
    compustat = compustat[compustat['time_avail_m'] >= '1970-01']
    
    df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
    print(f"After Compustat merge: {df.shape}")
    
    # Drop missing gvkey
    df = df.dropna(subset=['gvkey'])
    print(f"After dropping missing gvkey: {df.shape}")
    
    # Patent data
    patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
    patent = patent[['gvkey', 'year', 'ncitscale']].copy()
    
    df = df.merge(patent, on=['gvkey', 'year'], how='left')
    print(f"After patent merge: {df.shape}")
    
    # Create lags
    df = df.sort_values(['permno', 'time_avail_m'])
    df['temp'] = df.groupby('permno')['ncitscale'].shift(6)
    df['temp'] = df['temp'].fillna(0)
    df['ncitscale'] = df['temp']
    df = df.drop(columns=['temp'])
    
    df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)
    df['xrd_lag'] = df['xrd_lag'].fillna(0)
    print(f"After creating lags: {df.shape}")
    
    # June filter
    df = df[df['time_avail_m'] >= '1975-01']
    df = df[df['time_avail_m'].dt.month == 6]
    print(f"After June filter: {df.shape}")
    
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
    
    # Filter by gvkey
    df = df.sort_values(['gvkey', 'time_avail_m'])
    df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
    print(f"After gvkey filter: {df.shape}")
    
    # Drop financial firms
    df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
    print(f"After dropping financial: {df.shape}")
    
    # Drop negative ceq
    df = df[df['ceq'] >= 0]
    print(f"After ceq filter: {df.shape}")
    
    print(f"\nBefore size categorization: {df.shape}")
    print("Non-null tempCitationsRD:", df['tempCitationsRD'].notna().sum())
    
    # Check the size categorization step - THIS is where the issue is
    def calculate_size_breakpoints(group):
        nyse_stocks = group[group['exchcd'] == 1]
        if len(nyse_stocks) == 0:
            print(f"  WARNING: No NYSE stocks in time period {group['time_avail_m'].iloc[0]}")
            return group
        
        median_mve = nyse_stocks['mve_c'].median()
        # The current logic uses <= which might be causing issues
        group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
        
        # Debug: check how many get each category
        small_count = (group['sizecat'] == 1).sum()
        large_count = (group['sizecat'] == 2).sum()
        print(f"  {group['time_avail_m'].iloc[0]}: NYSE median={median_mve:.2f}, Small={small_count}, Large={large_count}")
        
        return group
    
    print("\nApplying size categorization...")
    df = df.groupby('time_avail_m').apply(calculate_size_breakpoints).reset_index(drop=True)
    print(f"After size categorization: {df.shape}")
    
    # Check for any rows that lost sizecat
    missing_sizecat = df['sizecat'].isna().sum()
    print(f"Missing sizecat values: {missing_sizecat}")
    
    # Create terciles
    print("\nCreating terciles...")
    def create_fastxtile_terciles(group):
        try:
            group['maincat'] = pd.qcut(group['tempCitationsRD'], q=3, labels=False, duplicates='drop') + 1
            return group
        except Exception as e:
            print(f"  qcut failed for {group['time_avail_m'].iloc[0]}: {e}")
            if group['tempCitationsRD'].notna().sum() > 0:
                group['maincat'] = 1.0
            else:
                group['maincat'] = np.nan
            return group
    
    df = df.groupby('time_avail_m').apply(create_fastxtile_terciles).reset_index(drop=True)
    print(f"After terciles: {df.shape}")
    
    # Check how many observations have both sizecat and maincat
    has_both = (~df['sizecat'].isna()) & (~df['maincat'].isna())
    print(f"Observations with both sizecat and maincat: {has_both.sum()}")
    
    # Create signal
    df['CitationsRD'] = np.nan
    df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
    df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0
    
    # Check signal creation
    signal_1 = (df['CitationsRD'] == 1).sum()
    signal_0 = (df['CitationsRD'] == 0).sum()
    signal_total = df['CitationsRD'].notna().sum()
    print(f"\nSignal created - 1s: {signal_1}, 0s: {signal_0}, Total: {signal_total}")
    
    # Expand to monthly
    print("\nExpanding to monthly...")
    keep_cols = ['permno', 'gvkey', 'time_avail_m', 'CitationsRD']
    df_slim = df[keep_cols].copy()
    
    df_expanded = pd.concat([
        df_slim.assign(time_avail_m=df_slim['time_avail_m'] + pd.DateOffset(months=i))
        for i in range(12)
    ], ignore_index=True)
    
    df = df_expanded.sort_values(['gvkey', 'time_avail_m'])
    
    # Final processing
    df_final = df[['permno', 'time_avail_m', 'CitationsRD']].copy()
    df_final = df_final.dropna(subset=['CitationsRD'])
    
    print(f"Final observations before yyyymm conversion: {len(df_final)}")
    
    # Convert to yyyymm
    df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month
    df_final['permno'] = df_final['permno'].astype('int64')
    df_final['yyyymm'] = df_final['yyyymm'].astype('int64')
    
    df_final = df_final[['permno', 'yyyymm', 'CitationsRD']].copy()
    df_final = df_final.set_index(['permno', 'yyyymm'])
    
    print(f"Final output shape: {df_final.shape}")
    
    # Compare to what we expect
    print(f"\nExpected ~480k observations, got {len(df_final)}")
    print(f"Missing approximately {480000 - len(df_final)} observations")

if __name__ == "__main__":
    debug_massive_missing()