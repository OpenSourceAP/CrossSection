# Predictor Validation Results

**Generated**: 2025-08-15 13:53:51

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 1%
- EXTREME_Q: 0.999
- TOL_DIFF_2: 0.1
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| Recomm_ShortInterest      | ✅         | ✅       | ❌ (47.17%)  | ✅ (0.00%)    | ✅ (99.900th diff 0.0E+00) |
| RIO_Volatility            | ✅         | ✅       | ❌ (4.44%)   | ❌ (4.32%)    | ❌ (99.900th diff 7.5E-01) |
| TrendFactor               | ✅         | ✅       | ✅ (0.12%)   | ❌ (97.14%)   | ❌ (99.900th diff 2.9E+00) |
| RDAbility                 | ✅         | ✅       | ✅ (0.02%)   | ❌ (10.90%)   | ❌ (99.900th diff 4.2E+00) |
| RIO_Disp                  | ✅         | ✅       | ✅ (0.26%)   | ❌ (3.79%)    | ❌ (99.900th diff 7.9E-01) |
| RIO_Turnover              | ✅         | ✅       | ✅ (0.15%)   | ❌ (3.65%)    | ❌ (99.900th diff 7.4E-01) |
| RIO_MB                    | ✅         | ✅       | ✅ (0.18%)   | ❌ (3.45%)    | ❌ (99.900th diff 7.4E-01) |
| MomOffSeason              | ✅         | ✅       | ✅ (0.00%)   | ❌ (1.06%)    | ❌ (99.900th diff 2.1E+00) |
| DivSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.99%)    | ❌ (99.900th diff 2.0E+00) |
| MomOffSeason06YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.92%)    | ❌ (99.900th diff 1.9E+00) |
| MomOffSeason11YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.88%)    | ❌ (99.900th diff 1.8E+00) |
| HerfAsset                 | ✅         | ✅       | ✅ (0.63%)   | ✅ (0.66%)    | ❌ (99.900th diff 2.3E-01) |
| MomOffSeason16YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.51%)    | ❌ (99.900th diff 6.1E-01) |
| MomVol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.42%)    | ❌ (99.900th diff 3.5E-01) |
| Herf                      | ✅         | ✅       | ✅ (0.20%)   | ✅ (0.19%)    | ✅ (99.900th diff 6.2E-02) |
| Investment                | ✅         | ✅       | ✅ (0.86%)   | ✅ (0.18%)    | ✅ (99.900th diff 2.7E-02) |
| DivInit                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99.900th diff 0.0E+00) |
| DivOmit                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99.900th diff 0.0E+00) |
| HerfBE                    | ✅         | ✅       | ✅ (0.63%)   | ✅ (0.00%)    | ✅ (99.900th diff 1.5E-05) |
| VarCF                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99.900th diff 1.3E-08) |
| CitationsRD               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99.900th diff 0.0E+00) |

**Overall**: 7/21 available predictors passed validation
  - Natural passes: 7
  - Overridden passes: 0
**Python CSVs**: 21/21 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### CitationsRD

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 647,592
- Common: 645,348

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    645348.0000 |    645348.0000 |    645348.0000 |    645348.0000 |
| mean       |         0.2153 |         0.2153 |         0.0000 |         0.0000 |
| std        |         0.4111 |         0.4111 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 645,348

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.70e-13 |     1.69e-15 |    396.0937 |     0.000 |
| Slope       |       1.0000 |     3.64e-15 |    2.74e+14 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/645348 (0.000%)
- Stata standard deviation: 4.11e-01

---

### DivInit

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivInit']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0191 |         0.0192 |       4.40e-05 |       3.21e-04 |
| std        |         0.1369 |         0.1371 |         0.0073 |         0.0536 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -7.3042 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         7.3042 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9997 * stata
- **R-squared**: 0.9971
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.99e-05 |     3.68e-06 |     13.5407 |     0.000 |
| Slope       |       0.9997 |     2.66e-05 |  37521.4503 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 218/4047630 (0.005%)
- Stata standard deviation: 1.37e-01

---

### DivOmit

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivOmit']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0039 |         0.0039 |       3.71e-06 |       5.96e-05 |
| std        |         0.0622 |         0.0623 |         0.0056 |         0.0893 |
| min        |         0.0000 |         0.0000 |        -1.0000 |       -16.0714 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |        16.0714 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9965 * stata
- **R-squared**: 0.9920
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.74e-05 |     2.77e-06 |      6.2781 |     0.000 |
| Slope       |       0.9965 |     4.44e-05 |  22464.6408 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 125/4047630 (0.003%)
- Stata standard deviation: 6.22e-02

---

### DivSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivSeason']

