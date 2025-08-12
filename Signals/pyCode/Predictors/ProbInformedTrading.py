# ABOUTME: Calculates probability of informed trading predictor from Easley et al
# ABOUTME: Runs line-by-line translation of Code/Predictors/ProbInformedTrading.do
#
# Run: python3 Predictors/ProbInformedTrading.py
# Input: SignalMasterTable.parquet, pin_monthly.parquet
# Output: ../pyData/Predictors/ProbInformedTrading.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.stata_fastxtile import fastxtile

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
master_df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = master_df[['permno', 'gvkey', 'time_avail_m', 'mve_c']].copy()

# gen year = yofd(dofm(time_avail_m))
df['time_avail_m'] = pd.to_datetime(df['time_avail_m'])
df['year'] = df['time_avail_m'].dt.year

# merge m:1 permno time_avail_m using "$pathDataIntermediate/pin_monthly", keep(master match) nogen
pin_df = pd.read_parquet('../pyData/Intermediate/pin_monthly.parquet')
pin_df['time_avail_m'] = pd.to_datetime(pin_df['time_avail_m'])
df = df.merge(pin_df[['permno', 'time_avail_m', 'a', 'u', 'es', 'eb']], 
              on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
# * generate yearly PIN measure from Easley et al
# gen pin = (a*u) / (a*u + es + eb)
df['pin'] = (df['a'] * df['u']) / (df['a'] * df['u'] + df['es'] + df['eb'])

# egen tempsize = fastxtile(mve_c), by(time_avail_m) n(2)
df['tempsize'] = fastxtile(df, 'mve_c', by='time_avail_m', n=2)

# replace pin = . if tempsize == 2
df.loc[df['tempsize'] == 2, 'pin'] = np.nan

# rename pin ProbInformedTrading
df['ProbInformedTrading'] = df['pin']

# SAVE
# Keep only required columns for output
output_df = df[['permno', 'time_avail_m', 'ProbInformedTrading']].copy()
output_df = output_df.dropna(subset=['ProbInformedTrading'])

# Convert time_avail_m to yyyymm format as integer
output_df['yyyymm'] = (output_df['time_avail_m'].dt.year * 100 + 
                       output_df['time_avail_m'].dt.month)

# Final output format
final_df = output_df[['permno', 'yyyymm', 'ProbInformedTrading']].copy()
final_df = final_df.sort_values(['permno', 'yyyymm'])

# Save to CSV
final_df.to_csv('../pyData/Predictors/ProbInformedTrading.csv', index=False)

print(f"ProbInformedTrading predictor saved with {len(final_df)} observations")