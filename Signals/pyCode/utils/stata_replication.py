# ABOUTME: Stata function replications for consistent behavior with Stata code
# ABOUTME: Usage: from utils.stata_replication import fill_date_gaps, stata_lag, stata_multi_lag, stata_quantile, stata_ineq_pd, stata_ineq_pl, relrank
# These functions are in principle not necessary. But if we want to exactly replicate the Stata code, we should try to use them.

import pandas as pd
import numpy as np
import polars as pl
import math
import re

# %% stata_multi_lag functions

def stata_multi_lag_pd(df, group_col, time_col, value_col, lag_list, freq='M', prefix='', fill_gaps=True):
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
        (Note: freq parameter kept for compatibility but gaps are always filled)
    prefix : str, default ''
        Optional prefix for column names (e.g., 'l' creates 'l12_at')
    
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

    if fill_gaps:
        # By default, fill date gaps to ensure proper calendar-based lag alignment
        out = fill_date_gaps(df, group_col, time_col)
    else:
        # In special cases, skip filling gaps (e.g. to save time)
        out = df
    
    # Sort by group and time
    out = out.sort_values([group_col, time_col])
    
    # Create all lag columns using simple shifts
    grouped_value = out.groupby(group_col)[value_col]
    
    for lag in lag_list:
        # Generate column name
        if prefix:
            col_name = f'{prefix}{lag}_{value_col}'
        else:
            col_name = f'{value_col}_lag{lag}'
        
        # Simple shift operation - works correctly because gaps are filled
        out[col_name] = grouped_value.shift(lag)
    
    return out
    
def stata_multi_lag_pl(df, group_col='permno', time_col='time_avail_m', value_col=['act', 'che'], lag_list=[1, 2], freq='M', prefix='', fill_gaps=True):
    """
    Create multiple Stata-style lags efficiently (Polars version).
    
    Parameters
    ----------
    df : pl.DataFrame
        Input dataframe
    group_col : str
        Column to group by (e.g., 'permno')
    time_col : str
        Time column (e.g., 'time_avail_m')
    value_col : list of str
        Columns to lag
    lag_list : list of int
        List of lag periods (e.g., [1, 2, 3, 6, 12])
    freq : str, default 'M'
        Frequency: 'M' for monthly, 'D' for daily, 'Q' for quarterly, 'Y' for yearly
    prefix : str, default ''
        Optional prefix for column names (e.g., 'l' creates 'l12_at')
    fill_gaps : bool, default True
        Whether to fill date gaps before lagging
    
    Returns
    -------
    pl.DataFrame
        Original dataframe with new lag columns added
    """
    # Convert freq to period_str for fill_date_gaps
    freq_map = {'M': '1mo', 'D': '1d', 'Q': '3mo', 'Y': '1y'}
    period_str = freq_map.get(freq, '1mo')
    
    if fill_gaps:
        df = fill_date_gaps_pl(df, group_col, time_col, period_str)
    else:
        df = df.with_columns(pl.col(time_col).cast(pl.Date))

    df = df.sort([group_col, time_col])
    # Create all lag columns using shift operations
    for v in value_col:
        for lag in lag_list:
            # Generate column name to match pandas version
            if prefix:
                col_name = f'{prefix}{lag}_{v}'
            else:
                col_name = f'{v}_lag{lag}'
            
            df = df.with_columns(
                pl.col(v).shift(lag).over(group_col).alias(col_name)
            )
    
    return df

def stata_multi_lag(df, group_col, time_col, value_col, lag_list, freq='M', prefix='', fill_gaps=True):
    """
    Create multiple Stata-style lags efficiently (unified wrapper).
    
    Automatically detects DataFrame type and calls appropriate implementation.
    
    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        Input dataframe
    group_col : str
        Column to group by (e.g., 'permno')
    time_col : str
        Time column (e.g., 'time_avail_m')
    value_col : str or list of str
        Column(s) to lag. Single string for pandas, list for polars
    lag_list : list of int
        List of lag periods (e.g., [1, 2, 3, 6, 12])
    freq : str, default 'M'
        Frequency: 'M' for monthly, 'D' for daily, 'Q' for quarterly, 'Y' for yearly
    prefix : str, default ''
        Optional prefix for column names (e.g., 'l' creates 'l12_at')
    fill_gaps : bool, default True
        Whether to fill date gaps before lagging
    
    Returns
    -------
    pd.DataFrame or pl.DataFrame
        Original dataframe with new lag columns added
    """
    if isinstance(df, pl.DataFrame):
        # Ensure value_col is a list for polars version
        if isinstance(value_col, str):
            value_col = [value_col]
        return stata_multi_lag_pl(df, group_col, time_col, value_col, lag_list, freq, prefix, fill_gaps)
    elif isinstance(df, pd.DataFrame):
        # Ensure value_col is a string for pandas version  
        if isinstance(value_col, list):
            if len(value_col) != 1:
                raise ValueError("Pandas version only supports single value_col. Use stata_multi_lag_pl directly for multiple columns.")
            value_col = value_col[0]
        return stata_multi_lag_pd(df, group_col, time_col, value_col, lag_list, freq, prefix, fill_gaps)
    else:
        raise TypeError(f"Unsupported DataFrame type: {type(df)}. Expected pd.DataFrame or pl.DataFrame.")
    
