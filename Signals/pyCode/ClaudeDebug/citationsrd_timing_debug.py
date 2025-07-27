# ABOUTME: Debug the timing issue in CitationsRD - why 201706-201803 missing
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_timing_debug.py

import pandas as pd
import numpy as np

def debug_june_dates_for_14755():
    """Debug what June dates are available for permno 14755 after all processing"""
    
    print("=== CitationsRD Timing Debug for Permno 14755 ===")
    
    # Run the complete process but focus on permno 14755
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
    
    print(f"June data after initial processing: {df.shape}")
    
    # Check permno 14755 at this stage
    permno_14755_june = df[df['permno'] == 14755].copy()
    print(f"Permno 14755 June observations: {len(permno_14755_june)}")
    
    if len(permno_14755_june) > 0:
        print("June dates for permno 14755:")
        june_dates = permno_14755_june['time_avail_m'].tolist()
        for date in june_dates:
            print(f"  {date.strftime('%Y-%m-%d')}")
        
        # Check which years will generate our missing dates
        # 201706-201803 comes from June 2017 (2017-06 + 0 to 11 months = 2017-06 to 2018-05)
        # So we need June 2017 in the data
        june_2017 = permno_14755_june[permno_14755_june['time_avail_m'] == '2017-06-01']
        print(f"\nJune 2017 data for permno 14755: {len(june_2017)}")
        
        if len(june_2017) > 0:
            print("June 2017 found! This should generate 201706-201805...")
        else:
            print("*** June 2017 MISSING - this explains the gap! ***")
    
    # Continue with rolling sums and filtering
    df = df.sort_values(['permno', 'time_avail_m'])
    df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    
    df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)
    
    print(f"\nAfter rolling sums: {df.shape}")
    
    # Check permno 14755 again
    permno_14755_rolling = df[df['permno'] == 14755].copy()
    print(f"Permno 14755 after rolling sums: {len(permno_14755_rolling)}")
    
    if len(permno_14755_rolling) > 0:
        print("June dates after rolling sums:")
        for _, row in permno_14755_rolling.iterrows():
            print(f"  {row['time_avail_m'].strftime('%Y-%m-%d')}: tempCitationsRD={row['tempCitationsRD']}")
    
    # Apply the gvkey filter (this is key!)
    print(f"\n--- Applying gvkey filter ---")
    df_before_gvkey = df.copy()
    df = df.sort_values(['gvkey', 'time_avail_m'])
    df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
    
    print(f"After gvkey filter: {df.shape}")
    
    # Check permno 14755 after gvkey filter
    permno_14755_after_gvkey = df[df['permno'] == 14755].copy()
    print(f"Permno 14755 after gvkey filter: {len(permno_14755_after_gvkey)}")
    
    if len(permno_14755_after_gvkey) > 0:
        print("Remaining June dates after gvkey filter:")
        for _, row in permno_14755_after_gvkey.iterrows():
            print(f"  {row['time_avail_m'].strftime('%Y-%m-%d')}")
        
        # Check specifically for June 2017
        june_2017_after = permno_14755_after_gvkey[permno_14755_after_gvkey['time_avail_m'] == '2017-06-01']
        if len(june_2017_after) == 0:
            print("*** June 2017 FILTERED OUT by gvkey filter! ***")
            
            # Check what happened - look at the gvkey data before filtering
            if len(permno_14755_rolling) > 0:
                gvkey_14755 = permno_14755_rolling['gvkey'].iloc[0]
                print(f"Gvkey for permno 14755: {gvkey_14755}")
                
                gvkey_data = df_before_gvkey[df_before_gvkey['gvkey'] == gvkey_14755].copy()
                gvkey_data = gvkey_data.sort_values('time_avail_m')
                print(f"All June data for gvkey {gvkey_14755}: {len(gvkey_data)}")
                
                print("June dates for this gvkey (first 5):")
                for i, (_, row) in enumerate(gvkey_data.head().iterrows()):
                    print(f"  {i+1}. {row['time_avail_m'].strftime('%Y-%m-%d')} (permno {row['permno']})")
                
                print("June dates for this gvkey (all):")
                all_dates = gvkey_data['time_avail_m'].tolist()
                for i, date in enumerate(all_dates):
                    marker = " *** FILTERED OUT ***" if i < 2 else ""
                    print(f"  {i+1}. {date.strftime('%Y-%m-%d')}{marker}")
                
                # The first 2 observations get dropped, so if June 2017 is among the first 2, it gets filtered out!
    
    # Continue with other filters
    df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
    df = df[df['ceq'] >= 0]
    
    print(f"\nAfter all filters: {df.shape}")
    permno_14755_final = df[df['permno'] == 14755]
    print(f"Final permno 14755 June dates: {len(permno_14755_final)}")
    
    if len(permno_14755_final) > 0:
        print("Final June dates that will be expanded:")
        for _, row in permno_14755_final.iterrows():
            expansion_start = row['time_avail_m']
            print(f"  {expansion_start.strftime('%Y-%m-%d')} -> will generate {expansion_start.strftime('%Y%m')}-{(expansion_start + pd.DateOffset(months=11)).strftime('%Y%m')}")

if __name__ == "__main__":
    debug_june_dates_for_14755()