*** Prepare data from daily stock file for use at monthly level
** Generate alternative bid-ask spread, illiquidity, alternative beta, idiosyncratic risk

** Import data
import delimited "$pathProject/DataRaw/d_CRSP.csv", clear

gen time_d = date(date, "YMD")
format time_d %td
drop date

// Save file
compress
save tempD, replace


*-----------------------------------
* Generate monthly level variables
*-----------------------------------
gen time_m = mofd(time_d)

// Illiquidity
gen double ill  = abs(ret)/(abs(prc)*vol)
*gen std_turn 	= vol/shrout
gen countzero	= 1 if vol == 0 // | vol ==.
gen turn 	    = vol/shrout
gen days 	    = 0 /* help variable because of some weirdness of collapse */

// Max price
replace prc = abs(prc)
gen     prcadj = prc/cfacshr

gcollapse (mean) ill (sum) countzero turn ///
	(max) maxret = ret maxpr = prcadj (count) ndays = days (skewness) ReturnSkew = ret, ///
	by(permno time_m)

gen zerotrade = (countzero + ((1/turn)/480000))*(21/ndays)

replace ReturnSkew = . if ndays < 15

* SAVE
*keep if y > 1960
rename time_m time_avail_m
format time_avail_m %tm
drop countzero ndays turn

compress
save "$pathProject/DataClean/m_DCRSP_1", replace

* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Estimate idiovol and various idiosyncractic skewness measures from daily returns
u tempD, clear
drop shrout vol prc

merge m:1 time_d using "$pathProject/DataClean/dFF", nogenerate keep(match)
replace ret = ret - rf
drop time_w umd rf cfacshr

* Set up CAPM to estimate idiovol
bys permno (time_d): gen time_temp = _n
xtset permno time_temp

// CAPM 
asreg ret mktrf, window(time_temp 20) min(15) by(permno) rmse
rename _rmse idiovol
gen ReturnSkewCAPM = ret - _b_cons - _b_mktrf*mktrf  // This is idiosyncratic return, skew computed below

// IdioVol as in HXZ citing Ali et al (2003)
drop _*
asreg ret mktrf, window(time_temp 252) min(100) by(permno) rmse
rename _rmse IdioVolAHT

// 3 Factor model
drop _*
asreg ret mktrf smb hml, window(time_temp 20) min(15) by(permno)
gen ReturnSkew3F = ret - _b_cons - _b_mktrf*mktrf - _b_smb*smb - _b_hml*hml  // This is idiosyncratic return, skew computed below

// Q Factor model
drop _* mktrf smb hml
merge m:1 time_d using "$pathProject/DataClean/d_qfactor", nogenerate keep(master match)
drop r_f_qfac
xtset permno time_temp
asreg ret r_mkt_qfac r_me_qfac r_ia_qfac r_roe_qfac, window(time_temp 20) min(15) by(permno)

gen ReturnSkewQF = ret - _b_cons - _b_r_mkt_qfac*r_mkt_qfac - _b_r_me_qfac*r_me_qfac ///
	- _b_r_ia_qfac*r_ia_qfac - _b_r_roe_qfac*r_roe_qfac // This is idiosyncratic return, skew computed below

drop _* *_qfac

// Collapse to monthly (last value for idiovol, skewness for ReturnSkew*)
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

drop if mi(idiovol)
sort permno time_avail_m time_d
gcollapse (lastnm) idiovol IdioVolAHT ///
    (sd) IdioVolCAPM = ReturnSkewCAPM IdioVol3F = ReturnSkew3F IdioVolQF = ReturnSkewQF ///
    (skewness) ReturnSkew*, by(permno time_avail_m)

compress

* SAVE 
save "$pathProject/DataClean/m_DCRSP_2", replace

* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Systematic volatility
u tempD, clear
drop shrout vol prc

merge m:1 time_d using "$pathProject/DataClean/dFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf cfacshr

merge m:1 time_d using "$pathProject/DataClean/d_vix", nogenerate keep(match) keepusing(dVIX)

