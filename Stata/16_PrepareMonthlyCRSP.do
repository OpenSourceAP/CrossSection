*** Prepare monthly CRSP ***

* Prepare distributions
import delimited "$pathProject/DataRaw/mCRSPdistributions.csv", clear
*create monthly date
gen time_d = date(rcrddt,"YMD")
format time_d %td
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d rcrddt

gcollapse (sum) divamt, by(permno time_avail_m)
save "$pathProject/DataClean/mCRSPdistributions", replace

** Now prepare monthly CRSP and match distributions
import delimited "$pathProject/DataRaw/mCRSP.csv", clear
rename siccd sicCRSP

* Make 2 digit SIC
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
destring sic*, replace

*create monthly date
gen time_d = date(date,"YMD")
format time_d %td
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d

* Incorporate delisting return
replace dlret = -.35 if dlret==. & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584)) ///
	& (exchcd == 1 | exchcd == 2)

replace dlret = -.55 if dlret==. & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584)) ///
	& exchcd == 3  // GHZ cite Johnson and Zhao (2007), Shumway and Warther (1999)

replace dlret = -1 if dlret < -1 & dlret !=.

replace dlret = 0 if dlret ==.

replace ret = ret + dlret

replace ret = dlret if ret ==. & dlret !=0

* Match distributions
merge 1:1 permno time_avail_m using "$pathProject/DataClean/mCRSPdistributions", nogenerate keep(master match)

* Replace dividend with 0 if missing
replace divamt = 0 if divamt ==.

* Store distribution code as string
*tostring distcd, replace force

** Housekeeping
drop dlret dlstcd date permco
*bysort permno time_avail_m: keep if _n == 1  // Remove duplicates (related to dividend amount in some share code classes)
compress

*** Compute beta, beta^2, R2 of CAPM regression and coskewness based on 60 months of past returns
merge m:1 time_avail_m using "$pathProject/DataClean/mFF", nogenerate keep(match)
merge m:1 time_avail_m using "$pathProject/DataClean/mMarket",  nogenerate keep(match)

* Set up CAPM. Need beta and r2
gen retrf = ret - rf
gen ewmktrf = ewretd - rf
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp

asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)
rename _b_ewmktrf Beta
// Square of beta
gen Betasq = Beta^2
rename _R2 r2CAPM
drop _*


*-------------------------------------------------------------------------------
* Residual momentum
asreg retrf mktrf hml smb, window(time_temp 36) min(36) by(permno) fitted

gen temp = l1._residuals  // To skip most recent month in what follows

* 6 month version
asrol temp, window(time_temp 6) min(6) by(permno) stat(mean sd)
gen ResidualMomentum6m = mean6_temp/sd6_temp

* 12 month version
asrol temp, window(time_temp 11) min(11) by(permno) stat(mean sd)
gen ResidualMomentum11m = mean11_temp/sd11_temp

drop temp* mean*temp sd*temp _*

*-------------------------------------------------------------------------------
* Pastor-Stambaugh liquidity beta
merge m:1 time_avail_m using "$pathProject/DataClean/mLiquidity", nogenerate keep(master match)

asreg retrf ps_innov mktrf hml smb, window(time_temp 60) min(36) by(permno)

rename _b_ps_innov BetaLiquidityPS
drop _*


*-------------------------------------------------------------------------------
// Coskewness
gen vwmktrf = vwretd - rf
asreg retrf vwmktrf, window(time_temp 60) min(20) by(permno)
gen tempResid = retrf - _b_cons - _b_vwmktrf*vwmktrf

* Compute various moving averages
drop _N*
asrol vwmktrf, gen(meanX) stat(mean) window(time_temp 60) min(20) by(permno)
gen tempResidMkt = vwmktrf - meanX
drop meanX

gen tempNum1 = tempResid*(tempResidMkt^2)
asrol tempNum1, gen(tempNumerator) stat(mean) window(time_temp 60) min(20) by(permno)

gen tempResid2 = tempResid^2
asrol tempResid2, gen(tempDenom1) stat(mean) window(time_temp 60) min(20) by(permno)

gen tempResidMkt2 = tempResidMkt^2
asrol tempResidMkt2, gen(tempDenom2) stat(mean) window(time_temp 60) min(20) by(permno)