**Observations**:
- Stata:  1,775,339
- Python: 1,981,491
- Common: 1,775,335

**Precision1**: 0.992% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.01e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.78e+06 |       1.78e+06 |       1.78e+06 |       1.78e+06 |
| mean       |         0.4456 |         0.4392 |        -0.0064 |        -0.0129 |
| std        |         0.4970 |         0.4963 |         0.0994 |         0.2000 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0120 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0120 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0032 + 0.9785 * stata
- **R-squared**: 0.9603
- **N observations**: 1,775,335

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0032 |     9.96e-05 |     31.9606 |     0.000 |
| Slope       |       0.9785 |     1.49e-04 |   6556.3925 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 17618/1775335 (0.992%)
- Stata standard deviation: 4.97e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13303  202412       1      0     1
1   15802  202412       1      0     1
2   16019  202412       1      0     1
3   16560  202412       1      0     1
4   20764  202412       0      1    -1
5   21372  202412       0      1    -1
6   32791  202412       0      1    -1
7   78981  202412       0      1    -1
8   81134  202412       0      1    -1
9   85903  202412       1      0     1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  201507       0      1    -1
1   10001  201510       0      1    -1
2   10001  201601       0      1    -1
3   10001  201604       0      1    -1
4   10002  199706       0      1    -1
5   10002  199709       0      1    -1
6   10002  199712       0      1    -1
7   10002  199803       0      1    -1
8   10014  193501       0      1    -1
9   10014  193504       0      1    -1
```

---

### Herf

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Herf']

**Observations**:
- Stata:  3,158,336
- Python: 3,152,103
- Common: 3,152,103

**Precision1**: 0.191% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.18e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.15e+06 |       3.15e+06 |       3.15e+06 |       3.15e+06 |
| mean       |         0.3294 |         0.3294 |      -6.78e-07 |      -2.44e-06 |
| std        |         0.2779 |         0.2779 |         0.0036 |         0.0131 |
| min        |         0.0000 |         0.0000 |        -0.5101 |        -1.8359 |
| 25%        |         0.1184 |         0.1184 |      -2.36e-09 |      -8.48e-09 |
| 50%        |         0.2537 |         0.2537 |         0.0000 |         0.0000 |
| 75%        |         0.4723 |         0.4724 |       2.68e-09 |       9.63e-09 |
| max        |         5.5471 |         5.5471 |         0.4787 |         1.7229 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9998
- **N observations**: 3,152,103

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.07e-06 |     3.18e-06 |     -0.9637 |     0.335 |
| Slope       |       1.0000 |     7.38e-06 | 135450.4159 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6011/3152103 (0.191%)
- Stata standard deviation: 2.78e-01

---

### HerfAsset

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['HerfAsset']

**Observations**:
- Stata:  2,547,057
- Python: 2,530,992
- Common: 2,530,992

**Precision1**: 0.661% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.28e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.53e+06 |       2.53e+06 |       2.53e+06 |       2.53e+06 |
| mean       |         0.3431 |         0.3431 |      -2.19e-07 |      -7.87e-07 |
| std        |         0.2779 |         0.2779 |         0.0051 |         0.0184 |
| min        |         0.0162 |         0.0162 |        -0.5110 |        -1.8388 |
| 25%        |         0.1214 |         0.1214 |      -2.43e-09 |      -8.75e-09 |
| 50%        |         0.2658 |         0.2658 |         0.0000 |         0.0000 |
| 75%        |         0.4886 |         0.4886 |       2.86e-09 |       1.03e-08 |
| max        |         1.0000 |         1.0000 |         0.4865 |         1.7509 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9997
- **N observations**: 2,530,992

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.47e-05 |     5.12e-06 |     -2.8755 |     0.004 |
| Slope       |       1.0000 |     1.16e-05 |  86297.3089 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16736/2530992 (0.661%)
- Stata standard deviation: 2.78e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   13798  202412  0.440552  0.437600  0.002952
1   22092  202412  0.249513  0.289656 -0.040142
2   77900  202412  0.391434  0.384627  0.006806
3   87471  202412  0.147025  0.126639  0.020386
4   87759  202412  0.656462  0.706623 -0.050162
5   90756  202412  0.298919  0.304100 -0.005181
6   13798  202411  0.439189  0.434813  0.004376
7   22092  202411  0.252521  0.292813 -0.040293
8   77900  202411  0.388057  0.379990  0.008067
9   87471  202411  0.141456  0.122618  0.018838
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   64630  198411  0.128355  0.639319 -0.510964
1   76977  199602  0.159518  0.663807 -0.504289
2   17347  198307  1.000000  0.513459  0.486541
3   64630  198412  0.129494  0.609773 -0.480279
4   76977  199603  0.158921  0.635532 -0.476612
5   17347  198308  1.000000  0.535763  0.464237
6   63547  198710  0.936233  0.473589  0.462644
7   69040  199409  0.976784  0.520936  0.455848
8   64630  198501  0.130470  0.580227 -0.449757
9   76977  199604  0.158597  0.607345 -0.448748
```

