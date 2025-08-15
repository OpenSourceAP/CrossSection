# Predictor Validation Results

**Generated**: 2025-08-14 19:55:31

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
| AgeIPO                    | ✅         | ❌       | NA          | NA           | NA                      |
| IndIPO                    | ✅         | ❌       | NA          | NA           | NA                      |
| RDIPO                     | ✅         | ❌       | NA          | NA           | NA                      |
| Recomm_ShortInterest      | ✅         | ✅       | ❌ (57.03%)  | ✅ (0.00%)    | ✅ (99.900th diff 0.0E+00) |
| PatentsRD                 | ✅         | ✅       | ❌ (21.05%)  | ✅ (0.02%)    | ✅ (99.900th diff 0.0E+00) |
| Mom6mJunk                 | ✅         | ✅       | ❌ (18.09%)  | ✅ (0.28%)    | ❌ (99.900th diff 5.8E-01) |
| DownRecomm                | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.03%)    | ✅ (99.900th diff 0.0E+00) |
| UpRecomm                  | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.02%)    | ✅ (99.900th diff 0.0E+00) |
| RDAbility                 | ✅         | ✅       | ❌ (1.43%)   | ❌ (10.38%)   | ❌ (99.900th diff 4.2E+00) |
| MomRev                    | ✅         | ✅       | ❌ (1.31%)   | ✅ (0.00%)    | ✅ (99.900th diff 0.0E+00) |
| TrendFactor               | ✅         | ✅       | ✅ (0.12%)   | ❌ (97.13%)   | ❌ (99.900th diff 2.0E+00) |
| MS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (32.97%)   | ❌ (99.900th diff 2.6E+00) |
| CitationsRD               | ✅         | ✅       | ✅ (0.00%)   | ❌ (21.54%)   | ❌ (99.900th diff 2.4E+00) |
| PS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (17.93%)   | ❌ (99.900th diff 2.4E+00) |
| IndRetBig                 | ✅         | ✅       | ✅ (0.21%)   | ❌ (6.70%)    | ❌ (99.900th diff 3.8E-01) |
| DivSeason                 | ✅         | ✅       | ✅ (0.00%)   | ❌ (5.21%)    | ❌ (99.900th diff 2.0E+00) |
| BetaTailRisk              | ✅         | ✅       | ✅ (0.00%)   | ❌ (4.15%)    | ✅ (99.900th diff 4.8E-02) |
| IndMom                    | ✅         | ✅       | ✅ (0.00%)   | ❌ (3.28%)    | ❌ (99.900th diff 1.7E+00) |
| HerfAsset                 | ✅         | ✅       | ✅ (0.00%)   | ❌ (1.44%)    | ❌ (99.900th diff 5.1E-01) |
| VolumeTrend               | ✅         | ✅       | ✅ (0.00%)   | ❌ (1.36%)    | ❌ (99.900th diff 1.8E+00) |
| Tax                       | ✅         | ✅       | ✅ (0.00%)   | ❌ (1.24%)    | ❌ (99.900th diff 1.1E-01) |
| MomOffSeason              | ✅         | ✅       | ✅ (0.00%)   | ❌ (1.06%)    | ❌ (99.900th diff 2.1E+00) |
| NumEarnIncrease           | ✅         | ✅       | ✅ (0.00%)   | ❌ (1.01%)    | ❌ (99.900th diff 3.6E+00) |
| Investment                | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.00%)    | ❌ (99.900th diff 1.8E-01) |
| CredRatDG                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.94%)    | ❌ (99.900th diff 6.6E+00) |
| retConglomerate           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.94%)    | ❌ (99.900th diff 1.2E-01) |
| MomOffSeason06YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.92%)    | ❌ (99.900th diff 1.9E+00) |
| MomOffSeason11YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.88%)    | ❌ (99.900th diff 1.8E+00) |
| Herf                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.79%)    | ❌ (99.900th diff 5.1E-01) |
| MomOffSeason16YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.51%)    | ❌ (99.900th diff 6.1E-01) |
| MomVol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.42%)    | ❌ (99.900th diff 3.5E-01) |
| Mom12mOffSeason           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.17%)    | ❌ (99.900th diff 3.0E-01) |
| EarnSupBig                | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.15%)    | ❌ (99.900th diff 1.5E+00) |
| MRreversal                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.15%)    | ❌ (99.900th diff 2.5E-01) |
| realestate                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.14%)    | ❌ (99.900th diff INF)   |
| ChForecastAccrual         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.12%)    | ❌ (99.900th diff 2.0E+00) |

**Overall**: 0/36 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 36/36 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### BetaTailRisk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaTailRisk']

**Observations**:
- Stata:  2,292,350
- Python: 2,332,084
- Common: 2,292,350

**Precision1**: 4.149% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.77e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.29e+06 |       2.29e+06 |       2.29e+06 |       2.29e+06 |
| mean       |         0.6390 |         0.6390 |      -3.78e-05 |      -7.39e-05 |
| std        |         0.5111 |         0.5109 |         0.0026 |         0.0052 |
| min        |       -10.7373 |       -10.7080 |        -0.0878 |        -0.1719 |
| 25%        |         0.3065 |         0.3066 |      -8.98e-04 |        -0.0018 |
| 50%        |         0.5661 |         0.5661 |      -1.37e-04 |      -2.69e-04 |
| 75%        |         0.8925 |         0.8923 |       4.95e-04 |       9.69e-04 |
| max        |         8.5702 |         8.5711 |         0.1976 |         0.3866 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9996 * stata
- **R-squared**: 1.0000
- **N observations**: 2,292,350

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.99e-04 |     2.78e-06 |     71.7608 |     0.000 |
| Slope       |       0.9996 |     3.39e-06 | 294509.4351 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 95107/2292350 (4.149%)
- Stata standard deviation: 5.11e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16099  202412  0.288367  0.293937 -0.005571
1   16400  202412  1.372777  1.339924  0.032854
2   18148  202412  0.111011  0.116482 -0.005471
3   77437  202412  1.854679  1.846069  0.008610
4   84411  202412  0.911352  0.901888  0.009464
5   89029  202412  0.608437  0.614334 -0.005897
6   89169  202412  1.567852  1.606029 -0.038177
7   16099  202411  0.323722  0.329289 -0.005567
8   16400  202411  1.385534  1.352590  0.032944
9   18148  202411  0.147289  0.152762 -0.005473
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   78050  199811 -0.557545 -0.755131  0.197586
1   78050  199812 -0.396312 -0.593467  0.197155
2   78050  199901 -0.158898 -0.349701  0.190803
3   78050  199902 -0.069994 -0.254714  0.184720
4   78050  199903  0.069028 -0.111589  0.180616
5   78050  199904  0.224322  0.047509  0.176813
6   78050  199905  0.378144  0.209011  0.169132
7   78050  199906  0.461683  0.294377  0.167306
8   78050  199907  0.347299  0.188068  0.159231
9   78050  199908  0.386259  0.234870  0.151388
```

---

### ChForecastAccrual

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChForecastAccrual']

**Observations**:
- Stata:  628,022
- Python: 2,222,319
- Common: 628,022

**Precision1**: 0.118% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    628022.0000 |    628022.0000 |    628022.0000 |    628022.0000 |
| mean       |         0.4775 |         0.4774 |      -1.51e-04 |      -3.03e-04 |
| std        |         0.4995 |         0.4995 |         0.0343 |         0.0688 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0020 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0020 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0010 + 0.9976 * stata
- **R-squared**: 0.9953
- **N observations**: 628,022

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.84e-04 |     5.99e-05 |     16.4257 |     0.000 |
| Slope       |       0.9976 |     8.67e-05 |  11503.3922 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 741/628022 (0.118%)
- Stata standard deviation: 4.99e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   91575  202412     0.0      1  -1.0
1   69032  202411     0.0      1  -1.0
2   69032  202410     0.0      1  -1.0
3   69032  202408     0.0      1  -1.0
4   69032  202407     0.0      1  -1.0
5   21889  202406     1.0      0   1.0
6   21186  202405     0.0      1  -1.0
7   69032  202405     0.0      1  -1.0
8   91575  202405     0.0      1  -1.0
9   69032  202404     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11406  199508     0.0      1  -1.0
1   11406  199509     0.0      1  -1.0
2   11406  199605     0.0      1  -1.0
3   11406  199709     0.0      1  -1.0
4   12473  201111     1.0      0   1.0
5   12473  201212     1.0      0   1.0
6   12473  201308     1.0      0   1.0
7   12473  201311     1.0      0   1.0
8   12473  201404     0.0      1  -1.0
9   12473  201405     0.0      1  -1.0
```

