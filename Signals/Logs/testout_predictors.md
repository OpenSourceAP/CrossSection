# Predictor Validation Results

**Generated**: 2025-08-30 09:49:58

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

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2              | T-stat     |
|---------------------------|------------|------------|---------------|--------------|-------------------------|------------|
| Recomm_ShortInterest*     | ✅         | ❌ (58.64%) | ❌ (+95.6%)  | ✅ (0.0%)     | ✅ (0.0E+00)             | SKIP       |

**Overall**: 1/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 1
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### Recomm_ShortInterest

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-20
- Reviewed by: ac
- Details: The do file was using asrol with stat(first) to fill in missing values. This method is not used anywhere else. Also, this method does not work properly. I really don't understand what it's doing See https://github.com/OpenSourceAP/CrossSection/issues/178. 

I wrote Recomm_ShortInterest.py from scratch to fill in the missing values properly. It results in far more observations than the do file. I checked a few of the Stata observations that are missing in Python and they all should be missing. They had ConsRecomm scores of around 3.0, which should not be an extreme quintile and therefore should be dropped.

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 20300 Stata observations)
- Test 2 - NumRows check: ❌ FAILED (Python has +95.58% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  34,619
- Python: 67,708
- Common: 14,319

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     14319.0000 |     14319.0000 |     14319.0000 |     14319.0000 |
| mean       |         0.5298 |         0.5299 |       6.98e-05 |       1.40e-04 |
| std        |         0.4991 |         0.4991 |         0.0084 |         0.0167 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0035 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9997
- **N observations**: 14,319

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.49e-04 |     1.02e-04 |      1.4583 |     0.145 |
| Slope       |       0.9999 |     1.40e-04 |   7145.7553 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Recomm_ShortInterest
     0   10044  201106                   1.0
     1   10044  201107                   1.0
     2   10044  201108                   1.0
     3   10044  201109                   1.0
     4   10044  201110                   1.0
     5   10044  201111                   1.0
     6   10044  201112                   1.0
     7   10044  201201                   1.0
     8   10044  201202                   1.0
     9   10044  201203                   1.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1/14319 (0.007%)
- Stata standard deviation: 4.99e-01

---

