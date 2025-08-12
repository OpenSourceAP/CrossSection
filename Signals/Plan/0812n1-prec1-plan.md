# Plan: Fixing Major Precision1 Failures

## Context
**Important: Before you start, read these doc(s)**: 
- DocsForClaude/leg3-Predictors.md for the big picture

## Mission
Fix the Precision1 failures for the predictors described below.
- Identify the root causes of the failures. 
  - Use `cd pyCode && python3 utils/test_predictor.py --predictors [predictor_name]` to find observations with large deviations.
  - Focus on *one* observation, find the exact line of code where the deviation first shows up.
  - Think about the underlying cause
    - Start with the line where the deviation first shows up. But also think about the previous lines too.
    - Examine the Stata counterpart (in `Code/Predictors/*.do`)
    - Check Stata command documentation in `DocsForClaude/stata_*.md` 
    - Think about what is causing the problem.
  - This is extremely important. Do not guess. Track down the problem.
- Write down a plan to fix the problem in Journal/
- Get the OK from the user to fix.

## List of Predictors with Major Precision1 Failures

Proceed in order from top to bottom.

### Group 1
These should be easier (might not be).

* **Mom12mOffSeason**

  * Precision1: 91.88%
  * Superset: ✅
  * Recent Fixes: None
  * Root Cause: Seasonal momentum calculation

* **OrgCap**

  * Precision1: 91.02%
  * Superset: ❌ (0.02%)
  * Recent Fixes: None
  * Root Cause: Organizational capital measures  

* **MS**

  * Precision1: 63.45%
  * Superset: ✅
  * Recent Fixes: **Major null handling fix**
  * Root Cause: Precision differences remain

* **PatentsRD**

  * Precision1: 15.70%
  * Superset: ❌ (29.14%)
  * Recent Fixes: **Month arithmetic fix**
  * Root Cause: Expansion logic partially fixed

* **IndRetBig**

  * Precision1: 87.02%
  * Superset: ❌ (3.47%)
  * Recent Fixes: None
  * Root Cause: Industry momentum calculation  

### Group 2
Hard past return predictors

* **Coskewness**

  * Precision1: 99.36%
  * Superset: ❌ (8.84%)
  * Recent Fixes: None
  * Root Cause: Mathematical formula errors

* **TrendFactor**

  * Precision1: 97.15%
  * Superset: ❌ (0.07%)
  * Recent Fixes: asreg standardization
  * Root Cause: Sign reversal in coefficients

* **retConglomerate**

  * Precision1: 94.06%
  * Superset: ❌ (22.32%)
  * Recent Fixes: Updates applied
  * Root Cause: Industry classification logic

### Group 3
Hard predictors doing random stuff  

* **PredictedFE**

  * Precision1: 95.81%
  * Superset: ❌ (0.27%)
  * Recent Fixes: None
  * Root Cause: Complex statistical calculation

* **Frontier**

  * Precision1: 84.22%
  * Superset: ✅
  * Recent Fixes: Fixes applied
  * Root Cause: Complex calculation logic

