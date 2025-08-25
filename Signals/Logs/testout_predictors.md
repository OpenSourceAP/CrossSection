# Predictor Validation Results

**Generated**: 2025-08-24 21:54:29

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
| MomVol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.09%)    | ✅ (99.900th diff 0.0E+00) |
| MomSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99.900th diff 3.0E-07) |
| Mom12m                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99.900th diff 2.5E-07) |
| Mom12mOffSeason           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99.900th diff 1.4E-15) |
| MomRev                    | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.00%)    | ✅ (99.900th diff 0.0E+00) |

**Overall**: 5/5 available predictors passed validation
  - Natural passes: 5
  - Overridden passes: 0
**Python CSVs**: 5/5 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### Mom12m

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom12m']

**Observations**:
- Stata:  3,713,622
- Python: 3,730,107
- Common: 3,713,622

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.50e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.71e+06 |       3.71e+06 |       3.71e+06 |       3.71e+06 |
| mean       |         0.1328 |         0.1328 |      -4.81e-12 |      -6.24e-12 |
| std        |         0.7707 |         0.7707 |       2.10e-08 |       2.72e-08 |
| min        |        -1.0000 |        -1.0000 |      -3.45e-06 |      -4.48e-06 |
| 25%        |        -0.2091 |        -0.2091 |      -4.67e-09 |      -6.06e-09 |
| 50%        |         0.0459 |         0.0459 |         0.0000 |         0.0000 |
| 75%        |         0.3214 |         0.3214 |       4.66e-09 |       6.05e-09 |
| max        |       436.6845 |       436.6845 |       4.31e-06 |       5.60e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,713,622

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.26e-11 |     1.10e-11 |      1.1398 |     0.254 |
| Slope       |       1.0000 |     1.41e-11 |    7.09e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3713622 (0.000%)
- Stata standard deviation: 7.71e-01

---

### Mom12mOffSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom12mOffSeason']

**Observations**:
- Stata:  3,865,561
- Python: 3,865,561
- Common: 3,865,561

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.43e-15 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.87e+06 |       3.87e+06 |       3.87e+06 |       3.87e+06 |
| mean       |         0.0113 |         0.0113 |       2.56e-21 |       4.39e-20 |
| std        |         0.0582 |         0.0582 |       2.93e-17 |       5.03e-16 |
| min        |        -0.5758 |        -0.5758 |      -8.88e-16 |      -1.53e-14 |
| 25%        |        -0.0153 |        -0.0153 |      -2.78e-17 |      -4.77e-16 |
| 50%        |         0.0096 |         0.0096 |         0.0000 |         0.0000 |
| 75%        |         0.0351 |         0.0351 |       2.78e-17 |       4.77e-16 |
| max        |         4.2943 |         4.2943 |       8.88e-16 |       1.53e-14 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,865,561

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.00e-16 |     1.75e-18 |   -399.0188 |     0.000 |
| Slope       |       1.0000 |     2.96e-17 |    3.38e+16 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3865561 (0.000%)
- Stata standard deviation: 5.82e-02

---

### MomRev

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomRev']

**Observations**:
- Stata:  262,210
- Python: 390,919
- Common: 261,800

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    261800.0000 |    261800.0000 |    261800.0000 |    261800.0000 |
| mean       |         0.5601 |         0.5601 |         0.0000 |         0.0000 |
| std        |         0.4964 |         0.4964 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 261,800

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.44e-13 |     2.83e-16 |   -509.8247 |     0.000 |
| Slope       |       1.0000 |     3.79e-16 |    2.64e+15 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/261800 (0.000%)
- Stata standard deviation: 4.96e-01

---

### MomSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomSeason']

**Observations**:
- Stata:  3,398,424
- Python: 3,398,424
- Common: 3,398,424

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.97e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0122 |         0.0122 |       4.37e-12 |       4.32e-11 |
| std        |         0.1011 |         0.1011 |       4.16e-09 |       4.11e-08 |
| min        |        -0.9957 |        -0.9957 |      -3.50e-07 |      -3.46e-06 |
| 25%        |        -0.0317 |        -0.0317 |      -1.00e-09 |      -9.89e-09 |
| 50%        |         0.0070 |         0.0070 |         0.0000 |         0.0000 |
| 75%        |         0.0487 |         0.0487 |       1.00e-09 |       9.89e-09 |
| max        |        15.9845 |        15.9845 |       6.00e-07 |       5.93e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,398,424

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.34e-12 |     2.27e-12 |     -1.9124 |     0.056 |
| Slope       |       1.0000 |     2.23e-11 |    4.48e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3398424 (0.000%)
- Stata standard deviation: 1.01e-01

---

### MomVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomVol']

**Observations**:
- Stata:  1,095,615
- Python: 1,096,292
- Common: 1,095,614

**Precision1**: 0.091% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.10e+06 |       1.10e+06 |       1.10e+06 |       1.10e+06 |
| mean       |         5.7085 |         5.7094 |       9.12e-04 |       3.17e-04 |
| std        |         2.8802 |         2.8808 |         0.0302 |         0.0105 |
| min        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| 75%        |         8.0000 |         8.0000 |         0.0000 |         0.0000 |
| max        |        10.0000 |        10.0000 |         1.0000 |         0.3472 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0002 * stata
- **R-squared**: 0.9999
- **N observations**: 1,095,614

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.81e-05 |     6.40e-05 |     -1.0645 |     0.287 |
| Slope       |       1.0002 |     1.00e-05 |  99913.1172 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 999/1095614 (0.091%)
- Stata standard deviation: 2.88e+00

---