* Finally, calculate coskewness
gen Coskewness = tempNumerator/(sqrt(tempResid2)*tempResidMkt2)
drop temp* _* time_temp rf retrf ewmktrf vwmktrf

*-----------------------------------------------------
* Calculate Acharya and Pedersen illiquidity measures
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP", keep(master match) keepusing(ill) nogenerate
replace ill = ill*10^6 // Scaling as in Acharya and Pedersen (2005)
xtset permno time_avail_m

gen double c_i = min(.25 +.3*ill*MarketCapitalization, 30)  // Amounts to winsorization of 10% of data

* Compute market illiquidity innovation and market return innovation
preserve

    // Filters in Acharya and Pedersen (2005)
    keep if abs(prc) > 5 & abs(prc) < 1000  
	keep if exchcd == 1 | exchcd == 2

	gen temp = shrout*abs(prc)  // Market cap of stock i
	gen double temp2 = min(ill, (30-.25)/(.3*MarketCapitalization))  // Unnormalized liquidity
	replace temp2 = . if mi(ill)
	gcollapse (mean) MarketIlliquidity = temp2 rM = vwretd MarketCapitalization [aweight = temp], by(time_avail_m)

	tsset time_avail_m
	gen double temp = .25 + MarketIlliquidity*l.MarketCapitalization
	gen double templ1 = .25 + l.MarketIlliquidity*l.MarketCapitalization
	gen double templ2 = .25 + l2.MarketIlliquidity*l.MarketCapitalization

	asreg temp templ1 templ2, window(time 60) min(48) fitted
	rename _residuals eps_c_M
	rename _b_cons APa0
	rename _b_templ1 APa1
	rename _b_templ2 APa2  // Acharya and Pedersen use coefficients from market model to compute stock (portfolio) illiquidity innovations
	drop _*

	gen tempRlag1 = l.rM
	gen tempRlag2 = l2.rM
	asreg rM tempRlag1 tempRlag2, window(time 60) min(48) fitted
	rename _residuals eps_r_M

	keep time_avail_m eps* AP*
	save temp, replace

restore

merge m:1 time_avail_m using temp, keep(master match) nogenerate
xtset permno time_avail_m

* Compute stock-level innovation in illiquidity (using coefficients from market model, see WP of Acharya and Pedersen)

gen double tempIll = min(ill, (30-.25)/(.3*MarketCapitalization))
gen double temp = .25 + tempIll*l.MarketCapitalization
gen double templ1 = .25 + l.tempIll*l.MarketCapitalization
gen double templ2 = .25 + l2.tempIll*l.MarketCapitalization
	
gen eps_c_i = temp - (APa0 + APa1*templ1 + APa2*templ2)

* Compute betas (requires some work because covariances are not implemented in asrol)

asrol ret eps_r_M eps_c_i eps_c_M, window(time 60) min(24) stat(mean) by(permno)
gen tempEpsDiff = eps_r_M - eps_c_M
asrol tempEpsDiff, window(time 60) min(24) stat(sd) by(permno)  // To make steps easier to follow, could have done this above in preserve/restore step
replace sd60_tempEpsDiff = sd60_tempEpsDiff^2

gen tempRR = (ret - mean60_ret)*(eps_r_M - mean60_eps_r_M)
gen tempCC = (eps_c_i - mean60_eps_c_i)*(eps_c_M - mean60_eps_c_M)
gen tempRC = (ret - mean60_ret)*(eps_c_M - mean60_eps_c_M)
gen tempCR = (eps_c_i - mean60_eps_c_i)*(eps_r_M - mean60_eps_r_M)

asrol tempRR tempCC tempRC tempCR, window(time 60) min(24) stat(mean) by(permno)

gen betaRR = mean60_tempRR/sd60_tempEpsDiff
gen betaCC = mean60_tempCC/sd60_tempEpsDiff
gen betaRC = mean60_tempRC/sd60_tempEpsDiff
gen betaCR = mean60_tempCR/sd60_tempEpsDiff
gen betaNet = betaRR + betaCC - betaRC - betaCR

foreach v of varlist betaRR betaCC betaRC betaCR betaNet {

replace `v' = . if  abs(prc) > 1000
}

drop temp* mean60* sd60* eps_* APa* ill vwretd ewretd MarketCapitalization c_i

compress
save "$pathProject/DataClean/m_CRSP", replace
