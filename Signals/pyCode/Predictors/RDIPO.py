# ABOUTME: RDIPO.py - calculates IPO firms with no R&D spending predictor
# ABOUTME: IPO and no R&D spending - binary indicator for IPO firms that have zero R&D expenditures
# ABOUTME: Reference: Gou, Lev and Shi 2006, Table 8 row 2

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, IPODates.parquet
# Output: ../pyData/Predictors/RDIPO.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'xrd']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Merge with IPO dates
ipo = pd.read_parquet('../pyData/Intermediate/IPODates.parquet')
ipo = ipo[['permno', 'IPOdate']].copy()
df = df.merge(ipo, on='permno', how='left')

# SIGNAL CONSTRUCTION
# Calculate months since IPO
df['months_since_ipo'] = (df['time_avail_m'].dt.year - df['IPOdate'].dt.year) * 12 + \
                        (df['time_avail_m'].dt.month - df['IPOdate'].dt.month)

# IPO period: between 6 months and 3 years (36 months) after IPO
df['tempipo'] = ((df['months_since_ipo'] <= 36) & (df['months_since_ipo'] > 6)).astype(int)

# Set to 0 if IPOdate is missing
df.loc[df['IPOdate'].isna(), 'tempipo'] = 0

# Create RDIPO indicator: IPO period AND no R&D spending
df['RDIPO'] = 0
df.loc[(df['tempipo'] == 1) & (df['xrd'] == 0), 'RDIPO'] = 1

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'RDIPO']].copy()

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'RDIPO']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/RDIPO.csv')

print("RDIPO predictor saved successfully")