---

### HerfBE

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['HerfBE']

**Observations**:
- Stata:  2,547,057
- Python: 2,530,992
- Common: 2,530,992

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.49e-05 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.53e+06 |       2.53e+06 |       2.53e+06 |       2.53e+06 |
| mean       |        70.5506 |        70.5537 |         0.0031 |       4.56e-07 |
| std        |      6738.2498 |      6738.4550 |         0.9337 |       1.39e-04 |
| min        |         0.0000 |         0.0000 |      -213.6088 |        -0.0317 |
| 25%        |         0.1251 |         0.1251 |      -2.45e-09 |      -3.64e-13 |
| 50%        |         0.2675 |         0.2674 |         0.0000 |         0.0000 |
| 75%        |         0.5118 |         0.5117 |       2.64e-09 |       3.92e-13 |
| max        |    859657.6583 |    859686.7510 |       821.3264 |         0.1219 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0009 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,530,992

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.23e-04 |     5.73e-04 |      1.6126 |     0.107 |
| Slope       |       1.0000 |     8.50e-08 |    1.18e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 9/2530992 (0.000%)
- Stata standard deviation: 6.74e+03

---

### Investment

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Investment']

**Observations**:
- Stata:  2,411,862
- Python: 2,391,854
- Common: 2,391,143

**Precision1**: 0.180% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.68e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.39e+06 |       2.39e+06 |       2.39e+06 |       2.39e+06 |
| mean       |         1.0035 |         1.0035 |       5.81e-05 |       3.17e-05 |
| std        |         1.8324 |         1.8323 |         0.0124 |         0.0068 |
| min        |     -2512.3491 |     -2512.3180 |        -8.0000 |        -4.3659 |
| 25%        |         0.6673 |         0.6674 |      -2.20e-08 |      -1.20e-08 |
| 50%        |         0.9330 |         0.9330 |         0.0000 |         0.0000 |
| 75%        |         1.2033 |         1.2033 |       2.20e-08 |       1.20e-08 |
| max        |       253.6225 |       253.6223 |         5.2631 |         2.8723 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 1.0000
- **N observations**: 2,391,143

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.31e-04 |     9.16e-06 |     14.3332 |     0.000 |
| Slope       |       0.9999 |     4.39e-06 | 227988.4522 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4313/2391143 (0.180%)
- Stata standard deviation: 1.83e+00

---

### MomOffSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason']

**Observations**:
- Stata:  3,396,704
- Python: 3,398,036
- Common: 3,396,703

