# Predictor Validation Results

**Generated**: 2025-08-27 17:18:22

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_NUMROWS: 5.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 1%
- EXTREME_Q: 0.999
- TOL_DIFF_2: 0.1
- TOL_TSTAT: 0.2
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2              | T-stat     |
|---------------------------|------------|------------|---------------|--------------|-------------------------|------------|
| MomOffSeason              | ✅         | ✅ (0.00%) | ✅ (+1.2%)   | ✅ (0.9%)     | ❌ (2.2E+00)             | SKIP       |

**Overall**: 0/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### MomOffSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.18% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,396,704
- Python: 3,436,865
- Common: 3,396,704

**Precision1**: 0.893% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.20e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0125 |         0.0124 |      -6.59e-05 |        -0.0024 |
| std        |         0.0270 |         0.0264 |         0.0060 |         0.2208 |
| min        |        -4.1713 |        -0.3549 |        -1.2656 |       -46.9028 |
| 25%        |       3.95e-04 |       3.59e-04 |      -5.00e-10 |      -1.85e-08 |
| 50%        |         0.0119 |         0.0118 |         0.0000 |         0.0000 |
| 75%        |         0.0240 |         0.0240 |       5.00e-10 |       1.85e-08 |
| max        |         1.5150 |         1.5150 |         3.8837 |       143.9315 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9545 * stata
- **R-squared**: 0.9513
- **N observations**: 3,396,704

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.00e-04 |     3.48e-06 |    143.6172 |     0.000 |
| Slope       |       0.9545 |     1.17e-04 |   8143.1419 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30342/3396704 (0.893%)
- Stata standard deviation: 2.70e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412 -0.009633  0.014271 -0.023904
1   12799  202412  0.024784  0.074968 -0.050184
2   14051  202412 -0.002322 -0.003499  0.001177
3   16086  202412 -0.064238 -0.019903 -0.044335
4   16794  202412 -0.000793  0.013392 -0.014186
5   17147  202412 -0.067903 -0.071290  0.003386
6   17901  202412 -0.031193 -0.021832 -0.009361
7   18065  202412  0.002178  0.002903 -0.000726
8   18103  202412 -0.019200  0.002476 -0.021675
9   19833  202412 -0.054061 -0.049822 -0.004239
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89169  202105 -0.287618 -4.171327  3.883708
1   44230  198407 -0.059679 -1.585526  1.525847
2   92161  199008 -0.128534 -1.574922  1.446388
3   79704  200304 -0.098913  1.166667 -1.265580
4   10097  199202 -0.105667  1.000000 -1.105667
5   77324  200102  0.013863  1.086957 -1.073094
6   10685  199512 -0.048412 -1.021461  0.973049
7   82810  200509 -0.172706 -1.145503  0.972797
8   78414  198610  0.354448  1.300000 -0.945552
9   79704  200302  0.079939  0.960578 -0.880639
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

