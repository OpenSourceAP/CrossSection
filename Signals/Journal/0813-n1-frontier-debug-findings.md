# Frontier Precision Failure Root Cause Analysis

## Problem Summary

The Frontier predictor has major precision failures:
- Precision1: 84.22% failed (threshold: <10%)
- Precision2: 99th percentile diff = 5.4E-01 (threshold: <1.00e-03)

## Root Cause Investigation

### Target Observation Analysis
Focused on permno 49315, yyyymm 197306 (largest deviation: -5.954080):

**Expected Results:**
- Stata Frontier: 10.828367
- Manual Python calculation: 10.82836798023169 (matches Stata perfectly)

**Actual Python Output:**
- Python Frontier: 4.874286999798234
- Difference: -5.954080 (exactly matches the largest test deviation)

### Key Findings

1. **Regression Calculation is Correct**
   - Training data correctly identified: 24,308 observations over 60-month window
   - Target industry (FF48=35) present in training data
   - Regression prediction: 13.806826861609863
   - Manual Frontier calculation: 10.82836798023169 ✅ (matches Stata)

2. **The Issue: Wrong logmefit_NS Value**
   - Working backwards from actual Python output (4.874287):
   - Actual logmefit_NS being used: 7.852746
   - Expected logmefit_NS: 13.806827
   - Difference: -5.954081 (exact match to test failure)

3. **Indexing Logic is Correct**
   - Mask selection works properly
   - Target observation correctly identified
   - Array positioning correct

### Hypothesis

The main script is somehow storing or using a different logmefit_NS value than what the regression produces. The step-by-step trace shows the correct value (13.806827) being calculated and assigned, but the final output uses 7.852746.

### Possible Causes

1. **Later Overwrite**: Another time period might be overwriting the correct value
2. **Array Misalignment**: The predictions array might be misaligned with the current_data indices
3. **Copy/Reference Issue**: The logmefit_NS assignment might have a DataFrame copy issue
4. **Concurrent Processing**: Some other part of the script might be interfering

### Next Steps

Need to:
1. Add debug prints to the actual main script to trace the target observation
2. Check if logmefit_NS gets overwritten in subsequent time periods
3. Verify that the predictions array alignment is correct throughout execution
4. Identify the exact step where the wrong value gets stored

### Impact

This appears to be a systematic issue affecting 84% of observations, suggesting a fundamental problem in the value assignment logic rather than an edge case.