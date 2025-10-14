# ABOUTME: forward_fill.py - utility to forward-fill missing quarterly data to match Stata behavior
# ABOUTME: Implements Stata's missing value handling logic for quarterly financial data

"""
forward_fill.py

This module provides utilities to forward-fill missing quarterly financial data
to replicate Stata's behavior when quarterly fields (ceqq, atq, etc.) are missing.

Usage:
    from utils.forward_fill import forward_fill_quarterly
    df = forward_fill_quarterly(df, fill_columns=['ceqq', 'atq'], group_col='gvkey')
"""

import pandas as pd
import polars as pl

def forward_fill_quarterly(df, fill_columns, group_col='gvkey', time_col='time_avail_m', method='last_valid'):
    """
    Forward-fill missing quarterly data to match Stata's behavior.
    
    Args:
        df: Polars DataFrame with quarterly data
        fill_columns: List of column names to forward-fill
        group_col: Column to group by (usually 'gvkey')
        time_col: Time column name
        method: Forward-fill method ('last_valid' for most recent non-null value)
    
    Returns:
        Polars DataFrame with forward-filled missing values
    """
    
    print(f"Forward-filling missing values in columns: {fill_columns}")
    
    # Convert to pandas for easier forward-fill operations
    df_pd = df.to_pandas()
    
    # Sort by group and time for proper forward-fill
    df_pd = df_pd.sort_values([group_col, time_col])
    
    # Forward-fill missing values within each group
    for col in fill_columns:
        if col in df_pd.columns:
            # Use pandas forward-fill (ffill) within groups
            df_pd[col] = df_pd.groupby(group_col)[col].ffill()
            print(f"  Forward-filled {col}: {df_pd[col].isna().sum()} remaining nulls")
    
    # Convert back to polars
    return pl.from_pandas(df_pd)

def apply_quarterly_fill_to_compustat(df, quarterly_columns=None):
    """
    Apply forward-fill logic specifically for Compustat quarterly data.
    
    Args:
        df: Polars DataFrame with Compustat data
        quarterly_columns: List of quarterly columns to fill (auto-detect if None)
    
    Returns:
        Polars DataFrame with forward-filled quarterly data
    """
    
    if quarterly_columns is None:
        # Common quarterly columns that benefit from forward-fill
        quarterly_columns = ['ceqq', 'atq', 'ltq', 'seqq', 'pstkq', 'txditcq']
        # Only include columns that exist in the dataframe
        quarterly_columns = [col for col in quarterly_columns if col in df.columns]
    
    if not quarterly_columns:
        print("No quarterly columns found to forward-fill")
        return df
    
    return forward_fill_quarterly(df, quarterly_columns, group_col='gvkey')