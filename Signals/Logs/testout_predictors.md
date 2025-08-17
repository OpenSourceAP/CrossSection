# Predictor Validation Results

**Generated**: 2025-08-16 20:55:33

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
| MS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (40.96%)   | ❌ (99.900th diff 3.2E+00) |

**Overall**: 0/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

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

**Precision1**: 40.957% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.24e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    473079.0000 |    473079.0000 |    473079.0000 |    473079.0000 |
| mean       |         3.8814 |         3.7162 |        -0.1652 |        -0.1071 |
| std        |         1.5421 |         1.5729 |         1.2195 |         0.7908 |
| min        |         1.0000 |         1.0000 |        -5.0000 |        -3.2424 |
| 25%        |         3.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         6.0000 |         6.0000 |         5.0000 |         3.2424 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.9702 + 0.7075 * stata
- **R-squared**: 0.4811
- **N observations**: 473,079

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.9702 |       0.0045 |    217.4696 |     0.000 |
| Slope       |       0.7075 |       0.0011 |    662.2915 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 193757/473079 (40.957%)
- Stata standard deviation: 1.54e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10104  202412       5      3     2
1   10693  202412       6      5     1
2   10966  202412       3      5    -2
3   11275  202412       3      5    -2
4   11308  202412       4      3     1
5   11581  202412       2      1     1
6   11884  202412       2      3    -1
7   11995  202412       4      5    -1
8   12060  202412       1      4    -3
9   12266  202412       3      5    -2
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10812  199006       6      1     5
1   10812  199007       6      1     5
2   10812  199008       6      1     5
3   10812  199009       6      1     5
4   10812  199010       6      1     5
5   10812  199011       6      1     5
6   10812  199012       6      1     5
7   10812  199101       6      1     5
8   10812  199102       6      1     5
9   10812  199103       6      1     5
```

---

