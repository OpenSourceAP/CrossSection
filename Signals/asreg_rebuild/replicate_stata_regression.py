#!/usr/bin/env python3
# ABOUTME: Replicates Stata regression with collinearity handling
# ABOUTME: Drops collinear variables like Stata's regress command

# Inputs: None (generates test data)
# Outputs: Regression results matching Stata format
# How to run: python3 replicate_stata_regression.py

# see https://chatgpt.com/g/g-p-67e5a37babd0819184da8c8c39fc932f/c/68a7a776-2040-8321-885e-e415de787173

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

def drop_collinear(
    X: pd.DataFrame,
    y: pd.Series | np.ndarray | None = None,
    sample_mask: pd.Series | np.ndarray | None = None,
    *,
    rtol: float | None = None,
    method: str = "qr",          # "qr" (fast, needs SciPy) or "greedy" (no deps)
    scale: bool = True,          # column-normalize for numerics (improves stability)
    return_reduced_X: bool = True
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
    is_const = (ptp == 0)
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
            tol = (rtol if rtol is not None else (eps * max(n, A_test.shape[1]) * diagR.max()))
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
        tol = (rtol if rtol is not None else (eps * max(n, A_test.shape[1])))
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
    keep_cols = [c for c in cols if (c in keep_set) and (c not in reasons or reasons[c] != "constant")]
    # Everything else is dropped either as constant or collinear
    drop_cols = [c for c in cols if c not in keep_cols]

    if return_reduced_X:
        return keep_cols, drop_cols, reasons, Xs[keep_cols]
    else:
        return keep_cols, drop_cols, reasons, None


def format_regression_output(model, X_vars, omitted_vars):
    """Format regression output to match Stata style"""
    
    print("-" * 75)
    print(f"{'Variable':<12} {'Coefficient':<13} {'Std. err.':<11} {'t':<7} {'P>|t|':<7} {'[95% Conf. Interval]':<24}")
    print("-" * 75)
    
    # Print coefficients for included variables
    for i, var in enumerate(X_vars):
        coef = model.params[i]
        se = model.bse[i]
        t_stat = model.tvalues[i]
        p_val = model.pvalues[i]
        conf_low = model.conf_int()[0][i]
        conf_high = model.conf_int()[1][i]
        
        print(f"{var:<12} {coef:>13.7f} {se:>11.7f} {t_stat:>7.2f} {p_val:>7.3f} {conf_low:>12.7f} , {conf_high:<11.7f}")
        print()
    
    # Print omitted variables
    for var in omitted_vars:
        print(f"{var:<12} {'0':<13} {'(omitted)':<11}")
        print()
    
    # Print constant
    const_idx = len(X_vars)
    coef = model.params[const_idx]
    se = model.bse[const_idx]
    t_stat = model.tvalues[const_idx]
    p_val = model.pvalues[const_idx]
    conf_low = model.conf_int()[0][const_idx]
    conf_high = model.conf_int()[1][const_idx]
    
    print(f"{'_cons':<12} {coef:>13.7f} {se:>11.7f} {t_stat:>7.2f} {p_val:>7.3f} {conf_low:>12.7f} , {conf_high:<11.7f}")
    print("-" * 75)


def main():
    # Load test data from CSV
    df = pd.read_csv('tf_testdat.csv')
    
    # Prepare X and y
    X_cols = ['A_3', 'A_5', 'A_10', 'A_20', 'A_50', 'A_100', 'A_200', 'A_400', 'A_600', 'A_800', 'A_1000']
    X = df[X_cols]
    y = df['fRet']
    
    print("# Regression Output\n")
    
    # Apply collinearity detection
    keep_cols, drop_cols, reasons, X_reduced = drop_collinear(X, y=y)
    
    print(f"Kept columns: {keep_cols}")
    print(f"Dropped columns: {drop_cols}")
    print(f"Reasons: {reasons}\n")
    
    # Add constant
    X_with_const = sm.add_constant(X_reduced)
    
    # Run regression
    model = sm.OLS(y.loc[X_reduced.index], X_with_const).fit()
    
    # Format output to match Stata
    format_regression_output(model, keep_cols, drop_cols)
    
    # Print additional statistics
    print(f"\nNumber of obs = {len(X_reduced)}")
    print(f"R-squared = {model.rsquared:.4f}")
    print(f"Adj R-squared = {model.rsquared_adj:.4f}")
    print(f"Root MSE = {np.sqrt(model.mse_resid):.4f}")


if __name__ == "__main__":
    main()