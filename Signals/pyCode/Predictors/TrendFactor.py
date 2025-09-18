# ABOUTME: TrendFactor following Han, Zhou, Zhu 2016 Table 1
# ABOUTME: calculates price trend factor using past 20-day returns and volumes

"""
TrendFactor.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/TrendFactor.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, date, ret, vol]
    - SignalMasterTable.parquet: Master table with columns [permno, yyyymm]

Outputs:
    - TrendFactor.csv: CSV file with columns [permno, yyyymm, TrendFactor]
"""

import pandas as pd
import polars as pl
from polars import coalesce, col, lit  # for convenience
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_ineq_pl
from utils.asrol import asrol
from utils.stata_replication import stata_quantile


# %% specialized regression utilities
# =============================================================================
# STATA REGRESSION UTILITIES (moved from utils/stata_regress.py)
# =============================================================================

from collections import deque
from typing import Iterable, Sequence, Tuple, Dict, List, Optional
import fnmatch
import warnings
import numpy as np
import statsmodels.api as sm


def drop_collinear(
    X: pd.DataFrame,
    y: pd.Series | np.ndarray | None = None,
    sample_mask: pd.Series | np.ndarray | None = None,
    *,
    rtol: float | None = None,
    method: str = "qr",  # "qr" (fast, needs SciPy) or "greedy" (no deps)
    scale: bool = True,  # column-normalize for numerics (improves stability)
    return_reduced_X: bool = True,
):
    """
    Identify and drop RHS columns that cause rank deficiency (Stata rmcoll-like).

    Parameters
    ----------
    X : DataFrame of numeric regressors (no constant automatically added).
    y : optional response; if given, the estimation sample uses rows finite in both X and y.
    sample_mask : optional boolean array to define the estimation sample explicitly.
                  If provided, it overrides y-based masking and is intersected with X finiteness.
    rtol : optional relative tolerance for rank determination.
           Default: eps * max(n, p) * largest_diag(R) for QR, or eps * max(n, p) * max(singular_value) for greedy.
    method : "qr" uses SciPy's QR with column pivoting (fast & robust). Falls back to "greedy" if SciPy not available.
    scale : if True, columns are L2-normalized before rank tests (recommended).
    return_reduced_X : if True, return X with only kept columns (same row subset).

    Returns
    -------
    keep_cols : list[str] in original order
    drop_cols : list[str] in original order
    reasons   : dict[col -> "constant" | "collinear"]
    X_reduced : DataFrame with kept columns on the estimation sample (only if return_reduced_X=True)

    Notes
    -----
    - This operates on the *current estimation sample* (Stata-like). Rows with any non-finite
      value in the used columns (and optionally y) are excluded.
    - Factor variables / dummies: including a full set of category dummies *plus* a constant will cause
      one dummy to be flagged as collinear (which is expected).
    - If you must preserve certain columns, pass them first in X's column order and use method="greedy",
      which tends to keep earlier independent columns.
    """
    # --- 0) Basic validations ---
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")
    non_num = [c for c in X.columns if not pd.api.types.is_numeric_dtype(X[c])]
    if non_num:
        raise TypeError(f"All columns must be numeric. Non-numeric columns: {non_num}")

    cols = list(X.columns)

    # --- 1) Build estimation sample mask (Stata does listwise deletion on current sample) ---
    finite_X = np.isfinite(X.to_numpy(dtype=float, copy=False)).all(axis=1)
    if sample_mask is not None:
        mask = np.asarray(sample_mask, dtype=bool) & finite_X
    elif y is not None:
        y_arr = np.asarray(y)
        if y_arr.ndim > 1:
            y_arr = y_arr.squeeze()
        mask = finite_X & np.isfinite(y_arr)
    else:
        mask = finite_X

    Xs = X.loc[mask]
    if Xs.shape[0] == 0:
        raise ValueError("No rows left after applying estimation-sample mask.")

    A = Xs.to_numpy(dtype=float, copy=False)  # n x p

    n, p = A.shape
    if p == 0:
        return [], [], {}, (Xs if return_reduced_X else None)

    # --- 2) Quick constant-column screening (gives clear reasons, also speeds the rank step) ---
    ptp = np.ptp(A, axis=0)  # max-min per column
    is_const = ptp == 0
    reasons = {}
    const_idx = np.where(is_const)[0].tolist()
    for j in const_idx:
        reasons[cols[j]] = "constant"

    keep_mask_pre = ~is_const
    cols_pre = [c for k, c in enumerate(cols) if keep_mask_pre[k]]
    A_pre = A[:, keep_mask_pre]
    if A_pre.shape[1] == 0:
        keep_cols = []
        drop_cols = cols[:]  # all constants
        if return_reduced_X:
            return keep_cols, drop_cols, reasons, Xs[keep_cols]
        else:
            return keep_cols, drop_cols, reasons, None

    # Optionally scale columns to unit norm (improves numerical stability of rank tests)
    if scale:
        norms = np.linalg.norm(A_pre, axis=0)
        # Norms should be >0 here (we removed constants), but guard anyway:
        norms[norms == 0] = 1.0
        A_test = A_pre / norms
    else:
        A_test = A_pre

    # --- 3) Rank-revealing step: QR w/ pivoting (fast) or greedy fallback ---
    # Determine tolerance (relative to the largest scale in the factorization)
    eps = np.finfo(A_test.dtype).eps
    if method == "qr":
        try:
            from scipy.linalg import qr as scipy_qr  # noqa

            Q, R, piv = scipy_qr(A_test, mode="economic", pivoting=True)
            diagR = np.abs(np.diag(R))
            # Set default tolerance if not provided
            tol = (
                rtol
                if rtol is not None
                else (eps * max(n, A_test.shape[1]) * diagR.max())
            )
            rank = int((diagR > tol).sum())
            piv = np.asarray(piv)
            indep_local = piv[:rank].tolist()
            dep_local = piv[rank:].tolist()
        except Exception:
            # SciPy not available or failed: fall back to greedy
            method = "greedy"

    if method == "greedy":
        # Greedy: keep earliest independent columns (in A_pre's order).
        # At each step, test if new col is in span(kept); if yes → dependent.
        tol = rtol if rtol is not None else (eps * max(n, A_test.shape[1]))
        indep_local = []
        dep_local = []
        for j in range(A_test.shape[1]):
            if not indep_local:
                # If this column has nonzero norm, keep it
                if np.linalg.norm(A_test[:, j]) > tol:
                    indep_local.append(j)
                else:
                    dep_local.append(j)
                continue
            # Project A_test[:, j] onto columns in indep_local, then check residual norm
            Aj = A_test[:, j]
            Akeep = A_test[:, indep_local]
            # Solve least squares Akeep * b ≈ Aj
            b, *_ = np.linalg.lstsq(Akeep, Aj, rcond=None)
            resid = Aj - Akeep @ b
            if np.linalg.norm(resid) > tol:
                indep_local.append(j)
            else:
                dep_local.append(j)

    # indep_local/dep_local are indices in A_pre/cols_pre space; map back to original columns
    keep_cols_preorder = [cols_pre[k] for k in indep_local]
    drop_cols_preorder = [cols_pre[k] for k in dep_local]
    for c in drop_cols_preorder:
        reasons[c] = "collinear"

    # Reconstitute full keep/drop *in original column order*
    keep_set = set(keep_cols_preorder)
    keep_cols = [
        c
        for c in cols
        if (c in keep_set) and (c not in reasons or reasons[c] != "constant")
    ]
    # Everything else is dropped either as constant or collinear
    drop_cols = [c for c in cols if c not in keep_cols]

    if return_reduced_X:
        return keep_cols, drop_cols, reasons, Xs[keep_cols]
    else:
        return keep_cols, drop_cols, reasons, None


