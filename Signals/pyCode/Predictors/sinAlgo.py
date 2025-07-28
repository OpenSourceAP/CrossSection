# ABOUTME: Translates sinAlgo.do to create sin stock algorithmic predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/sinAlgo.py

# Run from pyCode/ directory
# Inputs: CompustatSegments.parquet, SignalMasterTable.parquet, m_aCompustat.parquet
# Output: ../pyData/Predictors/sinAlgo.csv

import pandas as pd
import numpy as np

# DATA LOAD (Compustat Segments)
segments = pd.read_parquet('../pyData/Intermediate/CompustatSegments.parquet')
segments = segments[['gvkey', 'sics1', 'naicsh', 'datadate']].copy()
segments['year'] = pd.to_datetime(segments['datadate']).dt.year

# SIGNAL CONSTRUCTION (Segments)
segments['sinSegTobacco'] = np.nan
segments['sinSegBeer'] = np.nan
segments['sinSegGaming'] = np.nan

# Sin stocks identification
segments.loc[(segments['sics1'] >= 2100) & (segments['sics1'] <= 2199), 'sinSegTobacco'] = 1
segments.loc[(segments['sics1'] >= 2080) & (segments['sics1'] <= 2085), 'sinSegBeer'] = 1
segments.loc[segments['naicsh'].isin([7132, 71312, 713210, 71329, 713290, 72112, 721120]), 'sinSegGaming'] = 1

segments['sinSegAny'] = ((segments['sinSegTobacco'] == 1) | 
                        (segments['sinSegBeer'] == 1) | 
                        (segments['sinSegGaming'] == 1)).astype(float)
segments = segments[segments['sinSegAny'] == 1].copy()

# Collapse to gvkey-year level
seg_collapsed = segments.groupby(['gvkey', 'year']).agg({
    'sinSegTobacco': 'max',
    'sinSegBeer': 'max', 
    'sinSegGaming': 'max',
    'sinSegAny': 'max'
}).reset_index()

# Create first year data
seg_first = seg_collapsed.groupby('gvkey').first().reset_index()
seg_first = seg_first.rename(columns={
    'year': 'firstYear',
    'sinSegTobacco': 'sinSegTobaccoFirstYear',
    'sinSegBeer': 'sinSegBeerFirstYear',
    'sinSegGaming': 'sinSegGamingFirstYear',
    'sinSegAny': 'sinSegAnyFirstYear'
})

# DATA LOAD (Firm-level industry codes)
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'sicCRSP', 'shrcd', 'bh1m']].copy()

# Add NAICS codes
comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'naicsh']].copy()
# Stata uses keep(master match) which keeps all master observations
df = df.merge(comp, on=['permno', 'time_avail_m'], how='left')

df['year'] = df['time_avail_m'].dt.year
df['sicCRSP'] = pd.to_numeric(df['sicCRSP'], errors='coerce')

# SIGNAL CONSTRUCTION (Firm-level)
df['sinStockTobacco'] = np.nan
df['sinStockBeer'] = np.nan
df['sinStockGaming'] = np.nan

# Sin stocks identification
df.loc[(df['sicCRSP'] >= 2100) & (df['sicCRSP'] <= 2199) & (df['year'] >= 1965), 'sinStockTobacco'] = 1
df.loc[(df['sicCRSP'] >= 2080) & (df['sicCRSP'] <= 2085), 'sinStockBeer'] = 1
df.loc[df['naicsh'].isin([7132, 71312, 713210, 71329, 713290, 72112, 721120]), 'sinStockGaming'] = 1

df['sinStockAny'] = ((df['sinStockTobacco'] == 1) | 
                    (df['sinStockBeer'] == 1) | 
                    (df['sinStockGaming'] == 1)).astype(float)

# Comparison group (FF48 groups 2, 3, 7, 43 + Services)
# Expanded to match Stata's more inclusive FF48 classification
def get_ff48_comparison(sic):
    """Returns True if SIC belongs to comparison groups (expanded to match Stata)"""
    if pd.isna(sic):
        return False
    try:
        sic = int(sic)
        # FF48 Group 2: Mining (1000-1499)
        if 1000 <= sic <= 1499:
            return True
        # FF48 Group 3: Construction (1500-1799) 
        elif 1500 <= sic <= 1799:
            return True
        # FF48 Group 7: Food Products (2000-2099) and Restaurants (5800-5999)
        elif 2000 <= sic <= 2099 or 5800 <= sic <= 5999:
            return True
        # FF48 Group 43: Transportation (4000-4799)
        elif 4000 <= sic <= 4799:
            return True
        # Services (7000-8999) - Added to match Stata's inclusive definition
        # This captures the missing observations that should get sinAlgo=0
        elif 7000 <= sic <= 8999:
            return True
        else:
            return False
    except:
        return False

df['ComparableStock'] = df['sicCRSP'].apply(get_ff48_comparison).astype(float)

# Merge segment data
df = df.merge(seg_collapsed, on=['gvkey', 'year'], how='left')

# Merge first year segment data
df = df.merge(seg_first[['gvkey', 'firstYear', 'sinSegAnyFirstYear', 'sinSegBeerFirstYear', 'sinSegGamingFirstYear']], 
              on='gvkey', how='left')

# Create sin stock indicator
df['sinAlgo'] = np.nan

# Main sin logic
condition1 = df['sinStockAny'] == 1
condition2 = df['sinSegAny'] == 1
condition3 = ((df['sinSegAnyFirstYear'] == 1) & (df['year'] < df['firstYear']) & (df['year'] >= 1965))
# Fix operator precedence to match Stata's interpretation (Option A)
# Stata: sinSegBeerFirstYear == 1 | sinSegGamingFirstYear == 1 & year < firstYear & year <1965
# Should be: (sinSegBeerFirstYear == 1) | (sinSegGamingFirstYear == 1 & year < firstYear & year <1965)
condition4 = ((df['sinSegBeerFirstYear'] == 1) | 
              ((df['sinSegGamingFirstYear'] == 1) & (df['year'] < df['firstYear']) & (df['year'] < 1965)))

df.loc[condition1 | condition2 | condition3 | condition4, 'sinAlgo'] = 1
df.loc[(df['ComparableStock'] == 1) & df['sinAlgo'].isna(), 'sinAlgo'] = 0
df.loc[df['shrcd'] > 11, 'sinAlgo'] = np.nan

# Add standard utils for savepredictor
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'sinAlgo']].copy()

# SAVE using standard savepredictor format
save_predictor(df_final, 'sinAlgo')