* Set up CAPM to estimate systematic volatility
bys permno (time_d): gen time_temp = _n
xtset permno time_temp

asreg ret mktrf dVIX, window(time_temp 20) min(15) by(permno)
rename _b_dVIX betaVIX

gen time_avail_m = mofd(time_d)
format time_avail_m %tm
collapse (lastnm) betaVIX , by(permno time_avail_m)
* SAVE 
save "$pathProject/DataClean/m_DCRSP_3", replace

* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Estimate price delay from daily returns
u tempD, clear

drop shrout prc vol
format time_d %td

merge m:1 time_d using "$pathProject/DataClean/dFF", keepusing(rf mktrf) nogenerate keep(match)
replace ret = ret - rf

bys permno (time_d): gen time_temp = _n
xtset permno time_temp
foreach n of numlist 1/4 {
	gen mktLag`n' = l`n'.mktrf
}

asreg ret mktrf mktLag1 mktLag2 mktLag3 mktLag4, by(permno) window(time_temp 252) min(26) se

cap drop _adjR2 _Nobs _b_cons

winsor2 *_b_*, replace cut(1 99)
gen tempSum1 = _b_mktLag1 + 2*_b_mktLag2 + 3*_b_mktLag3 + 4*_b_mktLag4
gen tempSum2 = _b_mktLag1 + _b_mktLag2 + _b_mktLag3 + _b_mktLag4
gen PriceDelay = tempSum1/(_b_mktrf + tempSum2)

* Construct D3
drop tempSum*
winsor2 *_se*, replace cut(1 99)  // Not sure about winsorizing standard errors
gen tempSum1 = _b_mktLag1/_se_mktLag1 + 2*_b_mktLag2/_se_mktLag2 + 3*_b_mktLag3/_se_mktLag3 + 4*_b_mktLag4/_se_mktLag4
gen tempSum2 = _b_mktLag1/_se_mktLag1 + _b_mktLag2/_se_mktLag2 + _b_mktLag3/_se_mktLag3 + _b_mktLag4/_se_mktLag4
gen PriceDelayAdj = tempSum1/(_b_mktrf + tempSum2)

* Construct D1
rename _R2 R2Unrestricted
drop _* tempSum*

asreg ret mktrf, by(permno) window(time_temp 252) min(26) // Cannot entirely control that observations are the same as above

gen PriceDelayRsq = 1 - _R2/R2Unrestricted
drop _*

gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_d
gcollapse (mean) PriceDelay*, by(permno time_avail_m)

compress

* SAVE 
save "$pathProject/DataClean/m_DCRSP_4", replace

*-------------------------------------------------------------------------------
* Additional price delay measures from weekly returns
/*
u tempD, clear

drop shrout prc vol

format time_d %td
gen time_w = wofd(time_d)
format time_w %tw

merge m:1 time_d using "$pathProject/DataClean/dFF", keepusing(rf mktrf) nogenerate keep(match)
replace ret = ret - rf

bys permno time_w (time_d): gen wkret = exp(sum(ln(1+ret))) - 1
bys permno time_w (time_d): gen mktrf_w = exp(sum(ln(1+mktrf))) - 1

gcollapse (lastnm) wkret mktrf_w, by(permno time_w)

bys permno (time_w): gen time_temp = _n
xtset permno time_temp
foreach n of numlist 1/4 {
	gen mktLag`n' = l`n'.mktrf
}

asreg wkret mktrf_w mktLag1 mktLag2 mktLag3 mktLag4, by(permno) window(time_temp 52) min(13) se

* Construct D3
winsor2 *_b_* *_se*, replace cut(1 99)  // Not sure about winsorizing standard errors
gen tempSum1 = _b_mktLag1/_se_mktLag1 + 2*_b_mktLag2/_se_mktLag2 + 3*_b_mktLag3/_se_mktLag3 + 4*_b_mktLag4/_se_mktLag4
gen tempSum2 = _b_mktLag1/_se_mktLag1 + _b_mktLag2/_se_mktLag2 + _b_mktLag3/_se_mktLag3 + _b_mktLag4/_se_mktLag4
gen PriceDelayAdj = tempSum1/(_b_mktrf + tempSum2)

* Construct D1
rename _R2 R2Unrestricted
drop _* tempSum*

asreg wkret mktrf_w, by(permno) window(time_temp 52) min(17) se  // Cannot entirely control that observations are the same as above. Use min(17) to take into account.

gen PriceDelayRsq = 1 - _R2/R2Unrestricted
drop _*

gen time_avail_m = mofd(dofw(time_w))
format time_avail_m %tm
gcollapse (mean) PriceDelay*, by(permno time_avail_m)

compress

save "$pathProject/DataClean/m_DCRSP_4a", replace
*/

