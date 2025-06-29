#!/usr/bin/env python3
"""
ABOUTME: YAML-based column standardization module for DataDownloads scripts
ABOUTME: Replaces DTA file dependencies with version-controlled YAML schemas

This module provides the yaml_standardize_columns function that standardizes
DataFrame columns using YAML schema definitions instead of reading DTA files.
This eliminates the dependency on ../Data/Intermediate/ files while producing
identical results.
"""

import os
import yaml
import pandas as pd
import numpy as np


def yaml_standardize_columns(df, dataset_name):
    """
    Standardize DataFrame columns using YAML schema instead of DTA files.

    Args:
        df (pandas.DataFrame): Input DataFrame to standardize
        dataset_name (str): Name of dataset in YAML schema

    Returns:
        pandas.DataFrame: DataFrame with standardized columns
    """
    # Load YAML schema
    yaml_path = os.path.join(os.path.dirname(__file__), "column_schemas.yaml")

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            schemas = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading YAML schema: {e}")
        return df

    if dataset_name not in schemas:
        print(f"❌ Dataset '{dataset_name}' not found in YAML schema")
        return df

    schema = schemas[dataset_name]
    target_columns = schema['columns']
    special_handling = schema.get('special_handling', {})

    print(f"{dataset_name}: Starting YAML-based column standardization")

    df_standardized = df.copy()

    # Handle PIN special case: remove PIN column and add default parameters
    pin_parameters = special_handling.get('pin_parameters', {})
    if pin_parameters:
        remove_columns = pin_parameters.get('remove_columns', [])
        add_defaults = pin_parameters.get('add_defaults', {})
        
        # Remove specified columns
        for col in remove_columns:
            if col in df_standardized.columns:
                print(f"{dataset_name}: Removing PIN column: {col}")
                df_standardized = df_standardized.drop(columns=[col])
        
        # Add default parameter values
        for param, default_value in add_defaults.items():
            if param not in df_standardized.columns:
                print(f"{dataset_name}: Adding PIN parameter {param} = {default_value}")
                df_standardized[param] = default_value

    # Remove unwanted columns based on patterns
    remove_patterns = special_handling.get('remove_patterns', [])
    unwanted_cols = []

    for pattern in remove_patterns:
        if pattern == '__index_level_*':
            # Find columns starting with '__index_level_'
            unwanted_cols.extend([col for col in df_standardized.columns
                                  if col.startswith('__index_level_')])
        elif pattern == 'index':
            # Find exact 'index' column
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
        print(f"{dataset_name}: Column order standardized successfully "
              "using YAML schema")
    except KeyError as e:
        print(f"{dataset_name}: Error reordering columns: {e}")
        return df

    return df_standardized