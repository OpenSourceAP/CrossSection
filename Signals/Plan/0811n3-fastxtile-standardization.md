# Plan: fastxtile standardization

## Context
**Important: Before you start, read these docs**: 
- DocsForClaude/leg3-Predictors.md for the big picture
- DocsForClaude/accrualsbm-stata-fastxtile-migration.md to understand the current mission

## Mission
Standardize all fastxtile-based py scripts so that they use the `utils/stata_fastxtile.py` helper. Target: >99% Precision1 match for all predictors.

## Strategy: follow AccrualsBM.py migration
The migration was relatively easy. Steps are:
1. **Check the Do file version** for the targeted algorithm
  - In this case it's `Predictors/Code/AccrualsBM.do`
2. **Replaced local fastxtile** (lines 32-47) with `from utils.stata_fastxtile import fastxtile`
3. **Updated fastxtile calls**
   - `df.groupby('time_avail_m')['BM'].transform(lambda x: fastxtile(x, 5))`  
   - → `fastxtile(df, 'BM', by='time_avail_m', n=5)`

Run `python3 utils/test_predictors.py --predictors [predictor_name]` to check the quality of the migration.

### Debugging Methodology
- Focus on specific permno-yyyymm observations that fail
- Use bisection strategy before assuming "data differences"
- Write Debug/*.py scripts instead of long bash commands
- Never speculate about real data differences - keep investigating logic

## List of Predictors to Standardize

# py Scripts that are based on fastxtile

## Group 1
- **AccrualsBM**  
  - Standardized: YES
  - Output: AccrualsBM.csv (predictor)
  - Python CSV: yes  
  - Superset: yes (0.00%)  
  - Precision1: yes (0.00%)  
  - Precision2: yes (0.0E+00)  

- **ChForecastAccrual**  
  - Standardized: YES  
  - Output: ChForecastAccrual.csv (predictor)
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: NO (0.118%)  
  - Precision2: NO (1.0E+00)  

- **ChNAnalyst**  
  - Standardized: YES  
  - Output: ChNAnalyst.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.11%)  
  - Precision1: yes (0.007%)  
  - Precision2: NO (1.0E+00)  

- **CitationsRD**  
  - Standardized: YES  
  - Output: CitationsRD.csv (predictor)
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.002%)  
  - Precision2: NO (1.0E+00)  

## Group 2
- **DivYieldST**  
  - Standardized: yes  
  - Output: DivYieldST.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: NO (0.13%)  
  - Precision2: NO (3.0E+00)  

- **EquityDuration**  
  - Standardized: NO  
  - Output: EquityDuration.csv (predictor)
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.00%)  
  - Precision2: NO (3.3E+05)  

- **FirmAgeMom**  
  - Standardized: NO  
  - Output: FirmAgeMom.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (1.85%)  
  - Precision1: NO (0.39%)  
  - Precision2: NO (2.0E+00)  

- **GrAdExp**  
  - Standardized: NO  
  - Output: GrAdExp.csv (predictor) [Script not created]
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **MS**  
  - Standardized: yes  
  - Output: MS.csv (predictor)
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: NO (63.45%)  
  - Precision2: NO (5.0E+00)  

## Group 3  

- **MomRev**  
  - Standardized: YES  
  - Output: MomRev.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (1.26%)  
  - Precision1: yes (0.000%)  
  - Precision2: yes (0.0E+00)  

- **MomVol**  
  - Standardized: YES  
  - Output: MomVol.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: NO (0.417%)  
  - Precision2: NO (1.0E+00)  

- **NetDebtPrice**  
  - Standardized: yes  
  - Output: NetDebtPrice.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: yes (0.00%)  
  - Precision2: NO (4.2E-02)  

- **OScore**  
  - Standardized: YES  
  - Output: OScore.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.40%)  
  - Precision1: yes (0.000%)  
  - Precision2: yes (0.0E+00)  

- **OperProf**  
  - Standardized: YES  
  - Output: OperProf.csv (predictor)
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.000%)  
  - Precision2: NO (2.5E-01)  

## Group 4

- **PS**  
  - Standardized: yes  
  - Output: PS.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.00%)  
  - Precision1: NO (17.90%)  
  - Precision2: NO (5.0E+00)  

- **PatentsRD**  
  - Standardized: YES  
  - Output: PatentsRD.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (58.66%)  
  - Precision1: NO (15.700%)  
  - Precision2: NO (1.0E+00)  

- **ProbInformedTrading**  
  - Standardized: YES  
  - Output: ProbInformedTrading.csv (predictor)
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.000%)  
  - Precision2: yes (5.0E-08)  

- **RDAbility**  
  - Standardized: yes  
  - Output: RDAbility.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (4.95%)  
  - Precision1: NO (9.52%)  
  - Precision2: NO (1.9E+02)  

- **RDcap**  
  - Standardized: NO  
  - Output: RDcap.csv (predictor)
  - Python CSV: yes  
  - Superset: yes  
  - Precision1: yes (0.00%)  
  - Precision2: NO (1.3E-06)  

## Group 5  

- **ZZ1_Activism1_Activism2**  
  - Standardized: NO  
  - Output: Activism1.csv, Activism2.csv (predictors) [Script not created]
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue**  
  - Standardized: NO  
  - Output: AnalystValue.csv, AOP.csv, PredictedFE.csv (predictors), IntrinsicValue.csv (placebo)
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

- **ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility**  
  - Standardized: NO  
  - Output: RIO_MB.csv, RIO_Disp.csv, RIO_Turnover.csv, RIO_Volatility.csv (predictors)
  - Python CSV: —  
  - Superset: —  
  - Precision1: —  
  - Precision2: —  

## Group 6

- **sfe**  
  - Standardized: YES  
  - Output: sfe.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.20%)  
  - Precision1: yes (0.022%)  
  - Precision2: NO (1.0E+01)  

- **std_turn**  
  - Standardized: NO  
  - Output: std_turn.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.04%)  
  - Precision1: yes (0.00%)  
  - Precision2: NO (1.9E-05)  

- **tang**  
  - Standardized: YES  
  - Output: tang.csv (predictor)
  - Python CSV: yes  
  - Superset: NO (0.02%)  
  - Precision1: yes (0.002%)  
  - Precision2: NO (2.4E-03)  
