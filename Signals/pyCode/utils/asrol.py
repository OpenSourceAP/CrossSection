#!/usr/bin/env python3
# ABOUTME: Stata-style asrol rolling window statistics and regressions
# ABOUTME: Fast Polars implementations with consecutive period support and backward compatibility

import pandas as pd
from typing import Optional, Union
import polars as pl


def asrol_fast(
    df: Union[pl.DataFrame, pd.DataFrame], 
    group_col: str, 
    time_col: str, 
    value_col: str, 
    window: int, 
    stat: str = 'mean', 
    new_col_name: Optional[str] = None, 
    min_periods: int = 1,
    consecutive_only: bool = True
) -> Union[pl.DataFrame, pd.DataFrame]:
    """
    Fast Polars implementation of rolling statistics with consecutive period support
    
    Parameters:
    - df: DataFrame (Polars or pandas)
    - group_col: grouping variable (like permno)
    - time_col: time variable (like time_avail_m) 
    - value_col: variable to calculate rolling statistic on
    - window: window size (number of periods)
    - stat: statistic to calculate ('mean', 'sum', 'std', 'count', 'min', 'max')
    - new_col_name: name for new column (default: f'{stat}{window}_{value_col}')
    - min_periods: minimum observations required (default: 1)
    - consecutive_only: if True, only use consecutive periods like Stata (default: True)
    
    Returns:
    - DataFrame with new rolling statistic column added (same type as input)
    """
    # Determine input type for return
    is_pandas_input = isinstance(df, pd.DataFrame)
    
    # Convert to Polars if needed
    if is_pandas_input:
        df_pl = pl.from_pandas(df)
    else:
        df_pl = df.clone()
    
    # Default column name
    if new_col_name is None:
        new_col_name = f'{stat}{window}_{value_col}'
    
    # Sort by group and time for proper processing
    df_pl = df_pl.sort([group_col, time_col])
    
    if not consecutive_only:
        # Simple rolling without gap detection (faster path)
        result_pl = _simple_rolling(df_pl, group_col, value_col, window, stat, new_col_name, min_periods)
    else:
        # Stata-compatible rolling with gap detection
        result_pl = _stata_rolling(df_pl, group_col, time_col, value_col, window, stat, new_col_name, min_periods)
    
    # Return same type as input
    if is_pandas_input:
        return result_pl.to_pandas()
    else:
        return result_pl


def _simple_rolling(
    df_pl: pl.DataFrame,
    group_col: str,
    value_col: str,
    window: int,
    stat: str,
    new_col_name: str,
    min_periods: int
) -> pl.DataFrame:
    """Fast rolling without gap detection using native Polars"""
    
    # Rolling function mapping
    rolling_funcs = {
        'mean': lambda col: col.rolling_mean(window_size=window, min_periods=min_periods),
        'sum': lambda col: col.rolling_sum(window_size=window, min_periods=min_periods),
        'std': lambda col: col.rolling_std(window_size=window, min_periods=min_periods),
        'sd': lambda col: col.rolling_std(window_size=window, min_periods=min_periods),  # Alias for std
        'count': lambda col: col.is_not_null().cast(pl.Int32).rolling_sum(window_size=window, min_periods=min_periods),
        'min': lambda col: col.rolling_min(window_size=window, min_periods=min_periods),
        'max': lambda col: col.rolling_max(window_size=window, min_periods=min_periods),
        'first': lambda col: col.first()
    }
    
    if stat not in rolling_funcs:
        raise ValueError(f"Unsupported statistic: {stat}")
    
    # Apply rolling function grouped by group_col
    result = df_pl.with_columns(
        rolling_funcs[stat](pl.col(value_col)).over(group_col).alias(new_col_name)
    )
    
    return result


