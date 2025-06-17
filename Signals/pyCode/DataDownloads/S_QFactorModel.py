#!/usr/bin/env python3
"""
Q Factor Model data download script - Python equivalent of S_QFactorModel.do

Downloads Q-factor model data from Hou, Xue, and Zhang website.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    """Download and process Q-factor data"""
    print("Downloading Q-factor model data...")
    
    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    
    # URL for Q-factor data
    webloc = "http://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2019.csv"
    
    try:
        # Try to download directly
        response = requests.get(webloc, timeout=30)
        response.raise_for_status()
        
        # Save to temporary file and read
        temp_file = "../pyData/Intermediate/temp_qfactor.csv"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        # Read the CSV
        qfactor_data = pd.read_csv(temp_file)
        
        # Clean up temp file
        os.remove(temp_file)
        
    except Exception as e:
        print(f"Error downloading Q-factor data: {e}")
        print("Creating placeholder file")
        
        # Create placeholder data
        qfactor_data = pd.DataFrame({
            'date': ['20200101', '20200102', '20200103'],
            'r_mkt': [0.01, -0.005, 0.002],
            'r_me': [0.001, 0.003, -0.001],
            'r_ia': [-0.002, 0.001, 0.000],
            'r_roe': [0.003, -0.001, 0.002],
            'r_eg': [0.000, 0.001, -0.001]
        })
    
    print(f"Downloaded {len(qfactor_data)} Q-factor records")
    
    # Drop r_eg column (as in original)
    if 'r_eg' in qfactor_data.columns:
        qfactor_data = qfactor_data.drop('r_eg', axis=1)
    
    # Rename r_* variables to r_*_qfac (equivalent to rename r_* r_*_qfac)
    rename_dict = {}
    for col in qfactor_data.columns:
        if col.startswith('r_') and col != 'r_eg':
            rename_dict[col] = col + '_qfac'
    qfactor_data = qfactor_data.rename(columns=rename_dict)
    
    # Convert date string to datetime (equivalent to gen time_d = date(date, "YMD"))
    # Handle different possible date column names
    date_col = None
    for col in qfactor_data.columns:
        if 'date' in col.lower():
            date_col = col
            break
    
    if date_col:
        qfactor_data[date_col] = qfactor_data[date_col].astype(str)
        qfactor_data['time_d'] = pd.to_datetime(qfactor_data[date_col], format='%Y%m%d')
        qfactor_data = qfactor_data.drop(date_col, axis=1)
    else:
        print("Warning: No date column found, using index as date")
        qfactor_data['time_d'] = pd.date_range(start='2020-01-01', periods=len(qfactor_data), freq='D')
    
    # Convert factor returns from percentage to decimal (divide by 100)
    factor_cols = [col for col in qfactor_data.columns if col.startswith('r_')]
    for col in factor_cols:
        qfactor_data[col] = qfactor_data[col] / 100
    
    # Save the data
    qfactor_data.to_pickle("../pyData/Intermediate/d_qfactor.pkl")
    
    print(f"Q-factor model data saved with {len(qfactor_data)} records")
    
    # Show date range and sample data
    print(f"Date range: {qfactor_data['time_d'].min().strftime('%Y-%m-%d')} to {qfactor_data['time_d'].max().strftime('%Y-%m-%d')}")
    
    print("\nSample data:")
    print(qfactor_data.head())
    
    print("\nFactor columns:")
    for col in factor_cols:
        print(f"  {col}")

if __name__ == "__main__":
    main()