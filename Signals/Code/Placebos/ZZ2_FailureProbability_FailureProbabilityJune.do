* --------------
// Compute IdioRisk as prerequisite to FailureProbability
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 
* Set up CAPM to estimate idiovol
bys permno (time_d): gen time_temp = _n
xtset permno time_temp
* CAPM 
asreg ret mktrf, window(time_temp 20) min(15) by(permno) rmse
rename _rmse IdioRisk
drop if mi(IdioRisk)
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (lastnm) IdioRisk, by(permno time_avail_m)
save "$pathtemp/tempPlacebo", replace
// DATA LOAD
use permno gvkey time_avail_m ret prc using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout)
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", keep(master match) nogenerate keepusing(mktrf)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ceqq ltq cheq ibq) nogenerate keep(match)
merge 1:1 permno time_avail_m using "$pathtemp/tempPlacebo", keep(master match) nogenerate 
// SIGNAL CONSTRUCTION
gen tempMV = shrout*abs(prc)
gen tempTA = atq + .1*(tempMV - ceqq)
gen tempMV2 = tempMV
bys time_avail_m (tempMV2): gen tempRK = _N- _n + 1
replace tempMV2 = . if tempRK > 500 
egen tempTotMV = total(tempMV2), by(time_avail_m)  
gen tempRSIZE = log(tempMV/tempTotMV)
gen tempEXRET = log(1+ret) - log(1+mktrf)
gen tempNIMTA = ibq/(tempMV + ltq)
gen tempTLMTA = ltq/(tempMV + ltq)
gen tempCASHMTA = cheq/(tempMV + ltq)
winsor2 temp*, replace cut(5 95)
xtset permno time_avail_m
local rho = 2^(-1/3)
gen tempNIMTAAVG =( (1 - `rho'^3)/(1-`rho'^12))*(tempNIMTA + `rho'^3*l3.tempNIMTA + `rho'^6*l6.tempNIMTA + `rho'^9*l9.tempNIMTA)
gen tempEXRETAVG =( (1 - `rho')/(1-`rho'^12))*(tempEXRET + `rho'^1*l1.tempEXRET + `rho'^2*l2.tempEXRET + `rho'^3*l3.tempEXRET + ///
    `rho'^4*l4.tempEXRET + `rho'^5*l5.tempEXRET + `rho'^6*l6.tempEXRET + ///
    `rho'^7*l7.tempEXRET + `rho'^8*l8.tempEXRET + `rho'^9*l9.tempEXRET + `rho'^10*l10.tempEXRET + `rho'^11*l11.tempEXRET)

gen tempMB = tempMV/ceqq
gen tempPRICE = log(min(abs(prc), 15))
gen FailureProbability = -9.16 -.058*tempPRICE + .075*tempMB - 2.13*tempCASHMTA ///
    -.045*tempRSIZE + 100*1.41*IdioRisk - 7.13*tempEXRETAVG + 1.42*tempTLMTA - 20.26*tempNIMTAAVG  
    
label var FailureProbability "Failure Probability"
* Failure probability (June version)
gen FailureProbabilityJune = FailureProbability if month(dofm(time_avail_m)) == 6
bys permno (time_avail_m): replace FailureProbabilityJune = FailureProbabilityJune[_n-1] if mi(FailureProbabilityJune)
label var FailureProbabilityJune "Failure Probability (June version)"

// SAVE
do "$pathCode/saveplacebo" FailureProbability
do "$pathCode/saveplacebo" FailureProbabilityJune