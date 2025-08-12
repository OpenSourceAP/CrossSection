# Predictor Validation Results

**Generated**: 2025-08-12 17:22:51

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 0.001
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| EarnSupBig                | ✅         | ✅       | ❌ (3.76%)   | ✅ (0.16%)    | ❌ (99th diff 6.5E+00)   |
| OrgCap                    | ✅         | ✅       | ✅ (0.02%)   | ❌ (91.02%)   | ❌ (99th diff 1.6E+00)   |
| Frontier                  | ✅         | ✅       | ✅ (0.00%)   | ❌ (84.22%)   | ❌ (99th diff 5.4E-01)   |
| IndRetBig                 | ✅         | ✅       | ✅ (0.25%)   | ✅ (7.12%)    | ❌ (99th diff 8.8E-03)   |
| sinAlgo                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |

**Overall**: 1/5 available predictors passed validation
**Python CSVs**: 5/5 predictors have Python implementation

## Detailed Results

### EarnSupBig

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 87621 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EarnSupBig']

**Observations**:
- Stata:  2,327,518
- Python: 2,533,035
- Common: 2,239,897

**Precision1**: 0.156% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.51e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  EarnSupBig
     0   10002  200811   -0.755143
     1   10002  200812   -1.854773
     2   10003  198806   -0.001391
     3   10003  198807   -0.060459
     4   10003  198808   -0.047608
     5   10006  197804   -2.586295
     6   10006  197805   -2.586295
     7   10006  197806    0.224887
     8   10006  197807    0.224887
     9   10006  197808    0.224887
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3489/2239897 (0.156%)
- Stata standard deviation: 4.73e+12

**Most Recent Bad Observations**:
```
   permno  yyyymm    python         stata          diff
0   10100  200105 -0.382466 -5.363412e+13  5.363412e+13
1   10488  200105 -0.382466 -5.363412e+13  5.363412e+13
2   10680  200105 -0.382466 -5.363412e+13  5.363412e+13
3   11833  200105 -0.382466 -5.363412e+13  5.363412e+13
4   20248  200105 -0.382466 -5.363412e+13  5.363412e+13
5   39773  200105 -0.382466 -5.363412e+13  5.363412e+13
6   62296  200105 -0.382466 -5.363412e+13  5.363412e+13
7   69200  200105 -0.382466 -5.363412e+13  5.363412e+13
8   75526  200105 -0.382466 -5.363412e+13  5.363412e+13
9   75609  200105 -0.382466 -5.363412e+13  5.363412e+13
```

**Largest Differences**:
```
   permno  yyyymm    python         stata          diff
0   10613  197309  0.188875  3.580440e+14 -3.580440e+14
1   11165  197309  0.188875  3.580440e+14 -3.580440e+14
2   12141  197309  0.188875  3.580440e+14 -3.580440e+14
3   14227  197309  0.188875  3.580440e+14 -3.580440e+14
4   14569  197309  0.188875  3.580440e+14 -3.580440e+14
5   14702  197309  0.188875  3.580440e+14 -3.580440e+14
6   15078  197309  0.188875  3.580440e+14 -3.580440e+14
7   15457  197309  0.188875  3.580440e+14 -3.580440e+14
8   16986  197309  0.188875  3.580440e+14 -3.580440e+14
9   17523  197309  0.188875  3.580440e+14 -3.580440e+14
```

---

### Frontier

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Frontier']

**Observations**:
- Stata:  1,221,161
- Python: 1,308,554
- Common: 1,221,161

**Precision1**: 84.223% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.44e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1028495/1221161 (84.223%)
- Stata standard deviation: 9.78e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.677199 -0.780603  0.103404
1   10028  202412 -0.391396 -0.520535  0.129139
2   10066  202412  0.443135  0.568824 -0.125689
3   10104  202412 -2.215219 -1.953049 -0.262170
4   10107  202412 -1.635750 -1.238720 -0.397031
5   10145  202412 -1.328160 -0.719358 -0.608802
6   10200  202412 -0.170885 -0.101468 -0.069417
7   10220  202412 -1.211545 -1.234168  0.022623
8   10253  202412  3.311301  3.423937 -0.112636
9   10318  202412 -0.545215 -0.670803  0.125587
```

**Largest Differences**:
```
   permno  yyyymm        python      stata      diff
0   49315  197306  4.874287e+00  10.828367 -5.954080
1   49315  197307  2.170007e+00   7.243619 -5.073612
2   49315  197308  1.256226e+00   5.702786 -4.446560
3   49315  197309  6.350514e-01   4.663649 -4.028598
4   49315  197310  3.600313e-01   4.100815 -3.740783
5   49315  197311  6.525662e-01   4.171880 -3.519314
6   89631  200406 -2.398082e-14  -3.468813  3.468813
7   12111  199211 -3.463358e-01  -3.732341  3.386005
8   12111  199212 -2.203209e-01  -3.593663  3.373342
9   49315  197312  2.136465e-01   3.569990 -3.356343
```

---

### IndRetBig

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IndRetBig']

**Observations**:
- Stata:  2,607,795
- Python: 2,808,360
- Common: 2,601,282

**Precision1**: 7.120% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.82e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 185206/2601282 (7.120%)
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
0   19183  197409 -0.075931  0.210256 -0.286188
1   56371  197409 -0.075931  0.210256 -0.286188
2   69287  197409 -0.075931  0.210256 -0.286188
3   81649  197409 -0.075931  0.210256 -0.286188
4   13784  193207  0.923912  0.676327  0.247585
5   14381  193207  0.923912  0.676327  0.247585
6   14859  193207  0.923912  0.676327  0.247585
7   16352  193207  0.923912  0.676327  0.247585
8   18083  193207  0.923912  0.676327  0.247585
9   19297  193207  0.923912  0.676327  0.247585
```

---

### OrgCap

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OrgCap']

**Observations**:
- Stata:  1,243,383
- Python: 1,251,842
- Common: 1,243,092

**Precision1**: 91.016% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.59e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1131417/1243092 (91.016%)
- Stata standard deviation: 9.94e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412 -0.093992 -0.115577  0.021585
1   10145  202412 -0.423675  0.067139 -0.490814
2   10158  202412 -1.084997 -0.952382 -0.132615
3   10200  202412 -0.592701 -0.670615  0.077914
4   10220  202412 -0.288887 -0.358309  0.069422
5   10318  202412 -0.567394 -0.386875 -0.180519
6   10333  202412 -0.444889 -0.559429  0.114539
7   10382  202412  0.276140  0.055639  0.220501
8   10421  202412 -0.376262 -0.519943  0.143681
9   10516  202412 -0.841478 -0.470462 -0.371016
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23466  202407  0.587322  5.704437 -5.117115
1   23466  202410  0.597688  5.703661 -5.105974
2   23466  202411  0.598630  5.703661 -5.105031
3   23466  202406  0.576467  5.680564 -5.104097
4   23466  202409  0.612391  5.704437 -5.092047
5   23466  202408  0.614712  5.704437 -5.089725
6   63132  199106  2.167863  7.224134 -5.056271
7   23466  202412  0.609125  5.636973 -5.027849
8   30402  199712  0.709404  5.720303 -5.010899
9   30402  199706  0.695160  5.699004 -5.003845
```

---

### sinAlgo

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sinAlgo']

**Observations**:
- Stata:  233,503
- Python: 1,001,032
- Common: 233,503

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 23/233503 (0.010%)
- Stata standard deviation: 3.84e-01

---

