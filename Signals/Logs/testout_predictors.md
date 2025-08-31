# Predictor Validation Results

**Generated**: 2025-08-31 08:06:06

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
| RIO_Volatility            | ✅         | ✅ (0.17%) | ✅ (+0.0%)   | ✅ (0.1%)     | ❌ (7.5E-01)   | SKIP       |
| RIO_Turnover              | ✅         | ✅ (0.11%) | ✅ (+0.0%)   | ✅ (0.1%)     | ❌ (7.4E-01)   | SKIP       |
| RIO_Disp                  | ✅         | ✅ (0.23%) | ✅ (+0.1%)   | ✅ (0.1%)     | ❌ (7.9E-01)   | SKIP       |
| RIO_MB                    | ✅         | ✅ (0.03%) | ✅ (+0.1%)   | ✅ (0.1%)     | ✅ (0.0E+00)   | SKIP       |

**Overall**: 1/4 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 4/4 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### RIO_Disp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.06% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  497,437
- Python: 497,742
- Common: 496,313

**Precision1**: 0.100% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.90e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    496313.0000 |    496313.0000 |    496313.0000 |    496313.0000 |
| mean       |         3.5899 |         3.5909 |       9.95e-04 |       7.86e-04 |
| std        |         1.2664 |         1.2666 |         0.0317 |         0.0250 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7896 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7896 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0018 + 0.9998 * stata
- **R-squared**: 0.9994
- **N observations**: 496,313

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0018 |     1.35e-04 |     13.0912 |     0.000 |
| Slope       |       0.9998 |     3.55e-05 |  28174.5881 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 498/496313 (0.100%)
- Stata standard deviation: 1.27e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   21563  202412     4.0    3.0   1.0
1   91910  202412     5.0    4.0   1.0
2   92597  202411     4.0    3.0   1.0
3   22758  202406     4.0    3.0   1.0
4   16630  202405     5.0    4.0   1.0
5   18937  202405     4.0    3.0   1.0
6   10382  202403     5.0    4.0   1.0
7   18572  202403     4.0    3.0   1.0
8   15291  202401     3.0    2.0   1.0
9   25590  202401     3.0    2.0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10026  199903     5.0    4.0   1.0
1   10026  201806     3.0    2.0   1.0
2   10035  199004     5.0    4.0   1.0
3   10083  198705     4.0    3.0   1.0
4   10091  198808     4.0    3.0   1.0
5   10180  200001     5.0    4.0   1.0
6   10182  201804     4.0    3.0   1.0
7   10192  199007     5.0    4.0   1.0
8   10258  199104     5.0    4.0   1.0
9   10258  201705     5.0    4.0   1.0
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### RIO_MB

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.09% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  354,170
- Python: 354,474
- Common: 354,047

**Precision1**: 0.089% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    354047.0000 |    354047.0000 |    354047.0000 |    354047.0000 |
| mean       |         2.7904 |         2.7913 |       8.70e-04 |       6.41e-04 |
| std        |         1.3572 |         1.3576 |         0.0299 |         0.0220 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7368 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7368 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0000 * stata
- **R-squared**: 0.9995
- **N observations**: 354,047

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.91e-04 |     1.15e-04 |      6.8901 |     0.000 |
| Slope       |       1.0000 |     3.70e-05 |  27043.8615 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 316/354047 (0.089%)
- Stata standard deviation: 1.36e+00

---

### RIO_Turnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.01% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  445,546
- Python: 445,570
- Common: 445,078

