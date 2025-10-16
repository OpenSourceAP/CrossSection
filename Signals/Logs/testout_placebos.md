# Placebo Validation Results

**Generated**: 2025-10-16 09:53:16

**Configuration**:
- TOL_SUPERSET: 0.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Placebo                   | Superset  | Precision1   | R-squared | Precision2              |
|---------------------------|-----------|--------------|-----------|-------------------------|
| PM_q                      | ❌ (0.00%)   | ✅ (0.00%)    | 0.4222    | ✅ (99th diff 3.0E-09)   |
| OperProfLag_q             | ❌ (0.00%)   | ✅ (0.00%)    | 0.6407    | ✅ (99th diff 1.1E-05)   |
| CBOperProfLagAT_q         | ❌ (0.00%)   | ❌ (15.25%)   | 0.6982    | ❌ (99th diff 1.6E+00)   |
| cfpq                      | ❌ (0.00%)   | ✅ (0.43%)    | 0.9739    | ✅ (99th diff 1.0E-07)   |
| tang_q                    | ❌ (0.00%)   | ✅ (0.01%)    | 0.9994    | ✅ (99th diff 1.6E-07)   |
| OperProfRDLagAT           | ✅ (0.00%)   | ✅ (1.12%)    | 0.9998    | ✅ (99th diff 1.2E-02)   |
| ChangeRoA                 | ❌ (0.00%)   | ✅ (0.02%)    | 0.9999    | ✅ (99th diff 6.7E-08)   |
| GPlag_q                   | ❌ (0.00%)   | ✅ (0.04%)    | 0.9999    | ✅ (99th diff 1.8E-08)   |
| CFq                       | ✅ (0.00%)   | ✅ (0.02%)    | 1.0000    | ✅ (99th diff 2.1E-08)   |
| ChangeRoE                 | ❌ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 3.3E-09)   |
| PayoutYield_q             | ✅ (0.00%)   | ✅ (0.06%)    | 1.0000    | ✅ (99th diff 4.4E-08)   |
| rd_sale_q                 | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 6.7E-09)   |
| depr                      | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 8.8E-09)   |
| AssetTurnover             | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.0E-09)   |
| AMq                       | ❌ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.1E-08)   |

**Overall**: 6/15 available placebos passed validation
**Python CSVs**: 15/15 placebos have Python implementation

## Detailed Results

### AMq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AMq']

**Observations**:
- Stata:  2,584,378
- Python: 2,671,099
- Common: 2,584,377

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.15e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.58e+06 |       2.58e+06 |       2.58e+06 |       2.58e+06 |
| mean       |         3.7379 |         3.7379 |       3.16e-06 |       1.36e-07 |
| std        |        23.2695 |        23.2695 |         0.0035 |       1.50e-04 |
| min        |       -33.6391 |       -33.6391 |        -0.6348 |        -0.0273 |
| 25%        |         0.6615 |         0.6615 |      -3.34e-08 |      -1.44e-09 |
| 50%        |         1.4017 |         1.4017 |         0.0000 |         0.0000 |
| 75%        |         3.2088 |         3.2088 |       3.35e-08 |       1.44e-09 |
| max        |     11549.4230 |     11549.4231 |         3.4533 |         0.1484 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,584,377

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.19e-06 |     2.19e-06 |      1.4540 |     0.146 |
| Slope       |       1.0000 |     9.30e-08 |    1.08e+07 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      AMq
     0   19316  202412 3.937687
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 23/2584377 (0.001%)
- Stata standard deviation: 2.33e+01

---

### AssetTurnover

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover']

**Observations**:
- Stata:  2,796,921
- Python: 2,813,605
- Common: 2,796,921

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.00e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |         5.2784 |         5.2785 |       1.08e-04 |       4.15e-07 |
| std        |       261.1047 |       261.1082 |         0.0761 |       2.92e-04 |
| min        |         0.0000 |        -0.0000 |       -18.4493 |        -0.0707 |
| 25%        |         0.9854 |         0.9854 |      -3.85e-08 |      -1.47e-10 |
| 50%        |         1.8726 |         1.8726 |         0.0000 |         0.0000 |
| 75%        |         3.0805 |         3.0805 |       3.86e-08 |       1.48e-10 |
| max        |    108845.1100 |    108847.6000 |        27.7236 |         0.1062 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,796,921

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.73e-05 |     4.55e-05 |      0.8195 |     0.412 |
| Slope       |       1.0000 |     1.74e-07 |    5.74e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2796921 (0.001%)
- Stata standard deviation: 2.61e+02

