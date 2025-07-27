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

# Comparison group (FF48 groups 2, 3, 7, 43)
# Create simplified FF48 mapping
def get_ff48(sic):
    if pd.isna(sic):
        return np.nan
    sic = int(sic)
    if 100 <= sic <= 999:  # Agriculture
        return 1
    elif 1000 <= sic <= 1499:  # Mining
        return 2
    elif 1500 <= sic <= 1799:  # Construction  
        return 3
    elif 2000 <= sic <= 2799:  # Food
        return 7
    elif 4000 <= sic <= 4799:  # Transportation
        return 43
    else:
        return np.nan

df['tmpFF48'] = df['sicCRSP'].apply(get_ff48)
df['ComparableStock'] = (df['tmpFF48'].isin([2, 3, 7, 43])).astype(float)

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
condition4 = ((df['sinSegBeerFirstYear'] == 1) | (df['sinSegGamingFirstYear'] == 1)) & (df['year'] < df['firstYear']) & (df['year'] < 1965)

df.loc[condition1 | condition2 | condition3 | condition4, 'sinAlgo'] = 1
df.loc[(df['ComparableStock'] == 1) & df['sinAlgo'].isna(), 'sinAlgo'] = 0
df.loc[df['shrcd'] > 11, 'sinAlgo'] = np.nan

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'sinAlgo']].copy()
df_final = df_final.dropna(subset=['sinAlgo'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'sinAlgo']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/sinAlgo.csv')

print("sinAlgo predictor saved successfully")