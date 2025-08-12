# Plan: fastxtile standardization

## Context
**Important: Before you start, read these docs**: 
- DocsForClaude/leg3-Predictors.md for the big picture
- DocsForClaude/accrualsbm-stata-fastxtile-migration.md to understand the current mission

## Mission
Standardize all fastxtile-based py scripts so that they use the `utils/stata_fastxtile.py` helper. Target: >99% Precision1 match for all predictors.

## Strategy: follow AccrualsBM.py migration
The migration was relatively easy. Changes are:
1. **Replaced local fastxtile** (lines 32-47) with `from utils.stata_fastxtile import fastxtile`
2. **Updated fastxtile calls:**
   - `df.groupby('time_avail_m')['BM'].transform(lambda x: fastxtile(x, 5))`  
   - → `fastxtile(df, 'BM', by='time_avail_m', n=5)`

### Debugging Methodology
- Focus on specific permno-yyyymm observations that fail
- Use bisection strategy before assuming "data differences"
- Write Debug/*.py scripts instead of long bash commands
- Never speculate about real data differences - keep investigating logic

## List of Predictors to Standardize

# py Scripts that are based on fastxtile

- **AccrualsBM**  
  - Standardized: YES
  - Python CSV: yes  
  - Superset: yes (0.00%)  
  - Precision1: yes (0.00%)  
  - Precision2: yes (0.0E+00)  

- **ChForecastAccrual**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: NO (0.12%)  
  - Precision2: NO (1.0E+00)  

- **ChNAnalyst**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (0.11%)  
  - Precision1: yes (0.01%)  
  - Precision2: NO (1.0E+00)  

- **CitationsRD**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.00%)  
  - Precision2: NO (1.0E+00)  

- **ConsRecomm**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (0.23%)  
  - Precision1: yes (0.01%)  
  - Precision2: NO (1.0E+00)  

- **DivYieldST**  
  - Standardized: yes  
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: NO (0.13%)  
  - Precision2: NO (3.0E+00)  

- **EquityDuration**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.00%)  
  - Precision2: NO (3.3E+05)  

- **FirmAgeMom**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (1.85%)  
  - Precision1: NO (0.39%)  
  - Precision2: NO (2.0E+00)  

- **GrAdExp**  
  - Standardized: NO  
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **MS**  
  - Standardized: yes  
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: NO (63.45%)  
  - Precision2: NO (5.0E+00)  

- **MomRev**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (1.26%)  
  - Precision1: yes (0.00%)  
  - Precision2: yes (0.0E+00)  

- **MomVol**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: NO (0.42%)  
  - Precision2: NO (1.0E+00)  

- **NetDebtPrice**  
  - Standardized: yes  
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: yes (0.00%)  
  - Precision2: NO (4.2E-02)  

- **OScore**  
  - Standardized: NO  
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **OperProf**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.00%)  
  - Precision2: NO (2.5E-01)  

- **PS**  
  - Standardized: yes  
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: NO (17.90%)  
  - Precision2: NO (5.0E+00)  

- **PatentsRD**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (58.66%)  
  - Precision1: NO (15.70%)  
  - Precision2: NO (1.0E+00)  

- **ProbInformedTrading**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.00%)  
  - Precision2: yes (5.0E-08)  

- **RDAbility**  
  - Standardized: yes  
  - Python CSV: yes  
  - Superset: NO (4.95%)  
  - Precision1: NO (9.52%)  
  - Precision2: NO (1.9E+02)  

- **RDcap**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.00%)  
  - Precision2: NO (1.3E-06)  

- **ZZ1_Activism1_Activism2**  
  - Standardized: NO  
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue**  
  - Standardized: NO  
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility**  
  - Standardized: NO  
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **sfe**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (0.20%)  
  - Precision1: yes (0.02%)  
  - Precision2: NO (1.0E+01)  

- **std_turn**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (0.04%)  
  - Precision1: yes (0.00%)  
  - Precision2: NO (1.9E-05)  

- **tang**  
  - Standardized: NO  
  - Python CSV: yes  
  - Superset: NO (0.02%)  
  - Precision1: yes (0.00%)  
  - Precision2: NO (2.4E-03)  