def regress(X, y, add_constant=True, omit_collinear=True, return_full_coefs=True):
    """
    Replicate Stata's regress command with collinearity handling.

    Parameters
    ----------
    X : pd.DataFrame
        The independent variables
    y : pd.Series or array-like
        The dependent variable
    add_constant : bool
        Whether to add a constant term (default: True)
    omit_collinear : bool
        Whether to drop collinear variables (default: True)
    return_full_coefs : bool
        Whether to return full coefficients with zeros for omitted vars (default: True)

    Returns
    -------
    model : statsmodels regression results
        The fitted model
    kept_vars : list
        Variables kept in the model
    dropped_vars : list
        Variables dropped due to collinearity
    reasons : dict
        Reasons for dropping variables
    full_coefficients : pd.DataFrame (if return_full_coefs=True)
        Complete coefficient table with zeros for omitted variables
    """
    if omit_collinear:
        keep_cols, drop_cols, reasons, X_reduced = drop_collinear(X, y=y)
    else:
        X_reduced = X
        keep_cols = list(X.columns)
        drop_cols = []
        reasons = {}

    if add_constant:
        X_with_const = sm.add_constant(X_reduced)
    else:
        X_with_const = X_reduced

    # Run regression
    model = sm.OLS(y.loc[X_reduced.index], X_with_const).fit()

    if return_full_coefs:
        # Create full coefficient DataFrame with zeros for omitted variables
        full_coefs = {}

        # Add coefficients for kept variables using parameter names from model
        for var in keep_cols:
            if var in model.params.index:
                full_coefs[var] = {
                    "coefficient": model.params[var],
                    "std_err": model.bse[var],
                    "omitted": False,
                }

        # Add zeros for dropped variables
        for var in drop_cols:
            full_coefs[var] = {"coefficient": 0.0, "std_err": np.nan, "omitted": True}

        # Add constant if it was included
        if add_constant and "const" in model.params.index:
            full_coefs["_cons"] = {
                "coefficient": model.params["const"],
                "std_err": model.bse["const"],
                "omitted": False,
            }

        # Create DataFrame in original variable order, then add constant
        original_vars = list(X.columns)
        ordered_vars = [var for var in original_vars if var in full_coefs]
        if add_constant:
            ordered_vars.append("_cons")

        ordered_results = {var: full_coefs[var] for var in ordered_vars}
        full_coefficients = pd.DataFrame.from_dict(ordered_results, orient="index")

        return model, keep_cols, drop_cols, reasons, full_coefficients
    else:
        return model, keep_cols, drop_cols, reasons


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


