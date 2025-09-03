# Utils Module Census Report - Organized by Function

Doctor Andrew, here's the comprehensive census of utils/ modules and their usage in pyCode/Predictors/, organized by functionality.

## Data Processing & Analysis Functions

### Time Series & Lagging Functions
**Module**: `stata_replication.py` - `stata_multi_lag` function (35 scripts)
- CitationsRD.py, EarningsConsistency.py, FirmAgeMom.py, Mom12m.py, Mom6m.py, MomOffSeason.py, MomOffSeason06YrPlus.py, MomOffSeason11YrPlus.py, MomOffSeason16YrPlus.py, MomRev.py, MomSeason.py, MomSeason06YrPlus.py, MomSeason11YrPlus.py, MomSeason16YrPlus.py, MomSeasonShort.py, MomVol.py, PS.py, RDcap.py, ZZ1_NetDebtFinance.py, ZZ1_Payout_PayoutYield.py, ZZ1_RIO_.py, ZZ2_RealizedVolAHT.py, agr.py, chcsho.py, grcapx.py, grltnoa.py, hire.py, lgr.py, pchcapx_ia.py, pchdepr.py, pchgm_pct.py, pchsaleinv.py, ProbInformedTrading.py, roavol.py, sfe.py, spii.py, std_turn.py, turn.py, zerotrade.py

**Module**: `stata_replication.py` - `fill_date_gaps` function (3 scripts)
- PS.py, RDcap.py, Recomm_ShortInterest.py

### Rolling Window Calculations
**Module**: `asrol.py` (25 scripts)
- CitationsRD.py, DivInit.py, DivOmit.py, DivSeason.py, Herf.py, HerfAsset.py, HerfBE.py, MomOffSeason.py, MomOffSeason06YrPlus.py, MomOffSeason16YrPlus.py, MomVol.py, MS.py, VolumeTrend.py, ZZ1_NetDebtFinance.py, ZZ1_RealizedVolCall.py, ZZ1_RIO_.py, ZZ2_RealizedVolAHT.py, agr.py, chcsho.py, grcapx.py, grltnoa.py, hire.py, roavol.py, sfe.py, turn.py

### Ranking & Quantile Functions
**Module**: `stata_replication.py` - `relrank` function (3 scripts)
- EarnSupBig.py, IndRetBig.py, ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py

**Module**: `stata_fastxtile.py` - `fastxtile` function (6 scripts) 
- AccrualsBM.py, CitationsRD.py, PatentsRD.py, Recomm_ShortInterest.py, ZZ1_Activism1_Activism2.py, ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py

**Module**: `stata_replication.py` - `stata_quantile` function (1 script)
- CitationsRD.py

### Inequality & Comparison Functions
**Module**: `stata_replication.py` - `stata_ineq_pd` function (2 scripts)
- DivSeason.py, retConglomerate.py

**Module**: `stata_replication.py` - `stata_ineq_pl` function (2 scripts)
- MS.py, ShareVol.py

### Data Cleaning Functions
**Module**: `winsor2.py` (3 scripts)
- VolumeTrend.py, ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py, ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py

## Industry Classification Functions
**Module**: `sicff.py` (8 scripts)
- EarnSupBig.py, Frontier.py, IndRetBig.py, sinAlgo.py, ZZ1_OrgCap_OrgCapNoAdj.py, ZZ1_RealizedVolCall.py, ZZ2_RealizedVolAHT.py, agr.py

## Output Functions
**Module**: `save_standardized.py` - ESSENTIAL
**Usage**: Nearly every predictor (~100+ scripts)
*Core infrastructure for saving predictor output*

## Unused Modules (Candidates for Removal)

### Testing/Development Scripts (8 modules)
- `test_signalmaster.py` - Testing utility
- `test_dl.py` - Testing utility  
- `test_predictors.py` - Testing utility
- `PredictorSummaryComparison.py` - Analysis utility
- `column_standardizer_yaml.py` - DataDownloads configuration
- `portcheck.py` - Portfolio analysis standalone tool
- `fetch-doc.py` - Documentation utility
- `stata_regress.py` - Code moved inline to TrendFactor.py

## Summary by Function Type

**Most Critical Functions** (keep):
1. **Output/Save**: `save_standardized` (universal usage)
2. **Time Series**: `stata_multi_lag` (35 scripts)
3. **Rolling Windows**: `asrol` (25 scripts)
4. **Industry Classification**: `sicff` (8 scripts)
5. **Quantiles**: `fastxtile` (6 scripts)

**Lower Priority Functions** (evaluate):
- Data cleaning: `winsor2` (3 scripts)
- Gap filling: `fill_date_gaps` (3 scripts) 
- Ranking: `relrank` (3 scripts)
- Inequality comparisons: `stata_ineq_*` (4 scripts total)

**Safe to Remove**: 8 unused modules (testing, development, moved code)