---

### CBOperProfLagAT_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CBOperProfLagAT_q']

**Observations**:
- Stata:  1,911,489
- Python: 2,069,900
- Common: 1,911,488

**Precision1**: 15.253% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.62e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         0.0219 |         0.0127 |        -0.0092 |        -0.0523 |
| std        |         0.1758 |         0.1915 |         0.1064 |         0.6052 |
| min        |       -89.0698 |       -89.0698 |       -10.0952 |       -57.4331 |
| 25%        |        -0.0051 |        -0.0078 |      -1.16e-09 |      -6.62e-09 |
| 50%        |         0.0278 |         0.0275 |       1.71e-11 |       9.73e-11 |
| 75%        |         0.0571 |         0.0572 |       1.37e-09 |       7.80e-09 |
| max        |        22.7565 |        22.0339 |         1.8353 |        10.4415 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0072 + 0.9104 * stata
- **R-squared**: 0.6982
- **N observations**: 1,911,488

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0072 |     7.67e-05 |    -94.3982 |     0.000 |
| Slope       |       0.9104 |     4.33e-04 |   2102.8499 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  CBOperProfLagAT_q
     0   19316  202412           0.009463
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 291557/1911488 (15.253%)
- Stata standard deviation: 1.76e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10333  202412 -0.138080 -0.068818 -0.069262
1   10382  202412  0.042999  0.023126  0.019874
2   10516  202412  0.023663  0.018805  0.004858
3   10517  202412 -0.097929  0.305647 -0.403575
4   11144  202412  0.066241  0.050950  0.015291
5   11654  202412 -0.018806 -0.030510  0.011704
6   11731  202412  0.049574  0.026383  0.023191
7   11850  202412  0.045113  0.043205  0.001908
8   12009  202412  0.019519  0.017253  0.002266
9   12017  202412 -0.085506 -0.091540  0.006035
```

**Largest Differences**:
```
   permno  yyyymm    python     stata       diff
