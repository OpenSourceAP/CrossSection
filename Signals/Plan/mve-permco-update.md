# Plan for updating predictors to use mve_permco instead of mve_c

Due to data structure changes, we need to update predictors that currently use `mve_c` to use `mve_permco` instead. This ensures consistency with the new market value calculation methodology.

## Task 

Work on only one script at a time.

For the script you are working on:

- Search for all instances of `mve_c` in the file
- Replace `mve_c` with `mve_permco` 
- Ensure the script still runs without errors
- Run `python utils/test_predictor.py <predictor_name>` to verify the changes
- Update the progress tracking below
    - Mark with ✅ if the script is updated and tests pass

## Progress Tracking

### 1. Accounting-Based Predictors
These use accounting ratios and fundamental data:
- AccrualsBM.py
- AdExp.py
- AM.py
- BM.py
- CashProd.py
- CBOperProf.py
- CF.py
- cfp.py
- CompEquIss.py
- DebtIssuance.py
- EntMult.py
- EP.py
- GrAdExp.py
- Leverage.py
- MS.py
- NetDebtPrice.py
- NetPayoutYield.py
- OperProf.py
- OperProfRD.py
- PayoutYield.py
- PS.py
- RD.py
- RDcap.py
- roaq.py
- SP.py
- VarCF.py
- ZZ1_EBM_BPEBM.py
- ZZ1_FR_FRbook.py
- ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py 
- ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py 
- Frontier.py 

### 2. Purely Market Price Predictors
These only use market prices and returns:
- IndMom.py
- IndRetBig.py
- Size.py
- VolMkt.py
- TrendFactor.py

### 3. Scripts that filter on mve_c
1. ChNAnalyst.py - size quintiles, filters to bottom 40%
2. CitationsRD.py - NYSE median-based size categories
3. DelBreadth.py - filters below NYSE 20th percentile
4. EarnSupBig.py - size ranking within industries
6. PatentsRD.py - NYSE median-based size categories
7. ProbInformedTrading.py - size quintiles
8. std_turn.py - size terciles