---

### CitationsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 701,940
- Common: 645,360

**Precision1**: 21.536% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.43e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    645360.0000 |    645360.0000 |    645360.0000 |    645360.0000 |
| mean       |         0.2154 |         0.0000 |        -0.2154 |        -0.5239 |
| std        |         0.4111 |         0.0000 |         0.4111 |         1.0000 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.4327 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         0.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.0000 * stata
- **R-squared**: nan
- **N observations**: 645,360

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0000 |       0.0000 |         nan |       nan |
| Slope       |       0.0000 |       0.0000 |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 138984/645360 (21.536%)
- Stata standard deviation: 4.11e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10163  201105     0.0      1  -1.0
1   10259  201105     0.0      1  -1.0
2   10272  201105     0.0      1  -1.0
3   10302  201105     0.0      1  -1.0
4   10382  201105     0.0      1  -1.0
5   10463  201105     0.0      1  -1.0
6   10644  201105     0.0      1  -1.0
7   10874  201105     0.0      1  -1.0
8   11038  201105     0.0      1  -1.0
9   11077  201105     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  198306     0.0      1  -1.0
1   10006  198307     0.0      1  -1.0
2   10006  198308     0.0      1  -1.0
3   10006  198309     0.0      1  -1.0
4   10006  198310     0.0      1  -1.0
5   10006  198311     0.0      1  -1.0
6   10006  198312     0.0      1  -1.0
7   10006  198401     0.0      1  -1.0
8   10006  198402     0.0      1  -1.0
9   10006  198403     0.0      1  -1.0
```

---

### CredRatDG

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CredRatDG']

**Observations**:
- Stata:  2,559,713
- Python: 2,559,715
- Common: 2,559,713

**Precision1**: 0.941% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.63e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.56e+06 |       2.56e+06 |       2.56e+06 |       2.56e+06 |
| mean       |         0.0233 |         0.0155 |        -0.0077 |        -0.0514 |
| std        |         0.1508 |         0.1237 |         0.0967 |         0.6412 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -6.6310 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         6.6310 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0009 + 0.6308 * stata
- **R-squared**: 0.5915
- **N observations**: 2,559,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.52e-04 |     5.00e-05 |     17.0407 |     0.000 |
| Slope       |       0.6308 |     3.28e-04 |   1925.2210 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24086/2559713 (0.941%)
- Stata standard deviation: 1.51e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11990  202412     0.0      1  -1.0
1   13103  202412     0.0      1  -1.0
2   14328  202412     0.0      1  -1.0
3   15395  202412     0.0      1  -1.0
4   16086  202412     0.0      1  -1.0
5   16554  202412     0.0      1  -1.0
6   17672  202412     0.0      1  -1.0
7   18046  202412     0.0      1  -1.0
8   18048  202412     0.0      1  -1.0
9   18368  202412     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  198312     1.0      0   1.0
1   10006  198401     1.0      0   1.0
2   10006  198402     1.0      0   1.0
3   10006  198403     1.0      0   1.0
4   10006  198404     1.0      0   1.0
5   10006  198405     1.0      0   1.0
6   10025  200906     0.0      1  -1.0
7   10025  200907     0.0      1  -1.0
8   10025  200908     0.0      1  -1.0
9   10025  200909     0.0      1  -1.0
```

---

### DivSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivSeason']

**Observations**:
- Stata:  1,775,339
- Python: 4,041,685
- Common: 1,775,337

**Precision1**: 5.214% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.01e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.78e+06 |       1.78e+06 |       1.78e+06 |       1.78e+06 |
| mean       |         0.4456 |         0.3935 |        -0.0520 |        -0.1047 |
| std        |         0.4970 |         0.4885 |         0.2223 |         0.4473 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0120 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0120 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.8830 * stata
- **R-squared**: 0.8070
- **N observations**: 1,775,337

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.01e-04 |     2.16e-04 |      0.4650 |     0.642 |
| Slope       |       0.8830 |     3.24e-04 |   2724.9918 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 92565/1775337 (5.214%)
- Stata standard deviation: 4.97e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13407  202412       0      1    -1
1   14542  202412       0      1    -1
2   15920  202412       0      1    -1
3   16119  202412       0      1    -1
4   16611  202412       0      1    -1
5   17036  202412       0      1    -1
6   20447  202412       0      1    -1
7   20998  202412       0      1    -1
8   21372  202412       0      1    -1
9   21605  202412       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  198603       0      1    -1
1   10001  198604       0      1    -1
2   10001  198606       0      1    -1
3   10001  198607       0      1    -1
4   10001  198609       0      1    -1
5   10001  198610       0      1    -1
6   10001  198612       0      1    -1
7   10001  198701       0      1    -1
8   10001  201507       0      1    -1
9   10001  201510       0      1    -1
```

---

### DownRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 14792 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DownRecomm']

**Observations**:
- Stata:  463,983
- Python: 450,458
- Common: 449,191

**Precision1**: 0.025% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449191.0000 |    449191.0000 |    449191.0000 |    449191.0000 |
| mean       |         0.3815 |         0.3815 |         0.0000 |      -3.95e-21 |
| std        |         0.4857 |         0.4857 |         0.0159 |         0.0328 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0587 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0587 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9989
- **N observations**: 449,191

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.05e-04 |     3.02e-05 |      6.7888 |     0.000 |
| Slope       |       0.9995 |     4.89e-05 |  20427.2154 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DownRecomm
     0   10001  199311           0
     1   10002  200210           0
     2   10010  199311           0
     3   10011  199511           0
     4   10012  199402           0
     5   10016  199312           0
     6   10019  199403           0
     7   10025  199801           0
     8   10026  199311           0
     9   10028  202103           0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 114/449191 (0.025%)
- Stata standard deviation: 4.86e-01

---

### EarnSupBig

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EarnSupBig']

**Observations**:
- Stata:  2,327,518
- Python: 2,336,093
- Common: 2,323,705

**Precision1**: 0.152% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.47e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.32e+06 |       2.32e+06 |       2.32e+06 |       2.32e+06 |
| mean       |       5.45e+10 |        -0.1171 |      -5.45e+10 |        -0.0117 |
| std        |       4.64e+12 |         1.1736 |       4.64e+12 |         1.0000 |
| min        |      -6.79e+13 |       -60.7447 |      -3.58e+14 |       -77.1882 |
| 25%        |        -0.4066 |        -0.3996 |        -0.0034 |      -7.34e-16 |
| 50%        |        -0.0832 |        -0.0830 |       1.93e-09 |       4.17e-22 |
| 75%        |         0.2326 |         0.2271 |         0.0052 |       1.12e-15 |
| max        |       3.58e+14 |        60.4149 |       6.79e+13 |        14.6460 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.1171 + 0.0000 * stata
- **R-squared**: 0.0000
- **N observations**: 2,323,705

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.1171 |     7.70e-04 |   -152.1397 |     0.000 |
| Slope       |     1.53e-15 |     1.66e-16 |      9.2436 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3539/2323705 (0.152%)
- Stata standard deviation: 4.64e+12

**Most Recent Bad Observations**:
```
   permno  yyyymm    python         stata          diff
