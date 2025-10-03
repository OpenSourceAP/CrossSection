* --------------
// Compute SIGMA as prerequisite to FailureProbability
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
keep if time_d >= date("19601231","YMD")	

* Set up for asreg
bys permno (time_d): gen time_temp = _n
xtset permno time_temp

* SIGMA is "the standard deviation of each firm's daily stock return over the past 3 months"
asrol ret, stat(sd) window(time_temp 60) min(10) by(permno) gen(SIGMA)
drop if mi(SIGMA)
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (lastnm) SIGMA, by(permno time_avail_m)
save "$pathtemp/tempPlacebo", replace


// DATA LOAD
use permno gvkey time_avail_m ret prc using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout)
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", keep(master match) nogenerate keepusing(mktrf)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ceqq ltq cheq ibq) nogenerate keep(match)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(txditc seq ceq at lt pstk pstkrv pstkl txdb) nogenerate keep(match)
merge 1:1 permno time_avail_m using "$pathtemp/tempPlacebo", keep(master match) nogenerate 

// SIGNAL CONSTRUCTION
gen tempMV = shrout*abs(prc)
*gen tempTA = atq + .1*(tempMV - ceqq)
* RSIZE
gen tempMV2 = tempMV
bys time_avail_m (tempMV2): gen tempRK = _N- _n + 1
replace tempMV2 = . if tempRK > 500 
egen tempTotMV = total(tempMV2), by(time_avail_m)  
gen tempRSIZE = log(tempMV/tempTotMV)

* EXRET
gen tempEXRET = log(1+ret) - log(1+mktrf)

*NIMTA
gen tempNIMTA = ibq/(tempMV + ltq)

*TLMTA
gen tempTLMTA = ltq/(tempMV + ltq)

*CASHMTA
gen tempCASHMTA = cheq/(tempMV + ltq)

* "After total assets are adjusted, each of the seven explanatory variables is winsorized using a 5/95 percentile interval in order to eliminate outliers." (CHS (2008, p. 2935))
* Note: We do not need to construct the two TA ratios since those are not part of the predictor
winsor2 temp*, replace cut(5 95)

*NIMTAAVG and EXRETAVG
xtset permno time_avail_m
local rho = 2^(-1/3)
gen tempNIMTAAVG =( (1 - `rho'^3)/(1-`rho'^12))*(tempNIMTA + `rho'^3*l3.tempNIMTA + `rho'^6*l6.tempNIMTA + `rho'^9*l9.tempNIMTA)
gen tempEXRETAVG =( (1 - `rho')/(1-`rho'^12))*(tempEXRET + `rho'^1*l1.tempEXRET + `rho'^2*l2.tempEXRET + `rho'^3*l3.tempEXRET + ///
    `rho'^4*l4.tempEXRET + `rho'^5*l5.tempEXRET + `rho'^6*l6.tempEXRET + ///
    `rho'^7*l7.tempEXRET + `rho'^8*l8.tempEXRET + `rho'^9*l9.tempEXRET + `rho'^10*l10.tempEXRET + `rho'^11*l11.tempEXRET)

*MB
* Compute book equity ("Book equity is as defined in Davis, Fama, and French (2000) and outlined in detail in Cohen, Polk, and Vuolteenaho (2003)." (CHS, p.2935))
replace txditc = 0 if mi(txditc)
gen tempPS = pstk
replace tempPS = pstkrv if mi(tempPS)
replace tempPS = pstkl if mi(tempPS)

gen tempSE = seq
replace tempSE = ceq + tempPS if mi(tempSE)
replace tempSE = at - lt if mi(tempSE)

gen tempBE = tempSE + txditc - tempPS + txdb

* "We adjust the book value of equity in a similar [to TA, but not really clear how it is different] manner. Just under 2% of firm-months still have negative values for book equity even after this adjustment, and we replace these negative values with small positive values of $1 to ensure that the market-to-book ratios for these firms are in the right tail, not the left tail, of the distribution. (CHS, p. 2906)
gen tempBEAdj = tempBE + 0.1 * (tempMV - tempBE)
replace tempBEAdj = 1 / 1000000 if tempBEAdj < 0

gen tempMB = tempMV/tempBEAdj

*PRICE
gen tempPRICE = log(min(abs(prc), 15))

* Finally compute FailureProbability based on Table IV, 12-month column
gen FailureProbability = -9.16 -.058*tempPRICE + .075*tempMB - 2.13*tempCASHMTA ///
    -.045*tempRSIZE + 100*1.41*SIGMA - 7.13*tempEXRETAVG + 1.42*tempTLMTA - 20.26*tempNIMTAAVG  
    
label var FailureProbability "Failure Probability"

* Failure probability (June version)
gen FailureProbabilityJune = FailureProbability if month(dofm(time_avail_m)) == 6
bys permno (time_avail_m): replace FailureProbabilityJune = FailureProbabilityJune[_n-1] if mi(FailureProbabilityJune)
label var FailureProbabilityJune "Failure Probability (June version)"

// SAVE
do "$pathCode/saveplacebo" FailureProbability
do "$pathCode/saveplacebo" FailureProbabilityJune