def _stata_rolling(
    df_pl: pl.DataFrame,
    group_col: str,
    time_col: str,
    value_col: str,
    window: int,
    stat: str,
    new_col_name: str,
    min_periods: int
) -> pl.DataFrame:
    """Stata-compatible rolling with consecutive period detection"""
    
    # Add gap detection columns
    # Check if time column is integer (like fyear, time_temp) or datetime
    time_dtype = df_pl[time_col].dtype
    if time_dtype in [pl.Int16, pl.Int32, pl.Int64, pl.UInt16, pl.UInt32, pl.UInt64]:
        # Integer time column - use simple difference for gap detection
        df_with_gaps = df_pl.with_columns([
            pl.col(time_col).diff().over(group_col).alias("_days_diff"),
            pl.lit(0).alias("_segment_id")
        ])
        gap_threshold = 1  # Gap if difference > 1 for integer time
    else:
        # DateTime time column - use days difference
        df_with_gaps = df_pl.with_columns([
            pl.col(time_col).diff().dt.total_days().over(group_col).alias("_days_diff"),
            pl.lit(0).alias("_segment_id")
        ])
        gap_threshold = 90  # Gap if difference > 90 days for datetime
    
    # Identify breaks and create segment IDs
    df_with_gaps = df_with_gaps.with_columns([
        # Mark where gaps occur using dynamic threshold
        pl.when(pl.col("_days_diff") > gap_threshold)
        .then(1)
        .otherwise(0)
        .alias("_is_break")
    ])
    
    # Create cumulative segment IDs within each group
    df_with_gaps = df_with_gaps.with_columns([
        pl.col("_is_break").cum_sum().over(group_col).alias("_segment_id")
    ])
    
    # Create combined grouping key: (group_col, segment_id)
    df_with_gaps = df_with_gaps.with_columns([
        pl.concat_str([
            pl.col(group_col).cast(pl.Utf8),
            pl.lit("_seg_"),
            pl.col("_segment_id").cast(pl.Utf8)
        ]).alias("_group_segment")
    ])
    
    # Rolling function mapping
    rolling_funcs = {
        'mean': lambda col: col.rolling_mean(window_size=window, min_periods=min_periods),
        'sum': lambda col: col.rolling_sum(window_size=window, min_periods=min_periods),
        'std': lambda col: col.rolling_std(window_size=window, min_periods=min_periods),
        'sd': lambda col: col.rolling_std(window_size=window, min_periods=min_periods),  # Alias for std
        'count': lambda col: col.is_not_null().cast(pl.Int32).rolling_sum(window_size=window, min_periods=min_periods),
        'min': lambda col: col.rolling_min(window_size=window, min_periods=min_periods),
        'max': lambda col: col.rolling_max(window_size=window, min_periods=min_periods),
        'first': lambda col: col.first()
    }
    
    if stat not in rolling_funcs:
        raise ValueError(f"Unsupported statistic: {stat}")
    
    # Apply rolling function to consecutive segments
    result = df_with_gaps.with_columns(
        rolling_funcs[stat](pl.col(value_col)).over("_group_segment").alias(new_col_name)
    )
    
    # Clean up temporary columns
    result = result.drop(["_days_diff", "_is_break", "_segment_id", "_group_segment"])
    
    return result


# Backward compatibility aliases
def asrol(*args, **kwargs):
    """Alias for asrol_fast for backward compatibility"""
    return asrol_fast(*args, **kwargs)

def asrol_fast_calendar(*args, **kwargs):
    """Alias for asrol_calendar for backward compatibility"""
    return asrol_calendar(*args, **kwargs)

#%% asrol_calendar

