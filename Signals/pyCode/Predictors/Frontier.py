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

# Create time_avail (numeric months since 1960-01) to match Stata logic
stata_base = pd.to_datetime('1960-01-01')
df['time_avail'] = ((df['time_avail_m'].dt.year - stata_base.year) * 12 + 
                    (df['time_avail_m'].dt.month - stata_base.month))

# SIGNAL CONSTRUCTION
# Replace missing xad with 0
df['xad'] = df['xad'].fillna(0)

# Create variables - handle infinite values like Stata (set to NaN)
df['YtempBM'] = np.log(df['mve_c'])
df['YtempBM'] = df['YtempBM'].replace([np.inf, -np.inf], np.nan)

df['tempBook'] = np.log(df['ceq'])
df['tempBook'] = df['tempBook'].replace([np.inf, -np.inf], np.nan)

# Handle division by zero - set to NaN when denominator is 0 or missing
df['tempLTDebt'] = np.where((df['at'] == 0) | df['at'].isna(), np.nan, df['dltt'] / df['at'])

df['tempCapx'] = np.where((df['sale'] == 0) | df['sale'].isna(), np.nan, df['capx'] / df['sale'])

df['tempRD'] = np.where((df['sale'] == 0) | df['sale'].isna(), np.nan, df['xrd'] / df['sale'])

df['tempAdv'] = np.where((df['sale'] == 0) | df['sale'].isna(), np.nan, df['xad'] / df['sale'])

df['tempPPE'] = np.where((df['at'] == 0) | df['at'].isna(), np.nan, df['ppent'] / df['at'])

df['tempEBIT'] = np.where((df['at'] == 0) | df['at'].isna(), np.nan, df['ebitda'] / df['at'])

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

# Only process time periods where we have actual data (skip early periods with no data)
unique_times = sorted(df['time_avail'].unique())
# Filter to only process periods with sufficient history (after month 60 from start)
min_process_time = df['time_avail'].min() + 60
unique_times = [t for t in unique_times if t >= min_process_time]
print(f"Processing {len(unique_times)} time periods (skipping first 60 months)...")

for i, time_t in enumerate(unique_times):
    # Use Stata logic: time_avail <= t & time_avail_m > t - 60
    # This means: include data up to current period AND only recent data (5-year window)
    
    # Get training data using exact Stata condition
    train_data = df[(df['time_avail'] <= time_t) & (df['time_avail'] > time_t - 60)].copy()
    
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
        
        # Predict for current time period (time_avail == t)
        current_data = df[df['time_avail'] == time_t].copy()
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
        mask = (df['time_avail'] == time_t) & (df.index.isin(current_data.index))
        df.loc[mask, 'logmefit_NS'] = predictions
        
        if i % 120 == 0:  # Print progress every 120 periods (10 years)
            # Convert time_avail back to date for display
            display_date = stata_base + pd.DateOffset(months=time_t)
            print(f"Processed {i+1}/{len(unique_times)} periods, stored {len(predictions)} predictions for {display_date.strftime('%Y-%m')}")
        
    except Exception as e:
        if i % 120 == 0:
            display_date = stata_base + pd.DateOffset(months=time_t)
            print(f"Failed period {display_date.strftime('%Y-%m')}: {e}")
        continue

# Calculate Frontier
total_predictions = df['logmefit_NS'].notna().sum()
print(f"Total predictions generated: {total_predictions}")

df['Frontier'] = df['YtempBM'] - df['logmefit_NS']
df['Frontier'] = -1 * df['Frontier']

# Apply filters
print(f"Before ceq filter: {len(df)}")
df = df[(~df['ceq'].isna()) & (df['ceq'] > 0)].copy()
print(f"After ceq filter: {len(df)}")

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Frontier']].copy()
print(f"Before dropping NaN Frontier: {len(df_final)}")
df_final = df_final.dropna(subset=['Frontier'])
print(f"Final output: {len(df_final)} observations")

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