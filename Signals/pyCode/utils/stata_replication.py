# ABOUTME: Stata function replications for consistent behavior with Stata code
# ABOUTME: Usage: from utils.stata_replication import stata_lag, stata_multi_lag, stata_quantile, stata_ineq_pd, stata_ineq_pl

import pandas as pd
import numpy as np
import polars as pl
import math
import re


def stata_quantile(x, qs):
    """
    Compute Stata-style quantiles for a 1D array-like using only NumPy.

    Parameters
    ----------
    x : array-like
        Data (numeric). NaNs are ignored.
    qs : float or sequence of floats
        Quantiles requested. May be in [0,100] (percent) or [0,1] (fractions).

    Returns
    -------
    float or np.ndarray
        Scalar if one quantile requested, else array of quantiles.
    """
    arr = np.asarray(x, dtype=float)
    arr = arr[~np.isnan(arr)]  # drop NaNs
    arr.sort(kind="mergesort")  # stable sort like Stata
    n = arr.size

    if n == 0:
        return np.nan if np.isscalar(qs) else np.full(len(np.atleast_1d(qs)), np.nan)

    qs = np.atleast_1d(qs).astype(float)
    if np.all((qs >= 0) & (qs <= 1)):
        qs = qs * 100.0

    P = (qs / 100.0) * n
    out = np.empty_like(P, dtype=float)

    for j, p in enumerate(P):
        if p <= 0:
            out[j] = arr[0]
        elif p >= n:
            out[j] = arr[-1]
        else:
            # first rank > p
            idx = np.searchsorted(np.arange(1, n + 1), p, side="right")
            val = arr[idx]
            k = int(np.floor(p + 1e-12))
            if abs(p - k) < 1e-12 and 1 <= k < n:
                val = (arr[k - 1] + arr[k]) / 2
            out[j] = val

    return float(out[0]) if out.size == 1 else out


def stata_lag(df, group_col, time_col, value_col, lag_periods, freq='M', suffix=None):
    """
    Create a single Stata-style lag using shift + date validation.
    Matches Stata's l. operator behavior with calendar-based validation.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    group_col : str
        Column to group by (e.g., 'permno')
    time_col : str
        Time column (e.g., 'time_avail_m')
    value_col : str
        Column to lag
    lag_periods : int
        Number of periods to lag
    freq : str, default 'M'
        Frequency: 'M' for monthly, 'D' for daily, 'Q' for quarterly, 'Y' for yearly
    suffix : str, optional
        Custom suffix for the output column name. If None, uses f'_lag{lag_periods}'
    
    Returns
    -------
    pd.Series
        Lagged values with NaN where date validation fails
    
    Examples
    --------
    >>> df['ret_lag12'] = stata_lag(df, 'permno', 'time_avail_m', 'ret', 12)
    >>> df['at_l12'] = stata_lag(df, 'permno', 'time_avail_m', 'at', 12, suffix='_l12')
    """
    # Sort by group and time to ensure correct ordering
    df_sorted = df.sort_values([group_col, time_col])
    
    # Create lagged value using shift
    lagged_value = df_sorted.groupby(group_col)[value_col].shift(lag_periods)
    
    # Create lagged date using shift
    lagged_date = df_sorted.groupby(group_col)[time_col].shift(lag_periods)
    
    # Calculate expected date based on frequency
    time_series = pd.to_datetime(df_sorted[time_col])
    
    if freq == 'M':
        expected_date = time_series - pd.DateOffset(months=lag_periods)
    elif freq == 'D':
        expected_date = time_series - pd.DateOffset(days=lag_periods)
    elif freq == 'Q':
        expected_date = time_series - pd.DateOffset(months=lag_periods * 3)
    elif freq == 'Y':
        expected_date = time_series - pd.DateOffset(years=lag_periods)
    else:
        raise ValueError(f"Unsupported frequency: {freq}")
    
    # Convert lagged_date to datetime for comparison
    lagged_date = pd.to_datetime(lagged_date)
    
    # For monthly/quarterly/yearly frequency, compare at month level
    if freq in ['M', 'Q', 'Y']:
        # Compare year-month only (ignore day component)
        lagged_period = lagged_date.dt.to_period('M')
        expected_period = expected_date.dt.to_period('M')
        valid_mask = lagged_period == expected_period
    else:
        # For daily, compare exact dates
        valid_mask = lagged_date == expected_date
    
    # Set invalid lags to NaN
    result = lagged_value.where(valid_mask)
    
    # Restore original index order
    result.index = df_sorted.index
    result = result.reindex(df.index)
    
    return result