*-------------------------------------------------------------------------------
* Estimate tail risk for later use
u tempD, clear
keep permno time_d ret
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
preserve
	fcollapse (p5) ret, by(time_avail_m) fast
	rename ret retp5
	save temp, replace
restore
merge m:1 time_avail_m using temp, nogenerate
keep if ret <= retp5
gen tailex = log(ret/retp5)
gcollapse (mean) tailex, by(time_avail_m) 
save "$pathProject/DataClean/TailRisk", replace

*-------------------------------------------------------------------------------
* Estimate downside beta 

* Compute rolling averages of market excess return
use "$pathProject/DataClean/dFF", clear
sort time_d
gen time_temp = _n
asrol mktrf, window(time_temp 252) stat(mean) gen(mu_market) min(252)
keep if mktrf < mu_market  // Keep only if return less than mean of market over previous year
keep time_d mktrf rf
save temp, replace

* Match with daily returns
u tempD, clear
drop shrout prc vol
merge m:1 time_d using temp, nogenerate keep(master match)
replace ret = ret - rf

* Compute downside beta
bys permno (time_d): gen time_temp = _n
xtset permno time_temp

asreg ret mktrf, window(time_temp 252) min(50) by(permno)
rename _b_mktrf DownsideBeta
drop _*

gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d

gcollapse (lastnm) DownsideBeta, by(permno time_avail_m)

* SAVE 
save "$pathProject/DataClean/m_DCRSP_5", replace

*-------------------------------------------------------------------------------
* Frazzini-Pedersen beta and Dimson beta
u tempD, clear
drop shrout prc vol

merge m:1 time_d using "$pathProject/DataClean/dFF", keepusing(rf mktrf) nogenerate keep(match)
replace ret = ret - rf

gen LogRet = log(1+ret)
gen LogMkt = log(1+mktrf)

bys permno (time_d): gen time_temp = _n
xtset permno time_temp

* Standard deviations of log returns
asrol Log*, window(time_temp 252) min(120) by(permno) stat(sd)

* R2 of this regression is squared correlation coefficient
gen tempRi = l2.LogRet + l1.LogRet + LogRet
gen tempRm = l2.LogMkt + l1.LogMkt + LogMkt

asreg tempRi tempRm, window(time_temp 1260) min(750) by(permno) 

gen BetaFP = sqrt(_R2)*(sd252_LogRet/sd252_LogMkt)

drop _* Log* temp*

*----
*Dimson beta
gen tempMktLead = f.mktrf
gen tempMktLag  = l.mktrf

asreg ret tempMktLead mktrf tempMktLag, window(time_temp 20) min(15) by(permno)

gen BetaDimson = _b_tempMktLead + _b_mktrf + _b_tempMktLag

* Add both measures to m_DCRSP.dta
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d

gcollapse (lastnm) BetaFP BetaDimson, by(permno time_avail_m)

save "$pathProject/DataClean/m_DCRSP_6", replace


*-------------------------------------------------------------------------------
* Merge all separate files into one
use "$pathProject/DataClean/m_DCRSP_1", clear
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP_2", nogenerate keep(master match)
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP_3", nogenerate keep(master match)
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP_4", nogenerate keep(master match)
*merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP_4a", nogenerate keep(master match)
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP_5", nogenerate keep(master match)
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP_6", nogenerate keep(master match)
save "$pathProject/DataClean/m_DCRSP", replace

*-------------------------------------------------------------------------------
* Calculate liquidity factor for Pastor-Stambaugh