0   10100  200105  0.068662 -5.363412e+13  5.363412e+13
1   10488  200105  0.068662 -5.363412e+13  5.363412e+13
2   10680  200105  0.068662 -5.363412e+13  5.363412e+13
3   11833  200105  0.068662 -5.363412e+13  5.363412e+13
4   20248  200105  0.068662 -5.363412e+13  5.363412e+13
5   39773  200105  0.068662 -5.363412e+13  5.363412e+13
6   62296  200105  0.068662 -5.363412e+13  5.363412e+13
7   69200  200105  0.068662 -5.363412e+13  5.363412e+13
8   75526  200105  0.068662 -5.363412e+13  5.363412e+13
9   75609  200105  0.068662 -5.363412e+13  5.363412e+13
```

**Largest Differences**:
```
   permno  yyyymm    python         stata          diff
0   10613  197308  0.451178  3.580440e+14 -3.580440e+14
1   11165  197308  0.451178  3.580440e+14 -3.580440e+14
2   12141  197308  0.451178  3.580440e+14 -3.580440e+14
3   14227  197308  0.451178  3.580440e+14 -3.580440e+14
4   14569  197308  0.451178  3.580440e+14 -3.580440e+14
5   14702  197308  0.451178  3.580440e+14 -3.580440e+14
6   15078  197308  0.451178  3.580440e+14 -3.580440e+14
7   15457  197308  0.451178  3.580440e+14 -3.580440e+14
8   16986  197308  0.451178  3.580440e+14 -3.580440e+14
9   17523  197308  0.451178  3.580440e+14 -3.580440e+14
```

---

### Herf

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Herf']

**Observations**:
- Stata:  3,158,336
- Python: 3,165,145
- Common: 3,158,336

**Precision1**: 0.787% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.06e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.16e+06 |       3.16e+06 |       3.16e+06 |       3.16e+06 |
| mean       |         0.3294 |         0.3293 |      -7.55e-05 |      -2.72e-04 |
| std        |         0.2778 |         0.2776 |         0.0102 |         0.0368 |
| min        |         0.0000 |         0.0000 |        -2.2031 |        -7.9297 |
| 25%        |         0.1184 |         0.1185 |      -2.41e-09 |      -8.67e-09 |
| 50%        |         0.2537 |         0.2537 |         0.0000 |         0.0000 |
| 75%        |         0.4723 |         0.4722 |       2.70e-09 |       9.73e-09 |
| max        |         5.5471 |         4.3717 |         0.6667 |         2.3995 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9983 * stata
- **R-squared**: 0.9986
- **N observations**: 3,158,336

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.79e-04 |     8.91e-06 |     53.7839 |     0.000 |
| Slope       |       0.9983 |     2.07e-05 |  48282.1386 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24846/3158336 (0.787%)
- Stata standard deviation: 2.78e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12928  202412  0.396959  0.406861 -0.009902
1   14051  202412  0.132628  0.139513 -0.006885
2   19920  202412  0.205427  0.210144 -0.004717
3   20665  202412  0.165612  0.170717 -0.005105
4   77263  202412  0.638889  0.500000  0.138889
5   77900  202412  0.260348  0.264657 -0.004309
6   79666  202412  0.750000  0.678571  0.071429
7   83577  202412  0.214864  0.237275 -0.022411
8   83840  202412  0.210521  0.237032 -0.026510
9   88937  202412  0.555556  0.500000  0.055556
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   64785  200902  2.598195  4.801324 -2.203130
1   64785  200903  2.878780  5.074786 -2.196006
2   64785  200901  2.316989  4.496621 -2.179632
3   64785  200904  3.159325  5.322203 -2.162878
4   64785  200812  2.035793  4.156070 -2.120277
5   64785  200905  3.439983  5.547128 -2.107145
6   64785  200811  1.777768  3.825085 -2.047317
7   64785  200810  1.519743  3.449967 -1.930225
8   64785  200906  3.515275  5.430809 -1.915533
9   64785  200809  1.261732  3.021262 -1.759530
```

---

