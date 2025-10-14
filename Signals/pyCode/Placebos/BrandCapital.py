# ABOUTME: BrandCapital.py - calculates brand capital placebo
# ABOUTME: Python equivalent of BrandCapital.do, translates line-by-line from Stata code

"""
BrandCapital.py

Inputs:
    - a_aCompustat.parquet: gvkey, permno, time_avail_m, fyear, datadate, xad, xad0, at columns

Outputs:
    - BrandCapital.csv: permno, yyyymm, BrandCapital columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/BrandCapital.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting BrandCapital.py")

# DATA LOAD
# use gvkey permno time_avail_m fyear datadate xad xad0 at using "$pathDataIntermediate/a_aCompustat", clear
print("Loading a_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'fyear', 'datadate', 'xad', 'xad0', 'at'])

print(f"Loaded data: {len(df)} rows")

# SIGNAL CONSTRUCTION
# Sort by gvkey and fyear for processing
print("Sorting by gvkey and fyear...")
df = df.sort(['gvkey', 'fyear'])

# Convert to pandas for complex logic that's easier to implement
print("Converting to pandas for complex brand capital calculation...")
df_pandas = df.to_pandas()

# gen byte OK = !missing(xad)
df_pandas['OK'] = (~df_pandas['xad'].isna()).astype(int)

print("Computing brand capital...")
# Initialize brand capital
df_pandas['BrandCapital'] = np.nan
df_pandas['tempYear'] = np.nan
df_pandas['tempxad'] = df_pandas['xad'].fillna(0)

# Process each gvkey separately
results = []

for gvkey in df_pandas['gvkey'].unique():
    if pd.isna(gvkey):
        continue
        
    group = df_pandas[df_pandas['gvkey'] == gvkey].copy()
    group = group.sort_values('fyear')
    
    # Find first non-missing advertising expenditure year
    first_ok_idx = group[group['OK'] == 1].index
    if len(first_ok_idx) > 0:
        first_year = group.loc[first_ok_idx[0], 'fyear']
        group.loc[first_ok_idx[0], 'BrandCapital'] = group.loc[first_ok_idx[0], 'xad'] / (0.5 + 0.1)
        group.loc[first_ok_idx[0], 'tempYear'] = first_year
        
        # Set FirstNMyear for all observations in this gvkey
        group['FirstNMyear'] = first_year
        
        # Initialize the first brand capital value
        prev_bc = group.loc[first_ok_idx[0], 'BrandCapital']
        
        # Apply the recursive formula for subsequent years
        for idx in group.index[1:]:
            if group.loc[idx, 'fyear'] >= first_year:
                current_tempxad = group.loc[idx, 'tempxad']
                group.loc[idx, 'BrandCapital'] = (1 - 0.5) * prev_bc + current_tempxad
                prev_bc = group.loc[idx, 'BrandCapital']
        
        # Set to missing if conditions not met
        group.loc[group['fyear'] < first_year, 'BrandCapital'] = np.nan
        group.loc[group['xad'].isna(), 'BrandCapital'] = np.nan
        
        # Scale by assets: BrandCapital = BrandCapital/at
        group['BrandCapital'] = group['BrandCapital'] / group['at']
    
    results.append(group)

# Combine all results
if results:
    df_pandas = pd.concat(results, ignore_index=True)
else:
    df_pandas['BrandCapital'] = np.nan

print("Expanding to monthly data...")

# * Expand to monthly
# This creates 12 copies of each annual observation for each month
expanded_data = []

for _, row in df_pandas.iterrows():
    if pd.notna(row['time_avail_m']) and pd.notna(row['BrandCapital']):
        base_date = row['time_avail_m']
        for month_offset in range(12):
            new_row = row.copy()
            # Add months to the base date
            new_date = base_date + pd.DateOffset(months=month_offset)
            new_row['time_avail_m'] = new_date
            expanded_data.append(new_row)

if expanded_data:
    df_expanded = pd.DataFrame(expanded_data)
    
    # bysort gvkey time_avail_m (datadate): keep if _n == _N 
    # Keep the latest datadate for each gvkey-time combination
    df_expanded = df_expanded.sort_values(['gvkey', 'time_avail_m', 'datadate'])
    df_expanded = df_expanded.groupby(['gvkey', 'time_avail_m']).tail(1)
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    df_expanded = df_expanded.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    
    print(f"Generated BrandCapital for {len(df_expanded)} observations")
    
    # Convert back to polars
    df_final = pl.from_pandas(df_expanded[['permno', 'time_avail_m', 'BrandCapital']])
    
else:
    # Handle case where no valid data
    print("No valid brand capital data generated")
    df_final = pl.DataFrame({
        'permno': [], 
        'time_avail_m': [], 
        'BrandCapital': []
    })

# SAVE
# do "$pathCode/saveplacebo" BrandCapital
save_placebo(df_final, 'BrandCapital')

print("BrandCapital.py completed")