def _ensure_sorted(
    df: pd.DataFrame, by: List[str] | None, time: Optional[str]
) -> pd.DataFrame:
    """
    Sort by keys then time (if provided). Returns a new DataFrame.
    """
    if time is None:
        return df.copy()
    keys = (by or []) + [time]
    g = df.sort_values(keys, kind="mergesort")  # stable
    return g


def _coerce_numeric_block(
    df: pd.DataFrame, cols: List[str], ycol: str
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Ensure numeric dtypes; coerce non-numeric to float (NaN if fails) with a warning.
    """
    X = df[cols].copy()
    y = df[ycol].copy()
    for c in cols:
        if not pd.api.types.is_numeric_dtype(X[c]):
            warnings.warn(
                f"Column {c} is not numeric; coercing with pd.to_numeric(..., errors='coerce')."
            )
            X[c] = pd.to_numeric(X[c], errors="coerce")
    if not pd.api.types.is_numeric_dtype(y):
        warnings.warn(
            f"y column {ycol} is not numeric; coercing with pd.to_numeric(..., errors='coerce')."
        )
        y = pd.to_numeric(y, errors="coerce")
    return X, y


def _asreg_cross_sectional(
    df: pd.DataFrame,
    y: str,
    X: List[str] | str,
    by: List[str] | str | None,
    add_constant: bool,
    drop_collinear: bool,
    compute_se: bool,
    compute_residuals: bool,
    rtol: float | None,
) -> pd.DataFrame:
    """
    Run separate regressions for each group using all available data.
    This mimics Stata's "bys group_var: asreg y x_vars" behavior.
    Returns one row per group with regression results.
    """
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
        raise ValueError("window=None requires 'by' parameter to specify groups")

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
        if isinstance(name, (str, int, float, pd.Timestamp, pd.Period)):
            group_name = name
        else:
            group_name = "_".join(map(str, name))

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
            print(f"Warning: could not process group {group_name}: {e}")
            # Fill with NaN for this group if regression fails
            for col in all_result_cols:
                result_row[col] = np.nan

        results_list.append(result_row)

    # Convert to DataFrame
    results_df = pd.DataFrame(results_list)

    # If residuals are requested, compute them for all observations
    if compute_residuals:
        # Initialize residuals column with NaNs
        df_with_residuals = df.copy()
        df_with_residuals["_residuals"] = np.nan

        # For each group, compute residuals
        for name, group in df.groupby(by if single_by else by_list):
            # Get the coefficients for this group
            if single_by:
                group_mask = results_df[by_list[0]] == name
            else:
                # Multi-column groupby
                group_mask = True
                for i, col in enumerate(by_list):
                    group_mask = group_mask & (results_df[col] == name[i])

            group_coeffs = results_df[group_mask]
            if len(group_coeffs) == 0 or pd.isna(group_coeffs.iloc[0]["_Nobs"]):
                continue

            # Get coefficient values
            beta_values = []
            for col in X_cols:
                beta_values.append(group_coeffs.iloc[0][f"_b_{col}"])
            if add_constant:
                beta_values.append(group_coeffs.iloc[0]["_b_cons"])
            beta = np.array(beta_values)

            # Skip if any coefficient is NaN
            if np.any(np.isnan(beta)):
                continue

            # Compute residuals for this group
            X_group = group[X_cols].values
            y_group = group[y].values

            # Add constant if needed
            if add_constant:
                X_group = np.column_stack([X_group, np.ones(len(X_group))])

            # Compute yhat and residuals
            valid_mask = np.isfinite(y_group) & np.all(np.isfinite(X_group), axis=1)
            yhat = X_group @ beta
            residuals = y_group - yhat

            # Store residuals
            df_with_residuals.loc[group.index[valid_mask], "_residuals"] = residuals[
                valid_mask
            ]

        # Merge residuals into results (each group gets same coefficients but different residuals)
        # For cross-sectional, we return one row per original observation with residuals
        result_with_residuals = df.merge(results_df, on=by_list, how="left")
        result_with_residuals["_residuals"] = df_with_residuals["_residuals"]

        # Return with group columns, regression results, and residuals
        return result_with_residuals[by_list + all_result_cols + ["_residuals"]]

    # Return with group columns first, then regression results (no residuals)
    return results_df[by_list + all_result_cols]


def asreg(
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
            df, y, X, by, add_constant, drop_collinear, compute_se, False, rtol
        )

    # Rolling window case - validate parameters
    if time is None:
        raise ValueError(
            "`time` column must be provided for rolling window regressions."
        )
    if not isinstance(window, int) or window <= 0:
        raise ValueError(
            "`window` must be a positive integer for rolling window regressions."
        )
    if isinstance(by, str):
        by = [by]
    by = list(by) if by is not None else []

    rhs = _expand_columns(df, X)
    p_raw = len(rhs)
    if p_raw == 0:
        raise ValueError("No RHS columns found.")

    # Prepare and sort
    gdf = _ensure_sorted(df, by, time)
    X_df, y_s = _coerce_numeric_block(gdf, rhs, y)
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


def _compute_residuals_from_coeffs(
    df: pd.DataFrame,
    y: str,
    X: List[str],
    coef_df: pd.DataFrame,
    add_constant: bool = True,
) -> np.ndarray:
    """
    Compute residuals = y - X @ beta using pre-computed coefficients.

    Parameters
    ----------
    df : DataFrame with original data
    y : str name of dependent variable
    X : list of str names of independent variables
    coef_df : DataFrame with coefficient columns (_b_*)
    add_constant : whether constant was included in regression

    Returns
    -------
    np.ndarray of residuals aligned with df index
    """
    residuals = np.full(len(df), np.nan)

    # Get y values
    y_vals = df[y].to_numpy(dtype=float)

    # Get X matrix
    X_vals = df[X].to_numpy(dtype=float)

    # Coefficient column names
    beta_cols = [f"_b_{x}" for x in X]
    if add_constant:
        beta_cols.append("_b_cons")

    # Compute residuals row by row
    for i in range(len(df)):
        # Skip if no regression was run for this row (check _Nobs)
        if np.isnan(coef_df.iloc[i]["_Nobs"]):
            continue

        # Skip if y is missing
        if np.isnan(y_vals[i]):
            continue

        # Skip if any X is missing
        if np.any(np.isnan(X_vals[i])):
            continue

        # Get beta coefficients for this row
        beta = coef_df.iloc[i][beta_cols].to_numpy(dtype=float)

        # Skip if any coefficient is NaN (shouldn't happen if _Nobs exists, but be safe)
        if np.any(np.isnan(beta)):
            continue

        # Compute yhat = X @ beta
        if add_constant:
            # Last element of beta is constant
            yhat = np.dot(X_vals[i], beta[:-1]) + beta[-1]
        else:
            yhat = np.dot(X_vals[i], beta)

        # Compute residual
        residuals[i] = y_vals[i] - yhat

    return residuals


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
    compute_residuals: bool = False,  # Whether to compute and return residuals
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
      - If compute_residuals=True: _residuals column with y - yhat.

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
    compute_residuals : compute and return residuals = y - yhat in _residuals column.
    method : reserved; the solver auto-falls back from Cholesky to lstsq.
    rtol : optional tolerance forwarded to lstsq fallback.

    Returns
    -------
    DataFrame aligned to df.index with Stata-like column names.
    """
    # Handle cross-sectional case (window=None)
    if window is None:
        return _asreg_cross_sectional(
            df,
            y,
            X,
            by,
            add_constant,
            drop_collinear,
            compute_se,
            compute_residuals,
            rtol,
        )

    # Rolling window case - validate parameters
    if time is None:
        raise ValueError(
            "`time` column must be provided for rolling window regressions."
        )
    if not isinstance(window, int) or window <= 0:
        raise ValueError(
            "`window` must be a positive integer for rolling window regressions."
        )
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

    # Compute residuals if requested
    if compute_residuals:
        residuals = _compute_residuals_from_coeffs(
            df=gdf, y=y, X=rhs, coef_df=out_df, add_constant=add_constant
        )
        out_df["_residuals"] = residuals

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
    # Residuals (if requested)
    if compute_residuals:
        ordered_cols += ["_residuals"]

    return out_df[ordered_cols]


# %% actual file starts

print("=" * 80)
print("🏗️  TrendFactor.py")
print("Generating TrendFactor predictor using daily data with moving averages")
print("=" * 80)

print("📊 Loading daily CRSP data...")

# 1. Compute moving averages
# use permno time_d prc cfacpr using "$pathDataIntermediate/dailyCRSP", clear
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")

# convert time_d to datetime[D]
# tbc: should standardize in DataDownloads
daily_crsp = daily_crsp.with_columns(col("time_d").cast(pl.Date).alias("time_d"))

df_daily = daily_crsp.select(["permno", "time_d", "prc", "cfacpr"])
print(f"Daily CRSP data: {len(df_daily):,} observations")

print("🔄 Computing adjusted prices and time variables...")

# Adjust prices for splits etc
# Generate abs(prc)/cfacpr
df_daily = df_daily.with_columns((pl.col("prc").abs() / pl.col("cfacpr")).alias("P"))

# Generate time variable without trading day gaps for simplicity and generate month variable for sorting
# bys permno (time_d): Generate _n
df_daily = df_daily.sort(["permno", "time_d"])
df_daily = df_daily.with_columns(
    pl.int_range(pl.len()).over("permno").alias("time_temp")
)

# Generate mofd(time_d)
df_daily = df_daily.with_columns(
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
)

print("📈 Computing moving averages for 11 different lags...")

# Calculate moving average prices for various lag lengths
# xtset permno time_temp
lag_lengths = [3, 5, 10, 20, 50, 100, 200, 400, 600, 800, 1000]

# Convert to pandas for asrol_legacy operations
df_daily_pd = df_daily.to_pandas()

for L in lag_lengths:
    print(f"  Computing {L}-day moving average...")
    # asrol P, window(time_temp `L') stat(mean) by(permno) gen(A_`L')
    df_daily_pd = asrol(
        df_daily_pd,
        group_col="permno",
        time_col="time_temp",
        freq="1d",
        window=L,
        value_col="P",
        stat="mean",
        new_col_name=f"A_{L}",
        min_samples=1,  # Allow partial windows like Stata default
    )

# Convert back to polars
df_daily = pl.from_pandas(df_daily_pd).with_columns(
    col("time_avail_m").cast(pl.Date).alias("time_avail_m")
)

print("📅 Keeping only end-of-month observations...")

# Keep only last observation each month
# bys permno time_avail_m (time_d): keep if _n == _N
df_daily = df_daily.sort(["permno", "time_avail_m", "time_d"])
df_monthly = df_daily.group_by(["permno", "time_avail_m"], maintain_order=True).last()

print(f"Monthly data after filtering: {len(df_monthly):,} observations")

# Normalize by closing price at end of month
for L in lag_lengths:
    df_monthly = df_monthly.with_columns(
        (pl.col(f"A_{L}") / pl.col("P")).alias(f"A_{L}")
    )

# Keep only needed columns
moving_avg_cols = [f"A_{L}" for L in lag_lengths]
temp_ma = df_monthly.select(["permno", "time_avail_m"] + moving_avg_cols)

# %%

print(
    "📊 Creating monthly data with future returns and moving averages for regressions"
)

# 2. Run cross-sectional regressions on monthly data
# use permno time_avail_m ret prc exchcd shrcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
reg_input = pl.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "ret", "prc", "exchcd", "shrcd", "mve_c"],
).with_columns(col("time_avail_m").cast(pl.Date).alias("time_avail_m"))

