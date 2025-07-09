# ABOUTME: SignalMasterTable.py - creates monthly master table with firm identifiers and meta information
# ABOUTME: Direct line-by-line translation from Stata SignalMasterTable.do script

import pandas as pd
import numpy as np
from pathlib import Path
import os

def main():
    """
    SignalMasterTable
    Holds monthly list of firms with identifiers and some meta information
    """
    
    print("Starting SignalMasterTable.py...")
    
    # DATA LOAD
    print("Loading monthly CRSP data...")
    
    # Start with monthly CRSP - equivalent to Stata: u permno ticker exchcd shrcd time_avail_m mve_c prc ret sicCRSP using monthlyCRSP
    monthlyCRSP_path = Path("../pyData/Intermediate/monthlyCRSP.parquet")
    if not monthlyCRSP_path.exists():
        raise FileNotFoundError(f"Required input file not found: {monthlyCRSP_path}")
    
    df = pd.read_parquet(monthlyCRSP_path)
    
    # Keep only the columns we need (equivalent to Stata's 'using' with specific variables)
    required_cols = ['permno', 'ticker', 'exchcd', 'shrcd', 'time_avail_m', 'mve_c', 'prc', 'ret', 'sicCRSP']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in monthlyCRSP: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded monthlyCRSP: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Screen on Stock market information: common stocks and major exchanges
    print("Filtering for common stocks and major exchanges...")
    
    # keep if (shrcd == 10 | shrcd == 11 | shrcd == 12) & (exchcd == 1 | exchcd == 2 | exchcd == 3)
    df = df[(df['shrcd'].isin([10, 11, 12])) & (df['exchcd'].isin([1, 2, 3]))].copy()
    
    print(f"After filtering: {df.shape[0]} rows")
    
    # Merge with Compustat monthly data
    print("Merging with m_aCompustat...")
    
    # merge 1:1 permno time_avail_m using m_aCompustat, keepusing(gvkey sic) keep(master match) nogenerate
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    compustat_df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need
    comp_cols = ['permno', 'time_avail_m', 'gvkey', 'sic']
    missing_comp_cols = [col for col in comp_cols if col not in compustat_df.columns]
    if missing_comp_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_comp_cols}")
    
    compustat_df = compustat_df[comp_cols].copy()
    
    # Merge (left join to keep all CRSP observations)
    df = df.merge(compustat_df, on=['permno', 'time_avail_m'], how='left')
    
    print(f"After Compustat merge: {df.shape[0]} rows")
    
    # rename sic sicCS
    df = df.rename(columns={'sic': 'sicCS'})
    
    # add some auxiliary vars and clean up
    print("Adding auxiliary variables...")
    
    # gen NYSE = exchcd == 1
    df['NYSE'] = (df['exchcd'] == 1).astype(int)
    
    # xtset permno time_avail_m and gen bh1m = f.ret (Future buy and hold return)
    df = df.sort_values(['permno', 'time_avail_m'])
    df['bh1m'] = df.groupby('permno')['ret'].shift(-1)
    
    # keep gvkey permno ticker time_avail_m ret bh1m mve_c prc NYSE exchcd shrcd sicCS sicCRSP
    keep_cols = ['gvkey', 'permno', 'ticker', 'time_avail_m', 'ret', 'bh1m', 'mve_c', 'prc', 'NYSE', 'exchcd', 'shrcd', 'sicCS', 'sicCRSP']
    df = df[keep_cols].copy()
    
    # Fix data types to match Stata output
    df['exchcd'] = df['exchcd'].astype('int8')
    df['shrcd'] = df['shrcd'].astype('int8')
    df['sicCRSP'] = df['sicCRSP'].astype('int16')
    
    print(f"After adding auxiliary vars: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Add IBES ticker (if available)
    print("Checking for IBES-CRSP linking table...")
    
    IBESCRSPLink_path = Path("../pyData/Intermediate/IBESCRSPLinkingTable.parquet")
    if IBESCRSPLink_path.exists():
        print("Adding IBES-CRSP link...")
        
        # merge m:1 permno using IBESCRSPLinkingTable, keep(master match) nogenerate
        ibes_link = pd.read_parquet(IBESCRSPLink_path)
        
        # Merge on permno (many-to-one)
        df = df.merge(ibes_link, on='permno', how='left')
        
        print(f"After IBES link merge: {df.shape[0]} rows, {df.shape[1]} columns")
    else:
        print("Not adding IBES-CRSP link. Some signals cannot be generated.")
    
    # Add OptionMetrics secid (if available)
    print("Checking for OptionMetrics-CRSP linking table...")
    
    OptionMetricsLink_path = Path("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet")
    if OptionMetricsLink_path.exists():
        print("Adding OptionMetrics-CRSP link...")
        
        # merge m:1 permno using OPTIONMETRICSCRSPLinkingTable, keep(master match) nogenerate
        om_link = pd.read_parquet(OptionMetricsLink_path)
        
        # Merge on permno (many-to-one)
        df = df.merge(om_link, on='permno', how='left')
        
        print(f"After OptionMetrics link merge: {df.shape[0]} rows, {df.shape[1]} columns")
    else:
        print("Not adding OptionMetrics-CRSP link. Some signals cannot be generated.")
    
    # reinforce sort (equivalent to xtset permno time_avail_m)
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Reorder columns to match Stata output exactly
    stata_column_order = ['permno', 'ret', 'prc', 'shrcd', 'exchcd', 'sicCRSP', 'ticker', 'time_avail_m', 'mve_c', 'gvkey', 'sicCS', 'NYSE', 'bh1m', 'tickerIBES', 'secid', 'om_score']
    available_cols = [col for col in stata_column_order if col in df.columns]
    extra_cols = [col for col in df.columns if col not in stata_column_order]
    final_cols = available_cols + extra_cols
    df = df[final_cols]
    
    # SAVE
    print("Saving SignalMasterTable...")
    
    # Create output directory if it doesn't exist
    output_dir = Path("../pyData/Intermediate/")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as parquet (equivalent to Stata's save)
    output_path = output_dir / "SignalMasterTable.parquet"
    df.to_parquet(output_path, index=False)
    
    print(f"SignalMasterTable saved to: {output_path}")
    print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Column names: {list(df.columns)}")
    
    return df

if __name__ == "__main__":
    main()