### HerfAsset

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['HerfAsset']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 1.444% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.12e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         0.3431 |         0.3429 |      -1.26e-04 |      -4.52e-04 |
| std        |         0.2778 |         0.2776 |         0.0096 |         0.0344 |
| min        |         0.0162 |         0.0162 |        -0.6447 |        -2.3206 |
| 25%        |         0.1214 |         0.1215 |      -2.52e-09 |      -9.08e-09 |
| 50%        |         0.2657 |         0.2657 |         0.0000 |         0.0000 |
| 75%        |         0.4885 |         0.4884 |       2.91e-09 |       1.05e-08 |
| max        |         1.0000 |         1.0000 |         0.6436 |         2.3165 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9985 * stata
- **R-squared**: 0.9988
- **N observations**: 2,547,057

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.78e-04 |     9.50e-06 |     39.8123 |     0.000 |
| Slope       |       0.9985 |     2.15e-05 |  46398.4453 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36791/2547057 (1.444%)
- Stata standard deviation: 2.78e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11153  202412  0.332202  0.372792 -0.040590
1   11379  202412  0.626341  0.635870 -0.009529
2   12928  202412  0.261507  0.459600 -0.198092
3   13563  202412  0.022453  0.019441  0.003012
4   13798  202412  0.430744  0.437600 -0.006856
5   14051  202412  0.132821  0.139013 -0.006191
6   14469  202412  0.026686  0.019441  0.007244
7   15793  202412  0.022510  0.019441  0.003069
8   16773  202412  0.033162  0.019419  0.013743
9   18065  202412  0.583155  0.542521  0.040635
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11511  201705  0.355296  1.000000 -0.644704
1   53137  198208  0.678208  0.034624  0.643584
2   57015  200705  0.376106  1.000000 -0.623894
3   12715  198407  0.376506  1.000000 -0.623494
4   11511  201706  0.382062  1.000000 -0.617938
5   53137  198209  0.651516  0.034969  0.616548
6   57015  200706  0.403188  1.000000 -0.596812
7   12715  198408  0.403625  1.000000 -0.596375
8   73091  199705  0.372989  0.964393 -0.591403
9   11511  201707  0.408854  1.000000 -0.591145
```

---

### IndMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IndMom']

**Observations**:
- Stata:  4,043,138
- Python: 4,044,574
- Common: 4,043,138

**Precision1**: 3.278% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.72e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.04e+06 |       4.04e+06 |       4.04e+06 |       4.04e+06 |
| mean       |         0.0857 |         0.0841 |        -0.0016 |        -0.0093 |
| std        |         0.1736 |         0.1711 |         0.0184 |         0.1062 |
| min        |        -0.9265 |        -0.9265 |        -1.2736 |        -7.3369 |
| 25%        |        -0.0099 |        -0.0104 |      -3.43e-08 |      -1.97e-07 |
| 50%        |         0.0775 |         0.0767 |      -1.39e-09 |      -8.03e-09 |
| 75%        |         0.1676 |         0.1662 |       3.34e-09 |       1.92e-08 |
| max        |        10.5068 |        10.5068 |         0.1070 |         0.6162 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9801 * stata
- **R-squared**: 0.9888
- **N observations**: 4,043,138

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.54e-05 |     1.00e-05 |      9.4990 |     0.000 |
| Slope       |       0.9801 |     5.19e-05 |  18889.0096 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132529/4043138 (3.278%)
- Stata standard deviation: 1.74e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10606  202412  0.221829  0.362349 -0.140520
1   11404  202412  0.268826  0.301823 -0.032996
2   11674  202412  0.268826  0.301823 -0.032996
3   11809  202412  0.268826  0.301823 -0.032996
4   11955  202412  0.268826  0.301823 -0.032996
5   12476  202412  0.268826  0.301823 -0.032996
6   12558  202412  0.268826  0.301823 -0.032996
7   12781  202412  0.268826  0.301823 -0.032996
8   12981  202412  0.221829  0.362349 -0.140520
9   13019  202412  0.268826  0.301823 -0.032996
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11362  200003 -0.086561  1.187011 -1.273572
1   11694  200003 -0.086561  1.187011 -1.273572
2   26650  200003 -0.086561  1.187011 -1.273572
3   38746  200003 -0.086561  1.187011 -1.273572
4   48565  200003 -0.086561  1.187011 -1.273572
5   53831  200003 -0.086561  1.187011 -1.273572
6   54148  200003 -0.086561  1.187011 -1.273572
7   54439  200003 -0.086561  1.187011 -1.273572
8   55036  200003 -0.086561  1.187011 -1.273572
9   62383  200003 -0.086561  1.187011 -1.273572
```

---

### IndRetBig

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IndRetBig']

**Observations**:
- Stata:  2,607,795
- Python: 2,616,695
- Common: 2,602,394

**Precision1**: 6.699% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.80e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.60e+06 |       2.60e+06 |       2.60e+06 |       2.60e+06 |
| mean       |         0.0180 |         0.0180 |       1.34e-06 |       1.90e-05 |
| std        |         0.0704 |         0.0704 |         0.0021 |         0.0299 |
| min        |        -0.4860 |        -0.4717 |        -0.1171 |        -1.6643 |
| 25%        |        -0.0206 |        -0.0206 |      -2.78e-17 |      -3.94e-16 |
| 50%        |         0.0176 |         0.0177 |         0.0000 |         0.0000 |
| 75%        |         0.0554 |         0.0554 |       2.78e-17 |       3.94e-16 |
| max        |         1.8831 |         1.8831 |         0.2476 |         3.5177 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9991
- **N observations**: 2,602,394

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.27e-06 |     1.35e-06 |      3.9202 |     0.000 |
| Slope       |       0.9998 |     1.85e-05 |  53985.8175 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 174345/2602394 (6.699%)
- Stata standard deviation: 7.04e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10032  202412 -0.033698 -0.032256 -0.001442
1   10463  202412 -0.033698 -0.032256 -0.001442
2   10779  202412 -0.033698 -0.032256 -0.001442
3   11154  202412 -0.033698 -0.032256 -0.001442
4   12629  202412 -0.033698 -0.032256 -0.001442
5   13577  202412 -0.061087 -0.064159  0.003072
6   13704  202412 -0.033698 -0.032256 -0.001442
7   14185  202412 -0.061087 -0.064159  0.003072
8   16432  202412 -0.061087 -0.064159  0.003072
9   16560  202412 -0.061087 -0.064159  0.003072
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13784  193207  0.923912  0.676327  0.247585
1   14381  193207  0.923912  0.676327  0.247585
2   14859  193207  0.923912  0.676327  0.247585
3   16352  193207  0.923912  0.676327  0.247585
4   18083  193207  0.923912  0.676327  0.247585
5   19297  193207  0.923912  0.676327  0.247585
6   10886  200204  0.297786  0.093269  0.204517
7   27909  200204  0.297786  0.093269  0.204517
8   48143  200204  0.297786  0.093269  0.204517
9   54084  200204  0.297786  0.093269  0.204517
```

---

### Investment

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Investment']

**Observations**:
- Stata:  2,411,862
- Python: 2,419,987
- Common: 2,411,862

**Precision1**: 0.999% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.76e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |         1.0036 |         1.0035 |      -1.75e-04 |      -9.60e-05 |
| std        |         1.8269 |         1.8280 |         0.0448 |         0.0245 |
| min        |     -2512.3491 |     -2512.3180 |       -31.3369 |       -17.1529 |
| 25%        |         0.6665 |         0.6659 |      -2.24e-08 |      -1.22e-08 |
| 50%        |         0.9327 |         0.9323 |         0.0000 |         0.0000 |
| 75%        |         1.2036 |         1.2035 |       2.24e-08 |       1.23e-08 |
| max        |       253.6225 |       253.6223 |        12.0000 |         6.5685 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 1.0003 * stata
- **R-squared**: 0.9994
- **N observations**: 2,411,862

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.43e-04 |     3.29e-05 |    -13.4392 |     0.000 |
| Slope       |       1.0003 |     1.58e-05 |  63297.3080 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24097/2411862 (0.999%)
- Stata standard deviation: 1.83e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   90979  202606  1.120645  1.083741  0.036904
1   12373  202605  0.000000  0.684501 -0.684501
2   12799  202605  2.904973  1.971440  0.933533
3   14607  202605  0.419918  0.396650  0.023267
4   19912  202605  0.737917  0.925279 -0.187362
5   22899  202605  2.858161  2.718322  0.139839
6   88937  202605  0.563974  0.822234 -0.258260
7   90979  202605  1.142852  1.086498  0.056354
8   12373  202604  0.000000  0.681080 -0.681080
9   12799  202604  3.155432  2.144376  1.011055
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   82215  202006   0.267506  31.604452 -31.336946
1   82215  202007   0.291701  14.516804 -14.225103
2   50139  198108  36.000000  24.000000  12.000000
3   50817  198004  36.000000  24.000000  12.000000
4   51692  198102  36.000000  24.000000  12.000000
5   55335  198506  36.000000  24.000000  12.000000
6   82215  202008   0.320708   9.673856  -9.353148
7   87759  202306  30.158196  21.692593   8.465603
8   82215  202005  -0.016379   7.615222  -7.631601
9   82215  202009   0.356120   7.385860  -7.029740
```

---

### MRreversal

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MRreversal']

