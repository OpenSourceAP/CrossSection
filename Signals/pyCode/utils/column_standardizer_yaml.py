#!/usr/bin/env python3
"""
ABOUTME: Column structure enforcement module for DataDownloads scripts
ABOUTME: Uses 01_columns.yaml to enforce exact column order and data types

This module provides the standardize_columns function that enforces consistent
DataFrame column schemas and data types using the new 01_columns.yaml format.
The function performs these specific operations to ensure DataFrame compatibility:

1. COLUMN SELECTION: Keeps only the exact columns specified in the YAML structure
2. COLUMN ORDERING: Reorders columns to match the exact sequence in column_order
3. DATA TYPE ENFORCEMENT: Applies exact pandas dtypes from YAML (int32, float64, etc.)
4. MISSING COLUMNS: Adds missing columns with NaN values
5. EXTRA COLUMNS: Removes columns not in the structure
6. SPECIAL HANDLING: Handles index column cleanup

This eliminates the dependency on old column_schemas.yaml and provides exact
data type replication of Stata datasets.
"""

import os
import yaml
import pandas as pd
import numpy as np


def standardize_columns(df, dataset_name):
    """
    Enforce DataFrame column structure and data types using 01_columns.yaml.
    
    This function ensures the DataFrame has exactly the columns specified in the
    column structure, in the correct order, with exact data types matching Stata.
    
    Specific operations performed:
    - Removes columns not in the target structure
    - Adds missing columns with NaN values
    - Reorders columns to match column_order sequence
    - Enforces exact pandas dtypes (int32, float64, datetime64[ns], etc.)
    - Removes unwanted columns (index columns, __index_level_* patterns)
    
    Args:
        df (pandas.DataFrame): Input DataFrame to standardize
        dataset_name (str): Name of dataset in 01_columns.yaml (e.g.,
                           'CRSPdistributions')

    Returns:
        pandas.DataFrame: DataFrame with enforced column structure and data types
                         matching YAML definition
    """
    # Load column structure from 01_columns.yaml
    yaml_path = os.path.join(os.path.dirname(__file__), "../DataDownloads/01_columns.yaml")

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            structures = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading column structure: {e}")
        return df

    if dataset_name not in structures:
        print(f"❌ Dataset '{dataset_name}' not found in column structure")
        return df

    structure = structures[dataset_name]
    # Parse column_order (comma-separated string)
    column_order = structure.get('column_order', '')
    if isinstance(column_order, str):
        target_columns = [col.strip() for col in column_order.split(',')]
    else:
        target_columns = column_order

    print(f"{dataset_name}: Starting column standardization with data type enforcement")

    df_standardized = df.copy()

    # Remove unwanted index columns
    unwanted_cols = []
    
    # Remove columns starting with '__index_level_'
    unwanted_cols.extend([col for col in df_standardized.columns
                          if col.startswith('__index_level_')])
    
    # Remove exact 'index' column
    if 'index' in df_standardized.columns:
        unwanted_cols.append('index')

    if unwanted_cols:
        print(f"{dataset_name}: Removing unwanted columns: {unwanted_cols}")
        df_standardized = df_standardized.drop(columns=unwanted_cols)

    # Check for missing columns
    missing_cols = [col for col in target_columns
                    if col not in df_standardized.columns]
    if missing_cols:
        print(f"{dataset_name}: Adding missing columns: {missing_cols}")
        for col in missing_cols:
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

    # Apply data type enforcement from structure - one column at a time for robustness
    dtype_mappings = {
        'int8': 'int8',
        'int16': 'int16', 
        'int32': 'int32',
        'int64': 'int64',
        'float32': 'float32',
        'float64': 'float64',
        'datetime64[ns]': 'datetime64[ns]',
        'object': 'object'
    }
    
    conversion_count = 0
    for dtype_key, pandas_dtype in dtype_mappings.items():
        if dtype_key in structure:
            # Parse comma-separated column list
            dtype_columns_str = structure[dtype_key]
            if isinstance(dtype_columns_str, str):
                dtype_columns = [col.strip() for col in dtype_columns_str.split(',')]
            else:
                dtype_columns = dtype_columns_str
            
            # Apply dtype to existing columns ONE AT A TIME
            existing_dtype_cols = [col for col in dtype_columns if col in df_standardized.columns]
            for col in existing_dtype_cols:
                try:
                    # Smart type conversion based on target type
                    if pandas_dtype.startswith('int'):
                        # Handle integer conversion with NaN values
                        if df_standardized[col].isna().any():
                            # Use nullable integer types for columns with NaN
                            nullable_dtype = pandas_dtype.replace('int', 'Int')
                            df_standardized[col] = pd.to_numeric(df_standardized[col], errors='coerce').astype(nullable_dtype)
                        else:
                            # Safe integer conversion
                            df_standardized[col] = pd.to_numeric(df_standardized[col], errors='coerce').astype(pandas_dtype)
                    elif pandas_dtype.startswith('float'):
                        # Robust float conversion
                        df_standardized[col] = pd.to_numeric(df_standardized[col], errors='coerce').astype(pandas_dtype)
                    elif pandas_dtype == 'datetime64[ns]':
                        # Robust datetime conversion
                        df_standardized[col] = pd.to_datetime(df_standardized[col], errors='coerce')
                    elif pandas_dtype == 'object':
                        # Object conversion (strings)
                        df_standardized[col] = df_standardized[col].astype(str)
                    else:
                        # Fallback to direct conversion
                        df_standardized[col] = df_standardized[col].astype(pandas_dtype)
                    
                    conversion_count += 1
                    
                except Exception as e:
                    print(f"{dataset_name}: Warning - Could not convert column '{col}' to {pandas_dtype}: {e}")
                    # Continue with other columns instead of failing completely
                    
    if conversion_count > 0:
        print(f"{dataset_name}: Successfully converted {conversion_count} columns to target dtypes")

    return df_standardized