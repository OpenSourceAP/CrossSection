# Predictor Validation Results

**Generated**: 2025-09-04 12:30:23

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
| sfe                       | ✅         | ❌ (4.48%) | ✅ (-3.5%)   | ✅ (0.0%)     | ✅ (1.0E-07)   | SKIP       |
| RevenueSurprise           | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (2.3E-04)   | SKIP       |
| Activism2                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (2.4E-07)   | SKIP       |
| Activism1                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (0.0E+00)   | SKIP       |
| Governance                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (0.0E+00)   | SKIP       |

**Overall**: 4/5 available predictors passed validation
  - Natural passes: 4
  - Overridden passes: 0
**Python CSVs**: 5/5 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### Activism1

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  108,733
- Python: 108,768
- Common: 108,733

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    108733.0000 |    108733.0000 |    108733.0000 |    108733.0000 |
| mean       |        14.8865 |        14.8865 |         0.0000 |         0.0000 |
| std        |         2.7243 |         2.7243 |         0.0000 |         0.0000 |
| min        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| 25%        |        13.0000 |        13.0000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        17.0000 |        17.0000 |         0.0000 |         0.0000 |
| max        |        23.0000 |        23.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 108,733

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.68e-13 |     2.68e-15 |    286.4583 |     0.000 |
| Slope       |       1.0000 |     1.77e-16 |    5.64e+15 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/108733 (0.000%)
- Stata standard deviation: 2.72e+00

---

### Activism2

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  30,170
- Python: 30,170
- Common: 30,170

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.37e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     30170.0000 |     30170.0000 |     30170.0000 |     30170.0000 |
| mean       |         9.2631 |         9.2631 |      -9.04e-09 |      -7.15e-10 |
| std        |        12.6421 |        12.6421 |       3.44e-07 |       2.72e-08 |
| min        |         0.0000 |         0.0000 |      -4.00e-06 |      -3.16e-07 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         7.4388 |         7.4388 |         0.0000 |         0.0000 |
| 75%        |        10.7284 |        10.7284 |         0.0000 |         0.0000 |
| max        |       221.2826 |       221.2826 |       4.00e-06 |       3.16e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 30,170

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.30e-08 |     2.44e-09 |      9.4380 |     0.000 |
| Slope       |       1.0000 |     1.56e-10 |    6.43e+09 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/30170 (0.000%)
- Stata standard deviation: 1.26e+01

---

### Governance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  334,058
- Python: 334,058
- Common: 334,058

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    334058.0000 |    334058.0000 |    334058.0000 |    334058.0000 |
| mean       |         9.0443 |         9.0443 |         0.0000 |         0.0000 |
| std        |         2.5733 |         2.5733 |         0.0000 |         0.0000 |
| min        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 25%        |         7.0000 |         7.0000 |         0.0000 |         0.0000 |
| 50%        |         9.0000 |         9.0000 |         0.0000 |         0.0000 |
| 75%        |        11.0000 |        11.0000 |         0.0000 |         0.0000 |
| max        |        14.0000 |        14.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 334,058

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.54e-12 |     1.14e-14 |    222.5103 |     0.000 |
| Slope       |       1.0000 |     1.22e-15 |    8.23e+14 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/334058 (0.000%)
- Stata standard deviation: 2.57e+00

---

### RevenueSurprise

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  2,107,489
- Python: 2,107,507
- Common: 2,107,434

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.28e-04 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.11e+06 |       2.11e+06 |       2.11e+06 |       2.11e+06 |
| mean       |         0.0943 |         0.0976 |         0.0033 |       2.85e-05 |
| std        |       116.2025 |       114.0863 |         2.4006 |         0.0207 |
| min        |    -86414.3670 |    -84415.3972 |       -25.5825 |        -0.2202 |
| 25%        |        -0.7785 |        -0.7785 |      -1.56e-07 |      -1.34e-09 |
| 50%        |         0.1277 |         0.1277 |         0.0000 |         0.0000 |
| 75%        |         0.8664 |         0.8663 |       1.56e-07 |       1.34e-09 |
| max        |     27665.5370 |     27665.5361 |      1998.9698 |        17.2025 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0050 + 0.9817 * stata
- **R-squared**: 0.9999
- **N observations**: 2,107,434

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0050 |     7.73e-04 |      6.5117 |     0.000 |
| Slope       |       0.9817 |     6.66e-06 | 147489.3008 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 200/2107434 (0.009%)
- Stata standard deviation: 1.16e+02

---

### sfe

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 27372 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -3.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  611,076
- Python: 589,716
- Common: 583,704

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.02e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    583704.0000 |    583704.0000 |    583704.0000 |    583704.0000 |
| mean       |        -0.0203 |        -0.0203 |      -3.21e-07 |      -1.40e-07 |
| std        |         2.2883 |         2.2883 |       3.13e-04 |       1.37e-04 |
| min        |      -286.8050 |      -286.8050 |        -0.0446 |        -0.0195 |
| 25%        |         0.0261 |         0.0261 |      -1.55e-09 |      -6.77e-10 |
| 50%        |         0.0639 |         0.0639 |      -1.39e-17 |      -6.06e-18 |
| 75%        |         0.0959 |         0.0959 |       1.36e-09 |       5.96e-10 |
| max        |        12.2928 |        12.2928 |         0.0379 |         0.0166 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 583,704

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.22e-07 |     4.10e-07 |     -0.7846 |     0.433 |
| Slope       |       1.0000 |     1.79e-07 |    5.58e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/583704 (0.006%)
- Stata standard deviation: 2.29e+00

---