**Precision1**: 1.063% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.08e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0125 |         0.0124 |      -2.32e-05 |      -8.58e-04 |
| std        |         0.0270 |         0.0263 |         0.0057 |         0.2127 |
| min        |        -4.1713 |        -0.6858 |        -1.2021 |       -44.5515 |
| 25%        |       3.95e-04 |       3.88e-04 |      -5.00e-10 |      -1.85e-08 |
| 50%        |         0.0119 |         0.0118 |         0.0000 |         0.0000 |
| 75%        |         0.0240 |         0.0240 |       5.09e-10 |       1.89e-08 |
| max        |         1.5150 |         1.5150 |         3.8643 |       143.2185 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9539 * stata
- **R-squared**: 0.9547
- **N observations**: 3,396,703

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.51e-04 |     3.35e-06 |    164.6263 |     0.000 |
| Slope       |       0.9539 |     1.13e-04 |   8465.5718 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36098/3396703 (1.063%)
- Stata standard deviation: 2.70e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.059688 -0.048228 -0.011460
1   11153  202412  0.028703  0.040138 -0.011435
2   11379  202412 -0.006140  0.014271 -0.020410
3   12799  202412  0.031840  0.074968 -0.043128
4   12928  202412 -0.015958 -0.024719  0.008761
5   13563  202412  0.002435  0.005397 -0.002962
6   14051  202412 -0.005721 -0.003499 -0.002222
7   14469  202412  0.012587 -0.012774  0.025361
8   15793  202412  0.015663  0.018264 -0.002602
9   16086  202412 -0.013519 -0.019903  0.006384
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89169  202105 -0.307063 -4.171327  3.864264
1   44230  198407 -0.050843 -1.585526  1.534683
2   82810  200509  0.102561 -1.145503  1.248064
3   10097  199202 -0.202071  1.000000 -1.202071
4   79704  200304 -0.029805  1.166667 -1.196472
5   92161  199008 -0.390015 -1.574922  1.184907
6   77324  200102 -0.033026  1.086957 -1.119983
7   80054  200306 -0.027273 -1.002423  0.975150
8   10685  199512 -0.048334 -1.021461  0.973126
9   79704  200302  0.004316  0.960578 -0.956262
```

---

### MomOffSeason06YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason06YrPlus']

**Observations**:
- Stata:  2,425,319
- Python: 2,429,450
- Common: 2,425,318

**Precision1**: 0.924% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.93e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.43e+06 |       2.43e+06 |       2.43e+06 |       2.43e+06 |
| mean       |         0.0130 |         0.0131 |       9.06e-05 |         0.0028 |
| std        |         0.0324 |         0.0304 |         0.0104 |         0.3215 |
| min        |        -4.8725 |        -4.8725 |        -2.4925 |       -76.9952 |
| 25%        |         0.0027 |         0.0027 |      -4.55e-10 |      -1.40e-08 |
| 50%        |         0.0125 |         0.0126 |         0.0000 |         0.0000 |
| 75%        |         0.0233 |         0.0233 |       4.55e-10 |       1.40e-08 |
| max        |        15.8923 |        15.8923 |         2.3495 |        72.5785 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0015 + 0.8905 * stata
- **R-squared**: 0.8967
- **N observations**: 2,425,318

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0015 |     6.77e-06 |    224.1977 |     0.000 |
| Slope       |       0.8905 |     1.94e-04 |   4587.3336 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 22415/2425318 (0.924%)
- Stata standard deviation: 3.24e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412 -0.016246 -0.019014  0.002768
1   12799  202412  0.008633  0.023379 -0.014746
2   13563  202412 -0.048991 -0.048507 -0.000485
3   13828  202412 -0.002671 -0.008100  0.005430
4   13878  202412  0.011810  0.019389 -0.007578
5   14051  202412 -0.055700 -0.051790 -0.003910
6   77900  202412 -0.014109 -0.013602 -0.000507
7   79666  202412  0.006794 -0.008641  0.015435
8   79903  202412 -0.025067 -0.035089  0.010022
9   82156  202412 -0.051975 -0.101504  0.049529
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   12715  198603 -0.278162  2.214316 -2.492477
1   76356  198510  0.049160 -2.300340  2.349501
2   76356  198509  0.044722 -2.158295  2.203016
3   76356  198709  0.050363  2.121433 -2.071070
4   77173  201209  0.016259  1.996343 -1.980084
5   76356  198708  0.035481  1.898075 -1.862594
6   21849  198502 -0.120877  1.739228 -1.860105
7   76356  198507  0.037259 -1.810818  1.848078
8   76356  198607  0.033863 -1.810818  1.844681
9   77173  201210  0.016744  1.843035 -1.826291
```

---

### MomOffSeason11YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason11YrPlus']

**Observations**:
- Stata:  1,677,532
- Python: 1,678,292
- Common: 1,677,526

