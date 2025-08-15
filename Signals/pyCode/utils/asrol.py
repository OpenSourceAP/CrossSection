# ABOUTME: Utility functions for data processing, especially Stata translations
# ABOUTME: Contains asrol function equivalent to Stata's asrol command

import pandas as pd
import numpy as np

def stata_asrol(df, group_col, time_col, value_col, window, stat='mean', new_col_name=None, min_periods=1):
    """
    Stata-compatible asrol that respects consecutive periods
    
    Key difference: Only calculates rolling statistics within consecutive
    time periods, never across data gaps (>35 days).
    
    Parameters:
    - df: DataFrame
    - group_col: grouping variable (like permno)
    - time_col: time variable (like time_avail_m) 
    - value_col: variable to calculate rolling statistic on
    - window: window size (number of periods)
    - stat: statistic to calculate ('mean', 'sum', 'std', 'count', etc.)
    - new_col_name: name for new column (default: f'{stat}{window}_{value_col}')
    - min_periods: minimum observations required (default: 1)
    
    Returns:
    - DataFrame with new rolling statistic column added
    """
    if new_col_name is None:
        new_col_name = f'{stat}{window}_{value_col}'
    
    # Sort by group and time
    df = df.sort_values([group_col, time_col]).copy()
    
    # Initialize result column
    df[new_col_name] = np.nan
    
    # Create a mapping for rolling functions to avoid repeated if-elif chains
    stat_functions = {
        'mean': lambda x: x.rolling(window=window, min_periods=min_periods).mean(),
        'sum': lambda x: x.rolling(window=window, min_periods=min_periods).sum(),
        'std': lambda x: x.rolling(window=window, min_periods=min_periods).std(),
        'count': lambda x: x.rolling(window=window, min_periods=min_periods).count(),
        'min': lambda x: x.rolling(window=window, min_periods=min_periods).min(),
        'max': lambda x: x.rolling(window=window, min_periods=min_periods).max()
    }
    
    if stat not in stat_functions:
        raise ValueError(f"Unsupported statistic: {stat}")
    
    stat_func = stat_functions[stat]
    
    # Process each group separately using groupby for better performance
    def process_group(group_data):
        if len(group_data) == 0:
            return group_data
        
        # Calculate time differences to identify breaks
        group_data = group_data.sort_values(time_col)
        time_diff = group_data[time_col].diff().dt.days
        
        # Find break points where gap > 90 days (Stata tolerance for rolling calculations)
        breaks = np.where(time_diff > 90)[0]
        
        # Create segments
        start_indices = np.concatenate([[0], breaks])
        end_indices = np.concatenate([breaks - 1, [len(group_data) - 1]])
        
        # Process each consecutive segment
        result_values = np.full(len(group_data), np.nan)
        
        for start_idx, end_idx in zip(start_indices, end_indices):
            if end_idx >= start_idx:  # Valid segment
                segment_data = group_data.iloc[start_idx:end_idx+1]
                rolling_result = stat_func(segment_data[value_col])
                result_values[start_idx:end_idx+1] = rolling_result.values
        
        group_data[new_col_name] = result_values
        return group_data
    
    # Apply to each group - suppress the FutureWarning
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        result = df.groupby(group_col, group_keys=False).apply(process_group)
    
    return result

def asrol(df, group_col, time_col, value_col, window, stat='mean', new_col_name=None, min_periods=1, consecutive_only=True):
    """
    Python equivalent of Stata's asrol command for rolling statistics
    
    Parameters:
    - df: DataFrame
    - group_col: grouping variable (like permno)
    - time_col: time variable (like time_avail_m) 
    - value_col: variable to calculate rolling statistic on
    - window: window size (number of periods)
    - stat: statistic to calculate ('mean', 'sum', 'std', 'count', etc.)
    - new_col_name: name for new column (default: f'{stat}{window}_{value_col}')
    - min_periods: minimum observations required (default: 1)
    - consecutive_only: if True, only use consecutive periods like Stata (default: True)
    
    Returns:
    - DataFrame with new rolling statistic column added
    """
    if consecutive_only:
        # Use Stata-compatible method that respects consecutive periods
        return stata_asrol(df, group_col, time_col, value_col, window, stat, new_col_name, min_periods)
    
    # Original pandas method (allows gaps)
    if new_col_name is None:
        new_col_name = f'{stat}{window}_{value_col}'
    
    # Sort by group and time
    df = df.sort_values([group_col, time_col])
    
    # Apply rolling statistic by group
    if stat == 'mean':
        df[new_col_name] = df.groupby(group_col)[value_col].rolling(
            window=window, min_periods=min_periods
        ).mean().reset_index(level=0, drop=True)
    elif stat == 'sum':
        df[new_col_name] = df.groupby(group_col)[value_col].rolling(
            window=window, min_periods=min_periods
        ).sum().reset_index(level=0, drop=True)
    elif stat == 'std':
        df[new_col_name] = df.groupby(group_col)[value_col].rolling(
            window=window, min_periods=min_periods
        ).std().reset_index(level=0, drop=True)
    elif stat == 'count':
        df[new_col_name] = df.groupby(group_col)[value_col].rolling(
            window=window, min_periods=min_periods
        ).count().reset_index(level=0, drop=True)
    elif stat == 'min':
        df[new_col_name] = df.groupby(group_col)[value_col].rolling(
            window=window, min_periods=min_periods
        ).min().reset_index(level=0, drop=True)
    elif stat == 'max':
        df[new_col_name] = df.groupby(group_col)[value_col].rolling(
            window=window, min_periods=min_periods
        ).max().reset_index(level=0, drop=True)
    else:
        raise ValueError(f"Unsupported statistic: {stat}")
    
    return df