print("🎯 Computing size deciles based on NYSE stocks...")

# new, using stata_quantile function
qu10_data = reg_input.filter(pl.col("exchcd") == 1).to_pandas()
qu10_data = (
    qu10_data.groupby("time_avail_m")
    .agg(qu10=("mve_c", lambda x: stata_quantile(x, 0.10)))
    .reset_index()
)
qu10_data = pl.from_pandas(qu10_data).with_columns(
    col("time_avail_m").cast(pl.Date).alias("time_avail_m")
)

# Merge back
reg_input = reg_input.join(qu10_data, on="time_avail_m", how="left")


print("🔍 Applying filters for regression sample...")

# Filters need to be imposed here rather than at portfolio stage
reg_input = reg_input.filter(
    ((pl.col("exchcd") == 1) | (pl.col("exchcd") == 2) | (pl.col("exchcd") == 3))
    & ((pl.col("shrcd") == 10) | (pl.col("shrcd") == 11))
    & stata_ineq_pl(pl.col("prc").abs(), ">=", 5)
    & stata_ineq_pl(pl.col("mve_c"), ">=", pl.col("qu10"))
).drop(["exchcd", "shrcd", "qu10", "mve_c", "prc"])

print(f"After applying filters: {len(reg_input):,} observations")

# Merge moving averages
reg_input = reg_input.join(temp_ma, on=["permno", "time_avail_m"], how="inner")

