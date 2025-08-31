# Cleanup and standardization of utility functions and calls

## Utilities that should be used instead of in-line implementations

## Core Utility Modules

- **save_standardized.py**
  - `save_predictor`: Standardized predictor output formatting and saving
  - `save_placebo`: Placebo test result saving  

- **column_standardizer_yaml.py**
  - `standardize_columns`: Standardize column names for downloads  

- **stata_fastxtile.py**
  - `fastxtile`: Stata-equivalent percentile ranking

- **asreg.py**
  - `asreg_polars`: Rolling-window regressions using polars
  - `asreg_collinear`: Regression with collinearity handling (no rolling windows)

- **asrol.py**
  - `asrol_fast`: Rolling window statistics and regressions (polars)
  - `asrol_calendar`: Rolling window statistics and regressions by date (polars)
    - Not sure this is any slower than asrol_fast
    - May need to add more options (e.g. stats)

- **stata_regress.py**
  - `drop_collinear`: Drop collinear variables
  - `regress`: OLS regressionhis be deployed, if anywhere? should we just delete this?)

- **stata_replication.py**
  - `stata_multi_lag`: Multi-period lagged variables
  - `stata_ineq_pd`: Stata-style inequality operators for pandas
  - `stata_ineq_pl`: Stata-style inequality operators for polars
  - `stata_quantile`: Stata-style quantiles
  - `fill_date_gaps`: Fill date gaps to create a clean panel for lag operations

- **relrank.py**
  - `relrank`: Relative ranking within groups

- **sicff.py**
  - `sicff`: SIC to Fama-French industry mapping

- **winsor2.py**
  - `winsor2`: Data winsorization

## Files that use asreg 

**Updated all 10 predictor files using `asreg_polars`:
   - ✅ Beta.py
   - ✅ BetaLiquidityPS.py  
   - ✅ BetaTailRisk.py
   - ✅ RDAbility.py
   - ✅ ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py
   - ✅ ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
   - ✅ ZZ1_ResidualMomentum6m_ResidualMomentum.py
   - ✅ ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py
   - ✅ ZZ2_betaVIX.py (also fixed sys.path import)
   - ✅ ZZ2_IdioVolAHT.py (also fixed sys.path import)

**TrendFactor.py unchanged** - already uses `asreg_collinear` 

Doesn't seem like it's worth the effort to move anything else to use `asreg_collinear`. Seems like `asreg_polars` actually helps `RDAbility.py` replicate OP. Here are the t-stat results:

```
           signalname metric   old   new  diff  tstat_op                           Test in OP
16               Beta  tstat  1.72  1.75  0.03      2.57                       univariate reg
18    BetaLiquidityPS  tstat  1.94  2.03  0.09      2.54                 port sort CAPM alpha
19       BetaTailRisk  tstat  3.29  3.30  0.01      2.48                            port sort
152         RDAbility  tstat  1.52  1.74  0.22      2.61                          double sort
162       RealizedVol  tstat  2.60  2.61  0.01      2.86                            port sort
90          IdioVol3F  tstat  3.22  3.24  0.02      3.10                  port sort FF3 alpha
166      ReturnSkew3F  tstat  4.28  4.61  0.33      4.35                            port sort
10       AnalystValue  tstat  1.76  1.67 -0.09       NaN          port sort nonstandard p-val
1                 AOP  tstat  2.09  2.02 -0.07       NaN          port sort nonstandard p-val
145       PredictedFE  tstat  1.02  1.37  0.35       NaN     univariate reg nonstandard p-val
164  ResidualMomentum  tstat  8.29  8.37  0.08      8.22                         LS FF+ alpha
2    AbnormalAccruals  tstat  5.03  4.91 -0.12      8.43  port sort size adjusted nonstandard
189           betaVIX  tstat  3.58  3.61  0.03      3.90                            port sort
91         IdioVolAHT  tstat  2.53  2.50 -0.03      2.70                                  reg
```


# Other utility modules

## utils/asrol.py (17 scripts)

Almost all of these (if not all) are using `asrol_fast`, and just hiding behind the `asrol` wrapper. Let's try to move all of them to use `asrol_calendar_pd` instead. 

**IMPORTANT**: Do not make the move if the performance deteriorates. Compare with `Logs/testout_predictors 0827n2.md` to see if the performance deteriorates.

Group 1
- DivInit.py: ✅ uses `asrol_calendar_pd`
- DivOmit.py: ✅ uses `asrol_calendar_pd`
- DivSeason.py: ✅ uses `asrol_calendar_pd`

Group 2
- Herf.py
- HerfAsset.py
- HerfBE.py

Group 3
- MomOffSeason06YrPlus.py
- MomOffSeason11YrPlus.py
- MomOffSeason16YrPlus.py
- MomVol.py

Group 4
- CitationsRD.py: ✅ uses `asrol_calendar`
- MS.py: ✅ uses `asrol_calendar`
- Investment.py
- RDAbility.py: ✅ uses `asrol_calendar`
- Recomm_ShortInterest.py
- VarCF.py

Group 5
- TrendFactor.py
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py

## utils/stata_fastxtile.py (25 scripts)

- AccrualsBM.py
- ChForecastAccrual.py
- ChNAnalyst.py
- CitationsRD.py
- DivYieldST.py
- FirmAgeMom.py
- GrAdExp.py
- MomRev.py
- MomVol.py
- MS.py
- NetDebtPrice.py
- OperProf.py
- OScore.py
- PatentsRD.py
- ProbInformedTrading.py
- PS.py
- RDAbility.py
- RDcap.py
- Recomm_ShortInterest.py
- sfe.py
- std_turn.py
- tang.py
- ZZ1_Activism1_Activism2.py
- ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py

## utils/stata_ineq.py (5 scripts)

- DivSeason.py
- MS.py
- retConglomerate.py
- ShareVol.py
- TrendFactor.py

## utils/winsor2.py (5 scripts)

- VolumeTrend.py
- ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
- ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py
- ZZ1_OrgCap_OrgCapNoAdj.py
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py

## utils/relrank.py
Move the `relrank` function to `stata_replication.py`. Delete `relrank.py`. Update the following:
- EarnSupBig.py: ✅
- IntRetBig.py: ✅
- ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py: ✅