**Precision1**: 0.880% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.82e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.0135 |         0.0135 |       2.06e-05 |       8.09e-04 |
| std        |         0.0254 |         0.0242 |         0.0080 |         0.3162 |
| min        |        -2.6111 |        -1.0731 |        -1.4205 |       -55.8965 |
| 25%        |         0.0034 |         0.0034 |      -4.55e-10 |      -1.79e-08 |
| 50%        |         0.0128 |         0.0128 |         0.0000 |         0.0000 |
| 75%        |         0.0235 |         0.0234 |       4.55e-10 |       1.79e-08 |
| max        |         2.2478 |         2.2478 |         2.5829 |       101.6332 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0013 + 0.9028 * stata
- **R-squared**: 0.9000
- **N observations**: 1,677,526

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0013 |     6.69e-06 |    199.5419 |     0.000 |
| Slope       |       0.9028 |     2.32e-04 |   3886.5164 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 14757/1677526 (0.880%)
- Stata standard deviation: 2.54e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412  0.068397  0.029216  0.039180
1   32791  202412  0.002924 -0.009110  0.012034
2   77900  202412  0.019325  0.024432 -0.005106
3   79666  202412  0.020302  0.032062 -0.011760
4   79903  202412  0.004065  0.000592  0.003473
5   82156  202412 -0.017317 -0.023979  0.006662
6   84321  202412  0.005217 -0.102155  0.107372
7   86812  202412  0.007851  0.024643 -0.016792
8   87043  202412  0.047672  0.011518  0.036154
9   87404  202412 -0.000059 -0.010178  0.010120
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11803  201112 -0.028211 -2.611104  2.582893
1   77729  200404 -0.040883 -2.373474  2.332591
2   82163  201403  0.352963 -1.259050  1.612013
3   11803  201110  0.048556 -1.379478  1.428034
4   29153  197908 -0.998496  0.422049 -1.420545
5   82621  201509 -0.079410  1.246043 -1.325453
6   14761  200804 -0.022644  1.294914 -1.317558
7   82621  201508 -0.171515  0.951737 -1.123252
8   77173  201108  0.014516 -1.105233  1.119749
9   79689  201809  0.024521 -1.083838  1.108359
```

---

### MomOffSeason16YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason16YrPlus']

**Observations**:
- Stata:  1,027,449
- Python: 1,029,940
- Common: 1,027,449

**Precision1**: 0.510% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.05e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.03e+06 |       1.03e+06 |       1.03e+06 |       1.03e+06 |
| mean       |         0.0150 |         0.0150 |       1.49e-06 |       8.52e-05 |
| std        |         0.0175 |         0.0175 |       7.06e-04 |         0.0403 |
| min        |        -0.1110 |        -0.1110 |        -0.0501 |        -2.8566 |
| 25%        |         0.0053 |         0.0053 |      -4.27e-10 |      -2.44e-08 |
| 50%        |         0.0134 |         0.0134 |         0.0000 |         0.0000 |
| 75%        |         0.0230 |         0.0230 |       4.44e-10 |       2.54e-08 |
| max        |         0.3670 |         0.3670 |         0.0498 |         2.8419 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9982 * stata
- **R-squared**: 0.9984
- **N observations**: 1,027,449

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.77e-05 |     9.15e-07 |     30.3171 |     0.000 |
| Slope       |       0.9982 |     3.97e-05 |  25148.4282 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 5240/1027449 (0.510%)
- Stata standard deviation: 1.75e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412  0.002448  0.014200 -0.011752
1   32791  202412  0.024257 -0.002500  0.026758
2   52231  202412 -0.018362 -0.045180  0.026818
3   77900  202412 -0.004866 -0.005192  0.000326
4   79903  202412  0.000376 -0.007966  0.008342
5   82156  202412 -0.004761 -0.002425 -0.002336
6   86812  202412  0.006006 -0.011868  0.017874
7   87043  202412  0.039561  0.040528 -0.000967
8   87404  202412  0.025389  0.019622  0.005766
9   89169  202412  0.014077  0.020761 -0.006683
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   20002  199704  0.035400  0.085470 -0.050070
1   85401  202108  0.057048  0.007236  0.049812
2   41515  199310  0.051310  0.001904  0.049405
3   85401  202208  0.085915  0.036861  0.049054
4   85401  202209  0.059197  0.010437  0.048759
5   85401  202109  0.055278  0.006877  0.048401
6   41515  199309  0.086164  0.038549  0.047615
7   52250  201011  0.013986 -0.032840  0.046826
8   20002  199705  0.033726  0.079460 -0.045734
9   21785  200602  0.047106  0.002049  0.045057
```

---

### MomVol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomVol']

**Observations**:
- Stata:  1,095,615
- Python: 1,098,011
- Common: 1,095,587