print(f"After merging moving averages: {len(reg_input):,} observations")


print("Preparing for cross-sectional regression...")

print("Carefully creating fRet with left join")
# the cast(pl.Date) is important to ensure the merge works
reg_input = reg_input.sort(["permno", "time_avail_m"])
templead = (
    reg_input.with_columns(
        col("time_avail_m").dt.offset_by("-1mo").cast(pl.Date).alias("time_avail_m")
    )
    .rename({"ret": "fRet"})
    .select(["permno", "time_avail_m", "fRet"])
)

# left merge the fRet back into the original data
reg_input = reg_input.join(templead, on=["permno", "time_avail_m"], how="left").sort(
    ["time_avail_m", "permno"]
)


# %%

print("🔧 asreg regressions with asreg_collinear")

# bys time_avail_m: asreg fRet A_*
# Run cross-sectional regression by time_avail_m using asreg_collinear helper
feature_cols = [f"A_{L}" for L in lag_lengths]

betas_by_month = asreg_collinear(
    reg_input.to_pandas(),
    y="fRet",
    X="A_*",  # Will be expanded to all A_* columns
    by="time_avail_m",
    window=None,  # None means use all data per group (cross-sectional)
    add_constant=True,
    drop_collinear=True,
)
betas_by_month = pl.from_pandas(betas_by_month).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
)

