# === gpt5's asreg module ===



```python
#!/usr/bin/env python3
# ABOUTME: Module that replicates Stata's regress and adds a fast, minimal asreg (rolling OLS) helper.
# ABOUTME: Collinearity handling mirrors Stata-style behavior. Rolling core is implemented with cross-moment updates.

from __future__ import annotations

from collections import deque
from typing import Iterable, Sequence, Tuple, Dict, List, Optional

import fnmatch
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm


# --------------------------------------------------------------------------------------
# Existing functionality (kept with light documentation tweaks)
# --------------------------------------------------------------------------------------

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

    # --- 2) Quick constant-column screening ---
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
        norms[norms == 0] = 1.0
        A_test = A_pre / norms
    else:
        A_test = A_pre

    # --- 3) Rank-revealing step: QR w/ pivoting (fast) or greedy fallback ---
    eps = np.finfo(A_test.dtype).eps
    if method == "qr":
        try:
            from scipy.linalg import qr as scipy_qr  # noqa

            Q, R, piv = scipy_qr(A_test, mode="economic", pivoting=True)
            diagR = np.abs(np.diag(R))
            tol = rtol if rtol is not None else (eps * max(n, A_test.shape[1]) * diagR.max())
            rank = int((diagR > tol).sum())
            piv = np.asarray(piv)
            indep_local = piv[:rank].tolist()
            dep_local = piv[rank:].tolist()
        except Exception:
            method = "greedy"

    if method == "greedy":
        tol = rtol if rtol is not None else (eps * max(n, A_test.shape[1]))
        indep_local = []
        dep_local = []
        for j in range(A_test.shape[1]):
            if not indep_local:
                if np.linalg.norm(A_test[:, j]) > tol:
                    indep_local.append(j)
                else:
                    dep_local.append(j)
                continue
            Aj = A_test[:, j]
            Akeep = A_test[:, indep_local]
            b, *_ = np.linalg.lstsq(Akeep, Aj, rcond=None)
            resid = Aj - Akeep @ b
            if np.linalg.norm(resid) > tol:
                indep_local.append(j)
            else:
                dep_local.append(j)

    keep_cols_preorder = [cols_pre[k] for k in indep_local]
    drop_cols_preorder = [cols_pre[k] for k in dep_local]
    for c in drop_cols_preorder:
        reasons[c] = "collinear"

    keep_set = set(keep_cols_preorder)
    keep_cols = [
        c
        for c in cols
        if (c in keep_set) and (c not in reasons or reasons[c] != "constant")
    ]
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
    kept_vars : list
    dropped_vars : list
    reasons : dict
    full_coefficients : pd.DataFrame (if return_full_coefs=True)
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

        for var in keep_cols:
            if var in model.params.index:
                full_coefs[var] = {
                    "coefficient": model.params[var],
                    "std_err": model.bse[var],
                    "omitted": False,
                }

        for var in drop_cols:
            full_coefs[var] = {
                "coefficient": 0.0,
                "std_err": np.nan,
                "omitted": True,
            }

        if add_constant and "const" in model.params.index:
            full_coefs["_cons"] = {
                "coefficient": model.params["const"],
                "std_err": model.bse["const"],
                "omitted": False,
            }

        original_vars = list(X.columns)
        ordered_vars = [var for var in original_vars if var in full_coefs]
        if add_constant:
            ordered_vars.append("_cons")

        ordered_results = {var: full_coefs[var] for var in ordered_vars}
        full_coefficients = pd.DataFrame.from_dict(ordered_results, orient="index")

        return model, keep_cols, drop_cols, reasons, full_coefficients
    else:
        return model, keep_cols, drop_cols, reasons


# --------------------------------------------------------------------------------------
# New lightweight numeric core shared by asreg (and available for future reuse)
# --------------------------------------------------------------------------------------

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
            "sigma": float(np.sqrt(sigma2)) if sigma2 == sigma2 else np.nan,  # sqrt if finite
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


# --------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------

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


def _ensure_sorted(df: pd.DataFrame, by: List[str] | None, time: Optional[str]) -> pd.DataFrame:
    """
    Sort by keys then time (if provided). Returns a new DataFrame.
    """
    if time is None:
        return df.copy()
    keys = (by or []) + [time]
    g = df.sort_values(keys, kind="mergesort")  # stable
    return g


def _coerce_numeric_block(df: pd.DataFrame, cols: List[str], ycol: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Ensure numeric dtypes; coerce non-numeric to float (NaN if fails) with a warning.
    """
    X = df[cols].copy()
    y = df[ycol].copy()
    for c in cols:
        if not pd.api.types.is_numeric_dtype(X[c]):
            warnings.warn(f"Column {c} is not numeric; coercing with pd.to_numeric(..., errors='coerce').")
            X[c] = pd.to_numeric(X[c], errors="coerce")
    if not pd.api.types.is_numeric_dtype(y):
        warnings.warn(f"y column {ycol} is not numeric; coercing with pd.to_numeric(..., errors='coerce').")
        y = pd.to_numeric(y, errors="coerce")
    return X, y


# --------------------------------------------------------------------------------------
# New: asreg (lean, Stata-like)
# --------------------------------------------------------------------------------------

def asreg(
    df: pd.DataFrame,
    y: str,
    X: List[str] | str,
    *,
    by: List[str] | str | None = None,
    time: str | None = None,
    window: int = 60,
    min_obs: int = 10,
    expanding: bool = False,
    add_constant: bool = True,
    drop_collinear: bool = True,   # If a window is rank-deficient → emit NaNs for that row
    compute_se: bool = False,      # Conventional (non-robust) SEs and t-stats
    method: str = "auto",          # kept for future use; currently cholesky→lstsq
    rtol: float | None = None,
) -> pd.DataFrame:
    """
    Stata-like rolling OLS over a panel/time index.

    Behavior
    --------
    - Sorts by [by..., time] (if provided).
    - Right-aligned rolling window over *valid* rows (listwise within y and X).
    - On a row where valid_obs < max(min_obs, p+1), outputs NaNs.
    - If a window is rank-deficient and drop_collinear=True, outputs NaNs for that row.
    - Stats: _Nobs, _R2, _adjR2, _sigma; Coefs: _b_<var>, (_b_cons if add_constant).
      If compute_se=True: _se_<var>, _t_<var> (and _se_cons/_t_cons if applicable).

    Parameters
    ----------
    df : DataFrame containing y, X, by, and time columns.
    y  : str name of dependent variable.
    X  : list[str] or pattern string (supports wildcards like "A_*", or "A_* B_*").
    by : panel keys (list or single str) or None for single-group time series.
    time : time column; required for deterministic ordering.
    window : size in valid rows (if expanding=False) or ignored for expanding windows (uses all rows so far).
    min_obs : minimum valid rows needed to compute estimates for a row.
    expanding : use an expanding window from the first valid row (True) or a fixed-size rolling window (False).
    add_constant : include an intercept in each window.
    drop_collinear : if True, windows with rank < p are marked NaN.
    compute_se : compute conventional SEs and t-stats (slower).
    method : reserved; the solver auto-falls back from Cholesky to lstsq.
    rtol : optional tolerance forwarded to lstsq fallback.

    Returns
    -------
    DataFrame aligned to df.index with Stata-like column names.
    """
    if time is None:
        raise ValueError("`time` column must be provided for rolling alignment.")
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
        # Use positional indices within the sorted df
        pos = g.index.get_indexer(g.index)  # trivial, but keeps shape
        pos = g.index.to_numpy()            # absolute positions in gdf (i.e., df after sorting)
        # Extract arrays
        X_block = X_df.loc[g.index].to_numpy(dtype=float, copy=False)  # (n, p_raw)
        y_block = y_s.loc[g.index].to_numpy(dtype=float, copy=False)   # (n,)

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
                        Sxx, Sxy, Syy, Sy, n_valid,
                        compute_se=compute_se, add_constant=add_constant, rtol=rtol
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
                                    out_cols[f"_t_{name}"][pos[i]] = float(b_rhs[j] / se_rhs[j])
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
```
