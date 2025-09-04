# Placebo Validation Results

**Generated**: 2025-09-04 15:23:00

**Configuration**:
- TOL_SUPERSET: 0.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Placebo                   | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| sgr_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.0E-10)   |

**Overall**: 0/1 available placebos passed validation
**Python CSVs**: 1/1 placebos have Python implementation

## Detailed Results

### sgr_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 45 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr_q']

**Observations**:
- Stata:  2,457,701
- Python: 2,457,695
- Common: 2,457,656

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.03e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |         1.0672 |         1.0670 |      -1.23e-04 |      -4.30e-07 |
| std        |       286.5304 |       286.5304 |         0.1413 |       4.93e-04 |
| min        |     -3092.0000 |     -3092.0000 |      -146.0200 |        -0.5096 |
| 25%        |        -0.0374 |        -0.0374 |      -2.58e-09 |      -8.99e-12 |
| 50%        |         0.0794 |         0.0794 |         0.0000 |         0.0000 |
| 75%        |         0.2229 |         0.2229 |       2.55e-09 |       8.91e-12 |
| max        |    251440.0000 |    251440.0000 |        15.0962 |         0.0527 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,457,656

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.23e-04 |     9.02e-05 |     -1.3635 |     0.173 |
| Slope       |       1.0000 |     3.15e-07 |    3.18e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    sgr_q
     0   11545  199706 0.241882
     1   11545  199707 0.241882
     2   11545  199708 0.241882
     3   11545  199806 1.767560
     4   11545  199807 1.767560
     5   11545  199808 1.767560
     6   12837  198004 0.209407
     7   12837  198005 0.209407
     8   21346  197001 0.152858
     9   21346  197002 0.152858
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/2457656 (0.001%)
- Stata standard deviation: 2.87e+02

---

