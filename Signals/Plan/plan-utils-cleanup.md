# Cleanup and standardization of utility functions and calls

## Utilities that should be used instead of in-line implementations

## Core Utility Modules

Basic IO (TBC: combine savepredictor and saveplacebo)
- **savepredictor.py**
  - `save_predictor`: Standardized predictor output formatting and saving

- **saveplacebo.py**
  - `save_placebo`: Placebo test result saving  

- **column_standardizer_yaml.py**
  - `standardize_columns`: Standardize column names for downloads  

- **stata_fastxtile.py**
  - `fastxtile`: Stata-equivalent percentile ranking

TBC: separate asreg and asrol into different files
- **stata_asreg_asrol.py**
  - `asrol`: Rolling window statistics and regressions
    - **IMPORTANT**: NEED TO RATIONALIZE WITH `asrol_custom` from `Predictors/MS.py`
  - `asreg_polars`: Rolling-window regressions using polars
  - `asreg_collinear`: Regression with collinearity handling (no rolling windows)

- **stata_regress.py**
  - `drop_collinear`: Drop collinear variables
  - `regress`: OLS regression
  - `asreg`: (**IMPORTANT**: NEED TO RATIONALIZE THIS WITH `asreg_polars` and `asreg_collinear`. where should this be deployed, if anywhere? should we just delete this?)

- **stata_replication.py**
  - `stata_multi_lag`: Multi-period lagged variables
  - `stata_ineq_pd`: Stata-style inequality operators for pandas
  - `stata_ineq_pl`: Stata-style inequality operators for polars
  - `stata_quantile`: Stata-style quantiles
  - `fill_date_gaps`: Fill date gaps to create a clean panel for lag operations

TBC: add to stata_replication.py
- **relrank.py**
  - `relrank`: Relative ranking within groups

- **sicff.py**
  - `sicff`: SIC to Fama-French industry mapping

- **winsor2.py**
  - `winsor2`: Data winsorization




Extra:
- `Predictors/MS.py`: asrol_custom()
   - Should consider systematically using this.

## Files that use asreg 

**Current organization asreg-related utilities:**
- all in `utils/stata_asreg_asrol.py`
   - `asreg_collinear()`: for specifically dealing with collinearity problems in TrendFactor.py
   - `asreg_polars()`: a fast asreg used everywhere else

**Updated all 10 predictor files using polars asreg:**
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

**TrendFactor.py unchanged** - already uses `asreg_collinear()` 

# Other utility modules

## utils/asrol.py (17 scripts)

Group 1
- DivInit.py
- DivOmit.py
- DivSeason.py

Group 2
- Herf.py
- HerfAsset.py
- HerfBE.py
- Investment.py

Group 3
- MomOffSeason06YrPlus.py
- MomOffSeason11YrPlus.py
- MomOffSeason16YrPlus.py
- MomVol.py

Group 4
- CitationsRD.py
- RDAbility.py
- Recomm_ShortInterest.py
- TrendFactor.py
- VarCF.py
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

