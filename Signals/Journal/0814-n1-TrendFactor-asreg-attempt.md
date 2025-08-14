# TrendFactor asreg attempt 

Long story short: improving the asreg replication in TrendFactor.py does not help.

There was a flaw with the asreg.py: it doesn't replicate Stata's asreg for when there are too few observations to run a proper regression. Stata does some weird workaround and still provides coefficients, though many may be zero. 

We did a decent but not great replication of this process. But it made no difference in the Precision1 scores.

The updated asreg.py file was much much longer. Not worth it.

# Full asreg.py file

```
# ABOUTME: asreg.py - Stata-style asreg functionality using polars and polars-ols
# ABOUTME: Provides compact, general asreg-style helper for OLS over groups/windows

"""
asreg.py

Multi-purpose OLS over groups/windows (compact 'asreg') that replicates Stata's asreg behavior.
Uses polars and polars-ols for performance while maintaining exact compatibility with Stata.

Usage:
    from utils.asreg import asreg
    
    # Rolling 60-observation CAPM regression by permno
    result = asreg(
        df, y="retrf", X=["ewmktrf"],
        by=["permno"], t="time_avail_m", 
        mode="rolling", window_size=60, min_samples=20,
        outputs=("coef",)
    )

Functions:
    asreg() - Main regression function supporting rolling, expanding, and group modes
"""

from typing import Iterable, Literal, Sequence, Optional
import polars as pl
import polars_ols  # registers .least_squares on pl.Expr
import numpy as np

Mode = Literal["rolling", "expanding", "group"]


def _select_independent_columns_qr(X, tol=None):
    """
    Rank-revealing QR with column pivoting to find an independent set of columns.
    Returns indices of columns to keep (in original order) and the estimated rank.
    """
    try:
        from scipy.linalg import qr as sp_qr
    except Exception:
        return None, None  # signal: fall back to SVD

    # Column-pivoted QR
    Q, R, piv = sp_qr(X, mode='economic', pivoting=True)
    # Rank via diag(R) threshold
    if tol is None:
        eps = np.finfo(R.dtype).eps if np.issubdtype(R.dtype, np.floating) else 1e-12
        tol = max(X.shape) * eps * np.abs(R.diagonal()).max(initial=0.0)
    rank = int(np.sum(np.abs(np.diag(R)) > tol))
    keep_piv = np.sort(piv[:rank])   # back to original order
    return keep_piv.astype(int), rank


def _select_independent_columns_svd(X, tol=None):
    """
    Fallback when SciPy is unavailable: use SVD to estimate rank,
    then greedily pick columns that improve rank.
    """
    U, s, Vt = np.linalg.svd(X, full_matrices=False)
    if tol is None:
        tol = max(X.shape) * np.finfo(s.dtype).eps * (s[0] if s.size else 0.0)
    target_rank = int(np.sum(s > tol))
    if target_rank == 0:
        return np.array([], dtype=int), 0

    # Greedy Gram–Schmidt on columns (deterministic & stable enough for our use)
    keep = []
    proj = np.zeros((X.shape[0], 0), dtype=X.dtype)
    for j in range(X.shape[1]):
        col = X[:, [j]]
        if proj.size:
            # project col on span(proj) and take residual
            coeff = np.linalg.lstsq(proj, col, rcond=None)[0]
            resid = col - proj @ coeff
        else:
            resid = col
        if np.linalg.norm(resid) > tol:
            keep.append(j)
            proj = np.hstack([proj, resid / (np.linalg.norm(resid) + 1e-32)])
        if len(keep) == target_rank:
            break
    return np.array(keep, dtype=int), len(keep)


def _ols_stata_omits(X, y, add_const=True, drop_zero_var=True):
    """
    Solve OLS with Stata-like handling of collinearity:
      - Fit only on a full-rank subset of columns
      - Return full-length coefficient vector where omitted coefficients are 0
      - VCE expanded with zeros for omitted rows/cols
      - SE and t are NaN for omitted; rank reflects effective parameters

    Parameters
    ----------
    X : (n, p) array
    y : (n,) array
    add_const : if True, prepend an intercept column
    drop_zero_var : if True, pre-drop columns with no variation in-window

    Returns
    -------
    result : dict with keys:
      'beta' : (p_full,) coefficients with zeros for omitted
      'se'   : (p_full,) standard errors (NaN for omitted or if df<=0)
      't'    : (p_full,) t-stats (NaN for omitted or if df<=0)
      'V'    : (p_full, p_full) variance-covariance (zeros on omitted blocks)
      'rank' : effective rank used in the fit
      'nobs' : number of rows used
      'df_resid' : nobs - rank
      'mask_keep_cols' : boolean mask over full columns (True if included in fit)
    """
    y = np.asarray(y).reshape(-1)
    X = np.asarray(X)
    n = X.shape[0]

    # Add constant (like Stata's default)
    if add_const:
        X = np.column_stack([np.ones((n, 1), dtype=X.dtype), X])
        const_added = 1
    else:
        const_added = 0

    p_full = X.shape[1]

    # Drop rows with any NaN in X or y
    rowmask = np.isfinite(y)
    rowmask &= np.all(np.isfinite(X), axis=1)
    Xw = X[rowmask]
    yw = y[rowmask]
    nobs = Xw.shape[0]

    # Nothing to estimate
    if nobs == 0:
        return dict(beta=np.zeros(p_full), se=np.full(p_full, np.nan),
                    t=np.full(p_full, np.nan), V=np.zeros((p_full, p_full)),
                    rank=0, nobs=0, df_resid=np.nan,
                    mask_keep_cols=np.zeros(p_full, dtype=bool))

    # Optionally pre-drop zero-variance columns (within window)
    keep_mask = np.ones(p_full, dtype=bool)
    if drop_zero_var:
        col_std = Xw.std(axis=0)
        keep_mask &= col_std > 0
        # Fix: Always preserve intercept column if it was added
        if add_const:
            keep_mask[0] = True  # Force keep intercept column

    # If everything dropped, try to keep just the constant (if present)
    if not np.any(keep_mask):
        if add_const:
            keep_mask[0] = True  # keep intercept only
        else:
            # No estimable columns
            return dict(beta=np.zeros(p_full), se=np.full(p_full, np.nan),
                        t=np.full(p_full, np.nan), V=np.zeros((p_full, p_full)),
                        rank=0, nobs=nobs, df_resid=np.nan,
                        mask_keep_cols=np.zeros(p_full, dtype=bool))

    Xc = Xw[:, keep_mask]

    # Choose independent subset via QR pivoting; fall back to SVD if needed
    keep_idx_rel, rank = _select_independent_columns_qr(Xc)
    if keep_idx_rel is None:  # SciPy not available
        keep_idx_rel, rank = _select_independent_columns_svd(Xc)

    if rank == 0:
        # Only constant may remain, or truly nothing
        beta_full = np.zeros(p_full)
        V_full = np.zeros((p_full, p_full))
        return dict(beta=beta_full, se=np.full(p_full, np.nan),
                    t=np.full(p_full, np.nan), V=V_full,
                    rank=0, nobs=nobs, df_resid=np.nan,
                    mask_keep_cols=np.zeros(p_full, dtype=bool))

    # Map selected columns back to full X
    keep_cols_abs = np.where(keep_mask)[0][keep_idx_rel]
    X_sel = Xw[:, keep_cols_abs]

    # Solve OLS on the selected columns
    beta_sel, residuals, rnk, svals = np.linalg.lstsq(X_sel, yw, rcond=None)
    # RSS and sigma^2
    # residuals from lstsq: sum of squares residuals; if underdetermined, compute explicitly
    if residuals.size == 0:
        yhat = X_sel @ beta_sel
        rss = float(np.sum((yw - yhat) ** 2))
    else:
        rss = float(residuals[0])

    df_resid = nobs - rank
    if df_resid > 0:
        sigma2 = rss / df_resid
    else:
        sigma2 = np.nan

    # Variance-covariance on selected set
    try:
        XtX_inv = np.linalg.inv(X_sel.T @ X_sel)
        V_sel = sigma2 * XtX_inv if np.isfinite(sigma2) else np.full_like(XtX_inv, np.nan, dtype=float)
    except np.linalg.LinAlgError:
        V_sel = np.full((rank, rank), np.nan)

    # Expand beta and V to full size with zeros in omitted slots (Stata-like)
    beta_full = np.zeros(p_full, dtype=float)
    beta_full[keep_cols_abs] = beta_sel

    V_full = np.zeros((p_full, p_full), dtype=float)
    if np.all(np.isfinite(V_sel)):
        for i, ci in enumerate(keep_cols_abs):
            for j, cj in enumerate(keep_cols_abs):
                V_full[ci, cj] = V_sel[i, j]
    else:
        # If V_sel has NaNs due to df<=0 or inversion issues, keep zeros elsewhere
        V_full[:, :] = 0.0
        if V_sel.shape[0] == V_sel.shape[1] == rank:
            for i, ci in enumerate(keep_cols_abs):
                for j, cj in enumerate(keep_cols_abs):
                    V_full[ci, cj] = V_sel[i, j]

    # Standard errors and t-stats
    se_full = np.sqrt(np.diag(V_full))
    # For omitted coefficients, the diagonal is 0 => se = 0; make them NaN to avoid fake t=inf/0
    omitted = (se_full == 0.0) & (~np.isclose(beta_full, 0.0))
    se_full[se_full == 0.0] = np.nan  # Stata shows omitted SE as missing; mirror that

    with np.errstate(invalid='ignore', divide='ignore'):
        t_full = beta_full / se_full

    return dict(
        beta=beta_full,
        se=se_full,
        t=t_full,
        V=V_full,
        rank=rank,
        nobs=nobs,
        df_resid=df_resid,
        mask_keep_cols=np.isin(np.arange(p_full), keep_cols_abs)
    )


def _apply_group_ols_stata_style(lf: pl.LazyFrame, y: str, X: Sequence[str], over: Sequence[str], 
                                add_intercept: bool, min_samples: int) -> pl.LazyFrame:
    """
    Apply Stata-style OLS with collinearity handling to each group.
    Modifies the LazyFrame by adding coefficient columns (_coef_<name>).
    """
    # Convert to eager for group processing
    df = lf.collect()
    
    # Build coefficient names in the same order polars_ols would use
    coef_names = []
    if add_intercept:
        coef_names.append("const")
    coef_names.extend(X)
    
    # Initialize coefficient columns with nulls
    coef_cols = []
    for name in coef_names:
        df = df.with_columns(pl.lit(None, dtype=pl.Float64).alias(f"_coef_{name}"))
    
    if over:
        # Group by the specified columns and process each group
        for group_data in df.group_by(over, maintain_order=True):
            # group_data is a tuple (group_key, group_df)
            group_key, group_df = group_data
            
            # Extract data for this group
            y_data = group_df[y].to_numpy()
            X_data = group_df.select(X).to_numpy()
            
            # Check if we have enough samples
            valid_mask = np.isfinite(y_data) & np.all(np.isfinite(X_data), axis=1)
            n_valid = np.sum(valid_mask)
            
            if n_valid >= min_samples:
                # Run Stata-style OLS
                ols_result = _ols_stata_omits(X_data, y_data, add_const=add_intercept)
                beta = ols_result['beta']
                
                # Update coefficients for this group
                group_filter = True
                for i, col_name in enumerate(over):
                    group_filter = group_filter & (pl.col(col_name) == group_key[i])
                
                coef_updates = []
                for i, name in enumerate(coef_names):
                    coef_updates.append(
                        pl.when(group_filter).then(beta[i]).otherwise(pl.col(f"_coef_{name}"))
                        .alias(f"_coef_{name}")
                    )
                df = df.with_columns(coef_updates)
            # If not enough samples, coefficients remain null for this group
    else:
        # No grouping - apply to entire dataset
        y_data = df[y].to_numpy() 
        X_data = df.select(X).to_numpy()
        
        valid_mask = np.isfinite(y_data) & np.all(np.isfinite(X_data), axis=1)
        n_valid = np.sum(valid_mask)
        
        if n_valid >= min_samples:
            ols_result = _ols_stata_omits(X_data, y_data, add_const=add_intercept)
            beta = ols_result['beta']
            
            # Update all coefficients
            coef_updates = []
            for i, name in enumerate(coef_names):
                coef_updates.append(pl.lit(beta[i]).alias(f"_coef_{name}"))
            df = df.with_columns(coef_updates)
    
    return df.lazy()


def _valid_mask(y: str, X: Sequence[str]) -> pl.Expr:
    """Row-wise validity mask: True where y and all X are non-null."""
    m = pl.col(y).is_not_null()
    for x in X:
        m = m & pl.col(x).is_not_null()
    return m


def _agg_sum(expr: pl.Expr, *, mode: Mode, over: Sequence[str], window_size: Optional[int], min_samples: int) -> pl.Expr:
    """Aggregate `expr` according to mode (rolling/expanding/group) and groups `over`."""
    if mode == "rolling":
        return expr.rolling_sum(window_size, min_periods=min_samples).over(over)
    elif mode == "expanding":
        return expr.cumsum().over(over)
    else:
        # group mode: sum per group, broadcast back to rows
        return expr.sum().over(over)




def asreg(
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
    omit_collinear: bool = False,
    collinear_tol: float = 1e-10,
) -> pl.DataFrame | pl.LazyFrame:
    """Multi-purpose OLS over groups/windows (compact 'asreg').

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
        omit_collinear: Whether to handle collinear variables like Stata (set coef=0 instead of null)
        collinear_tol: Tolerance for detecting perfect collinearity (default 1e-10)

    Returns:
        DataFrame/LazyFrame with requested regression outputs
    """
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
                n_eff_grp = _valid_mask(y, X).cast(pl.Int64).sum().over(over)
                residuals = pl.when(n_eff_grp >= min_samples).then(residuals).otherwise(None)
            lf = lf.with_columns(resid=residuals)
            return lf.collect() if collect else lf
        # standard coefficients - use custom handler for omit_collinear=True
        if omit_collinear:
            # Use custom group processing for Stata-style collinearity handling
            lf = _apply_group_ols_stata_style(lf, y, X, over, add_intercept, min_samples)
            # Create a dummy struct column for compatibility
            coef_names = (["const"] if add_intercept else []) + list(X)
            coef = pl.struct([pl.col(f"_coef_{name}").alias(name) for name in coef_names])
        else:
            # Use standard polars_ols
            coef = yexpr.ols(
                *Xexprs,
                add_intercept=add_intercept,
                mode="coefficients",
                null_policy=null_policy,
                solve_method=solve_method,
            ).over(over)
            if over and min_samples > 1:
                n_eff_grp = _valid_mask(y, X).cast(pl.Int64).sum().over(over)
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
            coef_col_expr = pl.col("coef").struct.field("const").alias(f"{coef_prefix}const")
            if omit_collinear:
                # Replace nulls with 0.0 for Stata compatibility
                coef_col_expr = coef_col_expr.fill_null(0.0)
            coef_cols.append(coef_col_expr)
        
        for x in X:
            coef_col_expr = pl.col("coef").struct.field(x).alias(f"{coef_prefix}{x}")
            if omit_collinear:
                # Replace nulls with 0.0 for Stata compatibility
                coef_col_expr = coef_col_expr.fill_null(0.0)
            coef_cols.append(coef_col_expr)
            
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
        valid = _valid_mask(y, X)

        def z_expr(name: str) -> pl.Expr:
            return pl.lit(1.0) if name == "__const__" else pl.col(name)

        # names of design columns Z (include intercept as "__const__")
        Z_names = (["__const__"] if add_intercept else []) + list(X)

        # Helper to mask invalid rows (skip nulls)
        def mask(expr: pl.Expr) -> pl.Expr:
            return pl.when(valid).then(expr).otherwise(None)

        # Aggregate builders (per mode)
        agg = lambda e: _agg_sum(mask(e), mode=mode, over=over, window_size=window_size, min_samples=min_samples)

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
        n_eff = _agg_sum(valid.cast(pl.Int64), mode=mode, over=over, window_size=window_size, min_samples=min_samples)
        dof = (n_eff - k)

        rmse_expr = pl.when((dof > 0) & SSE.is_not_null())
        rmse_expr = rmse_expr.then((SSE / dof.cast(pl.Float64)).sqrt()).otherwise(None)
        lf = lf.with_columns(rmse=rmse_expr)

    # Drop struct unless explicitly requested
    if "coef" not in outputs:
        lf = lf.drop("coef")

    return lf.collect() if collect else lf
```    