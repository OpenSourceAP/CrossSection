# Precision1 Failure Pattern Analysis
**Date:** 2025-08-09  
**Source:** Logs/testout_predictors 0808n6.md  
**Task:** Investigate worst Precision1 failures for systematic patterns

## Summary
Analysis of 50+ predictors reveals systematic translation errors in complex calculations, not just precision loss. The worst failures show fundamental differences in calculation logic, data filtering, and mathematical formulas between Stata and Python implementations.

## Key Metric Definition
- **std_diff** = (python_value - stata_value) / std(all_stata_values)  
- **Precision1 failure**: When >0.1% of observations have std_diff >= 0.01
- **Worst failures**: >50% of observations failing Precision1 test

## Worst Precision1 Failures (>90% failure rate)

### 1. BetaTailRisk: 99.651% failure
```
Python vs Stata examples:
permno  yyyymm    python     stata      diff
10026   202412   0.016994   0.324815  -0.307821
10028   202412   0.073846  -0.427242   0.501088
10032   202412   0.035983   0.523027  -0.487044
```
**Pattern**: Systematic magnitude differences, Python values consistently smaller in absolute terms

### 2. Coskewness: 99.358% failure  
```
Status: Missing 407,320 Stata observations
Python vs Stata examples:
permno  yyyymm    python     stata      diff
10026   202401  -0.281231  -0.352961   0.071730
10032   202401   0.157133  -0.264077   0.421210
10044   202401   0.166441  -0.194824   0.361266
```
**Pattern**: Sign reversals + missing historical observations (1987-2016 period)

### 3. TrendFactor: 98.418% failure
```
Status: Missing 1,452 Stata observations  
Python vs Stata examples:
permno  yyyymm    python     stata      diff
10026   202412  -0.094924   0.032569  -0.127493
10032   202412  -0.092298   0.035968  -0.128266
10104   202412  -0.093959   0.034036  -0.127994
```
**Pattern**: Consistent sign reversal - Python negative, Stata positive

### 4. CompEquIss: 97.716% failure
```
100th percentile diff = 1.96e+03 (extreme magnitude difference)
Python vs Stata examples:
permno  yyyymm    python     stata      diff
10026   202412  -0.142015  -0.061804  -0.080211
10032   202412   0.633364  -0.400428   1.033791
10044   202412  -1.098442  -0.365838  -0.732604
```
**Pattern**: Extreme magnitude differences suggesting different calculation formulas

### 5. Mom12mOffSeason: 91.884% failure
**Pattern**: Systematic bias in momentum calculations

## Systematic Patterns Identified

### Pattern 1: Sign Reversals/Mathematical Formula Differences
**Predictors:** TrendFactor, Coskewness (partial), BetaTailRisk  
**Cause:** Fundamental differences in calculation logic
- TrendFactor: Python consistently negative, Stata positive
- Suggests opposite signs in regression coefficients or different mathematical operations

### Pattern 2: Missing Historical Observations  
**Predictors:** Coskewness (-407K), retConglomerate (-169K), TrendFactor (-1.4K)  
**Cause:** Different data filtering windows or availability logic
- Coskewness missing early observations (1987-2016 period visible in sample)
- retConglomerate significant observation loss suggests different inclusion criteria

### Pattern 3: Extreme Magnitude Differences
**Predictors:** CompEquIss (diff=1.96e+03), PriceDelaySlope (diff=1.6e+04)  
**Cause:** Different scaling factors or completely different formulas
- These are not precision issues - they're different calculations entirely

### Pattern 4: Consistent Temporal Bias
**All failing predictors:** Most recent bad observations from 202401-202412  
**Implication:** Translation errors are systematic across time, not edge cases

### Pattern 5: Complexity Correlation
**Successful predictors:** BM (0.03% failure), Accruals (0.01% failure), GP (0.01% failure)  
**Failed predictors:** Complex calculations involving rolling windows, betas, momentum  
**Implication:** Simple accounting ratios translate well; complex financial calculations fail

## Systematic Categorization of All Precision1 Failures

### Category A: Critical Formula Errors (>95% failure rate)
**Complete breakdown of calculation logic**
| Predictor | Failure Rate | Pattern | Root Cause |
|-----------|-------------|---------|------------|
| BetaTailRisk | 99.651% | Magnitude differences | Rolling window regression errors |
| Coskewness | 99.358% | Sign reversals + missing 407K obs | Co-moment calculation + data filtering |
| TrendFactor | 98.418% | Sign flip (Python-, Stata+) | Coefficient sign error |
| CompEquIss | 97.716% | Extreme magnitude (diff=1.96e+03) | Formula completely wrong |

