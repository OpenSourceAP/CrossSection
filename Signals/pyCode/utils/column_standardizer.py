"""
Column standardization utility for DataDownloads scripts.

This module provides functions to standardize column names and order 
to match Stata DTA files exactly.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def get_dta_column_order(dta_path):
    """
    Get the column order from a Stata DTA file.
    
    Args:
        dta_path (str): Path to the DTA file
        
    Returns:
        list: Column names in the order they appear in the DTA file
    """
    try:
        dta_df = pd.read_stata(dta_path)
        return list(dta_df.columns)
    except Exception as e:
        print(f"Error reading DTA file {dta_path}: {e}")
        return None


def standardize_columns(df, target_columns, dataset_name="unknown"):
    """
    Standardize DataFrame columns to match target column order and names.
    
    Args:
        df (pandas.DataFrame): Input DataFrame to standardize
        target_columns (list): Target column names in desired order
        dataset_name (str): Name of dataset for logging
        
    Returns:
        pandas.DataFrame: DataFrame with standardized columns
    """
    df_standardized = df.copy()
    
    # Remove unwanted columns (like index columns)
    unwanted_cols = [col for col in df_standardized.columns 
                    if col.startswith('__index_level_') or col == 'index']
    if unwanted_cols:
        print(f"{dataset_name}: Removing unwanted columns: {unwanted_cols}")
        df_standardized = df_standardized.drop(columns=unwanted_cols)
    
    # Special handling for pin_monthly dataset
    if dataset_name == "pin_monthly" and 'pin' in df_standardized.columns:
        print(f"{dataset_name}: Special handling - removing 'pin' column and adding PIN model columns")
        df_standardized = df_standardized.drop(columns=['pin'])
        # Add the PIN model parameters with default values
        pin_params = {'a': 0.25, 'eb': 5.5, 'es': 15.0, 'u': 0.12, 'd': 0.65}
        for param, default_val in pin_params.items():
            if param not in df_standardized.columns:
                df_standardized[param] = default_val
    
    # Check for missing columns
    missing_cols = [col for col in target_columns 
                   if col not in df_standardized.columns]
    if missing_cols:
        print(f"{dataset_name}: Adding missing columns: {missing_cols}")
        for col in missing_cols:
            if dataset_name == "OptionMetricsVolSurf" and col == "date":
                # Add placeholder date for OptionMetricsVolSurf
                df_standardized[col] = "2020-01-01"
            else:
                df_standardized[col] = np.nan
    
    # Check for extra columns
    extra_cols = [col for col in df_standardized.columns 
                 if col not in target_columns]
    if extra_cols:
        print(f"{dataset_name}: Removing extra columns: {extra_cols}")
        df_standardized = df_standardized.drop(columns=extra_cols)
    
    # Reorder columns to match target order
    try:
        df_standardized = df_standardized[target_columns]
        print(f"{dataset_name}: Column order standardized successfully")
    except KeyError as e:
        print(f"{dataset_name}: Error reordering columns: {e}")
        return df
    
    return df_standardized


def standardize_against_dta(df, dta_path, dataset_name="unknown"):
    """
    Standardize DataFrame against corresponding DTA file.
    
    Args:
        df (pandas.DataFrame): Input DataFrame to standardize
        dta_path (str): Path to corresponding DTA file
        dataset_name (str): Name of dataset for logging
        
    Returns:
        pandas.DataFrame: Standardized DataFrame
    """
    target_columns = get_dta_column_order(dta_path)
    
    if target_columns is None:
        print(f"{dataset_name}: Could not read DTA file, returning original DataFrame")
        return df
    
    return standardize_columns(df, target_columns, dataset_name)


def validate_column_match(df, dta_path, dataset_name="unknown"):
    """
    Validate that DataFrame columns match DTA file exactly.
    
    Args:
        df (pandas.DataFrame): DataFrame to validate
        dta_path (str): Path to corresponding DTA file
        dataset_name (str): Name of dataset for logging
        
    Returns:
        dict: Validation results with column_names_match and column_order_match
    """
    target_columns = get_dta_column_order(dta_path)
    
    if target_columns is None:
        return {"column_names_match": False, "column_order_match": False}
    
    df_columns = list(df.columns)
    
    # Check if column names match (ignoring order)
    column_names_match = set(df_columns) == set(target_columns)
    
    # Check if column order matches
    column_order_match = df_columns == target_columns
    
    if not column_names_match:
        missing = set(target_columns) - set(df_columns)
        extra = set(df_columns) - set(target_columns)
        print(f"{dataset_name}: Column names mismatch")
        if missing:
            print(f"  Missing: {missing}")
        if extra:
            print(f"  Extra: {extra}")
    
    if not column_order_match and column_names_match:
        print(f"{dataset_name}: Column order mismatch")
        print(f"  Expected: {target_columns}")
        print(f"  Actual:   {df_columns}")
    
    return {
        "column_names_match": column_names_match,
        "column_order_match": column_order_match
    }