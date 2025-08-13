# Plan: Fixing Major Precision1 Failures

## Context
**Important: Before you start, read these doc(s)**: 
- DocsForClaude/leg3-Predictors.md for the big picture

## Mission
Fix the Precision1 failures for the predictors described below.
- Identify the root causes of the failures. 
  - Use `cd pyCode && python3 utils/test_predictors.py --predictors [predictor_name]` to find observations with large deviations.
    - The large deviations are found in `Logs/testout_predictors.md`
  - Focus on *one* observation, find the exact line of code where the deviation first shows up.
  - Think about the underlying cause
    - Start with the line where the deviation first shows up. But also think about the previous lines too.
    - Examine the Stata counterpart (in `Code/Predictors/*.do`)
    - **IMPORTANT**: Check `DocsForClaude/traps.md` for common pitfalls when translating Stata code
    - grep for related notes in `Journal/*.md` and `DocsForClaude/stata_*.md`
    - Think about what is causing the problem.
  - This is extremely important. Do not guess. Track down the problem.
- Write down a plan to fix the problem in Journal/
- Get the OK from the user to fix.


## List of Predictors with Major Precision1 Failures

Unless directed otherwise, proceed in order from top to bottom.

### Groups 1-2
Completed.

### Group 3
These scripts are relatively simple. Hopefully the fix will be straightforward.

- **OrgCap**
  - Script: ZZ1_OrgCap_OrgCapNoAdj
  - Python CSV: yes
  - Superset: yes (100%) ✅ **FIXED**
  - Precision1: yes (14.23%) ✅ **MAJOR IMPROVEMENT** (was 91.02%, 77pt improvement)
  - Precision2: yes (99th diff 1.3E-01) ✅ **MAJOR FIX** (was 1.6E+00, 92% improvement)
  - Status: Skip for now 

- **PS**
  - Script: PS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (17.93%) ❌ **ATTEMPTED FIX** (minimal change from 17.90%)
  - Precision2: no (99th diff 1.0E+00) ❌ **IMPROVED** (was 5.0E+00, 80% improvement)
  - Status: **ATTEMPTED** ⚠️ (missing value logic fix applied, minor improvement)

### Group 4
Relatively complicated do files. Need to be more careful.

- **MS**
  - Script: MS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (32.97%) ❌ **MAJOR IMPROVEMENT** (was 63.45%, 48% improvement)
  - Precision2: no (99th diff 4.0E+00) ❌ **PARTIAL FIX** (logical bug fixed)
  - Status: **MAJOR PROGRESS** ⚠️ (significant precision improvement, deeper issues remain)


- **retConglomerate**
  - Script: retConglomerate
  - Python CSV: yes
  - Superset: no (23.24%) ❌ **WORSENED** (was 22.32%)
  - Precision1: no (91.16%) ❌ **SLIGHT IMPROVEMENT** (was 94.06%)
  - Precision2: no (99th diff 1.6E-01) ❌
  - Status: TBC

  
### Group 5
Complex and computationally intensive. Be very careful.

- **TrendFactor**
  - Script: TrendFactor
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (98.31%) ❌ **SLIGHT WORSENING** (was 97.15%)
  - Precision2: no (99th diff 5.0E-01) ❌ **WORSENED** (was 2.6E-01)
  - Status: TBC

- **Frontier**
  - Script: Frontier
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%) ✅ **COMPLETELY FIXED** (was 84.22%)
  - Precision2: yes (99th diff 5.4E-06) ✅ **COMPLETELY FIXED** (was 5.4E-01)
  - Status: ✅ **COMPLETE FIX**

- **IdioVolAHT**
  - Script: ZZ2_IdioVolAHT
  - Python CSV: yes
  - Superset: no (3.82%) ❌
  - Precision1: no (99.47%) ❌ **MAJOR REGRESSION** (was 17.59%)
  - Precision2: no (99th diff 2.2E-02) ❌ **WORSENED** (was 5.3E-03)
  - Status: TBC  

- **PatentsRD**
  - Script: PatentsRD
  - Python CSV: yes
  - Superset: no (21.05%) ❌ **IMPROVED** (was 29.14%)
  - Precision1: yes (0.02%) ✅ **COMPLETELY FIXED** (was 15.70%)
  - Precision2: yes (99th diff 0.0E+00) ✅ **COMPLETELY FIXED** (was 1.0E+00)
  - Status: ⚠️ **MAJOR FIX** (precision fixed, superset still needs work)  


# Group 6
Ignore these for now.

- **PriceDelayTstat**
  - Script: ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (19.38%) ❌
  - Precision2: no (99th diff 6.1E+00) ❌
  - Status: Needs human intervention

- **PredictedFE**
  - Script: ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (93.91%) ❌ **SLIGHT IMPROVEMENT** (was 95.81%)
  - Precision2: no (99th diff 1.4E-02) ❌ **IMPROVED** (was 2.3E-02)
  - Status: Needs human intervention