* Get list of NYSE and AMEX stocks from monthly CRSP data
import delimited "$pathProject/DataRaw/mCRSP.csv", clear
keep if exchcd == 1 | exchcd == 2
*create monthly date
gen time_d = date(date,"YMD")
format time_d %td
gen time_m = mofd(time_d)
format time_m %tm
keep permno time_m 
duplicates drop

save tempM, replace

* Now use daily data to compute stock-level liquidity 
u tempD, clear
gen time_m = mofd(time_d)
format time_m %tm

* Restrict to NYSE and AMEX stocks
merge m:1 permno time_m using tempM, keep(match) nogenerate

* Restrict to prices between 5 and 1000 USD
drop if abs(prc) < 5 | abs(prc) > 1000

* Drop if zero volume (not in PS but in Li et al's CFR paper)
drop if vol == 0 | mi(vol)

* Drop observations before 1962 
drop if yofd(time_d) < 1962

* Merge with market return (value-weighted)
drop cfacshr time_m shrout
merge m:1 time_d using "$pathProject/DataClean/dMarket", keepusing(vwretd) nogenerate keep(match)

* Generate variables relevant for regression
replace ret = ret - vwretd
gen v = abs(prc)*vol / 10^6
replace v = -1*v if ret < 0

* Regression (Note: This runs regression for every day but we only need the last one
* in each month. Therefore, this computes about 20 times more regressions than
* necessary, pretty inefficient. I wasn't sure how to adjust the code though.)

bys permno (time_d): gen time_temp = _n
xtset permno time_temp
gen tempLagRet = l.ret
gen tempLagV   = l.v

drop vol prc vwretd
asreg ret tempLagRet tempLagV, window(time_temp 20) min(15) by(permno)

rename _b_tempLagV gamma_it

gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d

gcollapse (lastnm) gamma_it, by(permno time_avail_m)

* Need average level and average change to compute innovations in liquidty
xtset permno time_avail_m
gen DeltaGamma = gamma_it - l.gamma_it

* Compute aggregate liquidity as monthly average
drop if mi(DeltaGamma)
gcollapse (mean) gammaLiquidity = gamma_it DeltaGamma, by(time_avail_m)

* Rescale with market capitalization relative to 1962
merge 1:1 time_avail_m using "$pathProject/DataClean/mMarket", keep(match) nogenerate keepusing(MarketCapitalization)

tsset time_avail_m
replace DeltaGamma = DeltaGamma * l.MarketCapitalization
replace gammaLiquidity = gammaLiquidity * l2.MarketCapitalization  // Correct or typo in Li et al?



* Now run liquidity innovation regression (Note: Need to do that recursively)
/* 
From Li et al: Pastor and Stambaugh carefully try to avoid any look-ahead bias when constructing
their traded liquidity factors. The liquidity risk innovations available on
WRDS, however, come out of the time-series regression given in Eq. (3) estimated
using data through the end of 2015, and thus use information only available
at the end of 2015 when calculating innovations at the start of the sample in
the 1960s. Estimated liquidity risk betas consequently cannot be calculated by
regressing stock returns onto the posted aggregate liquidity innovations. Instead,
when estimating liquidity risk betas in any month t using Eq. (4), the liquidity risk
innovations used in the regression must themselves be reestimated with Eq. (3)
using only data available up until time t.
*/

* Non-tradable factor using all observations
reg DeltaGamma l.DeltaGamma l.gammaLiquidity

predict L_NonTradable, resid

* Recursive tradable version
gen tempLagDeltaGamma = l.DeltaGamma
gen tempLagGamma =l.gammaLiquidity
asreg DeltaGamma tempLagDeltaGamma tempLagGamma, recursive fitted window(time_avail_m 12)
rename _residuals L_Tradable

drop _* temp* gammaLiquidity DeltaGamma MarketCapitalization

compress
save "$pathProject/DataClean/mLiquidity_Reconstruction", replace



*-------------------------------------------------------------------------------
erase temp.dta
erase tempD.dta
erase tempM.dta