# %%

print("📊 Computing 12-month rolling averages of beta coefficients...")

# For each lag length, compute rolling mean of beta coefficients
# asrol _b_A_`L', window(time_avail_m -13 -1) stat(mean) gen(EBeta_`L')
# This excludes the current month (uses months t-13 to t-1)
# Use min_samples=1 to allow partial windows in early periods (matches Stata default behavior)
for L in lag_lengths:
    betas_by_month = betas_by_month.with_columns(
        pl.col(f"_b_A_{L}")
        .shift(1)  # Exclude current month
        .rolling_mean(
            window_size=12, min_samples=1
        )  # Allow partial windows to match Stata
        .alias(f"EBeta_{L}")
    )


# Keep only time and expected betas
ebeta_cols = [f"EBeta_{L}" for L in lag_lengths]
temp_beta = betas_by_month.select(["time_avail_m"] + ebeta_cols)

# %%

print("🎯 Computing TrendFactor as the smoothed regression model predictions")

# grab the moving averages for each permno-month and make long
cols_A = [col for col in reg_input.columns if col.startswith("A_")]
df_final = (
    reg_input.select(["permno", "time_avail_m"] + cols_A)
    .unpivot(index=["time_avail_m", "permno"], variable_name="name", value_name="MA")
    .with_columns(col("name").str.replace("A_", "").cast(pl.Int64).alias("lag"))
    .select(["permno", "time_avail_m", "lag", "MA"])
)

