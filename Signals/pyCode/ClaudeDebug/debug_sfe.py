# ABOUTME: Debug script to investigate sfe missing observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/debug_sfe.py

# Debug specific missing observation: permno 11406 yyyymm 199103
# This should have sfe = 0.195122 according to Stata but is missing in Python

import pandas as pd
import numpy as np

print("=== DEBUGGING sfe MISSING OBSERVATION ===")
print("Target: permno 11406, yyyymm 199103 (should have sfe = 0.195122)")
print()

# Load the same data sources as the predictor
print("1. Loading IBES data...")
ibes = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
print(f"   IBES total: {len(ibes):,} rows")

# Apply same filters as predictor
ibes = ibes[ibes['fpi'] == '1'].copy()
print(f"   After fpi == '1': {len(ibes):,} rows")

ibes = ibes[pd.to_datetime(ibes['statpers']).dt.month == 3].copy()
print(f"   After March forecasts: {len(ibes):,} rows")

ibes = ibes[(~ibes['fpedats'].isna()) & (ibes['fpedats'] > ibes['statpers'] + pd.Timedelta(days=90))].copy()
print(f"   After forecast filtering: {len(ibes):,} rows")

# Create prc_time for merge
ibes['prc_time'] = ibes['time_avail_m'] - pd.DateOffset(months=3)
print(f"   IBES ready: {len(ibes):,} rows")

print("\n2. Loading SignalMasterTable...")
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'tickerIBES', 'prc', 'mve_c']].copy()
smt = smt.rename(columns={'time_avail_m': 'prc_time'})
print(f"   SMT ready: {len(smt):,} rows")

# Target observation should be from March 1991 data (time_avail_m - 12 months from 199103)
target_date = pd.Timestamp('1991-03-01')  # March 1991 for March 1991 forecast
prc_target_date = pd.Timestamp('1990-12-01')  # December 1990 for price data

print(f"\n3. Checking permno 11406 in SignalMasterTable for prc_time {prc_target_date}...")
smt_11406 = smt[smt['permno'] == 11406].copy()
print(f"   permno 11406 total SMT rows: {len(smt_11406)}")

if len(smt_11406) > 0:
    smt_11406_sorted = smt_11406.sort_values('prc_time')
    print("   Date range for permno 11406 in SMT:")
    print(f"   From: {smt_11406_sorted['prc_time'].min()}")
    print(f"   To: {smt_11406_sorted['prc_time'].max()}")
    
    # Check specific target date
    dec_1990_smt = smt_11406[smt_11406['prc_time'] == prc_target_date]
    print(f"\n   permno 11406 on {prc_target_date} in SMT: {len(dec_1990_smt)} rows")
    if len(dec_1990_smt) > 0:
        ticker = dec_1990_smt['tickerIBES'].iloc[0]
        prc = dec_1990_smt['prc'].iloc[0]
        print(f"   tickerIBES: {ticker}")
        print(f"   prc: {prc}")
    else:
        print("   No SMT entry for target date")

print(f"\n4. Checking IBES data for March 1991 forecast...")
if len(smt_11406) > 0 and len(dec_1990_smt) > 0:
    ticker = dec_1990_smt['tickerIBES'].iloc[0]
    print(f"   Looking for tickerIBES '{ticker}' on prc_time {prc_target_date}")
    print(f"   This means forecast from time_avail_m {target_date}")
    
    # Check IBES for this ticker and prc_time
    ibes_target = ibes[
        (ibes['tickerIBES'] == ticker) & 
        (ibes['prc_time'] == prc_target_date)
    ]
    print(f"   IBES matches: {len(ibes_target)} rows")
    
    if len(ibes_target) > 0:
        print("   IBES data found:")
        row = ibes_target.iloc[0]
        print(f"   time_avail_m: {row['time_avail_m']}")
        print(f"   medest: {row['medest']}")
        print(f"   numest: {row['numest']}")
        print(f"   statpers: {row['statpers']}")
        print(f"   fpedats: {row['fpedats']}")
    else:
        print("   No IBES data for this ticker/prc_time")
        # Check what's available for this ticker
        ticker_data = ibes[ibes['tickerIBES'] == ticker].copy()
        print(f"   Total IBES rows for ticker '{ticker}': {len(ticker_data)}")
        if len(ticker_data) > 0:
            print(f"   Date range: {ticker_data['time_avail_m'].min()} to {ticker_data['time_avail_m'].max()}")
            print(f"   prc_time range: {ticker_data['prc_time'].min()} to {ticker_data['prc_time'].max()}")

print("\n5. Checking Compustat data for merge...")
comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'datadate']].copy()

# Check if permno 11406 has data for March 1991
comp_11406 = comp[comp['permno'] == 11406].copy()
march_1991_comp = comp_11406[comp_11406['time_avail_m'] == target_date]
print(f"   permno 11406 on {target_date} in Compustat: {len(march_1991_comp)} rows")

if len(march_1991_comp) > 0:
    datadate = march_1991_comp['datadate'].iloc[0]
    datadate_month = pd.to_datetime(datadate).month
    print(f"   datadate: {datadate} (month: {datadate_month})")
    print(f"   December fiscal year end? {datadate_month == 12}")
else:
    print("   No Compustat data for March 1991")

print("\n=== COMPARISON WITH STATA ===")
print("Let me check what Stata has for this same observation...")