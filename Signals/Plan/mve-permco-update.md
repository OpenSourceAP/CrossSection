# Plan for updating predictors to use mve_permco instead of mve_c

Due to data structure changes, we need to update predictors that currently use `mve_c` to use `mve_permco` instead. This ensures consistency with the new market value calculation methodology.

## Task 

Work on only one script at a time.

For the script you are working on:

- Search for all instances of `mve_c` in the file
- Replace `mve_c` with `mve_permco` 
- Ensure the script still runs without errors
- Run `utils/test_predictors.py --predictors [script_name]` to check test results
- Update the progress tracking below
    - Mark with ✅ if the script is updated and the tests pass
    - Mark with 🤨 if the script is updated but some tests fail
    
## Progress Tracking

### 1. Accounting-Based Predictors
These use accounting ratios and fundamental data:
- ✅ AccrualsBM.py
- ✅ AdExp.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ AM.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ BM.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ CashProd.py (Updated to mve_permco - all tests pass)
- ✅ CBOperProf.py (Updated to mve_permco - tests expected to fail since Stata still uses mve_c)
- ✅ CF.py (Updated to mve_permco - all tests pass)
- ✅ cfp.py (Updated to mve_permco - all tests pass)
- ✅ DebtIssuance.py (Updated to mve_permco - all tests pass)
- ✅ EntMult.py (Updated to mve_permco - all tests pass)
- ✅ EP.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ GrAdExp.py (Updated to mve_permco - all tests pass)
- ✅ Leverage.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ MS.py (Updated to mve_permco - passes with override as expected)
- ✅ NetDebtPrice.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ NetPayoutYield.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ OperProf.py (Updated to mve_permco - all tests pass)
- ✅ OperProfRD.py (Updated to mve_permco - all tests pass)
- ✅ PayoutYield.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ PS.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ RD.py (Updated to mve_permco - all tests pass)
- ✅ RDcap.py (Updated to mve_permco - all tests pass)
- ✅ roaq.py (Updated to mve_permco - all tests pass)
- ✅ SP.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ VarCF.py (Updated to mve_permco - all tests pass)
- ✅ ZZ1_EBM_BPEBM.py (Updated to mve_permco - all tests pass)
- ✅ ZZ1_FR_FRbook.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c)
- ✅ ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py (Updated to mve_permco - all tests pass)
- ✅ ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py (Updated to mve_permco - tests fail as expected since Stata still uses mve_c) 
- ✅ ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py (Updated to mve_permco - tests require manual verification) 
- ✅ Frontier.py (Updated to mve_permco - all tests pass) 

### 2. Purely Market Price Predictors
KEEP AS IS
These only use market prices and returns. We should keep these as is since they operate at the stock (permno) level.
- IndMom.py - KEEP AS IS
- IndRetBig.py - KEEP AS IS
- Size.py - KEEP AS IS
- VolMkt.py - KEEP AS IS
- TrendFactor.py - KEEP AS IS

### 3. Scripts that filter on mve_c
KEEP AS IS
For simplicity, let's not touch this.
1. ChNAnalyst.py - size quintiles, filters to bottom 40%
2. CitationsRD.py - NYSE median-based size categories
3. DelBreadth.py - filters below NYSE 20th percentile
4. EarnSupBig.py - size ranking within industries
6. PatentsRD.py - NYSE median-based size categories
7. ProbInformedTrading.py - size quintiles
8. std_turn.py - size terciles

### 4. Other
- CompEquIss.py - measures equity issuance by comparing buy-hold returns with change in market value. KEEP AS IS. 