**Precision1**: 0.417% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.47e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.10e+06 |       1.10e+06 |       1.10e+06 |       1.10e+06 |
| mean       |         5.7085 |         5.7122 |         0.0036 |         0.0013 |
| std        |         2.8802 |         2.8790 |         0.0645 |         0.0224 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.3472 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| 75%        |         8.0000 |         8.0000 |         0.0000 |         0.0000 |
| max        |        10.0000 |        10.0000 |         1.0000 |         0.3472 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0075 + 0.9993 * stata
- **R-squared**: 0.9995
- **N observations**: 1,095,587

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0075 |     1.37e-04 |     54.5394 |     0.000 |
| Slope       |       0.9993 |     2.14e-05 |  46756.5279 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4567/1095587 (0.417%)
- Stata standard deviation: 2.88e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   19495  202412     9.0      8   1.0
1   20867  202412     6.0      5   1.0
2   22293  202412     8.0      7   1.0
3   46886  202412     3.0      2   1.0
4   85035  202412     2.0      1   1.0
5   90386  202412     4.0      3   1.0
6   90993  202412     7.0      6   1.0
7   13586  202411     9.0      8   1.0
8   34817  202411     4.0      3   1.0
9   93289  202411     3.0      2   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  194301     4.0      3   1.0
1   10006  195503     8.0      7   1.0
2   10014  196802    10.0      9   1.0
3   10064  198901     4.0      3   1.0
4   10066  198710     2.0      1   1.0
5   10071  199204     4.0      3   1.0
6   10078  200911     3.0      2   1.0
7   10089  198908     8.0      7   1.0
8   10102  193202     8.0      7   1.0
9   10102  193210     7.0      6   1.0
```

---

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 193,263
- Common: 173,240

**Precision1**: 10.903% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.23e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    173240.0000 |    173240.0000 |    173240.0000 |    173240.0000 |
| mean       |         0.4685 |         0.4185 |        -0.0499 |        -0.0093 |
| std        |         5.3534 |         5.6919 |         2.4820 |         0.4636 |
| min        |      -170.7315 |      -184.0284 |      -192.6819 |       -35.9922 |
| 25%        |        -0.2961 |        -0.3121 |      -2.33e-07 |      -4.35e-08 |
| 50%        |         0.4038 |         0.3749 |      -2.09e-09 |      -3.91e-10 |
| 75%        |         1.3891 |         1.3350 |       1.73e-07 |       3.23e-08 |
| max        |        83.8592 |        83.8592 |        81.7174 |        15.2645 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0301 + 0.9578 * stata
- **R-squared**: 0.8114
- **N observations**: 173,240

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0301 |       0.0060 |     -5.0538 |     0.000 |
| Slope       |       0.9578 |       0.0011 |    863.4236 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18888/173240 (10.903%)
- Stata standard deviation: 5.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14033  202608  0.502601  0.192091  0.310510
1   14033  202607  0.502601  0.192091  0.310510
2   14033  202606  0.502601  0.192091  0.310510
3   16968  202606  2.676225  4.362977 -1.686752
4   13159  202605  0.510686  0.628990 -0.118303
5   13918  202605  0.010309  0.838733 -0.828424
6   14033  202605  0.502601  0.192091  0.310510
7   14051  202605  0.131522  0.408131 -0.276609
8   14245  202605  0.943359  0.997209 -0.053850
9   14272  202605  0.272244  0.369297 -0.097053
```

**Largest Differences**:
```
   permno  yyyymm      python     stata       diff
0   86597  199512 -184.028411  8.653519 -192.68193
1   86597  199601 -184.028411  8.653519 -192.68193
2   86597  199602 -184.028411  8.653519 -192.68193
3   86597  199603 -184.028411  8.653519 -192.68193
4   86597  199604 -184.028411  8.653519 -192.68193
5   86597  199605 -184.028411  8.653519 -192.68193
6   86597  199606 -184.028411  8.653519 -192.68193
7   86597  199607 -184.028411  8.653519 -192.68193
8   86597  199608 -184.028411  8.653519 -192.68193
9   86597  199609 -184.028411  8.653519 -192.68193
```

---

### RIO_Disp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Disp']

**Observations**:
- Stata:  497,437
- Python: 513,429
- Common: 496,165

**Precision1**: 3.791% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.90e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    496165.0000 |    496165.0000 |    496165.0000 |    496165.0000 |
| mean       |         3.5899 |         3.5548 |        -0.0351 |        -0.0277 |
| std        |         1.2664 |         1.2633 |         0.1985 |         0.1567 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -3.1586 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         3.1586 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0177 + 0.9853 * stata
- **R-squared**: 0.9755
- **N observations**: 496,165

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0177 |     8.43e-04 |     21.0080 |     0.000 |
| Slope       |       0.9853 |     2.22e-04 |   4447.3615 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18809/496165 (3.791%)
- Stata standard deviation: 1.27e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12008  202412     3.0      4  -1.0
1   13954  202412     4.0      5  -1.0
2   14317  202412     3.0      4  -1.0
3   17812  202412     2.0      3  -1.0
4   18452  202412     2.0      3  -1.0
5   18784  202412     4.0      5  -1.0
6   18808  202412     4.0      5  -1.0
7   19076  202412     2.0      3  -1.0
8   20295  202412     2.0      3  -1.0
9   20751  202412     3.0      4  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11379  198901     1.0      5  -4.0
1   11453  198808     1.0      5  -4.0
2   11554  199101     1.0      5  -4.0
3   12088  201304     1.0      5  -4.0
4   12402  201107     1.0      5  -4.0
5   12916  201507     1.0      5  -4.0
6   12916  201509     1.0      5  -4.0
7   13041  201207     1.0      5  -4.0
8   14423  202005     1.0      5  -4.0
9   14423  202006     1.0      5  -4.0
```

---

### RIO_MB

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_MB']

**Observations**:
- Stata:  354,170
- Python: 366,984
- Common: 353,544

**Precision1**: 3.451% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.37e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    353544.0000 |    353544.0000 |    353544.0000 |    353544.0000 |
| mean       |         2.7894 |         2.7585 |        -0.0309 |        -0.0228 |
| std        |         1.3567 |         1.3451 |         0.1922 |         0.1417 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9483 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9483 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0209 + 0.9814 * stata
- **R-squared**: 0.9799
- **N observations**: 353,544

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0209 |     7.33e-04 |     28.4643 |     0.000 |
| Slope       |       0.9814 |     2.36e-04 |   4155.4612 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12200/353544 (3.451%)
- Stata standard deviation: 1.36e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11955  202412     1.0      2  -1.0
1   15400  202412     3.0      4  -1.0
2   16066  202412     2.0      3  -1.0
3   17812  202412     2.0      3  -1.0
4   18452  202412     2.0      3  -1.0
5   18649  202412     3.0      4  -1.0
6   19076  202412     2.0      3  -1.0
7   51925  202412     3.0      4  -1.0
8   70578  202412     1.0      2  -1.0
9   81540  202412     2.0      3  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   16827  201809     1.0      5  -4.0
1   19002  202007     1.0      5  -4.0
2   22321  202206     1.0      5  -4.0
3   22802  202209     1.0      5  -4.0
4   25698  198302     1.0      5  -4.0
5   28258  198010     1.0      5  -4.0
6   39757  198012     1.0      5  -4.0
7   50172  198010     1.0      5  -4.0
8   50172  198012     1.0      5  -4.0
9   51079  198112     1.0      5  -4.0
```