**Observations**:
- Stata:  3,518,261
- Python: 4,047,630
- Common: 3,518,261

**Precision1**: 0.147% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.47e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.52e+06 |       3.52e+06 |       3.52e+06 |       3.52e+06 |
| mean       |         0.0735 |         0.0735 |       2.72e-05 |       5.71e-05 |
| std        |         0.4754 |         0.4753 |         0.0279 |         0.0587 |
| min        |        -1.0000 |        -1.0000 |       -10.5241 |       -22.1353 |
| 25%        |        -0.1506 |        -0.1506 |      -3.18e-09 |      -6.68e-09 |
| 50%        |         0.0249 |         0.0249 |         0.0000 |         0.0000 |
| 75%        |         0.2121 |         0.2121 |       3.19e-09 |       6.70e-09 |
| max        |        80.0474 |        80.0474 |        11.6087 |        24.4167 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9979 * stata
- **R-squared**: 0.9966
- **N observations**: 3,518,261

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.82e-04 |     1.51e-05 |     12.1059 |     0.000 |
| Slope       |       0.9979 |     3.13e-05 |  31886.3042 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 5170/3518261 (0.147%)
- Stata standard deviation: 4.75e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14051  202412 -0.397438 -0.477612  0.080173
1   18103  202412  0.124620 -0.832065  0.956685
2   19920  202412 -0.869663 -0.751032 -0.118631
3   22888  202412  0.047891  0.039847  0.008044
4   14051  202411 -0.321738 -0.442272  0.120534
5   18103  202411  1.976194 -0.717398  2.693592
6   19920  202411 -0.912735 -0.671266 -0.241469
7   14051  202410 -0.406779 -0.397438 -0.009341
8   14093  202410 -0.814414 -0.845252  0.030838
9   18103  202410  2.781412 -0.570790  3.352202
```

**Largest Differences**:
```
   permno  yyyymm        python      stata       diff
0   15017  201806  1.074442e+01  -0.864316  11.608738
1   91201  201910 -6.217646e-03  10.517862 -10.524080
2   15017  201712  2.673172e-01  10.744422 -10.477105
3   15017  201801  2.916670e-01  10.612906 -10.321239
4   15017  201802  6.702154e-01  10.871568 -10.201353
5   75302  199310  8.500000e+00  -0.933400   9.433400
6   15017  201803  1.209567e+00   9.984651  -8.775083
7   32352  196704 -2.538463e-07   8.400002  -8.400003
8   76442  199206  1.000001e+00   9.166671  -8.166670
9   77562  199309  6.120002e+00  -0.775281   6.895283
```

---

### MS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MS']

**Observations**:
- Stata:  473,079
- Python: 473,079
- Common: 473,079

**Precision1**: 32.967% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.59e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    473079.0000 |    473079.0000 |    473079.0000 |    473079.0000 |
| mean       |         3.8814 |         3.7610 |        -0.1204 |        -0.0781 |
| std        |         1.5421 |         1.5342 |         1.0648 |         0.6905 |
| min        |         1.0000 |         1.0000 |        -5.0000 |        -3.2424 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         6.0000 |         6.0000 |         5.0000 |         3.2424 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.8246 + 0.7565 * stata
- **R-squared**: 0.5782
- **N observations**: 473,079

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.8246 |       0.0039 |    210.1710 |     0.000 |
| Slope       |       0.7565 |     9.39e-04 |    805.2808 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 155962/473079 (32.967%)
- Stata standard deviation: 1.54e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10104  202412       5      3     2
1   10220  202412       5      3     2
2   10693  202412       6      5     1
3   10966  202412       4      5    -1
4   11275  202412       2      5    -3
5   11308  202412       4      3     1
6   11809  202412       5      6    -1
7   11995  202412       4      5    -1
8   12060  202412       1      4    -3
9   12084  202412       5      6    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11170  199506       6      1     5
1   11170  199507       6      1     5
2   11170  199510       6      1     5
3   11170  199512       6      1     5
4   11170  199601       6      1     5
5   11170  199604       6      1     5
6   11170  199605       6      1     5
7   11170  199704       6      1     5
8   11170  199705       6      1     5
9   11233  199506       1      6    -5
```

---

### Mom12mOffSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Mom12mOffSeason']

**Observations**:
- Stata:  3,865,561
- Python: 3,872,777
- Common: 3,865,561

**Precision1**: 0.174% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.03e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.87e+06 |       3.87e+06 |       3.87e+06 |       3.87e+06 |
| mean       |         0.0113 |         0.0113 |      -9.37e-06 |      -1.61e-04 |
| std        |         0.0582 |         0.0582 |         0.0027 |         0.0468 |
| min        |        -0.5758 |        -0.5758 |        -0.5937 |       -10.2025 |
| 25%        |        -0.0153 |        -0.0153 |      -2.78e-17 |      -4.77e-16 |
| 50%        |         0.0096 |         0.0096 |         0.0000 |         0.0000 |
| 75%        |         0.0351 |         0.0351 |       2.78e-17 |       4.77e-16 |
| max        |         4.2943 |         4.2943 |         1.7645 |        30.3232 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9989 * stata
- **R-squared**: 0.9978
- **N observations**: 3,865,561

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.18e-06 |     1.41e-06 |      2.2562 |     0.024 |
| Slope       |       0.9989 |     2.38e-05 |  41987.6080 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6707/3865561 (0.174%)
- Stata standard deviation: 5.82e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14051  202412 -0.151982 -0.153266  0.001284
1   19920  202412 -0.039768 -0.047076  0.007308
2   14051  202411 -0.106340 -0.152717  0.046378
3   19920  202411 -0.060098 -0.066228  0.006131
4   14051  202410 -0.111803 -0.173580  0.061776
5   14093  202410  0.389423  0.447282 -0.057859
6   19920  202410 -0.095871 -0.039879 -0.055992
7   22888  202410  0.081582  0.165685 -0.084103
8   14051  202409 -0.124234 -0.109630 -0.014603
9   19920  202409 -0.058692  0.002076 -0.060769
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13755  202105  1.868581  0.104096  1.764484
1   13755  202104  1.868807  0.117770  1.751037
2   13755  202103  1.854758  0.132826  1.721932
3   89169  202011  0.924470  0.061787  0.862683
4   91201  201909  0.581489 -0.078939  0.660428
5   91201  201908  0.581671 -0.068485  0.650155
6   15017  201806  0.616414  1.210090 -0.593676
7   92161  199001  0.358816 -0.108663  0.467479
8   76442  199203  0.391427 -0.070062  0.461488
9   81215  199605  0.527138  0.075588  0.451550
```

---

### Mom6mJunk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 70860 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Mom6mJunk']

**Observations**:
- Stata:  391,738
- Python: 328,709
- Common: 320,878

**Precision1**: 0.281% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.77e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    320878.0000 |    320878.0000 |    320878.0000 |    320878.0000 |
| mean       |         0.0545 |         0.0544 |      -1.69e-04 |      -4.38e-04 |
| std        |         0.3852 |         0.3855 |         0.0174 |         0.0452 |
| min        |        -0.9947 |        -0.9947 |        -1.1543 |        -2.9969 |
| 25%        |        -0.1332 |        -0.1335 |      -2.99e-09 |      -7.76e-09 |
| 50%        |         0.0332 |         0.0333 |       9.17e-15 |       2.38e-14 |
| 75%        |         0.2000 |         0.2000 |       2.99e-09 |       7.77e-09 |
| max        |        47.6527 |        47.6527 |         1.2493 |         3.2436 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 0.9999 * stata
- **R-squared**: 0.9980
- **N observations**: 320,878

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.63e-04 |     3.11e-05 |     -5.2579 |     0.000 |
| Slope       |       0.9999 |     7.98e-05 |  12523.5442 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Mom6mJunk
     0   10026  201509   0.071515
     1   10026  201510   0.096434
     2   10026  201511   0.146379
     3   10026  201512   0.057645
     4   10026  201601  -0.007851
     5   10026  201602  -0.046296
     6   10026  201603  -0.021993
     7   10026  201604  -0.112035
     8   10026  201605  -0.127242
     9   10026  201606  -0.092484
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 903/320878 (0.281%)
- Stata standard deviation: 3.85e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   90979  202401 -0.064794  0.150524 -0.215318
1   90979  202312 -0.190532  0.065445 -0.255977
2   90979  202311 -0.348997 -0.103403 -0.245594
3   90353  202310  0.379207  0.206912  0.172295
4   90756  202310  0.153710  0.297667 -0.143957
5   90979  202310 -0.478251 -0.271199 -0.207052
6   90353  202309  0.537673  0.248826  0.288847
7   90756  202309  0.434465  0.411892  0.022573
8   90979  202309 -0.290354 -0.240253 -0.050101
9   90353  202308  0.491526  0.339849  0.151677
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10342  200001  1.736612  0.487289  1.249323
1   86360  200106 -0.469291  0.685000 -1.154291
2   69075  199304 -0.312500  0.833333 -1.145833
3   90352  201210 -0.685484  0.426830 -1.112313
4   80658  200110  1.066668  0.000000  1.066668
5   48565  199307  1.333332  0.272727  1.060605
6   24731  198604 -0.459091  0.545455 -1.004546
7   67126  199002  1.821039  0.829268  0.991771
8   83161  200409  0.763565 -0.222222  0.985787
9   79338  200206  0.933027 -0.043428  0.976455
```

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

