# ABOUTME: stata_ineq.py - Stata-compatible inequality operators with missing value handling
# ABOUTME: Provides functions that replicate Stata's treatment of missing values as positive infinity

"""
stata_ineq.py

Stata-compatible inequality operators that handle missing values according to Stata's rules:
- Missing values are treated as positive infinity in comparisons
- missing > finite = True
- finite > missing = False  
- missing > missing = False
- missing < finite = False
- finite < missing = True
- missing < missing = False

Usage:
    import pandas as pd
    import polars as pl
    from utils.stata_ineq import stata_ineq_pd, stata_ineq_pl
    
    # For pandas Series
    result = stata_ineq_pd(pd_series, ">", value)
    
    # For polars expressions
    df.with_columns([
        stata_ineq_pl(pl.col("x"), ">", pl.col("y")).alias("x_gt_y")
    ])

Functions:
    - stata_ineq_pd(s, op, rhs): Pandas Series version for x op rhs with Stata logic
    - stata_ineq_pl(e, op, rhs): Polars expression version for x op rhs with Stata logic

Note: These functions implement the exact behavior documented in DocsForClaude/traps.md
"""

import numpy as np
import pandas as pd
import polars as pl
import math
import re

# ================================
# PANDAS VERSION
# ================================

_OPMAP = {"=": "==", "~=": "!=", "^=": "!=", "==": "==", "!=": "!=", ">": ">", ">=": ">=", "<": "<", "<=": "<="}

_missing_token = re.compile(r"^\.(?:[a-z])?$")  # '.', '.a'..'.z' (collapsed)

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

# ================================
# POLARS VERSION
# ================================

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