# ABOUTME: Debug CitationsRD size and main category logic
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_categories_debug.py

import pandas as pd
import numpy as np

def debug_categories_and_final_output():
    """Debug the complete CitationsRD process focusing on categories and final output"""
    
    print("=== CitationsRD Categories and Final Output Debug ===")
    
    # Run the complete process up to the filtering
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
    
    df = df.sort_values(['permno', 'time_avail_m'])
    df['temp'] = df.groupby('permno')['ncitscale'].shift(6)
    df['temp'] = df['temp'].fillna(0)
    df['ncitscale'] = df['temp']
    df = df.drop(columns=['temp'])
    
    df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)
    df['xrd_lag'] = df['xrd_lag'].fillna(0)
    
    df = df[df['time_avail_m'] >= '1975-01']
    df = df[df['time_avail_m'].dt.month == 6]
    
    df = df.sort_values(['permno', 'time_avail_m'])
    df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    
    df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)
    
    # Apply filters
    df = df.sort_values(['gvkey', 'time_avail_m'])
    df = df.groupby('gvkey').apply(lambda x: x.iloc[2:], include_groups=False).reset_index(drop=True)
    df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
    df = df[df['ceq'] >= 0]
    
    print(f"After all filters: {df.shape}")
    
    # Check permno 14755
    permno_14755 = df[df['permno'] == 14755].copy()
    print(f"Permno 14755 after filters: {len(permno_14755)}")
    
    if len(permno_14755) > 0:
        print("Data for permno 14755:")
        print(permno_14755[['time_avail_m', 'mve_c', 'exchcd', 'tempCitationsRD']])
    
    # Size categories
    print("\n--- Size Categories ---")
    def calculate_size_breakpoints(group):
        nyse_stocks = group[group['exchcd'] == 1]
        if len(nyse_stocks) == 0:
            return group
        
        median_mve = nyse_stocks['mve_c'].median()
        group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
        return group
    
    df = df.groupby('time_avail_m').apply(calculate_size_breakpoints, include_groups=False).reset_index(drop=True)
    
    # Check permno 14755 size category
    permno_14755_size = df[df['permno'] == 14755]
    if len(permno_14755_size) > 0:
        print("Size categories for permno 14755:")
        print(permno_14755_size[['time_avail_m', 'mve_c', 'exchcd', 'sizecat']])
    
    # Main categories (terciles)
    print("\n--- Main Categories (Terciles) ---")
    df['maincat'] = np.nan
    
    # Assign maincat=1 to observations with missing tempCitationsRD
    df.loc[df['tempCitationsRD'].isna(), 'maincat'] = 1.0
    
    def create_terciles_per_period(group_df):
        if len(group_df) == 0:
            return group_df
        
        citations = group_df['tempCitationsRD']
        
        q33 = citations.quantile(0.333)
        q67 = citations.quantile(0.667)
        
        group_df['maincat'] = np.where(citations <= q33, 1.0, 
                                      np.where(citations <= q67, 2.0, 3.0))
        
        return group_df
    
    # Apply terciles only to valid data
    valid_mask = df['tempCitationsRD'].notna()
    if valid_mask.sum() > 0:
        valid_df = df[valid_mask].copy()
        tercile_df = valid_df.groupby('time_avail_m').apply(create_terciles_per_period, include_groups=False).reset_index(drop=True)
        df.loc[valid_mask, 'maincat'] = tercile_df['maincat'].values
    
    # Check permno 14755 main category
    permno_14755_main = df[df['permno'] == 14755]
    if len(permno_14755_main) > 0:
        print("Main categories for permno 14755:")
        print(permno_14755_main[['time_avail_m', 'tempCitationsRD', 'sizecat', 'maincat']])
    
    # Create CitationsRD signal
    print("\n--- CitationsRD Signal Creation ---")
    df['CitationsRD'] = np.nan
    df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
    df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0
    
    # Check permno 14755 signal
    permno_14755_signal = df[df['permno'] == 14755]
    if len(permno_14755_signal) > 0:
        print("CitationsRD signals for permno 14755:")
        print(permno_14755_signal[['time_avail_m', 'sizecat', 'maincat', 'CitationsRD']])
    
    print(f"\nTotal non-null CitationsRD signals: {df['CitationsRD'].notna().sum()}")
    
    # Expansion step
    print("\n--- Expansion to Monthly ---")
    keep_cols = ['permno', 'gvkey', 'time_avail_m', 'CitationsRD']
    df_slim = df[keep_cols].copy()
    
    # Only keep observations with non-null CitationsRD
    df_slim = df_slim.dropna(subset=['CitationsRD'])
    print(f"Observations to expand: {len(df_slim)}")
    
    # Check if permno 14755 has any non-null signals to expand
    permno_14755_to_expand = df_slim[df_slim['permno'] == 14755]
    print(f"Permno 14755 observations to expand: {len(permno_14755_to_expand)}")
    
    if len(permno_14755_to_expand) == 0:
        print("*** PROBLEM FOUND: Permno 14755 has no non-null CitationsRD signals to expand ***")
        print("This explains why it's missing from the final output!")
        
        # Check what happened to the signals
        all_14755 = df[df['permno'] == 14755]
        print("\nAll permno 14755 data before expansion:")
        print(all_14755[['time_avail_m', 'sizecat', 'maincat', 'CitationsRD']])
        
        return
    else:
        print("Permno 14755 data to expand:")
        print(permno_14755_to_expand)
    
    # Perform expansion
    df_expanded = pd.concat([
        df_slim.assign(time_avail_m=df_slim['time_avail_m'] + pd.DateOffset(months=i))
        for i in range(12)
    ], ignore_index=True)
    
    df_expanded = df_expanded.sort_values(['gvkey', 'time_avail_m'])
    
    # Final format
    df_final = df_expanded[['permno', 'time_avail_m', 'CitationsRD']].copy()
    df_final = df_final.dropna(subset=['CitationsRD'])
    df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month
    
    # Check final output for permno 14755
    final_14755 = df_final[df_final['permno'] == 14755]
    print(f"\nFinal output for permno 14755: {len(final_14755)} rows")
    if len(final_14755) > 0:
        missing_yyyymm = [201706, 201707, 201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803]
        available_yyyymm = final_14755['yyyymm'].tolist()
        
        print("Available yyyymm:")
        print(sorted(available_yyyymm))
        
        print("\nChecking missing dates:")
        for yyyymm in missing_yyyymm:
            exists = yyyymm in available_yyyymm
            print(f"  {yyyymm}: {'EXISTS' if exists else 'MISSING'}")

if __name__ == "__main__":
    debug_categories_and_final_output()