### MomRev

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3435 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomRev']

**Observations**:
- Stata:  262,210
- Python: 266,100
- Common: 258,775

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    258775.0000 |    258775.0000 |    258775.0000 |    258775.0000 |
| mean       |         0.5549 |         0.5549 |         0.0000 |         0.0000 |
| std        |         0.4970 |         0.4970 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 258,775

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.13e-13 |     1.45e-15 |   -354.3934 |     0.000 |
| Slope       |       1.0000 |     1.94e-15 |    5.15e+14 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  MomRev
     0   10028  200710       1
     1   10028  201707       1
     2   10057  197705       1
     3   10071  199007       1
     4   10087  200006       1
     5   10095  198911       1
     6   10100  200604       1
     7   10108  200504       1
     8   10142  199809       1
     9   10143  199104       1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/258775 (0.000%)
- Stata standard deviation: 4.97e-01

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

### NumEarnIncrease

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['NumEarnIncrease']

**Observations**:
- Stata:  2,823,456
- Python: 2,823,459
- Common: 2,823,456

**Precision1**: 1.010% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.63e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.82e+06 |       2.82e+06 |       2.82e+06 |       2.82e+06 |
| mean       |         1.2268 |         1.1965 |        -0.0303 |        -0.0157 |
| std        |         1.9293 |         1.9120 |         0.3730 |         0.1933 |
| min        |         0.0000 |         0.0000 |        -8.0000 |        -4.1465 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| max        |         8.0000 |         8.0000 |         8.0000 |         4.1465 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0036 + 0.9724 * stata
- **R-squared**: 0.9627
- **N observations**: 2,823,456

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0036 |     2.60e-04 |     13.8365 |     0.000 |
| Slope       |       0.9724 |     1.14e-04 |   8538.4923 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 28519/2823456 (1.010%)
- Stata standard deviation: 1.93e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13919  202412       0      3    -3
1   14987  202412       0      1    -1
2   15065  202412       0      5    -5
3   15129  202412       0      1    -1
4   15433  202412       0      4    -4
5   16048  202412       0      1    -1
6   16310  202412       0      1    -1
7   16536  202412       0      7    -7
8   16541  202412       0      4    -4
9   17809  202412       0      3    -3
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10056  200103       0      8    -8
1   10056  200104       0      8    -8
2   10056  200105       0      8    -8
3   10072  199209       0      8    -8
4   10082  199212       0      8    -8
5   10082  199304       0      8    -8
6   10082  199305       0      8    -8
7   10083  199006       0      8    -8
8   10083  199007       0      8    -8
9   10083  199008       0      8    -8
```

---

### PS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PS']

**Observations**:
- Stata:  463,944
- Python: 464,239
- Common: 463,941

**Precision1**: 17.931% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.36e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    463941.0000 |    463941.0000 |    463941.0000 |    463941.0000 |
| mean       |         5.0197 |         4.9729 |        -0.0468 |        -0.0276 |
| std        |         1.6958 |         1.8091 |         0.4595 |         0.2709 |
| min        |         0.0000 |         0.0000 |        -5.0000 |        -2.9484 |
| 25%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 50%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 75%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| max        |         9.0000 |         9.0000 |         6.0000 |         3.5381 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.2090 + 1.0323 * stata
- **R-squared**: 0.9364
- **N observations**: 463,941

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.2090 |       0.0021 |    -99.8754 |     0.000 |
| Slope       |       1.0323 |     3.95e-04 |   2613.7993 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 83191/463941 (17.931%)
- Stata standard deviation: 1.70e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11593  202412     5.0      6  -1.0
1   12641  202412     6.0      7  -1.0
2   13583  202412     8.0      7   1.0
3   13919  202412     5.0      6  -1.0
4   14419  202412     3.0      4  -1.0
5   14468  202412     3.0      4  -1.0
6   14540  202412     5.0      6  -1.0
7   14601  202412     5.0      6  -1.0
8   14791  202412     6.0      5   1.0
9   14826  202412     2.0      3  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10193  198802     7.0      1   6.0
1   10193  198803     7.0      1   6.0
2   10193  198809     1.0      6  -5.0
3   10193  198810     1.0      6  -5.0
4   10193  198811     1.0      6  -5.0
5   11317  198304     2.0      7  -5.0
6   11484  199603     1.0      6  -5.0
7   11538  199101     0.0      5  -5.0
8   11538  199102     0.0      5  -5.0
9   11538  199103     0.0      5  -5.0
```

---

### PatentsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 141420 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PatentsRD']

**Observations**:
- Stata:  671,832
- Python: 571,284
- Common: 530,412

**Precision1**: 0.023% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    530412.0000 |    530412.0000 |    530412.0000 |    530412.0000 |
| mean       |       2.26e-04 |         0.0000 |      -2.26e-04 |        -0.0150 |
| std        |         0.0150 |         0.0000 |         0.0150 |         1.0000 |
| min        |         0.0000 |         0.0000 |        -1.0000 |       -66.4913 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         0.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.0000 * stata
- **R-squared**: nan
- **N observations**: 530,412

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0000 |       0.0000 |         nan |       nan |
| Slope       |       0.0000 |       0.0000 |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  PatentsRD
     0   10006  198306          1
     1   10006  198307          1
     2   10006  198308          1
     3   10006  198309          1
     4   10006  198310          1
     5   10006  198311          1
     6   10006  198312          1
     7   10006  198401          1
     8   10006  198402          1
     9   10006  198403          1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 120/530412 (0.023%)
