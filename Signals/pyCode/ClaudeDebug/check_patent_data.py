# ABOUTME: Check patent data structure and columns
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/check_patent_data.py

import pandas as pd

def check_patent_data():
    """Check the structure of patent data"""
    
    print("=== Patent Data Structure ===")
    
    try:
        patents = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
        
        print(f"Shape: {patents.shape}")
        print(f"Columns: {list(patents.columns)}")
        print("\nFirst few rows:")
        print(patents.head())
        
        print("\nData types:")
        print(patents.dtypes)
        
    except Exception as e:
        print(f"Error reading patent data: {e}")

if __name__ == "__main__":
    check_patent_data()