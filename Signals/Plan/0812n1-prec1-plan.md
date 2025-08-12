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
These failures are linked to the stata 'relrank.ado' function. Using utils/relrank.py should take care of them (hopefully).

- **IndRetBig**
  - Script: IndRetBig
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (25.49%) ❌
  - Precision2: no (99th diff 1.8E-02) ❌
  - Status: TBC

- **PredictedFE**
  - Script: ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (95.81%) ❌
  - Precision2: no (99th diff 2.3E-02) ❌
  - Status: TBC

## Group 2
These scripts are relatively simple. Hopefully the fix will be straightforward.

- **ShareVol**
  - Script: ShareVol
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (14.38%) ❌
  - Precision2: no (99th diff 1.0E+00) ❌
  - Status: TBC

- **OrgCap**
  - Script: ZZ1_OrgCap_OrgCapNoAdj
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (91.02%) ❌
  - Precision2: no (99th diff 1.6E+00) ❌
  - Status: TBC

- **MS**
  - Script: MS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (63.45%) ❌
  - Precision2: no (99th diff 4.0E+00) ❌
  - Status: TBC

- **retConglomerate**
  - Script: retConglomerate
  - Python CSV: yes
  - Superset: no (22.32%) ❌
  - Precision1: no (94.06%) ❌
  - Precision2: no (99th diff 1.7E-01) ❌
  - Status: TBC

- **PS**
  - Script: PS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (17.90%) ❌
  - Precision2: no (99th diff 5.0E+00) ❌  
  - Status: TBC

## Group 3
Relatively complicated do files. Need to be more careful.

- **AbnormalAccruals**
  - Script: ZZ2_AbnormalAccruals_AbnormalAccrualsPercent
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (49.01%) ❌
  - Precision2: no (99th diff 1.5E-01) ❌
  - Status: TBC

- **RIO_Volatility**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: no (4.40%) ❌
  - Precision1: no (26.58%) ❌
  - Precision2: no (99th diff 4.0E+00) ❌
  - Status: TBC

- **RIO_Turnover**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (23.71%) ❌
  - Precision2: no (99th diff 3.0E+00) ❌
  
- **RIO_MB**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (17.07%) ❌
  - Precision2: no (99th diff 3.0E+00) ❌

- **IntanCFP**
  - Script: ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (15.60%) ❌
  - Precision2: no (99th diff 4.4E-02) ❌

- **IntanBM**
  - Script: ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (15.49%) ❌
  - Precision2: no (99th diff 3.0E-02) ❌

- **IntanEP**
  - Script: ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (13.83%) ❌
  - Precision2: no (99th diff 3.1E-02) ❌

# Group 4
Complex and computationally intensive. Be very careful.

- **TrendFactor**
  - Script: TrendFactor
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (97.15%) ❌
  - Precision2: no (99th diff 2.6E-01) ❌

- **Frontier**
  - Script: Frontier
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (84.22%) ❌
  - Precision2: no (99th diff 5.4E-01) ❌

- **IdioVolAHT**
  - Script: ZZ2_IdioVolAHT
  - Python CSV: yes
  - Superset: no (3.82%) ❌
  - Precision1: no (17.59%) ❌
  - Precision2: no (99th diff 5.3E-03) ❌

- **PatentsRD**
  - Script: PatentsRD
  - Python CSV: yes
  - Superset: no (29.14%) ❌
  - Precision1: no (15.70%) ❌
  - Precision2: no (99th diff 1.0E+00) ❌


# Group 5
Ignore these for now.

- **PriceDelayTstat**
  - Script: ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (19.38%) ❌
  - Precision2: no (99th diff 6.1E+00) ❌
