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

# Proper FF48 industry classification based on Ken French's methodology
def get_ff48(sic):
    if pd.isna(sic):
        return np.nan
    sic = int(sic)
    
    if 100 <= sic <= 999:
        return 1  # Agriculture
    elif 1000 <= sic <= 1099:
        return 2  # Mining
    elif 1200 <= sic <= 1399:
        return 3  # Coal
    elif 1400 <= sic <= 1499:
        return 4  # Oil
    elif 1500 <= sic <= 1999:
        return 5  # Construction
    elif 2000 <= sic <= 2099:
        return 6  # Food
    elif 2100 <= sic <= 2199:
        return 7  # Soda
    elif 2200 <= sic <= 2269 or 2270 <= sic <= 2299:
        return 8  # Textiles
    elif 2300 <= sic <= 2399:
        return 9  # Apparel
    elif 2400 <= sic <= 2499:
        return 10  # Wood
    elif 2500 <= sic <= 2549 or 2590 <= sic <= 2599:
        return 11  # Furniture
    elif 2600 <= sic <= 2699:
        return 12  # Paper
    elif 2700 <= sic <= 2749 or 2770 <= sic <= 2799:
        return 13  # Printing
    elif 2800 <= sic <= 2829 or 2840 <= sic <= 2899:
        return 14  # Chemicals
    elif 2830 <= sic <= 2839:
        return 15  # Drugs
    elif 2900 <= sic <= 2999:
        return 16  # Petroleum
    elif 3000 <= sic <= 3099:
        return 17  # Rubber
    elif 3100 <= sic <= 3199:
        return 18  # Leather
    elif 3200 <= sic <= 3299:
        return 19  # Stone
    elif 3300 <= sic <= 3399:
        return 20  # Steel
    elif 3400 <= sic <= 3499:
        return 21  # Fabricated Metal
    elif 3500 <= sic <= 3569 or 3580 <= sic <= 3599:
        return 22  # Machinery
    elif 3570 <= sic <= 3579:
        return 23  # Computers
    elif 3600 <= sic <= 3699:
        return 24  # Electronic Equipment
    elif 3700 <= sic <= 3799:
        return 25  # Transportation
    elif 3800 <= sic <= 3829 or 3860 <= sic <= 3899:
        return 26  # Instruments
    elif 3830 <= sic <= 3859:
        return 27  # Photo
    elif 3900 <= sic <= 3999:
        return 28  # Other Manufacturing
    elif 4000 <= sic <= 4099:
        return 29  # Railroad
    elif 4100 <= sic <= 4199:
        return 30  # Shipping
    elif 4200 <= sic <= 4299:
        return 31  # Transportation
    elif 4400 <= sic <= 4499:
        return 32  # Water
    elif 4500 <= sic <= 4599:
        return 33  # Aircraft
    elif 4600 <= sic <= 4699:
        return 34  # Communication
    elif 4700 <= sic <= 4799:
        return 35  # Communication
    elif 4800 <= sic <= 4899:
        return 36  # Communication  
    elif 4900 <= sic <= 4999:
        return 37  # Utilities
    elif 5000 <= sic <= 5099:
        return 38  # Wholesale
    elif 5100 <= sic <= 5199:
        return 39  # Wholesale
    elif 5200 <= sic <= 5999:
        return 40  # Retail
    elif 6000 <= sic <= 6099:
        return 41  # Banks
    elif 6100 <= sic <= 6199:
        return 42  # Insurance
    elif 6200 <= sic <= 6299:
        return 43  # Real Estate
    elif 6300 <= sic <= 6399:
        return 44  # Insurance
    elif 6400 <= sic <= 6499:
        return 45  # Insurance
    elif 6500 <= sic <= 6599:
        return 46  # Real Estate
    elif 6700 <= sic <= 6799:
        return 47  # Finance
    elif 7000 <= sic <= 8999:
        return 48  # Other
    else:
        return 48  # Other

df['tempFF48'] = df['sicCRSP'].apply(get_ff48)
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
        
        # Store predictions
        mask = (df['time_avail_m'] == current_date) & (df.index.isin(current_data.index))
        df.loc[mask, 'logmefit_NS'] = predictions
        
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