#!/usr/bin/env python3
# ABOUTME: Stata-style asrol rolling window statistics and regressions
# ABOUTME: Fast Polars implementations with consecutive period support and backward compatibility

import pandas as pd
from typing import Union
import polars as pl


def asrol_pl(
    df: pl.DataFrame,
    group_col: str,
    time_col: str,
    freq: str,
    window: int,
    value_col: str,
    stat: str,
    new_col_name: str = None,
    min_samples: int = 1,
    fill_gaps: bool = True,
) -> pl.DataFrame:
    """
    Simple polars-only asrol that uses fill_date_gaps for calendar-aware rolling.

    Parameters:
    - df: Polars DataFrame
    - group_col: grouping variable (like permno)
    - time_col: time variable (like time_avail_m)
    - value_col: variable to calculate rolling statistic on
    - window: window size (number of periods)
    - stat: statistic to calculate ('mean', 'sum', 'std', 'count', 'min', 'max')
    - new_col_name: name for new column (default: f'{stat}{window}_{value_col}')
    - min_samples: minimum observations required (default: 1)
    - fill_gaps: whether to fill date gaps before rolling (default: True)
    - freq: frequency for date gap filling (default: '1mo')

    Returns:
    - Polars DataFrame with new rolling statistic column added
    """
    from utils.stata_replication import fill_date_gaps_pl

    # Default column name
    if new_col_name is None:
        new_col_name = f"{stat}{window}_{value_col}"

    # Convert time column to Date for consistency
    df = df.with_columns(pl.col(time_col).cast(pl.Date))

    # Fill date gaps if requested (default behavior)
    if fill_gaps:
        # Fill gaps to create complete panel
        df_filled = fill_date_gaps_pl(
            df,
            group_col=group_col,
            time_col=time_col,
            period_str=freq,
            start_padding="-0mo",
            end_padding="0mo",
        )
    else:
        # Just sort without filling gaps
        df_filled = df.sort([group_col, time_col])

    # Define rolling operations using native polars functions
    rolling_ops = {
        "mean": lambda col: col.rolling_mean(
            window_size=window, min_samples=min_samples
        ),
        "sum": lambda col: col.rolling_sum(window_size=window, min_samples=min_samples),
        "std": lambda col: col.rolling_std(window_size=window, min_samples=min_samples),
        "sd": lambda col: col.rolling_std(window_size=window, min_samples=min_samples),
        "min": lambda col: col.rolling_min(window_size=window, min_samples=min_samples),
        "max": lambda col: col.rolling_max(window_size=window, min_samples=min_samples),
        "count": lambda col: col.is_not_null()
        .cast(pl.Int32)
        .rolling_sum(window_size=window, min_samples=min_samples),
    }

    if stat not in rolling_ops:
        raise ValueError(
            f"Unsupported statistic: {stat}. Supported: {list(rolling_ops.keys())}"
        )

    # Apply rolling operation grouped by group_col
    result = df_filled.with_columns(
        rolling_ops[stat](pl.col(value_col)).over(group_col).alias(new_col_name)
    )

    return result


def asrol(
    df: pl.DataFrame,
    group_col: str,
    time_col: str,
    freq: str,
    window: int,
    value_col: str,
    stat: str,
    new_col_name: str = None,
    min_samples: int = 1,
    fill_gaps: bool = True,
) -> Union[pl.DataFrame, pd.DataFrame]:
    """
    Wrapper for asrol_pl that handles both pandas and polars inputs.

    For pandas input: converts to polars, applies asrol_pl, converts back.
    For polars input: directly calls asrol_pl.

    Parameters:
    - df: DataFrame (Polars or pandas)
    """
    is_polars = isinstance(df, pl.DataFrame)
    if is_polars:
        return asrol_pl(
            df,
            group_col,
            time_col,
            freq,
            window,
            value_col,
            stat,
            new_col_name,
            min_samples,
            fill_gaps,
        )
    else:
        df_pl = pl.from_pandas(df)
        df_pl = asrol_pl(
            df_pl,
            group_col,
            time_col,
            freq,
            window,
            value_col,
            stat,
            new_col_name,
            min_samples,
            fill_gaps,
        )
        return df_pl.to_pandas()
