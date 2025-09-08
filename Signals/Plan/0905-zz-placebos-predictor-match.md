# Placebo - Closest Predictor Match
## Complete:
 - **AbnormalAccuralsPercent**: Completed in Predictors
    - `Predictors/ZZ2_AbnormalAccurals_AbnormalAccuralsPercent.py`
 - **FRBook**: Completed in Predictors
    - `Predictors/ZZ1_FR_FRBook.py`
 - **IntrinsicValue**: Completed in Predictors
    - `Predictors/ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py`
 - **OrgCapNoAdj**: Completed in Predictors
    - `Predictors/ZZ1_OrgCap_OrgCapNoAdj.py`
 - **ResidualMomentum6m**: Completed in Predictors
    - `Predictors/ZZ1_ResidualMomentum6m_ResidualMomentum.py`
 - **grcapx1y**: Completed in Predictors
    - `Predictors/ZZ1_grcapx_grcapx1y_grcapx3y.py`

## Incomplete:
 - **BetaDimson**: *BetaVIX*
 - **DelayAcct**/**DelayNonAcct**: *PriceDelay*
 - **DownsideBeta**: *MomOffSeason* and *BetaVIX* 
    - use *MomOffSeason* for asrol and *BetaVIX* for asreg
    - If needed, *TrendFactor* has asrol on daily data
 - **EarningsValueReference**/**EarningsTimeliness**/**EarningsConservatism**: *EarningsSuprise* and *Beta*
    - *EarningsSuprise* looks to have the same multi-lag equation, but just missing asreg that placebos do
    - Follow *Beta* for asreg
    - Follow `DataDownloads/B_CompustatAnnual.py` for expansion to monthly
 - **EarningsPersistence**/**EarningsPredictability**: Simpler version of Other Earnings Placebos
 - **IdioVolQF**: *ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F*
    - This is just subbing in Q factors for FF3 factors
 - **ReturnSkewQF**: *ReturnSkew3F*
 - **betaCC**/**betaRC**/**betaCR**/**betaRR**/**betaNet**: 
    - daily crsp part: see *Illiquidity*
    - asreg on monthly CRSP: see *Beta*    
    - asrol on monthly return data: see *DivInit*