---

### RIO_Turnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Turnover']

**Observations**:
- Stata:  445,546
- Python: 462,513
- Common: 444,882

**Precision1**: 3.653% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.42e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    444882.0000 |    444882.0000 |    444882.0000 |    444882.0000 |
| mean       |         3.2508 |         3.2165 |        -0.0343 |        -0.0254 |
| std        |         1.3471 |         1.3412 |         0.1963 |         0.1457 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9694 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9694 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0145 + 0.9850 * stata
- **R-squared**: 0.9788
- **N observations**: 444,882

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0145 |     7.65e-04 |     18.9302 |     0.000 |
| Slope       |       0.9850 |     2.17e-04 |   4531.8908 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16253/444882 (3.653%)
- Stata standard deviation: 1.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12008  202412     3.0      4  -1.0
1   13730  202412     2.0      3  -1.0
2   13954  202412     4.0      5  -1.0
3   15585  202412     3.0      4  -1.0
4   18452  202412     2.0      3  -1.0
5   18784  202412     4.0      5  -1.0
6   19076  202412     2.0      3  -1.0
7   20295  202412     2.0      3  -1.0
8   20751  202412     3.0      4  -1.0
9   21124  202412     2.0      3  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10342  199107     1.0      5  -4.0
1   11202  198712     1.0      5  -4.0
2   11269  198712     1.0      5  -4.0
3   11701  198807     1.0      5  -4.0
4   14423  202005     1.0      5  -4.0
5   16827  201809     1.0      5  -4.0
6   17695  202012     1.0      5  -4.0
7   17949  201904     1.0      5  -4.0
8   17949  201905     1.0      5  -4.0
9   19828  198010     1.0      5  -4.0
```

---

### RIO_Volatility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 20887 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Volatility']

**Observations**:
- Stata:  470,062
- Python: 493,527
- Common: 449,175

**Precision1**: 4.316% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.46e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449175.0000 |    449175.0000 |    449175.0000 |    449175.0000 |
| mean       |         3.4291 |         3.3898 |        -0.0392 |        -0.0293 |
| std        |         1.3400 |         1.3327 |         0.2186 |         0.1632 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9851 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9851 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0250 + 0.9813 * stata
- **R-squared**: 0.9734
- **N observations**: 449,175

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0250 |     8.90e-04 |     28.0960 |     0.000 |
| Slope       |       0.9813 |     2.42e-04 |   4057.7087 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Volatility
     0   10006  195405               4
     1   10006  197407               1
     2   10011  199103               3
     3   10011  199104               3
     4   10012  199602               3
     5   10012  199603               3
     6   10014  196704               5
     7   10014  197601               5
     8   10016  198610               3
     9   10019  199210               5
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 19387/449175 (4.316%)
- Stata standard deviation: 1.34e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13954  202412     4.0      5  -1.0
1   15585  202412     3.0      4  -1.0
2   16066  202412     2.0      3  -1.0
3   17812  202412     2.0      3  -1.0
4   18062  202412     3.0      4  -1.0
5   18452  202412     2.0      3  -1.0
6   18784  202412     4.0      5  -1.0
7   19076  202412     2.0      3  -1.0
8   20295  202412     2.0      3  -1.0
9   20751  202412     3.0      4  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10026  198701     1.0      5  -4.0
1   10537  198703     1.0      5  -4.0
2   10948  198709     1.0      5  -4.0
3   11212  198801     1.0      5  -4.0
4   11212  198802     1.0      5  -4.0
5   11277  198803     1.0      5  -4.0
6   11379  198901     1.0      5  -4.0
7   11453  198808     1.0      5  -4.0
8   11701  198807     1.0      5  -4.0
9   12402  201107     1.0      5  -4.0
```

