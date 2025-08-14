# Predictor Validation Results

**Generated**: 2025-08-14 17:22:58

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
| PatentsRD                 | ✅         | ✅       | ❌ (21.05%)  | ✅ (0.02%)    | ✅ (99.900th diff 0.0E+00) |
| Mom6mJunk                 | ✅         | ✅       | ❌ (18.09%)  | ✅ (0.28%)    | ❌ (99.900th diff 5.8E-01) |
| DownRecomm                | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.03%)    | ✅ (99.900th diff 0.0E+00) |
| UpRecomm                  | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.02%)    | ✅ (99.900th diff 0.0E+00) |
| RDAbility                 | ✅         | ✅       | ❌ (1.43%)   | ❌ (10.38%)   | ❌ (99.900th diff 4.2E+00) |
| MomRev                    | ✅         | ✅       | ❌ (1.31%)   | ✅ (0.00%)    | ✅ (99.900th diff 0.0E+00) |

**Overall**: 0/6 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 6/6 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

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

