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

- **TrendFactor**
  - Script: TrendFactor.py
  - Precision1: no (97.14%) ❌ 
  - Status: TBC

- **PredictedFE**
  - Script: ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
  - Precision1: no (93.91%) ❌ 
  - Status: TBC

- **MS**
  - Script: MS.py
  - Precision1: no (32.97%) ❌ 
  - Status: TBC

- **AbnormalAccruals**
  - Script: ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py
  - Precision1: no (27.95%) ❌ 
  - Status: TBC

- **CitationsRD**
  - Script: CitationsRD.py
  - Precision1: no (21.54%) ❌ 
  - Status: TBC

- **PS**
  - Script: PS.py
  - Precision1: no (17.93%) ❌ 
  - Status: TBC

- **IdioVolAHT**
  - Script: ZZ2_IdioVolAHT.py
  - Precision1: no (17.59%) ❌ 
  - Status: TBC

- **OrgCap**
  - Script: ZZ1_OrgCap_OrgCapNoAdj.py
  - Precision1: no (14.23%) ❌ 
  - Status: TBC