- Stata standard deviation: 1.50e-02

---

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2474 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 186,735
- Common: 170,792

**Precision1**: 10.378% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.21e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    170792.0000 |    170792.0000 |    170792.0000 |    170792.0000 |
| mean       |         0.4665 |         0.4237 |        -0.0428 |        -0.0080 |
| std        |         5.3811 |         5.7735 |         2.5914 |         0.4816 |
| min        |      -170.7315 |      -184.0284 |      -192.6819 |       -35.8070 |
| 25%        |        -0.3170 |        -0.3265 |      -2.25e-07 |      -4.18e-08 |
| 50%        |         0.4038 |         0.3761 |      -1.85e-09 |      -3.44e-10 |
| 75%        |         1.4004 |         1.3577 |       1.72e-07 |       3.20e-08 |
| max        |        83.8592 |       121.3608 |       120.7873 |        22.4465 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0240 + 0.9596 * stata
- **R-squared**: 0.7999
- **N observations**: 170,792

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0240 |       0.0063 |     -3.8242 |     0.000 |
| Slope       |       0.9596 |       0.0012 |    826.4031 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RDAbility
     0   10116  201606   0.825915
     1   10116  201607   0.825915
     2   10116  201608   0.825915
     3   10116  201609   0.825915
     4   10116  201610   0.825915
     5   10116  201611   0.825915
     6   10116  201612   0.825915
     7   10116  201701   0.825915
     8   10116  201702   0.825915
     9   10116  201703   0.825915
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 17724/170792 (10.378%)
- Stata standard deviation: 5.38e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16968  202606  2.676225  4.362977 -1.686752
1   13159  202605  0.510686  0.628990 -0.118303
2   13918  202605  0.010309  0.838733 -0.828424
3   14051  202605  0.131522  0.408131 -0.276609
4   14245  202605  0.864758  0.997209 -0.132450
5   14272  202605  0.272244  0.369297 -0.097053
6   14432  202605  0.768600  0.448311  0.320289
7   14436  202605  0.224077  0.334133 -0.110056
8   14551  202605  0.181759  0.240248 -0.058489
9   14556  202605  0.203567  0.303276 -0.099709
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

### Recomm_ShortInterest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 19744 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Recomm_ShortInterest']

**Observations**:
- Stata:  34,619
- Python: 35,589
- Common: 14,875

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     14875.0000 |     14875.0000 |     14875.0000 |     14875.0000 |
| mean       |         0.6764 |         0.6764 |         0.0000 |         0.0000 |
| std        |         0.4679 |         0.4679 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 14,875

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.14e-15 |     3.69e-17 |    112.1720 |     0.000 |
| Slope       |       1.0000 |     4.49e-17 |    2.23e+16 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 0/14875 (0.000%)
- Stata standard deviation: 4.68e-01

---

### Tax

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Tax']

**Observations**:
- Stata:  3,211,651
- Python: 3,213,292
- Common: 3,211,651

**Precision1**: 1.244% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.10e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.21e+06 |       3.21e+06 |       3.21e+06 |       3.21e+06 |
| mean       |         1.1689 |         1.1833 |         0.0144 |       7.57e-04 |
| std        |        19.0252 |        19.4556 |         4.0707 |         0.2140 |
| min        |     -2742.5000 |     -2742.5000 |        -1.0000 |        -0.0526 |
| 25%        |         0.0341 |         0.0265 |      -1.74e-08 |      -9.15e-10 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.4267 |         1.4359 |       1.28e-10 |       6.75e-12 |
| max        |      4463.7114 |      4463.7113 |      2022.5294 |       106.3082 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0144 + 1.0000 * stata
- **R-squared**: 0.9562
- **N observations**: 3,211,651

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0144 |       0.0023 |      6.3339 |     0.000 |
| Slope       |       1.0000 |     1.19e-04 |   8375.7860 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 39943/3211651 (1.244%)
- Stata standard deviation: 1.90e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python  stata       diff
0   22084  202606  29.805790    1.0  28.805790
1   55984  202606  -0.000000    1.0  -1.000000
2   12751  202605   0.121108    1.0  -0.878892
3   13332  202605   0.001470    1.0  -0.998530
4   14618  202605   0.004255    1.0  -0.995745
5   14734  202605  -0.000000    1.0  -1.000000
6   15305  202605   0.002373    1.0  -0.997627
7   15636  202605   0.153538    1.0  -0.846462
8   16401  202605   0.212764    1.0  -0.787236
9   17036  202605   0.077854    1.0  -0.922146
```

**Largest Differences**:
```
   permno  yyyymm       python  stata         diff
