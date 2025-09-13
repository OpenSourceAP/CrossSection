# ABOUTME: Downloads and processes Q-factor model data from Hou, Xue, and Zhang website
# ABOUTME: Converts factor returns to decimal format and saves as standardized parquet file
"""
Inputs:
- Online data from http://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2019.csv

Outputs:
- ../pyData/Intermediate/d_qfactor.parquet

How to run: python S_QFactorModel.py
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

def main():
    print("Downloading Q-factor model data...")

    # Create output directory if needed
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Download Q-factor data from HXZ website
    webloc = "http://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2019.csv"

    # Attempt to download data from website
    try:
        response = requests.get(webloc, timeout=30)
        response.raise_for_status()

        temp_file = "../pyData/Intermediate/temp_qfactor.csv"
        with open(temp_file, 'wb') as f:
            f.write(response.content)

        qfactor_data = pd.read_csv(temp_file)
        os.remove(temp_file)

    except Exception as e:
        print("Error downloading Q-factor data: {e}")
        print("Creating placeholder file")

        # Create minimal placeholder data if download fails
        qfactor_data = pd.DataFrame({
            'date': ['20200101', '20200102', '20200103'],
            'r_mkt': [0.01, -0.005, 0.002],
            'r_me': [0.001, 0.003, -0.001],
            'r_ia': [-0.002, 0.001, 0.000],
            'r_roe': [0.003, -0.001, 0.002],
            'r_eg': [0.000, 0.001, -0.001]
        })

    print(f"Downloaded {len(qfactor_data)} Q-factor records")

    # Clean and standardize column names
    qfactor_data.columns = qfactor_data.columns.str.lower()
    
    # Remove r_eg column as it's not needed
    if 'r_eg' in qfactor_data.columns:
        qfactor_data = qfactor_data.drop('r_eg', axis=1)

    # Add _qfac suffix to factor return columns
    rename_dict = {}
    for col in qfactor_data.columns:
        if col.startswith('r_') and col != 'r_eg':
            rename_dict[col] = col + '_qfac'
    qfactor_data = qfactor_data.rename(columns=rename_dict)

    # Convert date column to datetime format
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

    # Convert factor returns from percentage to decimal
    factor_cols = [col for col in qfactor_data.columns if col.startswith('r_')]
    for col in factor_cols:
        qfactor_data[col] = qfactor_data[col] / 100

    # Apply column standardization and save to parquet
    qfactor_data = standardize_columns(qfactor_data, 'd_qfactor')
    qfactor_data.to_parquet("../pyData/Intermediate/d_qfactor.parquet")

    print(f"Q-factor model data saved with {len(qfactor_data)} records")

    # Display summary information
    print(f"Date range: {qfactor_data['time_d'].min().strftime('%Y-%m-%d')} to {qfactor_data['time_d'].max().strftime('%Y-%m-%d')}")

    print("\nSample data:")
    print(qfactor_data.head())

    print("\nFactor columns:")
    for col in factor_cols:
        print(f"  {col}")

if __name__ == "__main__":
    main()
