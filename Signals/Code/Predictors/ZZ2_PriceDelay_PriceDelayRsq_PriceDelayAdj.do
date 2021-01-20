* -----------------------------------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 

// SIGNAL CONSTRUCTION
bys permno (time_d): gen time_temp = _n
xtset permno time_temp
foreach n of numlist 1/4 {

gen mktLag`n' = l`n'.mktrf
}

* Need regression for each June
gen ffyear= year(time_d-180)
sort ffyear permno time_d

by ffyear permno: asreg ret mktrf mktLag1 mktLag2 mktLag3 mktLag4, min(26) se
cap drop _adjR2 _Nobs _b_cons
*winsor2 *_b_*, replace cut(1 99)
gstats winsor _b_*, replace cuts(1.0 99.0)

gen tempSum1 = _b_mktLag1 + 2*_b_mktLag2 + 3*_b_mktLag3 + 4*_b_mktLag4
gen tempSum2 = _b_mktLag1 + _b_mktLag2 + _b_mktLag3 + _b_mktLag4
gen PriceDelay = tempSum1/(_b_mktrf + tempSum2)

* Construct D3
drop tempSum*
*winsor2 *_se*, replace cut(1 99)  // Not sure about winsorizing standard errors
gstats winsor _se*, replace cuts(1.0 99.0)
gen tempSum1 = _b_mktLag1/_se_mktLag1 + 2*_b_mktLag2/_se_mktLag2 + 3*_b_mktLag3/_se_mktLag3 + 4*_b_mktLag4/_se_mktLag4
gen tempSum2 = _b_mktLag1/_se_mktLag1 + _b_mktLag2/_se_mktLag2 + _b_mktLag3/_se_mktLag3 + _b_mktLag4/_se_mktLag4
gen PriceDelayAdj = tempSum1/(_b_mktrf + tempSum2)

* Construct D1
rename _R2 R2Unrestricted
drop _* tempSum*
by ffyear permno: asreg ret mktrf, min(26) // Cannot entirely control that observations are the same as above
gen PriceDelayRsq = 1 - _R2/R2Unrestricted
drop _*

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

bys permno ffyear (time_d): keep if _n == _N  // Keep only June
bys permno time_avail_m (time_d): keep if _n == 1 // Remove a few duplicates

xtset permno time_avail_m
replace time_avail_m = time_avail_m + 1 // Hou and Moskowitz skip one month

label var PriceDelay "Price delay"
label var PriceDelayRsq "Price delay (R2 based)"
label var PriceDelayAdj "Price delay (SE adjusted)"

gstats winsor PriceDelayAdj, by(time_avail_m) trim cuts(10 90) replace  // Trim very aggressively because coefficient/se not very well-behaved

* Make full panel
keep permno time_avail_m PriceDelay*
tsfill

foreach v of varlist PriceDelay* {

    bys permno (time_avail_m): replace `v' = `v'[_n-1] if mi(`v')
    
}

// SAVE 
do "$pathCode/savepredictor" PriceDelay
do "$pathCode/savepredictor" PriceDelayRsq
do "$pathCode/savepredictor" PriceDelayAdj