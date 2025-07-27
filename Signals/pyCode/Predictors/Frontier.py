# ABOUTME: Translates Frontier.do to create efficient frontier index predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Frontier.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_aCompustat.parquet
# Output: ../pyData/Predictors/Frontier.csv

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()

# Merge with Compustat
comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'at', 'ceq', 'dltt', 'capx', 'sale', 'xrd', 'xad', 'ppent', 'ebitda']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Replace missing xad with 0
df['xad'] = df['xad'].fillna(0)

# Create variables
df['YtempBM'] = np.log(df['mve_c'])
df['tempBook'] = np.log(df['ceq'])
df['tempLTDebt'] = df['dltt'] / df['at']
df['tempCapx'] = df['capx'] / df['sale']
df['tempRD'] = df['xrd'] / df['sale']
df['tempAdv'] = df['xad'] / df['sale']
df['tempPPE'] = df['ppent'] / df['at']
df['tempEBIT'] = df['ebitda'] / df['at']

# Create simplified FF48 industry classification
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
    elif 2000 <= sic <= 2111:  # Food
        return 4
    elif 2200 <= sic <= 2299:  # Textiles
        return 5
    elif 2300 <= sic <= 2399:  # Apparel
        return 6
    elif 2400 <= sic <= 2499:  # Wood
        return 7
    elif 2500 <= sic <= 2599:  # Furniture
        return 8
    elif 2600 <= sic <= 2699:  # Paper
        return 9
    elif 2700 <= sic <= 2799:  # Printing
        return 10
    elif 2800 <= sic <= 2899:  # Chemicals
        return 11
    elif 2900 <= sic <= 2999:  # Petroleum
        return 12
    elif 3000 <= sic <= 3099:  # Rubber
        return 13
    elif 3100 <= sic <= 3199:  # Leather
        return 14
    elif 3200 <= sic <= 3299:  # Stone, Clay
        return 15
    elif 3300 <= sic <= 3399:  # Primary Metals
        return 16
    elif 3400 <= sic <= 3499:  # Fabricated Metals
        return 17
    elif 3500 <= sic <= 3599:  # Machinery
        return 18
    elif 3600 <= sic <= 3699:  # Electrical Equipment
        return 19
    elif 3700 <= sic <= 3799:  # Transportation Equipment
        return 20
    else:
        return 21  # Other

df['tempFF48'] = df['sicCRSP'].apply(get_ff48)
df = df.dropna(subset=['tempFF48'])

# Prepare regression variables
reg_vars = ['tempBook', 'tempLTDebt', 'tempCapx', 'tempRD', 'tempAdv', 'tempPPE', 'tempEBIT']

# Rolling regression for each time period
df['logmefit_NS'] = np.nan
df = df.sort_values(['permno', 'time_avail_m'])

unique_times = sorted(df['time_avail_m'].unique())
for time_t in unique_times:
    # Define 5-year rolling window
    start_time = time_t - pd.DateOffset(months=60)
    
    # Get training data
    train_data = df[(df['time_avail_m'] > start_time) & (df['time_avail_m'] <= time_t)].copy()
    
    if len(train_data) < 50:  # Need minimum observations
        continue
        
    # Prepare training data
    train_data = train_data.dropna(subset=['YtempBM'] + reg_vars)
    
    if len(train_data) < 30:
        continue
    
    # Create industry dummies
    industry_dummies = pd.get_dummies(train_data['tempFF48'], prefix='ff48')
    
    # Prepare X matrix
    X = train_data[reg_vars].copy()
    X = pd.concat([X, industry_dummies], axis=1)
    
    y = train_data['YtempBM']
    
    # Fit regression
    try:
        reg = LinearRegression()
        reg.fit(X, y)
        
        # Predict for current time period
        current_data = df[df['time_avail_m'] == time_t].copy()
        current_data = current_data.dropna(subset=reg_vars)
        
        if len(current_data) == 0:
            continue
        
        # Create industry dummies for current data
        current_industry = pd.get_dummies(current_data['tempFF48'], prefix='ff48')
        
        # Align columns
        for col in industry_dummies.columns:
            if col not in current_industry.columns:
                current_industry[col] = 0
        current_industry = current_industry.reindex(columns=industry_dummies.columns, fill_value=0)
        
        X_pred = current_data[reg_vars].copy()
        X_pred = pd.concat([X_pred, current_industry], axis=1)
        
        predictions = reg.predict(X_pred)
        
        # Store predictions
        df.loc[df['time_avail_m'] == time_t, 'logmefit_NS'] = predictions
        
    except:
        continue

# Calculate Frontier
df['Frontier'] = df['YtempBM'] - df['logmefit_NS']
df['Frontier'] = -1 * df['Frontier']

# Apply filters
df = df[(~df['ceq'].isna()) & (df['ceq'] > 0)].copy()

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Frontier']].copy()
df_final = df_final.dropna(subset=['Frontier'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'Frontier']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/Frontier.csv')

print("Frontier predictor saved successfully")