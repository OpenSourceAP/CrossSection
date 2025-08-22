#!/usr/bin/env python3
# ABOUTME: Module that replicates Stata's regress command with collinearity handling
# ABOUTME: Drops collinear variables like Stata's regress command

import numpy as np
import pandas as pd
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
                    'coefficient': model.params[var],
                    'std_err': model.bse[var],
                    'omitted': False
                }
        
        # Add zeros for dropped variables
        for var in drop_cols:
            full_coefs[var] = {
                'coefficient': 0.0,
                'std_err': np.nan,
                'omitted': True
            }
        
        # Add constant if it was included
        if add_constant and 'const' in model.params.index:
            full_coefs['_cons'] = {
                'coefficient': model.params['const'],
                'std_err': model.bse['const'],
                'omitted': False
            }
        
        # Create DataFrame in original variable order, then add constant
        original_vars = list(X.columns)
        ordered_vars = [var for var in original_vars if var in full_coefs]
        if add_constant:
            ordered_vars.append('_cons')
        
        ordered_results = {var: full_coefs[var] for var in ordered_vars}
        full_coefficients = pd.DataFrame.from_dict(ordered_results, orient='index')
        
        return model, keep_cols, drop_cols, reasons, full_coefficients
    else:
        return model, keep_cols, drop_cols, reasons
