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
import sys
sys.path.append('.')
from utils.sicff import sicff

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()

# Merge with Compustat
comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'at', 'ceq', 'dltt', 'capx', 'sale', 'xrd', 'xad', 'ppent', 'ebitda']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# Create time_avail as numeric time variable (Stata monthly format) 
# Use Stata's tm format: months since 1960m1 = 0
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

# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Use unified sicff module for Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)
df = df.dropna(subset=['tempFF48'])

# Prepare regression variables
reg_vars = ['tempBook', 'tempLTDebt', 'tempCapx', 'tempRD', 'tempAdv', 'tempPPE', 'tempEBIT']

# Rolling regression for each time period
df['logmefit_NS'] = np.nan
df = df.sort_values(['permno', 'time_avail_m'])

# Process each unique time period like Stata's levelsof
unique_dates = sorted(df['time_avail_m'].unique())
# Only skip periods that can't have 60 months of training data (i.e., before 1960 + 60 months)
# But let the regression logic handle insufficient data rather than pre-filtering
# This matches Stata's approach of processing all available dates

# Process all time periods for complete data coverage
# unique_dates = unique_dates[::3]  # Commented out - was for faster testing only

print(f"Processing {len(unique_dates)} time periods (starting from {unique_dates[0].strftime('%Y-%m')})...")

for i, current_date in enumerate(unique_dates):
    # Use exact Stata logic: time_avail <= t & time_avail_m > t - 60
    # Where t is the numeric time representation of current_date
    
    # Convert current_date to time_avail for comparison (Stata tm format)
    current_time_avail = ((current_date.year - stata_base.year) * 12 + 
                         (current_date.month - stata_base.month))
    
    # Calendar-based 60 months back (like Stata `t' - 60)
    # Convert current time_avail back to date, subtract 60 months, then convert to time_avail
    months_back_60 = current_time_avail - 60
    
    # Get training data: time_avail <= current AND time_avail > 60 time units back
    train_data = df[(df['time_avail'] <= current_time_avail) & 
                   (df['time_avail'] > months_back_60)].copy()
    
    if len(train_data) < 3:  # Match Stata's very minimal threshold
        continue
        
    # Prepare training data
    train_data = train_data.dropna(subset=['YtempBM'] + reg_vars)
    
    if len(train_data) < 3:  # Allow very small samples like Stata (minimum for regression)
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
        
        # Predict for current time period (time_avail_m == current_date)
        current_data = df[df['time_avail_m'] == current_date].copy()
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
        
        # Store predictions - ensure proper alignment
        mask = (df['time_avail_m'] == current_date) & (df.index.isin(current_data.index))
        
        # Critical fix: Ensure predictions are assigned to correct observations
        # by explicitly matching indices rather than relying on mask ordering
        for idx, pred_value in zip(current_data.index, predictions):
            if (df.loc[idx, 'time_avail_m'] == current_date):
                df.loc[idx, 'logmefit_NS'] = pred_value
        
        if i % 60 == 0:  # Print progress every 60 periods (5 years)
            print(f"Processed {i+1}/{len(unique_dates)} periods, stored {len(predictions)} predictions for {current_date.strftime('%Y-%m')}")
        
    except Exception as e:
        if i % 60 == 0:
            print(f"Failed period {current_date.strftime('%Y-%m')}: {e}")
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