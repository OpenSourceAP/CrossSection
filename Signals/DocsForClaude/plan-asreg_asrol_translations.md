# Stata asreg/asrol Command Translations

## Overview
This document lists all .do files in `Code/Predictors/` that use Stata's `asreg` or `asrol` commands and describes the translation approaches used in Python.

## Files Using asreg/asrol (37 total)

### asreg Users (Rolling Regressions)
1. **Beta.do** - Rolling 60-month market beta regression
2. **BetaLiquidityPS.do** - Liquidity beta using asreg
3. **BetaTailRisk.do** - Tail risk beta estimation
4. **CitationsRD.do** - Uses asreg for patent citation analysis
5. **Coskewness.do** - Coskewness with market returns
6. **Investment.do** - Investment rolling mean
7. **MS.do** - Uses asreg for momentum strategy
8. **MomOffSeason.do** - Off-season momentum with asreg
9. **MomOffSeason06YrPlus.do** - 6+ year momentum
10. **MomOffSeason11YrPlus.do** - 11+ year momentum
11. **MomOffSeason16YrPlus.do** - 16+ year momentum
12. **Mom12mOffSeason.do** - 12-month off-season momentum
13. **MomVol.do** - Momentum volatility regression
14. **RDAbility.do** - R&D ability estimation
15. **Recomm_ShortInterest.do** - Analyst recommendations regression
16. **TrendFactor.do** - Trend factor estimation
17. **VarCF.do** - Cash flow variance regression
18. **VolMkt.do** - Market volatility regression
19. **VolSD.do** - Volatility standard deviation
20. **VolumeTrend.do** - Volume trend regression
21. **ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.do** - FF3 residuals
22. **ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.do** - Analyst value regressions
23. **ZZ1_ResidualMomentum6m_ResidualMomentum.do** - Rolling FF3 for residual momentum
24. **ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.do** - Real investment opportunities
25. **ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.do** - Abnormal accruals regression
26. **ZZ2_BetaFP.do** - Frazzini-Pedersen beta
27. **ZZ2_IdioVolAHT.do** - Idiosyncratic volatility
28. **ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.do** - Price delay regressions
29. **ZZ2_betaVIX.do** - VIX beta estimation

### asrol Users (Rolling Statistics)
1. **DivInit.do** - Rolling dividend statistics
2. **DivOmit.do** - Dividend omission tracking
3. **DivSeason.do** - Seasonal dividend patterns
4. **DivYieldST.do** - Short-term dividend yield
5. **Herf.do** - Herfindahl index calculation
6. **HerfAsset.do** - Asset-based Herfindahl
7. **HerfBE.do** - Book equity Herfindahl
8. **std_turn.do** - Standard deviation of turnover

## Translation Approaches

### Example 1: ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F

**Stata Code:**
```stata
bys permno time_avail_m: asreg ret mktrf smb hml, fit
```

**Python Translation Approach:**
- Uses `polars-ols` library for efficient grouped regressions
- Leverages polars' `least_squares.ols()` with `.over()` for by-group operations
- Key implementation:
```python
df_with_residuals = df.with_columns(
    pl.col("ret")
    .least_squares.ols(
        "mktrf", "smb", "hml", 
        mode="residuals", 
        add_intercept=True,
        null_policy="drop",
        solve_method="svd"
    )
    .over(["permno", "time_avail_m"])
    .alias("_residuals")
)
```

**Key Features:**
- Fast vectorized regression using polars-ols
- Handles missing values with `null_policy="drop"`
- Uses SVD for numerical stability
- Preserves Stata's _Nobs and _residuals naming convention

### Example 2: ZZ1_ResidualMomentum6m_ResidualMomentum

**Stata Code:**
```stata
asreg retrf mktrf hml smb, window(time_temp 36) min(36) by(permno) fit
asrol temp, window(time_temp 6) min(6) by(permno) stat(mean) gen(mean6_temp)
asrol temp, window(time_temp 6) min(6) by(permno) stat(sd) gen(sd6_temp)
```

**Python Translation Approach:**
- Custom rolling window regression function using numpy
- Pandas rolling statistics for asrol replacement
- Key implementation:

**For asreg (rolling regression):**
```python
def compute_rolling_residuals(group):
    for i in range(35, n):  # 36-month window
        window_idx = slice(i-35, i+1)
        # Extract window data and run OLS
        X_with_const = np.column_stack([np.ones(len(y_clean)), X_clean])
        coef = np.linalg.lstsq(X_with_const, y_clean, rcond=None)[0]
        # Calculate residual
        residuals[i] = y[i] - fitted
```

**For asrol (rolling statistics):**
```python
# Replace asrol with pandas rolling
df['mean6_temp'] = df.groupby('permno')['temp'].transform(
    lambda x: x.rolling(window=6, min_periods=6).mean()
)
df['sd6_temp'] = df.groupby('permno')['temp'].transform(
    lambda x: x.rolling(window=6, min_periods=6).std()
)
```

## Translation Strategy Summary

### For asreg (Rolling Regressions):
1. **Within-group regressions**: Use `polars-ols` with `.over()` grouping
2. **Rolling window regressions**: Custom numpy-based function with manual window management
3. **Handle minimum observations**: Explicit checks for `min()` parameter
4. **Preserve output columns**: Match Stata's `_b_`, `_residuals`, `_Nobs` naming

### For asrol (Rolling Statistics):
1. **Simple statistics (mean, sd)**: Use pandas `.rolling()` with appropriate window
2. **Complex statistics**: Custom rolling window functions
3. **By-group operations**: Use `.groupby().transform()` pattern
4. **Window specifications**: Convert Stata's window syntax to pandas window parameter

## Common Pitfalls and Solutions

1. **Window indexing**: Stata uses 1-based indexing, Python uses 0-based
2. **Missing data handling**: Stata's asreg handles NaN differently than numpy/pandas
3. **Minimum observations**: Must explicitly enforce Stata's `min()` parameter
4. **Performance**: Large datasets may require chunking or optimization
5. **Numerical precision**: Use appropriate solver methods (SVD vs normal equations)

## Testing Recommendations

When translating asreg/asrol code:
1. Compare residuals and coefficients for small test cases
2. Verify window boundaries match Stata's behavior
3. Check edge cases (start/end of time series)
4. Validate missing data handling
5. Test performance on full dataset

## Notes

- Total of 37 predictor files use asreg/asrol
- asreg is primarily used for rolling regressions (betas, residuals)
- asrol is primarily used for rolling statistics (mean, std, etc.)
- Translation complexity varies based on window type and regression specification