0   26542  198906  2023.529412    1.0  2022.529412
1   26542  198907  2023.529412    1.0  2022.529412
2   26542  198908  2023.529412    1.0  2022.529412
3   26542  198909  2023.529412    1.0  2022.529412
4   26542  198910  2023.529412    1.0  2022.529412
5   26542  198911  2023.529412    1.0  2022.529412
6   26542  198912  2023.529412    1.0  2022.529412
7   26542  199001  2023.529412    1.0  2022.529412
8   26542  199002  2023.529412    1.0  2022.529412
9   26542  199003  2023.529412    1.0  2022.529412
```

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

**Precision1**: 97.125% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.03e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |         0.2096 |         0.1785 |        -0.0311 |        -0.2019 |
| std        |         0.1540 |         0.1435 |         0.0551 |         0.3579 |
| min        |        -1.0711 |        -1.0712 |        -0.4212 |        -2.7352 |
| 25%        |         0.1242 |         0.1072 |        -0.0604 |        -0.3921 |
| 50%        |         0.2187 |         0.1848 |        -0.0256 |        -0.1663 |
| 75%        |         0.3000 |         0.2611 |         0.0031 |         0.0200 |
| max        |         3.2757 |         3.2813 |         2.7034 |        17.5546 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0038 + 0.8698 * stata
- **R-squared**: 0.8719
- **N observations**: 2,055,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0038 |     6.05e-05 |    -62.9716 |     0.000 |
| Slope       |       0.8698 |     2.32e-04 |   3741.4551 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1996758/2055856 (97.125%)
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

### UpRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 14792 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['UpRecomm']

**Observations**:
- Stata:  463,983
- Python: 450,458
- Common: 449,191

**Precision1**: 0.023% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449191.0000 |    449191.0000 |    449191.0000 |    449191.0000 |
| mean       |         0.3622 |         0.3622 |       2.23e-06 |       4.63e-06 |
| std        |         0.4806 |         0.4806 |         0.0153 |         0.0318 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0806 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0806 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9990
- **N observations**: 449,191

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.85e-04 |     2.86e-05 |      6.4772 |     0.000 |
| Slope       |       0.9995 |     4.75e-05 |  21061.2947 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  UpRecomm
     0   10001  199311         0
     1   10002  200210         0
     2   10010  199311         0
     3   10011  199511         0
     4   10012  199402         0
     5   10016  199312         0
     6   10019  199403         0
     7   10025  199801         0
     8   10026  199311         0
     9   10028  202103         0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 105/449191 (0.023%)
- Stata standard deviation: 4.81e-01

---

### VolumeTrend

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['VolumeTrend']

**Observations**:
- Stata:  3,655,889
- Python: 5,153,763
- Common: 3,655,889

**Precision1**: 1.357% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.80e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.66e+06 |       3.66e+06 |       3.66e+06 |       3.66e+06 |
| mean       |         0.0057 |         0.0057 |       5.70e-05 |         0.0028 |
| std        |         0.0207 |         0.0208 |         0.0022 |         0.1068 |
| min        |        -0.0566 |        -0.0517 |        -0.0631 |        -3.0497 |
| 25%        |        -0.0068 |        -0.0069 |      -2.22e-10 |      -1.07e-08 |
| 50%        |         0.0052 |         0.0052 |       6.53e-13 |       3.16e-11 |
| 75%        |         0.0184 |         0.0186 |       2.32e-10 |       1.12e-08 |
| max        |         0.0664 |         0.1665 |         0.1636 |         7.9103 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9983 * stata
- **R-squared**: 0.9887
- **N observations**: 3,655,889

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.67e-05 |     1.20e-06 |     55.6825 |     0.000 |
| Slope       |       0.9983 |     5.59e-05 |  17866.8269 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49596/3655889 (1.357%)
- Stata standard deviation: 2.07e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.042738 -0.007268 -0.035470
1   10253  202412 -0.051729 -0.054648  0.002919
2   11153  202412 -0.051729  0.001885 -0.053615
3   11379  202412 -0.036342 -0.014016 -0.022326
4   12828  202412 -0.051729 -0.054894  0.003165
5   12839  202412 -0.051729 -0.055632  0.003903
6   12928  202412  0.108894 -0.000076  0.108969
7   13563  202412 -0.019177 -0.051617  0.032440
8   13779  202412 -0.051729 -0.052743  0.001014
9   13828  202412 -0.051729 -0.036236 -0.015493
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   83630  201203  0.125749 -0.037886  0.163634
1   88937  202412  0.166484  0.006299  0.160185
2   83630  201204  0.119393 -0.032068  0.151461
3   30744  200111  0.155265  0.008748  0.146517
4   84521  201001  0.130462 -0.014673  0.145135
5   27167  201712  0.147492  0.003482  0.144010
6   83630  201205  0.112769 -0.029291  0.142060
7   84757  202003  0.145373  0.004022  0.141350
8   30744  200112  0.146678  0.008842  0.137836
9   27167  201801  0.141298  0.003938  0.137359
```

---

### realestate

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['realestate']

**Observations**:
- Stata:  1,448,154
- Python: 1,448,163
- Common: 1,448,154

**Precision1**: 0.144% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = inf (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.45e+06 |       1.45e+06 |       1.45e+06 |       1.45e+06 |
| mean       |      -9.58e-12 |           -inf |           -inf |           -inf |
| std        |         0.2476 |            N/A |            N/A |            N/A |
| min        |        -1.6407 |           -inf |           -inf |           -inf |
| 25%        |        -0.1188 |        -0.1191 |      -7.45e-09 |      -3.01e-08 |
| 50%        |        -0.0155 |        -0.0156 |         0.0000 |         0.0000 |
| 75%        |         0.0987 |         0.0986 |       7.51e-09 |       3.03e-08 |
| max        |        56.9154 |        56.9154 |         0.0043 |         0.0172 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -inf + nan * stata
- **R-squared**: nan
- **N observations**: 1,448,154

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2091/1448154 (0.144%)
- Stata standard deviation: 2.48e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12540  202412 -0.225637 -0.229901  0.004265
1   13142  202412  0.279480  0.275215  0.004265
2   13599  202412 -0.015268 -0.019533  0.004265
3   13760  202412 -0.441574 -0.445839  0.004265
4   14221  202412  0.228272  0.224007  0.004265
5   14339  202412  0.036196  0.031932  0.004265
6   14785  202412 -0.030344 -0.034609  0.004265
7   14985  202412 -0.078596 -0.082861  0.004265
8   15113  202412  0.148575  0.144310  0.004265
9   15802  202412  0.514576  0.510311  0.004265
```

**Largest Differences**:
```
   permno  yyyymm  python     stata  diff
0   10018  198704    -inf -0.186210  -inf
1   10018  198705    -inf -0.183145  -inf
2   10083  198612    -inf -0.145091  -inf
3   10083  198701    -inf -0.137382  -inf
4   10083  198702    -inf -0.133630  -inf
5   10083  198703    -inf -0.123486  -inf
6   10083  198704    -inf -0.121291  -inf
7   10083  198705    -inf -0.118227  -inf
8   10089  198704    -inf  0.018986  -inf
9   10089  198705    -inf  0.022050  -inf
```

---

### retConglomerate

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['retConglomerate']

**Observations**:
- Stata:  758,394
- Python: 759,896
- Common: 758,382

**Precision1**: 0.936% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.16e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    758382.0000 |    758382.0000 |    758382.0000 |    758382.0000 |
| mean       |         0.0106 |         0.0106 |      -1.25e-05 |      -1.49e-04 |
| std        |         0.0841 |         0.0841 |         0.0020 |         0.0240 |
| min        |        -0.8000 |        -0.8000 |        -0.4277 |        -5.0889 |
| 25%        |        -0.0313 |        -0.0313 |      -2.78e-17 |      -3.30e-16 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0495 |         0.0495 |       2.78e-17 |       3.30e-16 |
| max        |         4.3779 |         4.3779 |         0.4479 |         5.3290 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9997 * stata
- **R-squared**: 0.9994
- **N observations**: 758,382

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.83e-06 |     2.33e-06 |     -4.2168 |     0.000 |
| Slope       |       0.9997 |     2.75e-05 |  36318.4957 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7102/758382 (0.936%)
- Stata standard deviation: 8.41e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202412  0.056786  0.054399  0.002387
1   10253  202412  0.056786  0.054399  0.002387
2   10516  202412 -0.032018 -0.030640 -0.001378
3   10517  202412 -0.042844 -0.046507  0.003663
4   10547  202412  0.154688  0.156824 -0.002136
5   11308  202412 -0.032018 -0.030640 -0.001378
6   11533  202412  0.056786  0.054399  0.002387
7   11600  202412  0.018936  0.009173  0.009763
8   11664  202412  0.056786  0.054399  0.002387
9   11674  202412 -0.015938 -0.021246  0.005307
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   92294  202312  0.442967 -0.004954  0.447922
1   89704  202312  0.504775  0.063121  0.441655
2   92294  202303 -0.317724  0.110011 -0.427735
3   89704  202303 -0.449552 -0.110565 -0.338987
4   89704  202310  0.261615 -0.065595  0.327210
5   92294  202310  0.258598 -0.030708  0.289307
6   91617  200908 -0.137183  0.118579 -0.255762
7   89704  202301 -0.010305  0.221066 -0.231371
8   89704  202311  0.167854 -0.054588  0.222442
9   78432  200312  0.206723  0.009501  0.197222
```

---

### AgeIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 353,486
- Common: 0

---

### IndIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 4,047,630
- Common: 0

---

### RDIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 3,625,491
- Common: 0

---

