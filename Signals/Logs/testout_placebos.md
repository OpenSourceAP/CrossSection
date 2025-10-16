# Placebo Validation Results

**Generated**: 2025-10-16 11:37:10

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
| GrGMToGrSales             | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.3E-09)   |
| EarningsConservatism      | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 1.4E-07)   |

**Overall**: 2/2 available placebos passed validation
**Python CSVs**: 2/2 placebos have Python implementation

## Detailed Results

### EarningsConservatism

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsConservatism']

**Observations**:
- Stata:  1,467,671
- Python: 1,495,202
- Common: 1,467,671

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.45e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.47e+06 |       1.47e+06 |       1.47e+06 |       1.47e+06 |
| mean       |       -60.3159 |       -60.3726 |        -0.0567 |      -2.91e-06 |
| std        |     19491.2782 |     19490.5670 |        15.2672 |       7.83e-04 |
| min        |      -6.48e+06 |      -6.48e+06 |     -4582.1725 |        -0.2351 |
| 25%        |        -5.1421 |        -5.1259 |      -6.14e-07 |      -3.15e-11 |
| 50%        |         0.9096 |         0.9198 |         0.0000 |         0.0000 |
| 75%        |         5.4537 |         5.4463 |       6.39e-07 |       3.28e-11 |
| max        |    872129.2500 |    872120.6238 |       243.2624 |         0.0125 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0589 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,467,671

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0589 |       0.0126 |     -4.6773 |     0.000 |
| Slope       |       1.0000 |     6.46e-07 |    1.55e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/1467671 (0.006%)
- Stata standard deviation: 1.95e+04

---

### GrGMToGrSales

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrGMToGrSales']

**Observations**:
- Stata:  3,229,675
- Python: 3,231,484
- Common: 3,229,675

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.25e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |        -1.0320 |        -1.0308 |         0.0012 |       5.77e-06 |
| std        |       213.3399 |       212.9016 |         0.5417 |         0.0025 |
| min        |    -90231.3050 |    -89952.2742 |        -4.6620 |        -0.0219 |
| 25%        |        -0.0941 |        -0.0941 |      -2.50e-08 |      -1.17e-10 |
| 50%        |        -0.0024 |        -0.0024 |         0.0000 |         0.0000 |
| 75%        |         0.0784 |         0.0784 |       2.49e-08 |       1.17e-10 |
| max        |      7383.3198 |      7383.3528 |       279.0308 |         1.3079 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0009 + 0.9979 * stata
- **R-squared**: 1.0000
- **N observations**: 3,229,675

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.90e-04 |     1.77e-04 |     -5.0293 |     0.000 |
| Slope       |       0.9979 |     8.30e-07 |    1.20e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/3229675 (0.002%)
- Stata standard deviation: 2.13e+02

---