### Category B: Severe Calculation Errors (80-95% failure rate)  
**Major systematic biases**
| Predictor | Failure Rate | Pattern | Root Cause |
|-----------|-------------|---------|------------|
| retConglomerate | 94.057% | Missing 169K obs + differences | Complex calculation + data filtering |
| Mom12mOffSeason | 91.884% | Momentum calculation bias | Rolling window/seasonal logic |

### Category C: High Precision Errors (50-80% failure rate)
**Significant but not total calculation breakdown**
| Predictor | Failure Rate | Pattern | Root Cause |
|-----------|-------------|---------|------------|
| BetaLiquidityPS | 80.820% | Beta calculation differences | Regression estimation errors |
| Beta | 70.708% | Beta estimation bias | Rolling window regression |
| betaVIX | 69.594% | VIX beta differences | Market beta calculation |
| IntanBM | 64.552% | Book-to-market calculation | Intangible assets logic |
| MS | 63.487% | Missing 337 obs + differences | Market share calculation |

### Category D: Medium Precision Errors (10-50% failure rate)
**Partial calculation issues**
| Predictor | Failure Rate | Pattern | Root Cause |
|-----------|-------------|---------|------------|
| AbnormalAccruals | 49.009% | Missing 16K obs + accrual differences | Accrual estimation model |
| IntanSP | 41.462% | Intangible asset calculation | Accounting data processing |
| IntanEP | 42.603% | Intangible asset calculation | Accounting data processing |
| RIO_Volatility | 26.584% | Volatility measure differences | Time-series volatility calc |
| MomOffSeason06YrPlus | 24.784% | Seasonal momentum | Complex momentum logic |

### Category E: Low Precision Errors (1-10% failure rate)
**Minor but significant calculation differences**
| Predictor | Failure Rate | Pattern | Root Cause |
|-----------|-------------|---------|------------|
| IdioVolAHT | 8.544% | Idiosyncratic volatility | Volatility estimation |
| BetaFP | 5.980% | Beta calculation | Factor model regression |
| DivSeason | 5.205% | Seasonal dividend effects | Seasonal adjustment logic |
| IndMom | 3.284% | Industry momentum | Industry classification |
| HerfAsset | 1.443% | Concentration measure | Asset concentration calc |

## Root Cause Categories Summary

### Category A: Mathematical Formula Errors (Critical)
- **Examples:** TrendFactor (sign flip), BetaTailRisk, CompEquIss  
- **Symptoms:** Sign reversals, extreme magnitude differences
- **Likely causes:** Wrong regression formulas, incorrect coefficient signs, different mathematical operations

### Category B: Data Window/Filtering Differences (Major) 
- **Examples:** Coskewness (-407K obs), retConglomerate (-169K obs), TrendFactor (-1.4K obs)
- **Symptoms:** Missing historical observations, different sample sizes
- **Likely causes:** Different rolling window logic, data availability filters, lag/lead timing

### Category C: Scaling/Units Differences (Major)
- **Examples:** CompEquIss (diff=1.96e+03), PriceDelaySlope (diff=1.6e+04)
- **Symptoms:** Orders of magnitude differences
- **Likely causes:** Different normalization, wrong units, scaling factor errors

### Category D: Rolling Window Logic Errors (Major)
- **Examples:** Beta family (Beta, BetaLiquidityPS, BetaTailRisk), Momentum family
- **Symptoms:** Systematic biases in time-series calculations  
- **Likely causes:** Wrong lag operators (Stata `l6.` vs Python `shift(6)`), calendar vs position-based rolling

### Category E: Complex Accounting Logic Errors (Moderate)
- **Examples:** Intangible asset predictors (IntanBM, IntanSP, IntanEP), AbnormalAccruals
- **Symptoms:** Moderate precision loss with some missing observations
- **Likely causes:** Complex accounting data processing, accrual models, asset classification

## Updated Investigation Priorities (Based on Comprehensive Analysis)

### Priority 1 (Critical): Complete Formula Breakdown (>95% failure)
**These predictors require immediate attention - calculations are fundamentally wrong**
1. **TrendFactor** (98.4% failure) - Systematic sign reversal (Python negative, Stata positive)
   - *Debug approach*: Compare regression coefficient calculation step by step
