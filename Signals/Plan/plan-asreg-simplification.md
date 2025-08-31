# Plan: asreg simplification

# Part 1: asreg_polars 

From analysis of 10 completed predictor scripts, `asreg_polars` is used in two main patterns:

**Rolling Mode (7 scripts):**
- Beta.py: 60-day rolling, 20 min samples
- BetaLiquidityPS.py: 60-day rolling, 36 min samples  
- BetaTailRisk.py: 120-day rolling, 72 min samples
- RDAbility.py: 8-year rolling, 6 min samples
- ZZ1_ResidualMomentum6m_ResidualMomentum.py: 36-day rolling, 36 min samples
- ZZ2_betaVIX.py: 20-day rolling, 15 min samples
- ZZ2_IdioVolAHT.py: 252-day rolling, 100 min samples

**Group Mode (3 scripts):**
- ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py: Groups by permno-month, 15 min samples
- ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py: Groups by time_avail_m
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py: Groups by fyear-sic2, 1 min sample

**Unused Mode:**
- Expanding mode: Available but not used in any completed scripts

### Current asreg_polars Wrapper Complexity

The `asreg_polars` function in `utils/asreg.py` is ~200 lines of wrapper code that:
- Translates parameters between custom API and polars-ols
- Handles three modes (rolling, expanding, group)
- Manages coefficient output formatting
- Provides residual computation via manual calculation

## Direct polars-ols Alternative

### polars-ols Core Methods
- `pl.col("y").least_squares.ols()` - Basic OLS regression
- `pl.col("y").least_squares.rolling_ols()` - Rolling window regressions  
- `pl.col("y").least_squares.expanding_ols()` - Expanding window regressions

### Supported Modes
- `mode="predictions"` (default)
- `mode="residuals"`
- `mode="coefficients"` 
- `mode="statistics"` (OLS/WLS/Ridge only)

### Direct Equivalents

**Current Rolling Pattern:**
```python
df_with_beta = asreg_polars(
    df, y="retrf", X=["ewmktrf"], by=["permno"], 
    t="time_temp", mode="rolling", window_size=60, 
    min_samples=20, outputs=("coef",), coef_prefix="b_"
)
```

**Direct polars-ols:**
```python
df_with_beta = df.with_columns(
    pl.col("retrf").least_squares.rolling_ols(
        pl.col("ewmktrf"),
        window_size=60,
        min_periods=20,
        mode="coefficients",
        add_intercept=True
    ).over(["permno"]).alias("coef")
).with_columns([
    pl.col("coef").struct.field("const").alias("b_const"),
    pl.col("coef").struct.field("ewmktrf").alias("b_ewmktrf")
])
```

**Current Group Pattern:**
```python
df_with_residuals = asreg_polars(
    df, y="ret", X=["mktrf", "smb", "hml"], 
    by=["permno", "time_avail_m"], mode="group", 
    min_samples=15, outputs=("resid",)
)
```

**Direct polars-ols:**
```python
df_with_residuals = df.with_columns(
    pl.col("ret").least_squares.ols(
        pl.col("mktrf"), pl.col("smb"), pl.col("hml"),
        mode="residuals",
        add_intercept=True,
        null_policy="drop"
    ).over(["permno", "time_avail_m"]).alias("resid")
)
```

# Part 2: asreg_collinear

`asreg.py`'s `asreg_collinear`

Notes:
- used only in TrendFactor.py
    - but could potentially be used elsewhere 
- relies on stata_regress.py's regress
- stata_regress.py is only used through `asreg_collinear`


Plan:
- Move all of `asreg_collinear` related code into `TrendFactor.py`
    - Including all functions that it calls, directly or indirectly.