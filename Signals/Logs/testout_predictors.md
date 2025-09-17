# Predictor Validation Results

**Generated**: 2025-09-17 14:25:13

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

| Predictor                 | Superset   | NumRows       | Precision1   | Precision2    | T-stat     |
|---------------------------|------------|---------------|--------------|---------------|------------|
| MomOffSeason06YrPlus      | ✅ (0.00%) | ❌ (+9.8%)   | ❌ (1.3%)     | ❌ (3.5E+00)   | ❌ (+0.48)  |
| MomOffSeason11YrPlus      | ✅ (0.00%) | ✅ (+1.8%)   | ❌ (1.5%)     | ❌ (4.6E+00)   | ✅ (-0.03)  |
| MomOffSeason              | ✅ (0.00%) | ✅ (+1.2%)   | ✅ (0.9%)     | ❌ (2.2E+00)   | ✅ (-0.04)  |

**Overall**: 0/3 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 3/3 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### MomOffSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.18% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

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

### MomOffSeason06YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +9.76% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  2,425,319
- Python: 2,662,105
- Common: 2,425,319

**Precision1**: 1.311% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.46e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.43e+06 |       2.43e+06 |       2.43e+06 |       2.43e+06 |
| mean       |         0.0130 |         0.0132 |       1.15e-04 |         0.0036 |
| std        |         0.0324 |         0.0229 |         0.0223 |         0.6882 |
| min        |        -4.8725 |        -0.7500 |       -15.4780 |      -478.1221 |
| 25%        |         0.0027 |         0.0027 |      -4.55e-10 |      -1.40e-08 |
| 50%        |         0.0125 |         0.0125 |         0.0000 |         0.0000 |
| 75%        |         0.0233 |         0.0233 |       4.55e-10 |       1.40e-08 |
| max        |        15.8923 |         0.7811 |         4.8320 |       149.2626 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0065 + 0.5136 * stata
- **R-squared**: 0.5268
- **N observations**: 2,425,319

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0065 |     1.09e-05 |    591.9489 |     0.000 |
| Slope       |       0.5136 |     3.13e-04 |   1643.0826 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 31795/2425319 (1.311%)
- Stata standard deviation: 3.24e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412 -0.016035 -0.019014  0.002980
1   12799  202412  0.019427  0.023379 -0.003953
2   13563  202412 -0.016118 -0.048507  0.032389
3   13828  202412 -0.018830 -0.008100 -0.010729
4   13878  202412  0.007271  0.019389 -0.012117
5   14051  202412 -0.052231 -0.051790 -0.000441
6   15294  202412 -0.048290 -0.073018  0.024727
7   15793  202412 -0.051124 -0.048555 -0.002569
8   16086  202412 -0.011129 -0.002476 -0.008653
9   16773  202412 -0.069418 -0.072436  0.003018
```

**Largest Differences**:
```
   permno  yyyymm    python      stata       diff
0   13755  202011  0.414330  15.892301 -15.477971
1   13755  202111  0.414330  15.892301 -15.477971
2   13755  202211  0.414330  15.892301 -15.477971
3   83382  200510 -0.040478  -4.872470   4.831992
4   10685  199412 -0.042227  -3.649201   3.606974
5   86237  201012 -0.029337   3.244835  -3.274172
6   81728  200612 -0.093591  -3.352354   3.258763
7   88321  200611 -0.122625   2.289885  -2.412510
8   76356  198510  0.037454  -2.300340   2.337795
9   12715  198603 -0.003988   2.214316  -2.218304
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   16408  193402  0.015001 -0.110645  0.125646
1   16408  193403  0.015493 -0.043396  0.058889
2   16408  193802  0.018760 -0.036882  0.055642
3   16408  193502  0.013422 -0.036882  0.050304
4   16408  193602  0.013422 -0.036882  0.050304
5   16408  193702  0.013422 -0.036882  0.050304
6   16408  193807  0.014277 -0.031911  0.046187
7   16408  193407  0.011901 -0.031911  0.043812
8   16408  193507  0.011901 -0.031911  0.043812
9   16408  193607  0.011901 -0.031911  0.043812
```

---

### MomOffSeason11YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.79% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  1,677,532
- Python: 1,707,556
- Common: 1,677,532

**Precision1**: 1.504% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.55e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.0135 |         0.0136 |       5.08e-05 |         0.0020 |
| std        |         0.0254 |         0.0224 |         0.0117 |         0.4586 |
| min        |        -2.6111 |        -0.6522 |        -2.2556 |       -88.7393 |
| 25%        |         0.0034 |         0.0034 |      -4.55e-10 |      -1.79e-08 |
| 50%        |         0.0128 |         0.0128 |         0.0000 |         0.0000 |
| 75%        |         0.0235 |         0.0234 |       4.55e-10 |       1.79e-08 |
| max        |         2.2478 |         1.2500 |         2.6319 |       103.5419 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0030 + 0.7842 * stata
- **R-squared**: 0.7898
- **N observations**: 1,677,532

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0030 |     8.99e-06 |    329.9016 |     0.000 |
| Slope       |       0.7842 |     3.12e-04 |   2510.2788 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 25230/1677532 (1.504%)
- Stata standard deviation: 2.54e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412  0.022511  0.029216 -0.006706
1   12799  202412 -0.005228 -0.080205  0.074976
2   14051  202412 -0.029381 -0.028140 -0.001241
3   32791  202412 -0.002256 -0.009110  0.006855
4   77900  202412  0.015898  0.024432 -0.008534
5   79666  202412  0.023037  0.032062 -0.009025
6   79903  202412 -0.000149  0.000592 -0.000741
7   82156  202412 -0.025388 -0.023979 -0.001408
8   84321  202412  0.014481 -0.102155  0.116636
9   86812  202412  0.023247  0.024643 -0.001396
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11803  201112  0.020796 -2.611104  2.631900
1   77729  200404  0.016586 -2.373474  2.390060
2   33136  197712 -0.007831  2.247807 -2.255638
3   24110  198612 -0.046078  2.129370 -2.175448
4   65518  200005 -0.014146  1.961642 -1.975788
5   36492  197902  0.057469  1.643900 -1.586431
6   11803  201110  0.081820 -1.379478  1.461298
7   86092  201008  0.196499  1.608412 -1.411913
8   82163  201403  0.054147 -1.259050  1.313197
9   14761  200804  0.022150  1.294914 -1.272764
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