def stata_multi_lag(df, group_col, time_col, value_col, lag_list, freq='M', prefix=''):
    """
    Create multiple Stata-style lags efficiently.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    group_col : str
        Column to group by (e.g., 'permno')
    time_col : str
        Time column (e.g., 'time_avail_m')
    value_col : str
        Column to lag
    lag_list : list of int
        List of lag periods (e.g., [1, 2, 3, 6, 12])
    freq : str, default 'M'
        Frequency: 'M' for monthly, 'D' for daily, 'Q' for quarterly, 'Y' for yearly
    prefix : str, default ''
        Optional prefix for column names (e.g., 'l' to create 'l1_ret' instead of 'ret_lag1')
    
    Returns
    -------
    pd.DataFrame
        Original dataframe with new lag columns added
    
    Examples
    --------
    >>> df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 6, 12])
    >>> # Creates columns: ret_lag1, ret_lag2, ret_lag3, ret_lag6, ret_lag12
    
    >>> df = stata_multi_lag(df, 'permno', 'time_avail_m', 'at', [12], prefix='l')
    >>> # Creates column: l12_at
    """
    df_result = df.copy()
    
    # Sort once for efficiency
    df_sorted = df_result.sort_values([group_col, time_col])
    sorted_index = df_sorted.index
    
    # Convert time column to datetime once
    time_series = pd.to_datetime(df_sorted[time_col])
    
    # Pre-compute all shifts at once for efficiency
    value_series = df_sorted.groupby(group_col)[value_col]
    time_group = df_sorted.groupby(group_col)[time_col]
    
    for lag in lag_list:
        # Create lagged value and date
        lagged_value = value_series.shift(lag)
        lagged_date = pd.to_datetime(time_group.shift(lag))
        
        # Calculate expected date
        if freq == 'M':
            expected_date = time_series - pd.DateOffset(months=lag)
        elif freq == 'D':
            expected_date = time_series - pd.DateOffset(days=lag)
        elif freq == 'Q':
            expected_date = time_series - pd.DateOffset(months=lag * 3)
        elif freq == 'Y':
            expected_date = time_series - pd.DateOffset(years=lag)
        else:
            raise ValueError(f"Unsupported frequency: {freq}")
        
        # Validate dates
        if freq in ['M', 'Q', 'Y']:
            lagged_period = lagged_date.dt.to_period('M')
            expected_period = expected_date.dt.to_period('M')
            valid_mask = lagged_period == expected_period
        else:
            valid_mask = lagged_date == expected_date
        
        # Set invalid lags to NaN
        result = lagged_value.where(valid_mask)
        
        # Restore original index order
        result.index = sorted_index
        result = result.reindex(df.index)
        
        # Choose column name based on prefix
        if prefix == 'l':
            col_name = f'l{lag}_{value_col}'
        elif prefix:
            col_name = f'{prefix}{lag}_{value_col}'
        else:
            col_name = f'{value_col}_lag{lag}'
        
        df_result[col_name] = result
    
    return df_result


def validate_lag_requirements(df, group_col, time_col, value_col):
    """
    Validate that the dataframe meets requirements for lag operations.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    group_col : str
        Column to group by
    time_col : str
        Time column
    value_col : str
        Column to lag
    
    Raises
    ------
    ValueError
        If any requirements are not met
    """
    # Check columns exist
    missing_cols = []
    for col in [group_col, time_col, value_col]:
        if col not in df.columns:
            missing_cols.append(col)
    
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Check time column can be converted to datetime
    try:
        pd.to_datetime(df[time_col])
    except:
        raise ValueError(f"Cannot convert {time_col} to datetime")
    
    # Check for duplicate time periods within groups
    duplicates = df.groupby([group_col, time_col]).size()
    if (duplicates > 1).any():
        dup_groups = duplicates[duplicates > 1].index.tolist()[:5]
        raise ValueError(f"Duplicate time periods found for groups (showing first 5): {dup_groups}")


# ================================
# STATA INEQUALITY FUNCTIONS
# ================================

# Stata-compatible inequality operators with missing value handling
# Provides functions that replicate Stata's treatment of missing values as positive infinity

_OPMAP = {"=": "==", "~=": "!=", "^=": "!=", "==": "==", "!=": "!=", ">": ">", ">=": ">=", "<": "<", "<=": "<="}

_missing_token = re.compile(r"^\\.(?:[a-z])?$")  # '.', '.a'..'.z' (collapsed)

def _is_missing_rhs(x):
    # Accept Stata '.' / '.a'..'.z', plus Python None/NaN
    if isinstance(x, str) and _missing_token.fullmatch(x):
        return True
    try:
        # np.isnan on non-floats raises; guard with try
        return x is None or (isinstance(x, float) and np.isnan(x))
    except Exception:
        return False