2. **BetaTailRisk** (99.7% failure) - Magnitude differences, Python values consistently smaller  
   - *Debug approach*: Validate tail risk regression and scaling factors
3. **Coskewness** (99.4% failure) - Missing 407K observations + sign reversals
   - *Debug approach*: Check co-moment calculation formula and data filtering logic
4. **CompEquIss** (97.7% failure) - Extreme magnitude differences (factor of 1000+)
   - *Debug approach*: Verify equity issuance calculation completely

### Priority 2 (High): Severe Systematic Errors (80-95% failure)
**Major calculation issues but not total breakdown**
1. **retConglomerate** (94.1% failure) - Missing 169K observations
   - *Debug approach*: Investigate industry classification and data filtering
2. **Mom12mOffSeason** (91.9% failure) - Seasonal momentum calculation bias
   - *Debug approach*: Validate seasonal adjustment and rolling window logic

### Priority 3 (Medium): Beta Family Investigation (Multiple 70-80% failures)
**Common pattern suggests systematic regression estimation errors**
1. **BetaLiquidityPS** (80.8% failure) + **Beta** (70.7% failure) + **betaVIX** (69.6% failure)
   - *Debug approach*: Investigate rolling window regression implementation
   - *Focus*: Stata lag operators vs pandas operations, calendar vs position-based windows

### Priority 4 (Medium): Intangible Assets Logic (40-65% failures)
**Accounting data processing issues**
1. **IntanBM** (64.6%), **IntanSP** (41.5%), **IntanEP** (42.6%) - All intangible asset predictors
   - *Debug approach*: Compare intangible asset identification and calculation logic

### Priority 5 (Lower): Refinement Issues (<40% failure)
**These have partial success but need precision improvement**
1. **AbnormalAccruals** (49.0%) - Accrual model estimation
2. **RIO_Volatility** (26.6%) - Volatility calculation differences  
3. **MomOffSeason** family - Seasonal momentum variants

## Debugging Strategy by Priority

### For Priority 1 (Critical Formula Errors):
1. **Use bisection debugging** - Find specific permno-yyyymm observations that fail
2. **Trace calculation step-by-step** - Don't assume any Python operation matches Stata
3. **Focus on mathematical formulas** - These are likely completely wrong implementations
4. **Expected outcome**: Fix should dramatically improve failure rates from 95%+ to <1%

### For Priority 2-3 (Systematic Errors):
1. **Compare rolling window logic** - Stata `l6.` vs Python `shift(6)` behavior
2. **Validate data filtering** - Check why observations are missing
3. **Test regression implementations** - Verify coefficient calculation and scaling
4. **Expected outcome**: Fix should improve failure rates from 70-95% to <10%

### For Priority 4-5 (Refinement Issues):
1. **Compare accounting data processing** - Asset classification, accrual models
2. **Check edge case handling** - Missing data, extreme values
3. **Validate seasonal adjustments** - Calendar vs business day logic
4. **Expected outcome**: Fix should improve failure rates from 10-50% to <1%

## Key Insights for Future Debugging

1. **These are not precision issues** - They're systematic calculation differences
2. **Simple predictors work well** - Translation approach is sound for basic calculations  
3. **Complex predictors fail systematically** - Need line-by-line validation of mathematical operations
4. **Recent data shows consistent patterns** - Issues persist across time periods
5. **Missing data patterns suggest filtering differences** - Need to compare inclusion/exclusion logic

## Recommended Next Steps

1. **Start with TrendFactor** - Clear sign reversal pattern, easier to debug
2. **Use bisection debugging** - Focus on specific permno-yyyymm observations
3. **Compare Stata code line-by-line** - Don't assume Python equivalents are correct  
4. **Validate rolling window logic** - Especially Stata lag operators vs pandas operations
5. **Never give up due to "data differences"** - These patterns show systematic translation errors

## Debug Philosophy Reinforcement

- ❌ **WRONG:** "This must be due to data availability issues"
- ✅ **RIGHT:** Focus on specific failing observations and trace the calculation logic
- ❌ **WRONG:** Assume pandas methods match Stata operators  
- ✅ **RIGHT:** Research exact Stata behavior and replicate precisely
- ❌ **WRONG:** Accept convenient explanations about data patterns
- ✅ **RIGHT:** Investigate why specific permno-yyyymm observations fail

**The evidence shows these are translation bugs, not data issues. Keep debugging!**