---

### Recomm_ShortInterest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 16330 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Recomm_ShortInterest']

**Observations**:
- Stata:  34,619
- Python: 41,731
- Common: 18,289

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     18289.0000 |     18289.0000 |     18289.0000 |     18289.0000 |
| mean       |         0.5502 |         0.5502 |         0.0000 |         0.0000 |
| std        |         0.4975 |         0.4975 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 18,289

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.92e-14 |     1.86e-16 |   -103.2310 |     0.000 |
| Slope       |       1.0000 |     2.50e-16 |    4.00e+15 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Recomm_ShortInterest
     0   10051  200704                     1
     1   10104  200607                     1
     2   10104  200807                     1
     3   10104  200808                     1
     4   10104  200903                     1
     5   10104  200904                     1
     6   10104  200906                     1
     7   10104  201402                     1
     8   10104  201507                     1
     9   10104  201508                     1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/18289 (0.000%)
- Stata standard deviation: 4.97e-01

---

### TrendFactor

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['TrendFactor']

**Observations**:
- Stata:  2,058,231
- Python: 2,056,304
- Common: 2,055,856

**Precision1**: 97.137% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.87e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |         0.2096 |         0.1784 |        -0.0312 |        -0.2029 |
| std        |         0.1540 |         0.1465 |         0.0635 |         0.4122 |
| min        |        -1.0711 |        -1.0712 |        -0.7739 |        -5.0250 |
| 25%        |         0.1242 |         0.1041 |        -0.0599 |        -0.3890 |
| 50%        |         0.2187 |         0.1842 |        -0.0240 |        -0.1558 |
| 75%        |         0.3000 |         0.2615 |         0.0043 |         0.0276 |
| max        |         3.2757 |         3.2813 |         2.7034 |        17.5546 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0035 + 0.8675 * stata
- **R-squared**: 0.8316
- **N observations**: 2,055,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0035 |     7.08e-05 |    -48.9602 |     0.000 |
| Slope       |       0.8675 |     2.72e-04 |   3186.6579 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1997005/2055856 (97.137%)
- Stata standard deviation: 1.54e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.034304  0.032569 -0.066873
1   10032  202412 -0.029687  0.035968 -0.065654
2   10104  202412 -0.031745  0.034036 -0.065780
3   10107  202412 -0.030432  0.038111 -0.068543
4   10138  202412 -0.027677  0.037830 -0.065507
5   10145  202412 -0.030371  0.036421 -0.066792
6   10158  202412 -0.029219  0.032967 -0.062187
7   10200  202412 -0.029422  0.036853 -0.066275
8   10220  202412 -0.035664  0.030636 -0.066300
9   10252  202412 -0.031521  0.033475 -0.064996
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89901  202010  3.053600  0.350159  2.703441
1   89901  202009  2.889721  0.484879  2.404842
2   91040  201802  2.698260  0.729334  1.968925
3   91040  201803  2.514423  0.577583  1.936839
4   91040  201801  2.339864  0.533972  1.805892
5   91040  201710  0.944249 -0.810950  1.755198
6   89901  202011  1.883874  0.261689  1.622186
7   91040  201711  1.758396  0.145073  1.613322
8   66800  200907  3.200631  1.620982  1.579649
9   91040  201709  0.771731 -0.776422  1.548153
```

---

### VarCF

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['VarCF']

**Observations**:
- Stata:  2,547,003
- Python: 2,547,003
- Common: 2,547,003

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.35e-08 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         1.3777 |         1.3777 |      -3.72e-08 |      -1.70e-10 |
| std        |       219.5846 |       219.5846 |       3.07e-05 |       1.40e-07 |
| min        |         0.0000 |         0.0000 |        -0.0179 |      -8.13e-05 |
| 25%        |       6.28e-04 |       6.28e-04 |      -6.13e-11 |      -2.79e-13 |
| 50%        |         0.0026 |         0.0026 |       4.84e-14 |       2.20e-16 |
| 75%        |         0.0139 |         0.0139 |       6.25e-11 |       2.84e-13 |
| max        |    106471.4300 |    106471.4184 |         0.0062 |       2.83e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,547,003

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.54e-08 |     1.48e-08 |      5.7660 |     0.000 |
| Slope       |       1.0000 |     6.74e-11 |    1.48e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2547003 (0.000%)
- Stata standard deviation: 2.20e+02

---

