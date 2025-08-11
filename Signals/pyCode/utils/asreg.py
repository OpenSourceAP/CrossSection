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
import polars_ols as pls  # registers .least_squares on pl.Expr

Mode = Literal["rolling", "expanding", "group"]

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
    null_policy: str = "skip",  # New parameter for handling nulls
    solve_method: str = "svd",  # New parameter for solver
) -> pl.DataFrame | pl.LazyFrame:
    """Multi-purpose OLS over groups/windows (compact 'asreg').
    
    Replicates Stata's asreg functionality with exact behavior matching.
    
    Args:
        df: Input DataFrame or LazyFrame
        y: Dependent variable column name
        X: Independent variable column names
        by: Grouping columns (e.g., ["permno"] for by-permno regressions)
        t: Time/order column for rolling/expanding windows
        mode: Regression mode - "rolling", "expanding", or "group"  
        window_size: Number of observations for rolling windows
        min_samples: Minimum observations required per regression
        add_intercept: Whether to include intercept term
        outputs: Which outputs to compute - "coef", "yhat", "resid", "rmse"
        coef_prefix: Prefix for coefficient column names
        collect: Whether to collect LazyFrame to DataFrame
        
    Returns:
        DataFrame/LazyFrame with requested regression outputs
        
    Examples:
        # CAPM Beta (60-month rolling, min 20, by permno)
        beta = asreg(
            df, y="retrf", X=["ewmktrf"],
            by=["permno"], t="time_avail_m",
            mode="rolling", window_size=60, min_samples=20,
            outputs=("coef",)
        )
        # Beta coefficient in column "b_ewmktrf"
        
        # Per-group regression with residuals
        result = asreg(
            df, y="ret", X=["mktrf","smb","hml"],
            by=["permno","month"], mode="group", min_samples=4,
            outputs=("coef","resid")
        )
    """
    lf = df.lazy() if isinstance(df, pl.DataFrame) else df
    p = len(X) + (1 if add_intercept else 0)
    min_samples = max(min_samples or p, 1)
    
    if mode != "group" and t is None:
        raise ValueError("t= (time/order column) is required for rolling/expanding")
    if mode == "rolling" and window_size is None:
        raise ValueError("window_size is required for rolling")
    if mode != "group":
        lf = lf.sort([*(by or []), t])  # deterministic window order

    yexpr = pl.col(y).least_squares
    Xexprs = [pl.col(c) for c in X]
    over = (by or [])
    
    if mode == "group":
        if "resid" in outputs and len(outputs) == 1:
            # Direct residuals mode - more efficient
            residuals = yexpr.ols(*Xexprs, add_intercept=add_intercept, mode="residuals",
                                 null_policy=null_policy, solve_method=solve_method).over(over)
            if by and min_samples > 1:
                residuals = pl.when(pl.len().over(by) >= min_samples).then(residuals).otherwise(None)
            lf = lf.with_columns(resid=residuals)
            return lf.collect() if collect else lf
        else:
            # Standard coefficient mode
            coef = yexpr.ols(*Xexprs, add_intercept=add_intercept, mode="coefficients", 
                             null_policy=null_policy, solve_method=solve_method).over(over)
            if by and min_samples > 1:
                coef = pl.when(pl.len().over(by) >= min_samples).then(coef).otherwise(None)
    elif mode == "rolling":
        coef = yexpr.rolling_ols(*Xexprs, window_size=window_size,
                                 min_periods=min_samples, add_intercept=add_intercept,
                                 mode="coefficients").over(over)
    else:  # expanding
        coef = yexpr.expanding_ols(*Xexprs,
                                   min_periods=min_samples, add_intercept=add_intercept,
                                   mode="coefficients").over(over)

    lf = lf.with_columns(coef=coef)

    need_coef_cols = any(o in {"coef", "yhat", "resid", "rmse"} for o in outputs)
    if need_coef_cols:
        cols = ([pl.col("coef").struct.field("const").alias(f"{coef_prefix}const")] if add_intercept else [])
        cols += [pl.col("coef").struct.field(x).alias(f"{coef_prefix}{x}") for x in X]
        lf = lf.with_columns(cols)

    if any(o in {"yhat", "resid", "rmse"} for o in outputs):
        yhat = (pl.col(f"{coef_prefix}const") if add_intercept else pl.lit(0.0))
        for x in X:
            yhat = yhat + pl.col(f"{coef_prefix}{x}") * pl.col(x)
        lf = lf.with_columns(yhat.alias("yhat"))

    if any(o in {"resid", "rmse"} for o in outputs):
        lf = lf.with_columns((pl.col(y) - pl.col("yhat")).alias("resid"))

    if "rmse" in outputs:
        # Calculate RMSE: sqrt(sum(residuals^2) / (n - k))  
        # where n is number of observations, k is number of parameters
        # (residuals were already calculated above)
        k = p  # number of parameters (including intercept if present)
        if mode == "rolling":
            # For rolling windows: each observation gets the RMSE from its window
            lf = lf.with_columns(
                (pl.col("resid").pow(2).rolling_sum(window_size, min_periods=min_samples).over(over) / 
                 (pl.col("resid").is_not_null().cast(pl.Int32).rolling_sum(window_size, min_periods=min_samples).over(over) - k).clip(lower_bound=1)
                ).sqrt().alias("rmse")
            )
        elif mode == "expanding":
            # For expanding windows: RMSE grows as window expands
            lf = lf.with_columns(
                (pl.col("resid").pow(2).cumsum().over(over) / 
                 (pl.int_range(pl.len()).over(over) + 1 - k).clip(lower_bound=1)
                ).sqrt().alias("rmse")
            )
        else:  # group
            # For group regressions: sqrt(sum(resid^2) / (n-k)) for each group
            lf = lf.with_columns(
                (pl.col("resid").pow(2).sum().over(over) / 
                 (pl.count().over(over) - k).clip(lower_bound=1)
                ).sqrt().alias("rmse")
            )

    if "coef" not in outputs:
        lf = lf.drop("coef")

    return lf.collect() if collect else lf