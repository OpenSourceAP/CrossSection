# ABOUTME: Translates sinAlgo.do to create sin stock algorithmic predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/sinAlgo.py

# Run from pyCode/ directory  
# Inputs: CompustatSegments.parquet, SignalMasterTable.parquet, m_aCompustat.parquet
# Output: ../pyData/Predictors/sinAlgo.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.sicff import sicff

# DATA LOAD (Compustat Segments)
segments = pd.read_parquet('../pyData/Intermediate/CompustatSegments.parquet')
segments = segments[['gvkey', 'sics1', 'naicsh', 'datadate']].copy()
segments['year'] = segments['datadate'].dt.year

# SIGNAL CONSTRUCTION
segments['sinSegTobacco'] = np.nan
segments['sinSegBeer'] = np.nan  
segments['sinSegGaming'] = np.nan

# Sin stocks - exact translation of Stata conditions
# replace sinSegTobacco = 1 if sics1 >= 2100 & sics1 <= 2199
tobacco_mask = (segments['sics1'] >= 2100) & (segments['sics1'] <= 2199)
segments.loc[tobacco_mask, 'sinSegTobacco'] = 1

# replace sinSegBeer = 1 if sics1 >=2080 & sics1 <= 2085
beer_mask = (segments['sics1'] >= 2080) & (segments['sics1'] <= 2085)
segments.loc[beer_mask, 'sinSegBeer'] = 1

# replace sinSegGaming = 1 if naics == 7132 | naics == 71312 | naics == 713210 | naics == 71329 | naics == 713290 | naics == 72112 | naics == 721120
gaming_codes = [7132, 71312, 713210, 71329, 713290, 72112, 721120]
gaming_mask = segments['naicsh'].isin(gaming_codes)
segments.loc[gaming_mask, 'sinSegGaming'] = 1

# gen sinSegAny = 1 if sinSegTobacco == 1 | sinSegBeer == 1 | sinSegGaming == 1
any_mask = (segments['sinSegTobacco'] == 1) | (segments['sinSegBeer'] == 1) | (segments['sinSegGaming'] == 1)
segments['sinSegAny'] = np.nan
segments.loc[any_mask, 'sinSegAny'] = 1

# keep if sinSegAny == 1
segments = segments[segments['sinSegAny'] == 1].copy()

# gcollapse (max) sinSeg*, by(gvkey year)
seg_collapsed = segments.groupby(['gvkey', 'year']).agg({
    'sinSegTobacco': 'max',
    'sinSegBeer': 'max',
    'sinSegGaming': 'max', 
    'sinSegAny': 'max'
}).reset_index()

# Save temp file equivalent
temp = seg_collapsed.copy()

# "a stock identified as sinful using the segments data will be characterized as sinful throughout its history." (page 19)
# bys gvkey (year): keep if _n == 1
first_year = temp.groupby('gvkey').first().reset_index()
# rename year firstYear
first_year = first_year.rename(columns={'year': 'firstYear'})
# rename sinSeg* sinSeg*FirstYear  
first_year = first_year.rename(columns={
    'sinSegTobacco': 'sinSegTobaccoFirstYear',
    'sinSegBeer': 'sinSegBeerFirstYear',
    'sinSegGaming': 'sinSegGamingFirstYear',
    'sinSegAny': 'sinSegAnyFirstYear'
})

# DATA LOAD (Firm-level industry codes)
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'sicCRSP', 'shrcd', 'bh1m']].copy()

# Add NAICS codes - merge 1:1 permno time_avail_m using m_aCompustat, keepusing(naicsh) keep(master match) nogenerate
comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'naicsh']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='left')

# gen year = year(dofm(time_avail_m))
df['year'] = df['time_avail_m'].dt.year
# destring sicCRSP, replace
df['sicCRSP'] = pd.to_numeric(df['sicCRSP'], errors='coerce')

# SIGNAL CONSTRUCTION
df['sinStockTobacco'] = np.nan
df['sinStockBeer'] = np.nan
df['sinStockGaming'] = np.nan