# convert smoothed betas to long
beta_long = (
    betas_by_month.unpivot(
        index="time_avail_m", variable_name="name", value_name="EBeta"
    )
    .filter(col("name").str.starts_with("EBeta_"))
    .with_columns(col("name").str.replace("EBeta_", "").cast(pl.Int64).alias("lag"))
    .select(["time_avail_m", "lag", "EBeta"])
)

# join the betas to the moving averages and compute the trend factor
# if there are NAs, TrendFactor is null (not zero!)
df_final = (
    df_final.join(beta_long, on=["time_avail_m", "lag"], how="left")
    .with_columns(EBeta_MA=pl.col("EBeta") * pl.col("MA"))
    .group_by(["permno", "time_avail_m"])
    .agg(
        TrendFactor=col("EBeta_MA").sum(),
        N_MA_used=col("EBeta_MA")
        .is_not_null()
        .sum(),  # required since python sum of nulls is zero
    )
    .filter(col("N_MA_used") == 11)
)  # 11 is the number of MA used in the regression

print(f"Generated TrendFactor values: {len(df_final):,} observations")

# %%

print("💾 Saving TrendFactor predictor...")
save_predictor(df_final, "TrendFactor")
print("✅ TrendFactor.csv saved successfully")
print("🎉 TrendFactor computation completed!")
