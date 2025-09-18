# ABOUTME: Idiosyncratic risk predictor using RMSE from 252-day rolling CAPM regression
# ABOUTME: Usage: python3 ZZ2_IdioVolAHT.py (run from pyCode/ directory)

import polars as pl
import sys
import os
from typing import List, Dict, Tuple, Optional, Sequence, Iterable, Literal, Union
import polars_ols as pls  # Registers .least_squares namespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
# from utils.asreg import asreg_polars
from utils.save_standardized import save_predictor

# %% custom asreg function
# the standard polars-ols rolling regression works fine
# but to match Stata exactly, for now, we'll use this custom function


Mode = Literal["rolling", "expanding", "group"]


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
        raise ImportError(
            "polars-ols is required for asreg_polars. Install with: pip install polars-ols"
        )

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
                residuals = (
                    pl.when(n_eff_grp >= min_samples).then(residuals).otherwise(None)
                )
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
            coef_cols.append(
                pl.col("coef").struct.field("const").alias(f"{coef_prefix}const")
            )
        coef_cols += [
            pl.col("coef").struct.field(x).alias(f"{coef_prefix}{x}") for x in X
        ]
        lf = lf.with_columns(coef_cols)

    # yhat / resid via manual calculation to avoid polars-ols predict issues
    if any(o in {"yhat", "resid", "rmse"} for o in outputs):
        yhat = pl.col(f"{coef_prefix}const") if add_intercept else pl.lit(0.0)
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
        agg = lambda e: _agg_sum_polars(
            mask(e),
            mode=mode,
            over=over,
            window_size=window_size,
            min_samples=min_samples,
        )

        # Moment sums
        yy = agg(pl.col(y) * pl.col(y)).cast(pl.Float64)

        zy = {zi: agg(z_expr(zi) * pl.col(y)).cast(pl.Float64) for zi in Z_names}

        zz = {}
        for i, zi in enumerate(Z_names):
            for j, zj in enumerate(Z_names[i:]):
                zz[(zi, Z_names[i + j])] = agg(
                    z_expr(zi) * z_expr(Z_names[i + j])
                ).cast(pl.Float64)

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
        n_eff = _agg_sum_polars(
            valid.cast(pl.Int64),
            mode=mode,
            over=over,
            window_size=window_size,
            min_samples=min_samples,
        )
        dof = n_eff - k

        rmse_expr = pl.when((dof > 0) & SSE.is_not_null())
        rmse_expr = rmse_expr.then((SSE / dof.cast(pl.Float64)).sqrt()).otherwise(None)
        lf = lf.with_columns(rmse=rmse_expr)

    # Drop struct unless explicitly requested
    if "coef" not in outputs:
        lf = lf.drop("coef")

    return lf.collect() if collect else lf


def _valid_mask_polars(y: str, X: Sequence[str]) -> pl.Expr:
    """Row-wise validity mask: True where y and all X are non-null."""
    m = pl.col(y).is_not_null()
    for x in X:
        m = m & pl.col(x).is_not_null()
    return m


def _agg_sum_polars(
    expr: pl.Expr,
    *,
    mode: Mode,
    over: Sequence[str],
    window_size: Optional[int],
    min_samples: int,
) -> pl.Expr:
    """Aggregate `expr` according to mode (rolling/expanding/group) and groups `over`."""
    if mode == "rolling":
        return expr.rolling_sum(window_size, min_periods=min_samples).over(over)
    elif mode == "expanding":
        return expr.cumsum().over(over)
    else:
        # group mode: sum per group, broadcast back to rows
        return expr.sum().over(over)


# %% main
print("Starting ZZ2_IdioVolAHT.py...")

# Data load
print("Loading daily CRSP and Fama-French data...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")


# Select required columns
df = daily_crsp.select(["permno", "time_d", "ret"])
print(f"Daily CRSP data: {df.shape[0]} rows")

# Merge with FF data
print("Merging with Fama-French factors...")
df = df.join(daily_ff.select(["time_d", "rf", "mktrf"]), on="time_d", how="inner")
print(f"After merge: {df.shape[0]} rows")

# Calculate excess return (Stata: replace ret = ret - rf)
df = df.with_columns([(pl.col("ret") - pl.col("rf")).alias("ret")])


# Critical: Filter out missing returns before creating time index
# This ensures rolling windows contain exactly 252 valid observations
df = df.filter(pl.col("ret").is_not_null() & pl.col("mktrf").is_not_null())

# Critical: Sort data first (from Beta.py success pattern)
df = df.sort(["permno", "time_d"])

# Set up time index for rolling window (Stata: time_temp = _n)
df = df.with_columns([pl.int_range(pl.len()).over("permno").alias("time_temp")])


# Use utils/asreg.py helper for rolling regression with RMSE
print("Running 252-day rolling CAPM regressions...")
# This replicates: asreg ret mktrf, window(time_temp 252) min(100) by(permno) rmse
df = asreg_polars(
    df,
    y="ret",  # Excess return (already calculated above)
    X=["mktrf"],
    by=["permno"],
    t="time_temp",
    mode="rolling",
    window_size=252,
    min_samples=100,
    add_intercept=True,  # Stata's asreg includes intercept by default
    outputs=("rmse",),  # Only need RMSE output (equivalent to Stata's _rmse)
    coef_prefix="b_",
)


print("Calculating idiosyncratic volatility...")
# Extract IdioVolAHT from RMSE (rename _rmse IdioVolAHT in Stata)
df = df.with_columns([pl.col("rmse").alias("IdioVolAHT")])

# Convert to monthly and keep last observation per month
df = df.with_columns([pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")])

# Keep last non-missing IdioVolAHT per permno-month (Stata: gcollapse (lastnm))
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg(
    [pl.col("IdioVolAHT").drop_nulls().last().alias("IdioVolAHT")]
)


# Select final data
result = df.select(["permno", "time_avail_m", "IdioVolAHT"])
print(f"Calculated IdioVolAHT for {result.shape[0]} observations")

# Save predictor
save_predictor(result, "IdioVolAHT")
print("ZZ2_IdioVolAHT.py completed successfully")