# Sin stocks
# replace sinStockTobacco = 1 if sicCRSP >= 2100 & sicCRSP <= 2199 & year >= 1965  // Footnote 14, page 19
tobacco_stock_mask = (df['sicCRSP'] >= 2100) & (df['sicCRSP'] <= 2199) & (df['year'] >= 1965)
df.loc[tobacco_stock_mask, 'sinStockTobacco'] = 1

# replace sinStockBeer = 1 if sicCRSP >=2080 & sicCRSP <= 2085
beer_stock_mask = (df['sicCRSP'] >= 2080) & (df['sicCRSP'] <= 2085)  
df.loc[beer_stock_mask, 'sinStockBeer'] = 1

# replace sinStockGaming = 1 if naicsh == 7132 | naicsh == 71312 | naicsh == 713210 | naicsh == 71329 | naicsh == 713290 | naicsh == 72112 | naicsh == 721120
gaming_stock_mask = df['naicsh'].isin(gaming_codes)
df.loc[gaming_stock_mask, 'sinStockGaming'] = 1

# gen sinStockAny = 1 if sinStockTobacco == 1 | sinStockBeer == 1 | sinStockGaming == 1
stock_any_mask = (df['sinStockTobacco'] == 1) | (df['sinStockBeer'] == 1) | (df['sinStockGaming'] == 1)
df['sinStockAny'] = np.nan
df.loc[stock_any_mask, 'sinStockAny'] = 1

# Comparison group (top of page 22, FF48 groups 2, 3, 7, 43)
# sicff sicCRSP, generate(tmpFF48) industry(48)
df['tmpFF48'] = df['sicCRSP'].apply(lambda x: sicff(x, industry=48) if pd.notna(x) else np.nan)
# gen ComparableStock = 1 if tmpFF48 == 2 | tmpFF48 == 3 | tmpFF48 == 7 | tmpFF48 == 43
comparable_mask = df['tmpFF48'].isin([2, 3, 7, 43])
df['ComparableStock'] = np.nan
df.loc[comparable_mask, 'ComparableStock'] = 1

# Merge segment data - merge m:1 gvkey year using temp, keep(master match) nogenerate
df = df.merge(temp, on=['gvkey', 'year'], how='left')

# Merge first year segment data - merge m:1 gvkey using tempFirstYear, keep(master match) nogenerate  
df = df.merge(first_year, on='gvkey', how='left')

# Finally, create sin stock indicator
df['sinAlgo'] = np.nan

# replace sinAlgo = 1 if ///
#         sinStockAny == 1 | /// *Stock-level sin indicator is equal to 1*
#         sinSegAny == 1 |  /// *Stock-segment sin indicator is equal to 1*
#         sinSegAnyFirstYear == 1 & year < firstYear & year >=1965  | ///  *backfill sin history (with tobacco not being a sin stock before 1965)
#         sinSegBeerFirstYear == 1 | sinSegGamingFirstYear == 1 & year < firstYear & year <1965

# Breaking down the complex condition
condition1 = df['sinStockAny'] == 1
condition2 = df['sinSegAny'] == 1  
condition3 = (df['sinSegAnyFirstYear'] == 1) & (df['year'] < df['firstYear']) & (df['year'] >= 1965)
# Note: Stata precedence - this should be parsed as: sinSegBeerFirstYear == 1 | (sinSegGamingFirstYear == 1 & year < firstYear & year <1965)
condition4a = df['sinSegBeerFirstYear'] == 1
condition4b = (df['sinSegGamingFirstYear'] == 1) & (df['year'] < df['firstYear']) & (df['year'] < 1965)
condition4 = condition4a | condition4b

sin_mask = condition1 | condition2 | condition3 | condition4
df.loc[sin_mask, 'sinAlgo'] = 1

# replace sinAlgo = 0 if ComparableStock == 1 & mi(sinAlgo)
comparable_not_sin_mask = (df['ComparableStock'] == 1) & df['sinAlgo'].isna()
df.loc[comparable_not_sin_mask, 'sinAlgo'] = 0

# replace sinAlgo = . if shrcd > 11
df.loc[df['shrcd'] > 11, 'sinAlgo'] = np.nan

# SAVE
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'sinAlgo']].copy()

# SAVE using standard savepredictor format
save_predictor(df_final, 'sinAlgo')