# %% fill_date_gaps


def fill_date_gaps(df, group_col='permno', time_col='time_avail_m', period_str='1mo', 
    start_padding="-0mo", end_padding="0mo"):
    """
    Fill date gaps to create a clean panel for lag operations.
    Replicates Stata: xtset [group_col] [time_col]; tsfill

    General pandas/polars wrapper on fill_date_gaps_pl
    
    df: pd.DataFrame or pl.DataFrame
    period_str: 1mo
    start_padding: 0mo, 3mo, 6mo, 12mo
    end_padding: -0mo, -3mo, -6mo, -12mo: adds 0, 3, 6, 12 months to the start of the time series
    """

    # polars path
    if isinstance(df, pl.DataFrame):
        return fill_date_gaps_pl(df, group_col, time_col, period_str, start_padding, end_padding)
    
    # pandas path
    elif isinstance(df, pd.DataFrame):
        # convert to polars
        out = pl.from_pandas(df)
        out = fill_date_gaps_pl(out, group_col, time_col, period_str, start_padding, end_padding)
        return out.to_pandas()


def fill_date_gaps_pl(df, group_col='permno', time_col='time_avail_m', period_str='1mo', 
    start_padding="-0mo", end_padding="0mo"):
    """
    Fill date gaps to create a clean panel for lag operations.
    Replicates Stata: xtset [group_col] [time_col]; tsfill
    
    period_str: 1mo
    start_padding: 0mo, 3mo, 6mo, 12mo
    end_padding: -0mo, -3mo, -6mo, -12mo: adds 0, 3, 6, 12 months to the start of the time series
    """

    # force time_col to be a date
    df = df.with_columns(pl.col(time_col).cast(pl.Date))
    
    # create a backbone of group-time with no gaps
    out = df.group_by(group_col).agg(
            pl.col(time_col).min().alias("time_min"),
            pl.col(time_col).max().alias("time_max")
        ).with_columns(
            pl.date_ranges(
                pl.col("time_min").dt.offset_by(start_padding), 
                pl.col("time_max").dt.offset_by(end_padding),
                period_str).alias(time_col)
        ).explode(time_col).select(
            [group_col, time_col]
        )

    # merge input onto backbone and sort
    out = out.join(df, on=[group_col, time_col], how="left")
    out = out.sort([group_col, time_col])

    return out


#%% Replicating Other Stata Functions


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


def relrank(df: pd.DataFrame, value_col: str, by, out: str | None = None) -> pd.Series | pd.DataFrame:
    """
    Pandas equivalent of Stata:
        by <byvars>: relrank <value_col>, gen(<out>) ref(<value_col>)

    Behavior:
    - Computes the empirical CDF / relative rank of `value_col` within each group `by`.
    - Ties get the same value (average rank), matching Stata `cumul, equal`.
    - Output is in (0, 1]; singleton groups yield 1.0.
    - Missing values in `value_col` => NaN in the result (Stata sets missing when ref is missing).

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    value_col : str
        Column to rank; this is both the "value" and the "reference" (ref(value_col)).
    by : str | list[str]
        Grouping columns (Stata's `by:`). Can be a column name or list of names.
    out : str | None, default None
        If provided, writes the result to `df[out]` and returns the DataFrame.
        If None, returns a Series aligned to `df.index`.

    Returns
    -------
    pd.Series | pd.DataFrame
        Series of relative ranks (if out is None) or the mutated DataFrame (if out is a string).

    Notes
    -----
    - This mirrors Stata's `relrank` used as:
        by <byvars>: relrank v, gen(newv) ref(v)
      which internally calls `cumul` with `equal` tie handling.
    - Implementation detail:
        We use pandas' `rank(method="average", pct=True)` within each group.
        See docs:
        * pandas.Series.rank: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rank.html
        * pandas.GroupBy: https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html

    Examples
    --------
    # Stata:
    # by tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
    # Python (pandas):
    # df = relrank(df, "mve_c", by=["tempFF48", "time_avail_m"], out="tempRK")

    # Stata loop:
    # foreach v of varlist SG BM AOP LTG {
    #     by time_avail_m: relrank `v', gen(rank`v') ref(`v')
    # }
    # Python (pandas):
    # for v in ["SG","BM","AOP","LTG"]:
    #     df = relrank(df, v, by="time_avail_m", out=f"rank{v}")
    """
    # Group and compute percentile ranks with average tie handling (Stata: cumul, equal)
    # pct=True returns rank / group_size -> values in (0, 1]
    ranks = (
        df.groupby(by, dropna=False, sort=False)[value_col]
          .rank(method="average", pct=True)
    )

    # pandas already yields NaN for rows where value_col is NaN,
    # which matches Stata relrank setting generated value to missing if ref is missing.
    if out is not None:
        df[out] = ranks
        return df
    return ranks
