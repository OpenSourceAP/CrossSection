#!/usr/bin/env python3
# ABOUTME: Consolidated module containing all asreg and asrol functions for Stata replication
# ABOUTME: Combines fast polars implementations with pandas-based alternatives for complete coverage

import numpy as np
import pandas as pd
from collections import deque
from typing import List, Dict, Tuple, Optional, Sequence, Iterable, Literal, Union
import fnmatch
import warnings
import polars as pl

# Import stata_quantile from the consolidated stata_replication module
from .stata_replication import stata_quantile

try:
    import polars_ols as pls  # registers .least_squares on pl.Expr
except ImportError:
    pls = None

Mode = Literal["rolling", "expanding", "group"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

# stata_quantile is now imported from stata_replication.py
# The original function definition has been moved there

def _expand_columns(df: pd.DataFrame, X: str | Sequence[str]) -> List[str]:
    """
    Expand a list of RHS columns. If X is a string with wildcards, match df columns.
    Keeps the DataFrame's column order.
    """
    if isinstance(X, str):
        # Allow comma or whitespace separated patterns; simplest is a single pattern
        patterns = [p for p in [t.strip() for t in X.replace(",", " ").split()] if p]
        if not patterns:
            raise ValueError("X pattern is empty.")
        out: List[str] = []
        for col in df.columns:
            if any(fnmatch.fnmatch(col, pat) for pat in patterns):
                out.append(col)
        if not out:
            raise ValueError(f"No columns match pattern(s): {patterns}")
        return out
    else:
        # Respect DF order for provided names
        name_set = set(X)
        return [c for c in df.columns if c in name_set]


def _solve_ols_from_crossmoments(
    Sxx: np.ndarray,
    Sxy: np.ndarray,
    Syy: float,
    Sy: float,
    nobs: int,
    *,
    compute_se: bool,
    add_constant: bool,
    rtol: float | None = None,
) -> Tuple[np.ndarray | None, np.ndarray | None, Dict[str, float | int]]:
    """
    Solve OLS given cross-moments for a single window.

    Parameters
    ----------
    Sxx : (p,p) ndarray = X'X
    Sxy : (p,)  ndarray = X'y
    Syy : scalar           sum(y^2)
    Sy  : scalar           sum(y)
    nobs : int             number of observations in the window
    compute_se : bool      whether to compute conventional SEs (needs invertible Sxx)
    add_constant : bool    whether X included a constant column (affects TSS/R^2)
    rtol : float | None    tolerance for rank (used in lstsq fallback)

    Returns
    -------
    beta : (p,) or None
    se   : (p,) or None
    meta : dict with rank, rss, tss, r2, adj_r2, sigma
    """
    p = Sxx.shape[0]
    beta = None
    se = None

    # Try fast Cholesky first (requires SPD -> full column rank)
    rank = p
    try:
        L = np.linalg.cholesky(Sxx)
        # Solve Sxx * beta = Sxy via two triangular solves
        beta = np.linalg.solve(L.T, np.linalg.solve(L, Sxy))

        # RSS via identity: RSS = Syy - 2*b'Sxy + b'Sxx b
        rss = float(Syy - 2.0 * beta.dot(Sxy) + beta.dot(Sxx.dot(beta)))
        if rss < 0 and rss > -1e-10:  # guard tiny negatives
            rss = 0.0

        # TSS around the mean when constant is present; else around zero
        if add_constant and nobs > 0:
            tss = float(Syy - (Sy * Sy) / nobs)
            if tss < 0 and tss > -1e-10:
                tss = 0.0
        else:
            tss = float(Syy)

        if compute_se:
            # Inverse via Cholesky (solve for identity)
            I = np.eye(p, dtype=Sxx.dtype)
            Sxx_inv = np.linalg.solve(L.T, np.linalg.solve(L, I))
            dof = max(nobs - rank, 0)
            sigma2 = float(rss / dof) if dof > 0 else np.nan
            se = np.sqrt(np.maximum(np.diag(Sxx_inv), 0.0) * sigma2)
        else:
            dof = max(nobs - rank, 0)
            sigma2 = float(rss / dof) if dof > 0 else np.nan

        r2 = np.nan if tss <= 0 else (1.0 - rss / tss)
        adj_r2 = np.nan
        if nobs > 1 and nobs > rank and tss > 0:
            adj_r2 = 1.0 - (1.0 - r2) * (nobs - 1) / (nobs - rank)

        meta = {
            "rank": rank,
            "rss": rss,
            "tss": tss,
            "r2": r2,
            "adj_r2": adj_r2,
            "sigma": (
                float(np.sqrt(sigma2)) if sigma2 == sigma2 else np.nan
            ),  # sqrt if finite
        }
        return beta, se, meta
    except np.linalg.LinAlgError:
        # Fall back to SVD-based least squares (works for singular Sxx too)
        pass

    # LSTSQ fallback (may be rank-deficient)
    rcond = rtol if rtol is not None else None  # let numpy choose default
    beta_lstsq, resid, fallback_rank, svals = np.linalg.lstsq(Sxx, Sxy, rcond=rcond)
    rank = int(fallback_rank)

    # If not full column rank, treat as unusable for asreg (Stata-like conservative)
    # Caller will decide to output NaNs for the window when rank < p.
    # Compute RSS anyway (for completeness), using the same identity:
    rss = float(Syy - 2.0 * beta_lstsq.dot(Sxy) + beta_lstsq.dot(Sxx.dot(beta_lstsq)))
    if rss < 0 and rss > -1e-10:
        rss = 0.0

    if add_constant and nobs > 0:
        tss = float(Syy - (Sy * Sy) / nobs)
        if tss < 0 and tss > -1e-10:
            tss = 0.0
    else:
        tss = float(Syy)

    r2 = np.nan if tss <= 0 else (1.0 - rss / tss)
    adj_r2 = np.nan
    if nobs > 1 and nobs > rank and tss > 0:
        adj_r2 = 1.0 - (1.0 - r2) * (nobs - 1) / (nobs - rank)

    meta = {
        "rank": rank,
        "rss": rss,
        "tss": tss,
        "r2": r2,
        "adj_r2": adj_r2,
        "sigma": np.nan,  # not defined if rank<p (we won't compute SEs)
    }

    if rank < p:
        return None, None, meta  # signal rank deficiency to caller
    else:
        # Full rank via lstsq; can produce SEs if requested
        beta = beta_lstsq
        if compute_se:
            # Use pseudoinverse: (X'X)^(-1) = V S^{-2} V'
            # Build from SVD of Sxx: Sxx = U S V'  => inv = V S^{-1} U'
            # For symmetric Sxx, U≈V, but we use full pseudoinverse for safety.
            U, S, Vt = np.linalg.svd(Sxx, full_matrices=False)
            inv_s = np.diag(1.0 / S)
            Sxx_inv = Vt.T @ inv_s @ U.T
            dof = max(nobs - rank, 0)
            sigma2 = float(rss / dof) if dof > 0 else np.nan
            se = np.sqrt(np.maximum(np.diag(Sxx_inv), 0.0) * sigma2)
            meta["sigma"] = float(np.sqrt(sigma2)) if sigma2 == sigma2 else np.nan
        return beta, se, meta


def _asreg_cross_sectional(
    df: pd.DataFrame,
    y: str,
    X: List[str] | str,
    by: List[str] | str | None,
    add_constant: bool,
    drop_collinear: bool,
    compute_se: bool,
    rtol: float | None,
) -> pd.DataFrame:
    """
    Run separate regressions for each group using all available data.
    This mimics Stata's "bys group_var: asreg y x_vars" behavior.
    Returns one row per group with regression results.
    """
    # Import here to avoid circular dependencies
    import statsmodels.api as sm
    # We need the drop_collinear and regress functions from asreg_rebuild
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from asreg_rebuild.stata_regress import regress
    
    # Expand X column patterns
    if isinstance(X, str):
        X_cols = _expand_columns(df, X)
    else:
        X_cols = X

    # Group handling
    if isinstance(by, str):
        by_list = [by]
        single_by = True
    else:
        by_list = by
        single_by = False

    if not by_list:
        raise ValueError(
            "window=None requires 'by' parameter to specify groups"
        )

    # Prepare column names
    stat_cols = ["_Nobs", "_R2", "_adjR2", "_sigma"]
    coef_cols = [f"_b_{col}" for col in X_cols]
    if add_constant:
        coef_cols.append("_b_cons")

    if compute_se:
        se_cols = [f"_se_{col}" for col in X_cols]
        t_cols = [f"_t_{col}" for col in X_cols]
        if add_constant:
            se_cols.append("_se_cons")
            t_cols.append("_t_cons")
        all_result_cols = stat_cols + coef_cols + se_cols + t_cols
    else:
        all_result_cols = stat_cols + coef_cols

    # List to store results for each group
    results_list = []

    # Process each group (use original by for groupby to get correct name format)
    for name, group in df.groupby(by if single_by else by_list):
        # Handle different types of group names
        if isinstance(name, (str, int, float)):
            group_name = name
        elif hasattr(name, '__iter__') and not isinstance(name, str):
            # name is a tuple for multi-column groupby
            group_name = "_".join(map(str, name))
        else:
            # name is likely a Timestamp or other single object
            group_name = str(name)

        # Extract X and y for this group
        X_group = group[X_cols]
        y_group = group[y]

        # Initialize result row for this group
        result_row = {}
        
        # Add group identifier(s)
        if single_by:
            # For single grouping column, name is a scalar
            result_row[by_list[0]] = name
        else:
            # For multiple grouping columns, name is a tuple
            for i, col in enumerate(by_list):
                result_row[col] = name[i]

        try:
            # Run regress for this group
            model, keep_cols, drop_cols, reasons, full_coefs = regress(
                X_group,
                y_group,
                add_constant=add_constant,
                omit_collinear=drop_collinear,
                return_full_coefs=True,
            )

            # Fill stats
            result_row["_Nobs"] = model.nobs
            result_row["_R2"] = model.rsquared
            result_row["_adjR2"] = model.rsquared_adj
            result_row["_sigma"] = np.sqrt(model.mse_resid)

            # Fill coefficients
            for col in X_cols:
                if col in full_coefs.index:
                    result_row[f"_b_{col}"] = full_coefs.loc[col, "coefficient"]
                else:
                    result_row[f"_b_{col}"] = 0.0  # Omitted due to collinearity

            # Fill constant
            if add_constant:
                result_row["_b_cons"] = model.params.get("const", np.nan)

            # Fill SEs and t-stats if requested
            if compute_se:
                for col in X_cols:
                    if col in full_coefs.index:
                        result_row[f"_se_{col}"] = full_coefs.loc[col, "std_err"]
                        if full_coefs.loc[col, "std_err"] > 0:
                            result_row[f"_t_{col}"] = (
                                full_coefs.loc[col, "coefficient"]
                                / full_coefs.loc[col, "std_err"]
                            )
                        else:
                            result_row[f"_t_{col}"] = np.nan
                    else:
                        result_row[f"_se_{col}"] = np.nan
                        result_row[f"_t_{col}"] = np.nan

                if add_constant:
                    const_se = model.bse.get("const", np.nan)
                    const_coef = model.params.get("const", np.nan)
                    result_row["_se_cons"] = const_se
                    if const_se > 0:
                        result_row["_t_cons"] = const_coef / const_se
                    else:
                        result_row["_t_cons"] = np.nan

        except Exception as e:
            print(f"Error processing group {group_name}: {e}")
            # Fill with NaN for this group if regression fails
            for col in all_result_cols:
                result_row[col] = np.nan

        results_list.append(result_row)

    # Convert to DataFrame
    results_df = pd.DataFrame(results_list)
    
    # Return with group columns first, then regression results
    return results_df[by_list + all_result_cols]

# =============================================================================
# ASREG FUNCTIONS
# =============================================================================

def asreg_collinear(
    df: pd.DataFrame,
    y: str,
    X: List[str] | str,
    *,
    by: List[str] | str | None = None,
    time: str | None = None,
    window: int | None = None,
    min_obs: int = 10,
    expanding: bool = False,
    add_constant: bool = True,
    drop_collinear: bool = True,  # If a window is rank-deficient → emit NaNs for that row
    compute_se: bool = False,  # Conventional (non-robust) SEs and t-stats
    method: str = "auto",  # kept for future use; currently cholesky→lstsq
    rtol: float | None = None,
) -> pd.DataFrame:
    """
    Stata-like rolling OLS over a panel/time index, or cross-sectional regressions by group.

    Behavior
    --------
    If window is None:
      - Runs separate regression for each group in 'by' using all data (like "bys group: asreg").
      - All observations in each group get the same regression coefficients.
      - Ignores 'time' and 'expanding' parameters.

    If window is an int:
      - Sorts by [by..., time] (if provided).
      - Right-aligned rolling window over *valid* rows (listwise within y and X).
      - On a row where valid_obs < max(min_obs, p+1), outputs NaNs.

    Common behavior:
      - If a window/group is rank-deficient and drop_collinear=True, outputs NaNs for that row/group.
      - Stats: _Nobs, _R2, _adjR2, _sigma; Coefs: _b_<var>, (_b_cons if add_constant).
      - If compute_se=True: _se_<var>, _t_<var> (and _se_cons/_t_cons if applicable).

    Parameters
    ----------
    df : DataFrame containing y, X, by, and time columns.
    y  : str name of dependent variable.
    X  : list[str] or pattern string (supports wildcards like "A_*", or "A_* B_*").
    by : panel keys (list or single str) or None for single-group time series.
    time : time column; required for deterministic ordering when window is not None.
    window : None for cross-sectional (all data per group), or int for rolling window size.
    min_obs : minimum valid rows needed to compute estimates for a row.
    expanding : use an expanding window from the first valid row (True) or a fixed-size rolling window (False).
              Only applies when window is an int.
    add_constant : include an intercept in each window.
    drop_collinear : if True, windows with rank < p are marked NaN.
    compute_se : compute conventional SEs and t-stats (slower).
    method : reserved; the solver auto-falls back from Cholesky to lstsq.
    rtol : optional tolerance forwarded to lstsq fallback.

    Returns
    -------
    DataFrame aligned to df.index with Stata-like column names.
    """
    # Handle cross-sectional case (window=None)
    if window is None:
        return _asreg_cross_sectional(
            df, y, X, by, add_constant, drop_collinear, compute_se, rtol
        )

    # Rolling window case - validate parameters
    if time is None:
        raise ValueError("`time` column must be provided for rolling window regressions.")
    if not isinstance(window, int) or window <= 0:
        raise ValueError("`window` must be a positive integer for rolling window regressions.")
    if isinstance(by, str):
        by = [by]
    by = list(by) if by is not None else []

    rhs = _expand_columns(df, X)
    p_raw = len(rhs)
    if p_raw == 0:
        raise ValueError("No RHS columns found.")

    # Prepare and sort
    gdf = df.copy()
    # Sort by keys then time
    if time is not None:
        keys = (by or []) + [time]
        gdf = gdf.sort_values(keys, kind="mergesort")  # stable
    
    # Coerce numeric
    X_df = gdf[rhs].copy()
    y_s = gdf[y].copy()
    for c in rhs:
        if not pd.api.types.is_numeric_dtype(X_df[c]):
            warnings.warn(
                f"Column {c} is not numeric; coercing with pd.to_numeric(..., errors='coerce')."
            )
            X_df[c] = pd.to_numeric(X_df[c], errors="coerce")
    if not pd.api.types.is_numeric_dtype(y_s):
        warnings.warn(
            f"y column {y} is not numeric; coercing with pd.to_numeric(..., errors='coerce')."
        )
        y_s = pd.to_numeric(y_s, errors="coerce")
    
    idx = gdf.index.to_numpy()

    # Augment with constant if requested
    aug_names: List[str] = rhs[:]
    if add_constant:
        aug_names = aug_names + ["_cons"]

    # Pre-allocate output arrays
    n_all = len(gdf)
    out_cols: Dict[str, np.ndarray] = {
        "_Nobs": np.full(n_all, np.nan, dtype=float),
        "_R2": np.full(n_all, np.nan, dtype=float),
        "_adjR2": np.full(n_all, np.nan, dtype=float),
        "_sigma": np.full(n_all, np.nan, dtype=float),
    }
    for name in rhs:
        out_cols[f"_b_{name}"] = np.full(n_all, np.nan, dtype=float)
        if compute_se:
            out_cols[f"_se_{name}"] = np.full(n_all, np.nan, dtype=float)
            out_cols[f"_t_{name}"] = np.full(n_all, np.nan, dtype=float)
    if add_constant:
        out_cols["_b_cons"] = np.full(n_all, np.nan, dtype=float)
        if compute_se:
            out_cols["_se_cons"] = np.full(n_all, np.nan, dtype=float)
            out_cols["_t_cons"] = np.full(n_all, np.nan, dtype=float)

    # Work group-by-group
    if by:
        groups = gdf.groupby(by, sort=False, group_keys=False, dropna=False)
    else:
        # single implicit group
        gkey = pd.Series(0, index=gdf.index)
        groups = gdf.groupby(gkey, sort=False, group_keys=False)

    for _, g in groups:
        # Get positional indices within the sorted df (gdf)
        pos = gdf.index.get_indexer(g.index)  # positions of this group's indices in gdf
        # Extract arrays
        X_block = X_df.loc[g.index].to_numpy(dtype=float, copy=False)  # (n, p_raw)
        y_block = y_s.loc[g.index].to_numpy(dtype=float, copy=False)  # (n,)

        n_g = X_block.shape[0]
        p = p_raw + (1 if add_constant else 0)

        # Valid row mask (listwise): finite y and finite X row
        valid = np.isfinite(y_block) & np.isfinite(X_block).all(axis=1)

        # Rolling state
        Sxx = np.zeros((p, p), dtype=float)
        Sxy = np.zeros((p,), dtype=float)
        Sy = 0.0
        Syy = 0.0
        n_valid = 0

        # Store most recent window rows for subtraction (fixed window only)
        q: deque[Tuple[np.ndarray, float]] = deque()

        # Helper to add/remove a row vector
        def _add_row(x_aug: np.ndarray, y_val: float) -> None:
            nonlocal Sxx, Sxy, Sy, Syy, n_valid
            Sxx += np.outer(x_aug, x_aug)
            Sxy += x_aug * y_val
            Sy += y_val
            Syy += y_val * y_val
            n_valid += 1

        def _sub_row(x_aug: np.ndarray, y_val: float) -> None:
            nonlocal Sxx, Sxy, Sy, Syy, n_valid
            Sxx -= np.outer(x_aug, x_aug)
            Sxy -= x_aug * y_val
            Sy -= y_val
            Syy -= y_val * y_val
            n_valid -= 1

        # Main scan
        for i in range(n_g):
            if valid[i]:
                # Build augmented x row
                if add_constant:
                    x_aug = np.empty((p,), dtype=float)
                    x_aug[:-1] = X_block[i, :]
                    x_aug[-1] = 1.0
                else:
                    x_aug = X_block[i, :]

                y_val = float(y_block[i])

                # Add current row to window
                _add_row(x_aug, y_val)
                q.append((x_aug, y_val))

                # If fixed window, trim to `window` valid rows
                if not expanding:
                    while n_valid > window:
                        x_old, y_old = q.popleft()
                        _sub_row(x_old, y_old)

                # Check sample size threshold
                min_needed = max(min_obs, p + 1)  # require >p DOF for stable OLS/SEs
                if n_valid >= min_needed:
                    beta, se, meta = _solve_ols_from_crossmoments(
                        Sxx,
                        Sxy,
                        Syy,
                        Sy,
                        n_valid,
                        compute_se=compute_se,
                        add_constant=add_constant,
                        rtol=rtol,
                    )
                    # If rank-deficient and we want to drop collinear windows -> NaNs
                    if beta is None or (drop_collinear and int(meta["rank"]) < p):
                        # leave NaNs in outputs for this row
                        pass
                    else:
                        # Write stats
                        out_cols["_Nobs"][pos[i]] = float(n_valid)
                        out_cols["_R2"][pos[i]] = float(meta["r2"])
                        out_cols["_adjR2"][pos[i]] = float(meta["adj_r2"])
                        out_cols["_sigma"][pos[i]] = float(meta["sigma"])

                        # Coefficients map: [rhs..., _cons?]
                        if add_constant:
                            b_rhs = beta[:-1]
                            b_c = float(beta[-1])
                        else:
                            b_rhs = beta
                            b_c = None

                        for j, name in enumerate(rhs):
                            out_cols[f"_b_{name}"][pos[i]] = float(b_rhs[j])
                        if add_constant:
                            out_cols["_b_cons"][pos[i]] = b_c

                        if compute_se and se is not None:
                            if add_constant:
                                se_rhs = se[:-1]
                                se_c = float(se[-1])
                            else:
                                se_rhs = se
                                se_c = None
                            for j, name in enumerate(rhs):
                                out_cols[f"_se_{name}"][pos[i]] = float(se_rhs[j])
                                # Guard div-by-zero
                                if se_rhs[j] > 0:
                                    out_cols[f"_t_{name}"][pos[i]] = float(
                                        b_rhs[j] / se_rhs[j]
                                    )
                                else:
                                    out_cols[f"_t_{name}"][pos[i]] = np.nan
                            if add_constant:
                                out_cols["_se_cons"][pos[i]] = se_c
                                if se_c is not None and se_c > 0:
                                    out_cols["_t_cons"][pos[i]] = float(b_c / se_c)
                                else:
                                    out_cols["_t_cons"][pos[i]] = np.nan
                else:
                    # Not enough obs yet: leave NaNs
                    pass
            else:
                # Current row invalid → keep window as-is; emit NaNs for this row
                # (Design choice: we do NOT reuse last coefficients on invalid rows.)
                pass

    # Assemble output DataFrame (aligned to original df index order)
    out_df = pd.DataFrame(out_cols, index=gdf.index)
    # Reindex back to the input df's original order
    out_df = out_df.reindex(df.index)

    # Column order: stats first, then coefficients (and optional SE/t grouped)
    ordered_cols: List[str] = ["_Nobs", "_R2", "_adjR2", "_sigma"]
    # Coefs
    ordered_cols += [f"_b_{c}" for c in rhs]
    if add_constant:
        ordered_cols += ["_b_cons"]
    # SE and t (if requested)
    if compute_se:
        ordered_cols += [f"_se_{c}" for c in rhs]
        if add_constant:
            ordered_cols += ["_se_cons"]
        ordered_cols += [f"_t_{c}" for c in rhs]
        if add_constant:
            ordered_cols += ["_t_cons"]

    return out_df[ordered_cols]


def _valid_mask_polars(y: str, X: Sequence[str]) -> pl.Expr:
    """Row-wise validity mask: True where y and all X are non-null."""
    m = pl.col(y).is_not_null()
    for x in X:
        m = m & pl.col(x).is_not_null()
    return m


def _agg_sum_polars(expr: pl.Expr, *, mode: Mode, over: Sequence[str], window_size: Optional[int], min_samples: int) -> pl.Expr:
    """Aggregate `expr` according to mode (rolling/expanding/group) and groups `over`."""
    if mode == "rolling":
        return expr.rolling_sum(window_size, min_periods=min_samples).over(over)
    elif mode == "expanding":
        return expr.cumsum().over(over)
    else:
        # group mode: sum per group, broadcast back to rows
        return expr.sum().over(over)


def asreg_polars(
    df: pl.DataFrame | pl.LazyFrame,
    *,
    y: str,
    X: Sequence[str],
    by: Optional[Sequence[str]] = None,
    t: Optional[str] = None,
    mode: Mode = "rolling",
    window_size: Optional[int] = None,
    min_samples: Optional[int] = None,
    add_intercept: bool = True,
    outputs: Iterable[str] = ("coef",),
    coef_prefix: str = "b_",
    collect: bool = True,
    null_policy: str = "drop",
    solve_method: str = "svd",
) -> pl.DataFrame | pl.LazyFrame:
    """Multi-purpose OLS over groups/windows using polars (fast, no collinearity handling).

    Args:
        df: Input DataFrame or LazyFrame
        y: Dependent variable column name
        X: Independent variable column names
        by: Grouping columns (e.g., ["permno"] for by-permno regressions)
        t: Time/order column for rolling/expanding windows
        mode: "rolling", "expanding", or "group"
        window_size: Number of observations for rolling windows
        min_samples: Minimum observations required per regression (>= number of parameters)
        add_intercept: Whether to include an intercept term
        outputs: Any of "coef", "yhat", "resid", "rmse"
        coef_prefix: Prefix for coefficient columns (only used when materializing separate coef cols)
        collect: Whether to collect LazyFrame to DataFrame
        null_policy: Passed to polars-ols (e.g., "drop"); controls how nulls are handled in estimation
        solve_method: Numerical solver hint (e.g., "svd", "qr")

    Returns:
        DataFrame/LazyFrame with requested regression outputs
    """
    if pls is None:
        raise ImportError("polars-ols is required for asreg_polars. Install with: pip install polars-ols")
    
    lf = df.lazy() if isinstance(df, pl.DataFrame) else df
    over = list(by or [])

    # Parameter counts
    k = len(X) + (1 if add_intercept else 0)
    min_samples = max(min_samples or k, 1)

    # Ordering
    if mode != "group" and t is None:
        raise ValueError("t= (time/order column) is required for rolling/expanding")
    if mode == "rolling" and window_size is None:
        raise ValueError("window_size is required for rolling")
    if mode != "group":
        lf = lf.sort([*over, t])  # deterministic window order

    # Build base expressions
    yexpr = pl.col(y).least_squares
    Xexprs = [pl.col(c) for c in X]

    # Coefficients
    if mode == "group":
        if set(outputs) == {"resid"}:
            # Fast path: compute residuals directly without materializing coefficients
            residuals = yexpr.ols(
                *Xexprs,
                add_intercept=add_intercept,
                mode="residuals",
                null_policy=null_policy,
                solve_method=solve_method,
            ).over(over)
            # enforce min_samples at group level
            if over and min_samples > 1:
                n_eff_grp = _valid_mask_polars(y, X).cast(pl.Int64).sum().over(over)
                residuals = pl.when(n_eff_grp >= min_samples).then(residuals).otherwise(None)
            lf = lf.with_columns(resid=residuals)
            return lf.collect() if collect else lf
        # standard coefficients
        coef = yexpr.ols(
            *Xexprs,
            add_intercept=add_intercept,
            mode="coefficients",
            null_policy=null_policy,
            solve_method=solve_method,
        ).over(over)
        if over and min_samples > 1:
            n_eff_grp = _valid_mask_polars(y, X).cast(pl.Int64).sum().over(over)
            coef = pl.when(n_eff_grp >= min_samples).then(coef).otherwise(None)
    elif mode == "rolling":
        coef = yexpr.rolling_ols(
            *Xexprs,
            window_size=window_size,
            min_periods=min_samples,
            add_intercept=add_intercept,
            mode="coefficients",
            null_policy=null_policy,
        ).over(over)
    else:  # expanding
        coef = yexpr.expanding_ols(
            *Xexprs,
            min_periods=min_samples,
            add_intercept=add_intercept,
            mode="coefficients",
            null_policy=null_policy,
        ).over(over)

    lf = lf.with_columns(coef=coef)

    # Materialize named coefficient columns when needed by outputs
    need_coef_cols = any(o in {"coef", "yhat", "resid", "rmse"} for o in outputs)
    if need_coef_cols:
        coef_cols: list[pl.Expr] = []
        if add_intercept:
            coef_cols.append(pl.col("coef").struct.field("const").alias(f"{coef_prefix}const"))
        coef_cols += [pl.col("coef").struct.field(x).alias(f"{coef_prefix}{x}") for x in X]
        lf = lf.with_columns(coef_cols)

    # yhat / resid via manual calculation to avoid polars-ols predict issues
    if any(o in {"yhat", "resid", "rmse"} for o in outputs):
        yhat = (pl.col(f"{coef_prefix}const") if add_intercept else pl.lit(0.0))
        for x in X:
            yhat = yhat + pl.col(f"{coef_prefix}{x}") * pl.col(x)
        lf = lf.with_columns(yhat.alias("yhat"))

    if any(o in {"resid", "rmse"} for o in outputs):
        lf = lf.with_columns(resid=(pl.col(y) - pl.col("yhat")).alias("resid"))

    # RMSE with correct SSE and DOF per window/group
    if "rmse" in outputs:
        valid = _valid_mask_polars(y, X)

        def z_expr(name: str) -> pl.Expr:
            return pl.lit(1.0) if name == "__const__" else pl.col(name)

        # names of design columns Z (include intercept as "__const__")
        Z_names = (["__const__"] if add_intercept else []) + list(X)

        # Helper to mask invalid rows (skip nulls)
        def mask(expr: pl.Expr) -> pl.Expr:
            return pl.when(valid).then(expr).otherwise(None)

        # Aggregate builders (per mode)
        agg = lambda e: _agg_sum_polars(mask(e), mode=mode, over=over, window_size=window_size, min_samples=min_samples)

        # Moment sums
        yy = agg(pl.col(y) * pl.col(y)).cast(pl.Float64)

        zy = {zi: agg(z_expr(zi) * pl.col(y)).cast(pl.Float64) for zi in Z_names}

        zz = {}
        for i, zi in enumerate(Z_names):
            for j, zj in enumerate(Z_names[i:]):
                zz[(zi, Z_names[i + j])] = agg(z_expr(zi) * z_expr(Z_names[i + j])).cast(pl.Float64)

        # Access coefficient fields from the struct (uses "const" for intercept)
        def b_field(zi: str) -> pl.Expr:
            if zi == "__const__":
                return pl.col("coef").struct.field("const").cast(pl.Float64)
            return pl.col("coef").struct.field(zi).cast(pl.Float64)

        # term2 = 2 * b' (Z'Y)
        t2 = None
        for zi in Z_names:
            contrib = b_field(zi) * zy[zi]
            t2 = contrib if t2 is None else (t2 + contrib)
        term2 = 2.0 * t2 if t2 is not None else pl.lit(None, dtype=pl.Float64)

        # term3 = b' (Z'Z) b  [double the off-diagonals]
        t3 = None
        for i, zi in enumerate(Z_names):
            bi = b_field(zi)
            for j, zj in enumerate(Z_names[i:]):
                zj_name = Z_names[i + j]
                bj = b_field(zj_name)
                factor = pl.lit(1.0) if j == 0 else pl.lit(2.0)  # j==0 => zi==zj
                contrib = factor * bi * bj * zz[(zi, zj_name)]
                t3 = contrib if t3 is None else (t3 + contrib)

        SSE = yy - term2 + t3

        # Effective sample size & DOF
        n_eff = _agg_sum_polars(valid.cast(pl.Int64), mode=mode, over=over, window_size=window_size, min_samples=min_samples)
        dof = (n_eff - k)

        rmse_expr = pl.when((dof > 0) & SSE.is_not_null())
        rmse_expr = rmse_expr.then((SSE / dof.cast(pl.Float64)).sqrt()).otherwise(None)
        lf = lf.with_columns(rmse=rmse_expr)

    # Drop struct unless explicitly requested
    if "coef" not in outputs:
        lf = lf.drop("coef")

    return lf.collect() if collect else lf

# =============================================================================
# ASROL FUNCTIONS  
# =============================================================================

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


def stata_asrol(*args, **kwargs):
    """Alias for asrol_fast with consecutive_only=True"""
    kwargs['consecutive_only'] = True
    return asrol_fast(*args, **kwargs)