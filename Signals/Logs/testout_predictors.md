# Predictor Validation Results

**Generated**: 2025-08-31 00:13:54

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

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2    | T-stat     |
|---------------------------|------------|------------|---------------|--------------|---------------|------------|
| AbnormalAccruals          | ✅         | ✅ (0.60%) | ✅ (+4.5%)   | ❌ (9.0%)     | ❌ (1.0E+00)   | SKIP       |

**Overall**: 0/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### AbnormalAccruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +4.47% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  2,570,664
- Python: 2,685,478
- Common: 2,555,191

**Precision1**: 8.983% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.56e+06 |       2.56e+06 |       2.56e+06 |       2.56e+06 |
| mean       |       3.62e-05 |       3.47e-05 |      -1.50e-06 |      -9.33e-06 |
| std        |         0.1611 |         0.1594 |         0.0252 |         0.1567 |
| min        |        -8.2957 |        -8.2790 |        -2.0186 |       -12.5287 |
| 25%        |        -0.0406 |        -0.0404 |      -4.85e-09 |      -3.01e-08 |
| 50%        |         0.0069 |         0.0070 |      -2.58e-10 |      -1.60e-09 |
| 75%        |         0.0526 |         0.0526 |       3.55e-09 |       2.21e-08 |
| max        |         2.8119 |         2.8119 |         7.8119 |        48.4851 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9772 * stata
- **R-squared**: 0.9755
- **N observations**: 2,555,191

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.75e-07 |     1.56e-05 |     -0.0432 |     0.966 |
| Slope       |       0.9772 |     9.70e-05 |  10077.9620 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 229537/2555191 (8.983%)
- Stata standard deviation: 1.61e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   18136  202609 -0.026650 -0.028342  0.001692
1   29946  202609  0.108293  0.092957  0.015336
2   13142  202608 -0.125493 -0.145704  0.020211
3   14033  202608  1.382135  1.391868 -0.009733
4   15623  202608 -0.091212 -0.093782  0.002570
5   16632  202608 -0.026517 -0.029087  0.002570
6   18136  202608 -0.026650 -0.028342  0.001692
7   18886  202608  0.142143  0.140494  0.001650
8   19655  202608 -0.036532 -0.038729  0.002197
9   19779  202608 -0.113665 -0.115499  0.001834
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   82215  202206  0.288585 -7.523344  7.811929
1   82215  202207  0.288585 -7.523344  7.811929
2   82215  202208  0.288585 -7.523344  7.811929
3   82215  202209  0.288585 -7.523344  7.811929
4   82215  202210  0.288585 -7.523344  7.811929
5   82215  202211  0.288585 -7.523344  7.811929
6   82215  202212  0.288585 -7.523344  7.811929
7   82215  202301  0.288585 -7.523344  7.811929
8   82215  202302  0.288585 -7.523344  7.811929
9   82215  202303  0.288585 -7.523344  7.811929
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

