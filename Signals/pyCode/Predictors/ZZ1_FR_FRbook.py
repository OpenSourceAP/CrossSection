# ABOUTME: Pension Funding Status following Franzoni and Marin 2006, Table 3B
# ABOUTME: Computes funding status metrics using pension plan asset/obligation data from Compustat

# Run: python3 Predictors/ZZ1_FR_FRbook.py
# Inputs: SignalMasterTable.parquet, CompustatPensions.parquet, m_aCompustat.parquet  
# Outputs: pyData/Predictors/FR.csv, pyData/Placebos/FRbook.csv

import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor, save_placebo

# DATA LOAD
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = signal_master[['permno', 'gvkey', 'time_avail_m', 'shrcd', 'mve_permco']].copy()
df = df.dropna(subset=['gvkey'])

# Extract year for pension data merge
df['year'] = df['time_avail_m'].dt.year

# Merge with pension data
pensions = pd.read_parquet('../pyData/Intermediate/CompustatPensions.parquet')
df = df.merge(pensions, on=['gvkey', 'year'], how='inner')

# Merge with Compustat for book assets
compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df.merge(compustat[['gvkey', 'time_avail_m', 'at']], 
              on=['gvkey', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
# Fair Value of Plan Assets
df['FVPA'] = np.where(
    (df['year'] >= 1980) & (df['year'] <= 1986),
    df['pbnaa'],
    np.where(
        (df['year'] >= 1987) & (df['year'] <= 1997),
        df['pplao'] + df['pplau'],
        np.where(
            df['year'] >= 1998,
            df['pplao'],
            np.nan
        )
    )
)

# Projected Benefit Obligation
df['PBO'] = np.where(
    (df['year'] >= 1980) & (df['year'] <= 1986),
    df['pbnvv'],
    np.where(
        (df['year'] >= 1987) & (df['year'] <= 1997),
        df['pbpro'] + df['pbpru'],
        np.where(
            df['year'] >= 1998,
            df['pbpro'],
            np.nan
        )
    )
)

# Funding Ratio scaled by market value
df['FR'] = (df['FVPA'] - df['PBO']) / df['mve_permco']
df.loc[df['shrcd'] > 11, 'FR'] = np.nan

# Funding Ratio scaled by book assets
df['FRbook'] = (df['FVPA'] - df['PBO']) / df['at']
df.loc[df['shrcd'] > 11, 'FRbook'] = np.nan

# SAVE FR
save_predictor(df, 'FR')

# SAVE FRbook (as placebo)  
save_placebo(df, 'FRbook')

print("FR (Predictor) and FRbook (Placebo) saved successfully")