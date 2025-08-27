# ABOUTME: Stata function replications for consistent behavior with Stata code
# ABOUTME: Usage: from utils.stata_replication import fill_date_gaps, stata_lag, stata_multi_lag, stata_quantile, stata_ineq_pd, stata_ineq_pl

import pandas as pd
import numpy as np
import polars as pl
import math
import re


def fill_date_gaps(df, group_col='permno', time_col='time_avail_m'):
    """
    Fill date gaps to create a clean panel for lag operations.
    Replicates Stata: xtset [group_col] [time_col]; tsfill
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    group_col : str, default 'permno'
        Column to group by (e.g., 'permno', 'gvkey')
    time_col : str, default 'time_avail_m'
        Time column (e.g., 'time_avail_m', 'date')
    
    Returns
    -------
    pd.DataFrame
        Dataframe with date gaps filled, creating a balanced panel
        within each group's original date range
    
    Examples
    --------
    >>> df_filled = fill_date_gaps(df, 'permno', 'time_avail_m')
    >>> df_filled = fill_date_gaps(df, 'gvkey', 'datadate')
    """
    # Get all unique groups and time periods
    group_list = df[group_col].unique()
    time_list = df[time_col].unique()
    
    # Create balanced panel with all combinations
    full_idx = pd.MultiIndex.from_product([group_list, time_list], names=[group_col, time_col])
    df_balanced = df.set_index([group_col, time_col]).reindex(full_idx).reset_index()\
        .sort_values([group_col, time_col])
    
    # Keep only observations within each group's original date range
    time_ranges = df.groupby(group_col)[time_col].agg(time_min='min', time_max='max').reset_index()
    df_balanced = df_balanced.merge(time_ranges, on=group_col, how='left')
    df_balanced = df_balanced.query(f'{time_col} >= time_min & {time_col} <= time_max').drop(columns=['time_min', 'time_max'])
    
    return df_balanced.sort_values([group_col, time_col])


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


def stata_multi_lag(df, group_col, time_col, value_col, lag_list, freq='M', 
                    prefix='', fill_gaps=False):
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
        Optional prefix for column names (e.g., 'l' creates 'l12_at')
    fill_gaps : bool, default False
        Whether to fill date gaps before lagging. When True, creates balanced panel
        to ensure proper calendar-based lag alignment.
    
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
    def _validate_lag_dates(lagged_date, time_series, lag, freq):
        """Helper function to validate lag dates using calendar-based logic."""
        # Calculate expected date based on frequency
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
        
        # Convert lagged_date to datetime for comparison
        lagged_date = pd.to_datetime(lagged_date)
        
        # For monthly/quarterly/yearly frequency, compare at month level
        if freq in ['M', 'Q', 'Y']:
            lagged_period = lagged_date.dt.to_period('M')
            expected_period = expected_date.dt.to_period('M')
            valid_mask = lagged_period == expected_period
        else:
            # For daily, compare exact dates
            valid_mask = lagged_date == expected_date
        
        return valid_mask

    out = df.copy()
    
    # Fill date gaps if requested
    if fill_gaps:
        out = fill_date_gaps(out, group_col, time_col)
    
    time_series = pd.to_datetime(out[time_col])
    
    # Pre-compute groupby objects for efficiency
    grouped_value = out.groupby(group_col)[value_col]
    grouped_time = out.groupby(group_col)[time_col]
    
    # Create all lag columns
    for lag in lag_list:
        # Create lagged value and date
        lagged_value = grouped_value.shift(lag)
        lagged_date = grouped_time.shift(lag)
        
        # Validate dates using helper function
        valid_mask = _validate_lag_dates(lagged_date, time_series, lag, freq)
        
        # Set invalid lags to NaN
        result = lagged_value.where(valid_mask)
        
        # Generate column name
        if prefix:
            col_name = f'{prefix}{lag}_{value_col}'
        else:
            col_name = f'{value_col}_lag{lag}'
        
        out[col_name] = result
    
    return out.sort_values([group_col, time_col])


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
    op_map = {"=": "==", "~=": "!=", "^=": "!=", 
              **{k: k for k in (">", ">=", "<", "<=", "==", "!=")}}
    op = op_map.get(op, op)
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
        rhs_check = (rhs.is_not_null() if hasattr(rhs, 'is_not_null') 
                     else pl.lit(True))
        return e.eq(rhs) & e.is_not_null() & rhs_check
    if op == "!=":
        # If either side is null, return True (Stata behavior)
        rhs_null = (rhs.is_null() if hasattr(rhs, 'is_null') 
                    else pl.lit(False))
        return e.ne(rhs) | e.is_null() | rhs_null
    if op == ">":
        return e_inf > rhs_inf
    if op == ">=":
        return e_inf >= rhs_inf
    if op == "<":
        # Handle the complex Stata logic for less-than with nulls
        rhs_null = (rhs.is_null() if hasattr(rhs, 'is_null') 
                    else pl.lit(False))
        return (pl.when(e.is_null() & rhs_null)
                .then(pl.lit(False))
                .when(e.is_null())
                .then(pl.lit(False))
                .when(rhs_null)
                .then(pl.lit(True))
                .otherwise(e < rhs))
    if op == "<=":
        # Handle the complex Stata logic for less-than-equal with nulls
        rhs_null = (rhs.is_null() if hasattr(rhs, 'is_null') 
                    else pl.lit(False))
        return (pl.when(e.is_null() & rhs_null)
                .then(pl.lit(False))
                .when(e.is_null())
                .then(pl.lit(False))
                .when(rhs_null)
                .then(pl.lit(True))
                .otherwise(e <= rhs))
