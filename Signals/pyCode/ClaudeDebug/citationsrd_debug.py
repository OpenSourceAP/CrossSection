# ABOUTME: Debug CitationsRD missing observations - focus on permno 10006 in 1983
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_debug.py

import pandas as pd
import numpy as np

# Load both datasets to compare
print("Loading Stata and Python data...")
stata_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/Data/Predictors/CitationsRD.csv')
python_df = pd.read_csv('/Users/idrees/Desktop/CrossSection/Signals/pyData/Predictors/CitationsRD.csv')

print(f"Stata shape: {stata_df.shape}")
print(f"Python shape: {python_df.shape}")

# Focus on problematic permno 10006 in 1983
print("\n=== Debugging permno 10006 in 1983 ===")

# Check Stata data for this permno/period
stata_10006 = stata_df[stata_df['permno'] == 10006]
stata_10006_1983 = stata_10006[(stata_10006['yyyymm'] >= 198301) & (stata_10006['yyyymm'] <= 198312)]

print(f"\nStata permno 10006 in 1983:")
print(stata_10006_1983[['permno', 'yyyymm', 'CitationsRD']])

# Check Python data for this permno/period  
python_10006 = python_df[python_df['permno'] == 10006]
python_10006_1983 = python_10006[(python_10006['yyyymm'] >= 198301) & (python_10006['yyyymm'] <= 198312)]

print(f"\nPython permno 10006 in 1983:")
print(python_10006_1983[['permno', 'yyyymm', 'CitationsRD']])

# Check what earliest data we have for permno 10006
print(f"\nStata permno 10006 earliest/latest:")
if len(stata_10006) > 0:
    print(f"First: {stata_10006['yyyymm'].min()}, Last: {stata_10006['yyyymm'].max()}, Count: {len(stata_10006)}")

print(f"\nPython permno 10006 earliest/latest:")
if len(python_10006) > 0:
    print(f"First: {python_10006['yyyymm'].min()}, Last: {python_10006['yyyymm'].max()}, Count: {len(python_10006)}")

# Let's trace through the intermediate data to see where the issue is
print("\n=== Tracing intermediate data ===")

# Load SignalMasterTable to see if permno 10006 exists in June 1982 (which would create 1983 signals)
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt_10006 = smt[smt['permno'] == 10006]

print(f"\nSignalMasterTable permno 10006 around 1982-1983:")
smt_10006_early = smt_10006[(smt_10006['time_avail_m'] >= '1982-01') & (smt_10006['time_avail_m'] <= '1983-12')]
print(smt_10006_early[['permno', 'time_avail_m', 'gvkey']].head(20))

# Check if June 1982 exists (this would generate 1983 monthly observations)
june_1982 = smt_10006[smt_10006['time_avail_m'] == '1982-06']
print(f"\nJune 1982 data for permno 10006:")
print(june_1982[['permno', 'time_avail_m', 'gvkey']])