0   47271  197509 -7.457557  2.637612 -10.095169
1   47271  197510 -7.457557  2.637612 -10.095169
2   47271  197511 -7.457557  2.637612 -10.095169
3   47271  197506 -6.031755  3.686070  -9.717825
4   47271  197507 -6.031755  3.686070  -9.717825
5   47271  197508 -6.031755  3.686070  -9.717825
6   47271  197512 -6.634300  2.979892  -9.614192
7   47271  197601 -6.634300  2.979892  -9.614192
8   47271  197602 -6.634300  2.979892  -9.614192
9   36784  197407 -5.845767  2.393422  -8.239189
```

---

### CFq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CFq']

**Observations**:
- Stata:  2,797,878
- Python: 3,041,093
- Common: 2,797,878

**Precision1**: 0.020% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.14e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |        -0.0128 |        -0.0128 |       1.39e-05 |       1.18e-05 |
| std        |         1.1714 |         1.1714 |         0.0080 |         0.0069 |
| min        |      -917.6409 |      -917.6410 |        -1.6696 |        -1.4252 |
| 25%        |         0.0039 |         0.0039 |      -6.64e-10 |      -5.67e-10 |
| 50%        |         0.0195 |         0.0195 |      -4.51e-14 |      -3.85e-14 |
| 75%        |         0.0369 |         0.0369 |       6.62e-10 |       5.65e-10 |
| max        |       163.1038 |       163.1038 |         8.6011 |         7.3423 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,797,878

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.33e-05 |     4.80e-06 |      2.7786 |     0.005 |
| Slope       |       1.0000 |     4.10e-06 | 244098.1884 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 572/2797878 (0.020%)
- Stata standard deviation: 1.17e+00

---

### ChangeRoA

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoA']

**Observations**:
- Stata:  2,296,769
- Python: 2,389,987
- Common: 2,296,768

**Precision1**: 0.025% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.72e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |        -0.0019 |        -0.0019 |       2.10e-06 |       8.97e-06 |
| std        |         0.2344 |         0.2344 |         0.0024 |         0.0102 |
| min        |       -55.1174 |       -55.1174 |        -0.8505 |        -3.6276 |
| 25%        |        -0.0078 |        -0.0078 |      -4.27e-10 |      -1.82e-09 |
| 50%        |      -7.35e-05 |      -7.34e-05 |      -3.68e-13 |      -1.57e-12 |
| 75%        |         0.0058 |         0.0058 |       4.28e-10 |       1.83e-09 |
| max        |       136.3447 |       136.3447 |         1.3543 |         5.7764 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 2,296,768

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.95e-06 |     1.57e-06 |      1.2417 |     0.214 |
| Slope       |       0.9999 |     6.70e-06 | 149137.2741 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChangeRoA
     0   19316  202412  -0.036712
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 567/2296768 (0.025%)
- Stata standard deviation: 2.34e-01

---

### ChangeRoE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoE']

**Observations**:
- Stata:  2,360,217
- Python: 2,435,546
- Common: 2,360,216

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.26e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.36e+06 |       2.36e+06 |       2.36e+06 |       2.36e+06 |
| mean       |      -8.46e-04 |      -8.49e-04 |      -3.65e-06 |      -1.17e-07 |
| std        |        31.1263 |        31.1265 |         0.0976 |         0.0031 |
| min        |    -14927.4960 |    -14927.4966 |       -61.0000 |        -1.9598 |
| 25%        |        -0.0196 |        -0.0196 |      -1.10e-09 |      -3.53e-11 |
| 50%        |      -6.95e-04 |      -6.94e-04 |      -1.27e-12 |      -4.09e-14 |
| 75%        |         0.0130 |         0.0130 |       1.09e-09 |       3.50e-11 |
| max        |     14925.0560 |     14925.0557 |        61.0000 |         1.9598 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,360,216

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.65e-06 |     6.35e-05 |     -0.0575 |     0.954 |
| Slope       |       1.0000 |     2.04e-06 | 489862.3152 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChangeRoE
     0   19316  202412  -0.070941
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 91/2360216 (0.004%)
- Stata standard deviation: 3.11e+01

---

### GPlag_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GPlag_q']

**Observations**:
- Stata:  2,216,580
- Python: 2,339,969
- Common: 2,216,579

**Precision1**: 0.037% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.83e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.22e+06 |       2.22e+06 |       2.22e+06 |       2.22e+06 |
| mean       |         0.0808 |         0.0808 |       5.41e-06 |       7.63e-06 |
| std        |         0.7089 |         0.7089 |         0.0065 |         0.0091 |
| min        |        -9.0482 |        -9.0482 |        -3.0442 |        -4.2943 |
| 25%        |         0.0314 |         0.0314 |      -1.36e-09 |      -1.92e-09 |
| 50%        |         0.0731 |         0.0731 |         0.0000 |         0.0000 |
| 75%        |         0.1240 |         0.1240 |       1.36e-09 |       1.92e-09 |
| max        |       598.7442 |       598.7442 |         3.2404 |         4.5711 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,216,579

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.51e-06 |     4.37e-06 |      1.7189 |     0.086 |
| Slope       |       1.0000 |     6.12e-06 | 163304.8505 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  GPlag_q
     0   19316  202412 0.018425
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 825/2216579 (0.037%)
- Stata standard deviation: 7.09e-01

---

### OperProfLag_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfLag_q']

**Observations**:
- Stata:  2,395,707
- Python: 2,481,973
- Common: 2,395,703

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.06e-05 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.40e+06 |       2.40e+06 |       2.40e+06 |       2.40e+06 |
| mean       |       -70.1479 |            N/A |            N/A |            N/A |
| std        |    252624.7247 |            N/A |            N/A |            N/A |
| min        |      -3.48e+08 |           -inf |           -inf |           -inf |
| 25%        |        -0.0048 |        -0.0211 |      -1.79e-08 |      -7.07e-14 |
| 50%        |         0.0444 |         0.0389 |      -1.65e-09 |      -6.54e-15 |
| 75%        |         0.0849 |         0.0783 |       5.05e-09 |       2.00e-14 |
| max        |       9.52e+07 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0844 + 1.0060 * stata
- **R-squared**: 0.6407
- **N observations**: 2,395,691

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0844 |       0.0069 |    -12.1644 |     0.000 |
| Slope       |       1.0060 |     4.87e-04 |   2066.9770 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfLag_q
     0   19316  202412      -0.021109
     1   37233  197003      -1.557332
     2   37233  197004      -1.557332
     3   37233  197005      -1.557332
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2395703 (0.001%)
- Stata standard deviation: 2.53e+05

---

### OperProfRDLagAT

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT']

**Observations**:
- Stata:  2,742,767
- Python: 2,855,231
- Common: 2,742,767

**Precision1**: 1.122% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.19e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.74e+06 |       2.74e+06 |       2.74e+06 |       2.74e+06 |
| mean       |         0.1294 |         0.1302 |       8.35e-04 |       7.03e-04 |
| std        |         1.1878 |         1.1878 |         0.0179 |         0.0151 |
| min        |      -200.7273 |      -200.7273 |        -1.6015 |        -1.3483 |
| 25%        |         0.0319 |         0.0323 |      -2.45e-09 |      -2.07e-09 |
| 50%        |         0.1281 |         0.1287 |       1.23e-10 |       1.03e-10 |
| 75%        |         0.2154 |         0.2162 |       3.48e-09 |       2.93e-09 |
| max        |       226.5365 |       226.5365 |         2.9988 |         2.5246 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0009 + 0.9999 * stata
- **R-squared**: 0.9998
- **N observations**: 2,742,767

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.51e-04 |     1.09e-05 |     78.1040 |     0.000 |
| Slope       |       0.9999 |     9.12e-06 | 109686.6719 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30773/2742767 (1.122%)
- Stata standard deviation: 1.19e+00

---

### PM_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PM_q']

**Observations**:
- Stata:  2,492,083
- Python: 2,823,485
- Common: 2,492,082

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.05e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |        -3.9606 |        -4.4080 |        -0.4474 |        -0.0026 |
| std        |       171.1246 |       263.0373 |       199.9347 |         1.1684 |
| min        |    -64982.0000 |   -183220.0000 |   -183147.0040 |     -1070.2553 |
| 25%        |        -0.0250 |        -0.0250 |      -1.28e-09 |      -7.51e-12 |
| 50%        |         0.0340 |         0.0340 |         0.0000 |         0.0000 |
| 75%        |         0.0816 |         0.0816 |       1.28e-09 |       7.46e-12 |
| max        |     18403.0000 |     28930.0000 |     28930.3781 |       169.0603 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.4520 + 0.9988 * stata
- **R-squared**: 0.4222
- **N observations**: 2,492,082

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.4520 |       0.1267 |     -3.5682 |     0.000 |
| Slope       |       0.9988 |     7.40e-04 |   1349.5667 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      PM_q
     0   19316  202412 -0.461944
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 108/2492082 (0.004%)
- Stata standard deviation: 1.71e+02

---

### PayoutYield_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PayoutYield_q']

**Observations**:
- Stata:  1,310,000
- Python: 2,903,425
- Common: 1,310,000

**Precision1**: 0.064% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.41e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.31e+06 |       1.31e+06 |       1.31e+06 |       1.31e+06 |
| mean       |         0.0309 |         0.0309 |       9.93e-06 |       2.89e-05 |
| std        |         0.3442 |         0.3442 |       9.33e-04 |         0.0027 |
| min        |       1.15e-17 |        -0.0152 |        -0.1056 |        -0.3067 |
| 25%        |         0.0045 |         0.0045 |      -2.96e-10 |      -8.60e-10 |
| 50%        |         0.0106 |         0.0106 |      -2.09e-13 |      -6.07e-13 |
| 75%        |         0.0230 |         0.0231 |       2.97e-10 |       8.63e-10 |
| max        |       217.7060 |       217.7060 |         0.3391 |         0.9851 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,310,000

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.86e-06 |     8.19e-07 |     12.0474 |     0.000 |
| Slope       |       1.0000 |     2.37e-06 | 422102.7711 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 839/1310000 (0.064%)
- Stata standard deviation: 3.44e-01

---

### cfpq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfpq']

**Observations**:
- Stata:  2,252,622
- Python: 2,430,653
- Common: 2,252,621

**Precision1**: 0.432% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.25e+06 |       2.25e+06 |       2.25e+06 |       2.25e+06 |
| mean       |       2.37e-04 |       8.75e-04 |       6.38e-04 |       8.89e-04 |
| std        |         0.7177 |         0.7129 |         0.1161 |         0.1618 |
| min        |      -306.2332 |      -306.2333 |       -20.5189 |       -28.5906 |
| 25%        |        -0.0228 |        -0.0225 |      -9.36e-10 |      -1.30e-09 |
| 50%        |         0.0110 |         0.0111 |       4.86e-13 |       6.78e-13 |
| 75%        |         0.0389 |         0.0389 |       9.50e-10 |       1.32e-09 |
| max        |       250.7536 |       250.7536 |        66.0967 |        92.0978 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9803 * stata
- **R-squared**: 0.9739
- **N observations**: 2,252,621

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.43e-04 |     7.68e-05 |      8.3732 |     0.000 |
| Slope       |       0.9803 |     1.07e-04 |   9163.8064 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     cfpq
     0   19316  202412 0.029232
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 9737/2252621 (0.432%)
- Stata standard deviation: 7.18e-01

---

### depr

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['depr']

**Observations**:
- Stata:  3,462,713
- Python: 3,526,532
- Common: 3,462,713

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.77e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |         0.4261 |         0.4261 |      -1.05e-05 |      -1.17e-06 |
| std        |         8.9356 |         8.9356 |         0.0037 |       4.12e-04 |
| min        |        -2.3523 |        -2.3523 |        -1.4752 |        -0.1651 |
| 25%        |         0.0910 |         0.0910 |      -3.06e-09 |      -3.43e-10 |
| 50%        |         0.1480 |         0.1480 |         0.0000 |         0.0000 |
| 75%        |         0.2717 |         0.2717 |       2.97e-09 |       3.32e-10 |
| max        |      2457.7500 |      2457.7500 |         0.2782 |         0.0311 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,462,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.04e-05 |     1.98e-06 |     -5.2527 |     0.000 |
| Slope       |       1.0000 |     2.22e-07 |    4.51e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132/3462713 (0.004%)
- Stata standard deviation: 8.94e+00

---

### rd_sale_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['rd_sale_q']

**Observations**:
- Stata:  566,115
- Python: 783,507
- Common: 566,115

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    566115.0000 |    566115.0000 |    566115.0000 |    566115.0000 |
| mean       |         7.6746 |         7.6747 |       1.35e-04 |       7.37e-07 |
| std        |       183.2067 |       183.2067 |         0.1055 |       5.76e-04 |
| min        |     -3937.0000 |     -3937.0000 |       -29.0278 |        -0.1584 |
| 25%        |         0.0468 |         0.0468 |      -2.04e-09 |      -1.11e-11 |
| 50%        |         0.1117 |         0.1117 |      -2.22e-16 |      -1.21e-18 |
| 75%        |         0.2509 |         0.2509 |       1.93e-09 |       1.05e-11 |
| max        |     31684.3340 |     31684.3333 |        52.2216 |         0.2850 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 566,115

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.34e-04 |     1.40e-04 |      0.9582 |     0.338 |
| Slope       |       1.0000 |     7.65e-07 |    1.31e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/566115 (0.001%)
- Stata standard deviation: 1.83e+02

---

### tang_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['tang_q']

**Observations**:
- Stata:  1,675,098
- Python: 2,417,352
- Common: 1,675,094

**Precision1**: 0.014% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.55e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.6565 |         0.6565 |      -3.03e-06 |      -8.78e-06 |
| std        |         0.3446 |         0.3447 |         0.0086 |         0.0251 |
| min        |        -0.4077 |        -0.4077 |        -0.9940 |        -2.8845 |
| 25%        |         0.5451 |         0.5451 |      -1.26e-08 |      -3.66e-08 |
| 50%        |         0.6594 |         0.6594 |       2.83e-11 |       8.21e-11 |
| 75%        |         0.7667 |         0.7667 |       1.27e-08 |       3.68e-08 |
| max        |       158.7655 |       158.7656 |         6.1017 |        17.7068 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9994
- **N observations**: 1,675,094

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.51e-06 |     1.44e-05 |      0.3138 |     0.754 |
| Slope       |       1.0000 |     1.94e-05 |  51614.4811 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm   tang_q
     0   12750  198212 0.647900
     1   12750  198301 0.647900
     2   12750  198302 0.647900
     3   19316  202412 0.562276
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 237/1675094 (0.014%)
- Stata standard deviation: 3.45e-01

---

