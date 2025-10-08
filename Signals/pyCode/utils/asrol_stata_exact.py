#!/usr/bin/env python3
# ABOUTME: Stata-exact asrol implementation using population variance (N) instead of sample variance (N-1)
# ABOUTME: Provides asrol functions that match Stata's exact behavior for beta calculations

import pandas as pd
import numpy as np
from typing import Optional, Union
import polars as pl

def asrol_pl_stata(
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
    Stata-exact polars asrol that uses population variance (N) instead of sample variance (N-1)
    
    Key difference: For 'sd' statistic, uses ddof=0 (population) instead of ddof=1 (sample)
    to match Stata's default behavior where type="population"
    """
    from utils.stata_replication import fill_date_gaps_pl

    # Default column name
    if new_col_name is None:
        new_col_name = f"{stat}{window}_{value_col}"

    # Convert time column to Date for consistency
    df = df.with_columns(pl.col(time_col).cast(pl.Date))

    # Fill date gaps if requested (default behavior)
    if fill_gaps:
        df_filled = fill_date_gaps_pl(
            df,
            group_col=group_col,
            time_col=time_col,
            period_str=freq,
            start_padding="-0mo",
            end_padding="0mo",
        )
    else:
        df_filled = df.sort([group_col, time_col])

    # For standard deviation, we need custom implementation to use population variance
    if stat in ['std', 'sd']:
        # Use a simpler approach: calculate using rolling variance formula
        # rolling_var_population = E[X^2] - E[X]^2 where E uses population mean
        
        # Calculate rolling mean (population mean)
        df_filled = df_filled.with_columns([
            pl.col(value_col)
            .rolling_mean(window_size=window, min_samples=min_samples)
            .over(group_col)
            .alias('_rolling_mean')
        ])
        
        # Calculate rolling mean of squares
        df_filled = df_filled.with_columns([
            (pl.col(value_col) ** 2)
            .rolling_mean(window_size=window, min_samples=min_samples)
            .over(group_col)
            .alias('_rolling_mean_sq')
        ])
        
        # Calculate population variance: E[X^2] - (E[X])^2
        # Then take square root for standard deviation
        result = df_filled.with_columns([
            (pl.col('_rolling_mean_sq') - (pl.col('_rolling_mean') ** 2))
            .sqrt()
            .alias(new_col_name)
        ]).drop(['_rolling_mean', '_rolling_mean_sq'])
        
    else:
        # Standard rolling operations for other statistics
        rolling_ops = {
            "mean": lambda col: col.rolling_mean(
                window_size=window, min_samples=min_samples
            ),
            "sum": lambda col: col.rolling_sum(window_size=window, min_samples=min_samples),
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


def asrol_stata_exact(
    df: Union[pl.DataFrame, pd.DataFrame],
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
    Wrapper for Stata-exact asrol that handles both pandas and polars inputs.
    Uses population variance (N) instead of sample variance (N-1) for 'sd' statistic.
    """
    is_polars = isinstance(df, pl.DataFrame)
    if is_polars:
        return asrol_pl_stata(
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
        df_pl = asrol_pl_stata(
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