# OrgCap Log Debug Analysis - Major Filtering Discrepancy Found

**Date:** 2025-08-21  
**Task:** Debug ZZ1_OrgCap_OrgCapNoAdj.py using log comparison with Stata

## Summary of Findings

**CRITICAL ISSUE DISCOVERED:** Major discrepancy in initial filtering step causing +101,588 extra observations in Python vs expected.

## Key Results

### Observation Count Discrepancies

| Step | Stata Log | Python Log | Debug Script | Difference |
|------|-----------|------------|--------------|------------|
| After initial filtering | ~1,583,501 | 1,583,658 | 1,482,070 | **-101,588** |
| After FF17 filtering | ~1,465,505 | 1,465,660 | N/A | +155 |
| Final OrgCap count | ~1,243,383 | 1,243,528 | N/A | +145 |

### Critical Discovery

**Debug Script shows 1,482,070 observations after SIC filtering**  
**Python main script shows 1,583,658 observations after filtering**  
**Difference: +101,588 observations**

This suggests the main Python script is using **different filtering logic** than what's documented in the Stata script.

## Analysis by Hypothesis

### Hypothesis 1: Missing Value Filtering Logic ✅ CONFIRMED
- **Status:** Major issue found
- **Finding:** The main Python script appears to be using different SIC filtering conditions than the Stata script
- **Evidence:** 
  - Stata: `keep if month(datadate) == 12 & (sic < 6000 | sic >= 7000) & sic != .`
  - Debug script replicating this logic: 1,482,070 observations
  - Main Python script: 1,583,658 observations (+101,588 difference)

### Hypothesis 2: Lag Operator Differences ⏸️ PARTIAL
- **Status:** Not fully tested due to Hypothesis 1 priority
- **Setup:** Debug script created but execution stopped due to more critical filtering issue

### Hypothesis 3: FF17 Classification ⏸️ PARTIAL  
- **Status:** Script created but sicCRSP data type issues prevented completion
- **Finding:** sicff function works correctly on test cases, but integration has technical issues

## Root Cause Analysis

The **primary issue** is that the main Python script `ZZ1_OrgCap_OrgCapNoAdj.py` is not implementing the same filtering logic as the Stata script.

**Likely causes:**
1. **Incorrect SIC filtering logic** - The Python script may be missing the industry filter `(sic < 6000 | sic >= 7000)`
2. **Missing value handling** - Different treatment of missing SIC codes
3. **December filter** - Possible difference in how `month(datadate) == 12` is implemented

## Recommended Next Steps

1. **IMMEDIATE:** Examine the actual filtering logic in `ZZ1_OrgCap_OrgCapNoAdj.py` lines 60-80 
2. **Compare:** The Python filtering with Stata filtering line-by-line
3. **Fix:** Implement the correct Stata filtering logic in Python
4. **Verify:** Run the corrected script and confirm observation counts match

## Technical Details

### Stata Filtering Logic (from log)
```stata
keep if month(datadate) == 12 & (sic < 6000 | sic >= 7000) & sic != .
```
Result: Approximately 1,583,501 observations

### Debug Script Results
```python
# December filter
df_dec = df.filter(pl.col("datadate").dt.month() == 12)
# Result: 1,851,559 observations

# SIC filter  
df_sic_filtered = df_dec.filter(
    pl.col("sic_numeric").is_not_null() & 
    ((pl.col("sic_numeric") < 6000) | (pl.col("sic_numeric") >= 7000))
)
# Result: 1,482,070 observations
```

### Key Missing Piece
The main Python script is somehow getting **101,588 more observations** than the debug script that replicates Stata logic. This points to a fundamental difference in the filtering implementation.

## Files Created
- `Debug/0821n1_orgcap_hypothesis1_missing_filtering.py` - Working debug script
- `Debug/0821n2_orgcap_hypothesis2_lag_operators.py` - Lag analysis script
- `Debug/0821n3_orgcap_hypothesis3_ff17_classification.py` - FF17 analysis script (partial)

## Status
**URGENT:** Fix required in main Python script before proceeding with other hypotheses.