**Precision1**: 0.131% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.42e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    445078.0000 |    445078.0000 |    445078.0000 |    445078.0000 |
| mean       |         3.2513 |         3.2526 |         0.0013 |       9.62e-04 |
| std        |         1.3475 |         1.3479 |         0.0362 |         0.0269 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7421 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7421 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0015 + 0.9999 * stata
- **R-squared**: 0.9993
- **N observations**: 445,078

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0015 |     1.42e-04 |     10.5857 |     0.000 |
| Slope       |       0.9999 |     4.03e-05 |  24810.6590 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 585/445078 (0.131%)
- Stata standard deviation: 1.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   21563  202412     4.0    3.0   1.0
1   18937  202405     4.0    3.0   1.0
2   18572  202403     4.0    3.0   1.0
3   15291  202401     3.0    2.0   1.0
4   16436  202311     4.0    3.0   1.0
5   78003  202309     4.0    3.0   1.0
6   91606  202307     4.0    3.0   1.0
7   18558  202301     3.0    2.0   1.0
8   18576  202207     2.0    1.0   1.0
9   21589  202207     4.0    3.0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  195909     4.0    3.0   1.0
1   10014  196902     5.0    4.0   1.0
2   10022  192809     5.0    4.0   1.0
3   10022  192901     5.0    4.0   1.0
4   10035  199004     5.0    4.0   1.0
5   10057  193607     5.0    4.0   1.0
6   10057  193609     5.0    4.0   1.0
7   10057  194101     4.0    3.0   1.0
8   10057  195009     5.0    4.0   1.0
9   10083  198705     4.0    3.0   1.0
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10022  192809     5.0    4.0   1.0
1   10022  192901     5.0    4.0   1.0
2   10057  193607     5.0    4.0   1.0
3   10057  193609     5.0    4.0   1.0
4   10057  194101     4.0    3.0   1.0
5   10137  194602     3.0    2.0   1.0
6   10137  194703     3.0    2.0   1.0
7   10233  193204     2.0    1.0   1.0
8   10559  194405     5.0    4.0   1.0
9   10671  192705     3.0    2.0   1.0
```

---

### RIO_Volatility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.04% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  470,062
- Python: 470,257
- Common: 469,253

**Precision1**: 0.138% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.46e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    469253.0000 |    469253.0000 |    469253.0000 |    469253.0000 |
| mean       |         3.4332 |         3.4345 |         0.0014 |         0.0010 |
| std        |         1.3412 |         1.3417 |         0.0371 |         0.0276 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7456 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7456 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0016 + 0.9999 * stata
- **R-squared**: 0.9992
- **N observations**: 469,253

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0016 |     1.49e-04 |     10.5698 |     0.000 |
| Slope       |       0.9999 |     4.04e-05 |  24777.9202 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 646/469253 (0.138%)
- Stata standard deviation: 1.34e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   21563  202412     4.0    3.0   1.0
1   14045  202410     5.0    4.0   1.0
2   22758  202406     4.0    3.0   1.0
3   18937  202405     4.0    3.0   1.0
4   18572  202403     4.0    3.0   1.0
5   88264  202401     5.0    4.0   1.0
6   18955  202309     5.0    4.0   1.0
7   78003  202309     4.0    3.0   1.0
8   17357  202305     3.0    2.0   1.0
9   18561  202305     5.0    4.0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10035  199004     5.0    4.0   1.0
1   10062  199006     5.0    4.0   1.0
2   10062  199403     4.0    3.0   1.0
3   10083  198705     4.0    3.0   1.0
4   10125  199008     4.0    3.0   1.0
5   10137  194308     4.0    3.0   1.0
6   10137  194602     3.0    2.0   1.0
7   10166  199002     5.0    4.0   1.0
8   10233  193204     2.0    1.0   1.0
9   10258  199104     5.0    4.0   1.0
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10137  194308     4.0    3.0   1.0
1   10137  194602     3.0    2.0   1.0
2   10233  193204     2.0    1.0   1.0
3   10284  192910     3.0    2.0   1.0
4   10559  194405     5.0    4.0   1.0
5   10591  193704     3.0    2.0   1.0
6   10671  192705     3.0    2.0   1.0
7   10698  194503     5.0    4.0   1.0
8   10823  194908     4.0    3.0   1.0
9   11148  193810     5.0    4.0   1.0
```

---