def stata_ineq_pd(s: pd.Series, op: str, rhs) -> pd.Series:
    """
    Stata-style numeric inequalities for pandas.
    - Numeric missing values (NaN) behave like Stata: greater than any number.
    - Equality/inequality treat missing like Stata: NaN == c -> False; NaN != c -> True.
    - Supports RHS 'missing' via '.', '.a'..'.z', None, or NaN (all treated the same).
    """
    op = _OPMAP.get(op, op)
    if op not in {">", ">=", "<", "<=", "==", "!="}:
        raise ValueError(f"Unsupported operator: {op}")

    # If RHS is a Stata missing token: use is-missing semantics directly
    if _is_missing_rhs(rhs):
        if op in (">", ">="):   # x >= .  <=> is missing
            return s.isna()
        if op in ("<", "<="):   # x < .   <=> not missing
            return ~s.isna()
        if op == "==":          # x == .  <=> is missing
            return s.isna()
        if op == "!=":          # x != .  <=> not missing
            return ~s.isna()

    # Regular numeric RHS: map NaN -> +inf for inequality comparisons
    s_inf = s.fillna(np.inf)

    if op == "==":  # missing never equals a number in Stata
        return s.eq(rhs) & s.notna()
    if op == "!=":  # missing is not equal to any number in Stata
        return s.ne(rhs) | s.isna()

    # Inequalities: with +inf fill, missings naturally behave as Stata wants
    if op == ">":
        return s_inf.gt(rhs)
    if op == ">=":
        return s_inf.ge(rhs)
    if op == "<":
        # Ensure missings (now +inf) don't pass a '<' check
        return s_inf.lt(rhs) & s.notna()
    if op == "<=":
        return s_inf.le(rhs) & s.notna()

def _is_missing_rhs_pl(x):
    if isinstance(x, str) and _missing_token.fullmatch(x):
        return True
    if x is None:
        return True
    try:
        return isinstance(x, float) and math.isnan(x)
    except Exception:
        return False

def stata_ineq_pl(e: pl.Expr, op: str, rhs) -> pl.Expr:
    """
    Stata-style numeric inequalities for Polars.
    - Numeric nulls behave like Stata by treating nulls as +inf for inequalities.
    - Supports RHS 'missing' via '.', '.a'..'.z', None, or NaN.
    - Handles both scalar RHS and expression RHS that might be null.
    """
    op = {"=": "==", "~=": "!=", "^=": "!=", **{k: k for k in (">", ">=", "<", "<=", "==", "!=")}}.get(op, op)
    if op not in {">", ">=", "<", "<=", "==", "!="}:
        raise ValueError(f"Unsupported operator: {op}")

    # Check if RHS is a literal missing value  
    if _is_missing_rhs_pl(rhs):
        if op in (">", ">=", "=="):
            return e.is_null()
        if op in ("<", "<="):
            return e.is_not_null()
        if op == "!=":
            return e.is_not_null()

    # Handle case where RHS might be an expression that could be null
    # Convert both sides to +inf when null for inequality comparisons
    e_inf = e.fill_null(float("inf"))
    
    # If rhs is an expression, also handle its nulls
    if hasattr(rhs, 'fill_null'):  # It's a polars expression
        rhs_inf = rhs.fill_null(float("inf"))
    else:
        rhs_inf = rhs  # It's a scalar

    if op == "==":
        # Both sides must be non-null and equal
        return e.eq(rhs) & e.is_not_null() & (rhs.is_not_null() if hasattr(rhs, 'is_not_null') else pl.lit(True))
    if op == "!=":
        # If either side is null, return True (Stata behavior)
        return e.ne(rhs) | e.is_null() | (rhs.is_null() if hasattr(rhs, 'is_null') else pl.lit(False))
    if op == ">":
        return e_inf > rhs_inf
    if op == ">=":
        return e_inf >= rhs_inf
    if op == "<":
        # Handle the complex Stata logic for less-than with nulls
        return pl.when(e.is_null() & (rhs.is_null() if hasattr(rhs, 'is_null') else pl.lit(False)))\
                 .then(pl.lit(False))\
                 .when(e.is_null())\
                 .then(pl.lit(False))\
                 .when(rhs.is_null() if hasattr(rhs, 'is_null') else pl.lit(False))\
                 .then(pl.lit(True))\
                 .otherwise(e < rhs)
    if op == "<=":
        # Handle the complex Stata logic for less-than-equal with nulls
        return pl.when(e.is_null() & (rhs.is_null() if hasattr(rhs, 'is_null') else pl.lit(False)))\
                 .then(pl.lit(False))\
                 .when(e.is_null())\
                 .then(pl.lit(False))\
                 .when(rhs.is_null() if hasattr(rhs, 'is_null') else pl.lit(False))\
                 .then(pl.lit(True))\
                 .otherwise(e <= rhs)