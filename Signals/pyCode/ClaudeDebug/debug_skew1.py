# ABOUTME: Debug script to investigate skew1 missing observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/debug_skew1.py

# Debug specific missing observation: permno 10353 yyyymm 199601
# This should have skew1 = -0.045004 according to Stata but is missing in Python

import pandas as pd
import numpy as np

print("=== DEBUGGING skew1 MISSING OBSERVATION ===")
print("Target: permno 10353, yyyymm 199601 (should have skew1 = -0.045004)")
print()

# This is likely the same OptionMetrics secid mapping issue as dCPVolSpread
target_date = pd.Timestamp('1996-01-01')

print("1. Loading SignalMasterTable...")
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
print(f"   SMT total: {len(smt):,} rows")

# Check permno 10353 in January 1996
smt_10353 = smt[smt['permno'] == 10353].copy()
print(f"   permno 10353 total SMT rows: {len(smt_10353)}")

if len(smt_10353) > 0:
    smt_10353_sorted = smt_10353.sort_values('time_avail_m')
    print("   Date range for permno 10353 in SMT:")
    print(f"   From: {smt_10353_sorted['time_avail_m'].min()}")
    print(f"   To: {smt_10353_sorted['time_avail_m'].max()}")
    
    # Check specific target date
    jan_1996_smt = smt_10353[smt_10353['time_avail_m'] == target_date]
    print(f"\n   permno 10353 on {target_date} in SMT: {len(jan_1996_smt)} rows")
    if len(jan_1996_smt) > 0:
        secid = jan_1996_smt['secid'].iloc[0]
        print(f"   secid: {secid}")
        
        # Check if secid is NaN
        if pd.isna(secid):
            print("   secid is NaN - this observation gets no OptionMetrics data")
        else:
            print("   secid is valid - checking OptionMetrics data...")
            
            # Load OptionMetrics data
            print("\n2. Loading OptionMetrics data...")
            options = pd.read_parquet('../pyData/Intermediate/OptionMetricsXZZ.parquet')
            print(f"   OptionMetrics total: {len(options):,} rows")
            
            # Check for this secid and date
            opt_match = options[
                (options['secid'] == secid) & 
                (options['time_avail_m'] == target_date)
            ]
            print(f"   OptionMetrics matches for secid {secid} on {target_date}: {len(opt_match)} rows")
            
            if len(opt_match) > 0:
                print("   OptionMetrics data found:")
                row = opt_match.iloc[0]
                if 'skew1' in row:
                    print(f"   skew1: {row['skew1']}")
                else:
                    print("   skew1 column not found in OptionMetrics data")
                    print(f"   Available columns: {list(opt_match.columns)}")
            else:
                print("   No OptionMetrics data found for this secid/date")
                
                # Check what dates are available for this secid
                secid_data = options[options['secid'] == secid].copy()
                print(f"   Total OptionMetrics rows for secid {secid}: {len(secid_data)}")
                if len(secid_data) > 0:
                    print(f"   Date range: {secid_data['time_avail_m'].min()} to {secid_data['time_avail_m'].max()}")
    else:
        print("   No SMT entry for target date")

print("\n=== COMPARISON WITH STATA ===")
print("Let me check what Stata SignalMasterTable has for this observation...")

# Check Stata SignalMasterTable
print("\n3. Checking Stata SignalMasterTable...")
import subprocess
import sys

# Check Stata SMT for permno 10353 in Jan 1996
stata_check = f'''python3 -c "
import pandas as pd
smt = pd.read_stata('../Data/Intermediate/SignalMasterTable.dta')
jan_1996 = smt[(smt['permno'] == 10353) & (smt['time_avail_m'] == pd.Timestamp('1996-01-01'))]
print(f'Stata SMT permno 10353 Jan 1996: {{len(jan_1996)}} rows')
if len(jan_1996) > 0:
    print(f'secid: {{jan_1996[\\"secid\\"].iloc[0]}}')
"'''

print("   Running Stata SMT check...")
try:
    result = subprocess.run(stata_check, shell=True, capture_output=True, text=True, cwd='/Users/idrees/Desktop/CrossSection/Signals')
    if result.returncode == 0:
        print("   Stata SMT result:")
        print("  ", result.stdout.strip())
    else:
        print("   Error checking Stata SMT:", result.stderr)
except Exception as e:
    print("   Could not check Stata SMT:", e)

print("\n=== SUMMARY ===")
print("This will show if the issue is:")
print("1. Missing secid mapping in Python SMT")
print("2. Different secid mapping between Python and Stata SMT") 
print("3. Missing OptionMetrics data for the correct secid")