def asrol_calendar(
    df: pl.DataFrame, 
    group_col: str, 
    date_col: str, 
    value_col: str, 
    stat: str = 'mean',
    window: str = '12mo', 
    min_obs: int = 1,
    require_prev_obs: bool = False,
    ) -> pl.DataFrame:
    """
    hand built polars asrol that 
      - constructs windows based a date duration
      - replaces with na if there are not enough observations in the window
    input: polars dataframe
    output: polars dataframe with a new column
    requires_prev_obs seems like it helps fit in a minority of cases, but in most cases it actually hurts. I left it in here for documentation to say we tried to match the stata.
    Created after asrol_fast. Made from painstakingly testing MS.py.
    """

    # grab the stat function
    stat_dict = {'mean': pl.mean, 'std': pl.std, 'min': pl.min, 'max': pl.max, 'sum': pl.sum}
    stat_fun = stat_dict[stat]

    # First, add previous observation information to the original dataframe if require_prev_obs is True
    df_with_prev = df.sort(pl.col([group_col, date_col]))
    if require_prev_obs:
        df_with_prev = df_with_prev.with_columns([
            # Add columns for previous observation check
            pl.col(date_col).shift(1).over(group_col).alias('prev_date'),
            pl.col(value_col).shift(1).over(group_col).alias('prev_value')
        ]).with_columns([
            # Check if previous date is exactly 1 month before (accounting for varying month lengths)
            (((pl.col('prev_date') + pl.duration(days=31)) >= pl.col(date_col)) &
            ((pl.col('prev_date') + pl.duration(days=27)) <= pl.col(date_col)) &
            pl.col('prev_value').is_not_null()).alias('has_valid_prev_obs')
        ])

    df_addition = df_with_prev.with_columns(
        pl.col([group_col, date_col]).set_sorted()
    ).rolling(index_column=date_col, period=window, group_by=group_col).agg(
        [
            pl.last(value_col).alias(f'{value_col}_last'),
            stat_fun(value_col).alias(f'{value_col}_{stat}'),
            pl.count(value_col).alias(f'{value_col}_obs')
        ] + ([pl.last('has_valid_prev_obs').alias('has_valid_prev_obs')] if require_prev_obs else [])
    )
    
    # Apply the final condition based on min_obs and require_prev_obs
    if require_prev_obs:
        df_addition = df_addition.with_columns(
            pl.when(
                (pl.col(f'{value_col}_obs') >= min_obs) & pl.col('has_valid_prev_obs')
            ).then(pl.col(f'{value_col}_{stat}'))
            .otherwise(pl.lit(None))
            .alias(f'{value_col}_{stat}')
        )
    else:
        df_addition = df_addition.with_columns(
            pl.when(
                pl.col(f'{value_col}_obs') >= min_obs
            ).then(pl.col(f'{value_col}_{stat}'))
            .otherwise(pl.lit(None))
            .alias(f'{value_col}_{stat}')
        )

    return df.join(
        df_addition.select([group_col, date_col, f'{value_col}_{stat}']),
        on=[group_col, date_col],
        how='left',
        coalesce=True
    )


def asrol_calendar_pd(
    df: pd.DataFrame, 
    group_col: str, 
    date_col: str, 
    value_col: str, 
    stat: str = 'mean',
    window: str = '12mo', 
    min_obs: int = 1,
    require_prev_obs: bool = False,
    ) -> pd.DataFrame:
    """
    Pandas wrapper for asrol_calendar function.
    Converts pandas DataFrame to polars, applies asrol_calendar, then converts back.
    
    Parameters:
    - df: pandas DataFrame
    - group_col: grouping variable (like permno)
    - date_col: date column (like time_avail_m)
    - value_col: variable to calculate rolling statistic on
    - stat: statistic to calculate ('mean', 'sum', 'std', 'count', 'min', 'max')
    - window: window duration (e.g., '12mo', '24mo', '6mo')
    - min_obs: minimum observations required in window (default: 1)
    - require_prev_obs: require previous observation (default: False)
    
    Returns:
    - pandas DataFrame with new rolling statistic column added
    """
    # Convert pandas to polars
    df_pl = pl.from_pandas(df)
    
    # Apply asrol_calendar
    result_pl = asrol_calendar(
        df_pl, 
        group_col, 
        date_col, 
        value_col, 
        stat, 
        window, 
        min_obs, 
        require_prev_obs
    )
    
    # Convert back to pandas
    return result_pl.to_pandas()
