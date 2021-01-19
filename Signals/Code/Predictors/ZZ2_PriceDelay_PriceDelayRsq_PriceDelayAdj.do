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
asreg ret mktrf mktLag1 mktLag2 mktLag3 mktLag4, by(permno) window(time_temp 252) min(26) se
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
asreg ret mktrf, by(permno) window(time_temp 252) min(26) // Cannot entirely control that observations are the same as above
gen PriceDelayRsq = 1 - _R2/R2Unrestricted
drop _*
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
gcollapse (mean) PriceDelay*, by(permno time_avail_m)
xtset permno time_avail_m
gen temp = l.PriceDelay  // Hou and Moskowitz skip one month
drop PriceDelay
rename temp PriceDelay
label var PriceDelay "Price delay"
gen temp = l.PriceDelayRsq  // Hou and Moskowitz skip one month
drop PriceDelayRsq
rename temp PriceDelayRsq
label var PriceDelayRsq "Price delay (R2 based)"
gen temp = l.PriceDelayAdj  // Hou and Moskowitz skip one month
drop PriceDelayAdj
rename temp PriceDelayAdj
label var PriceDelayAdj "Price delay (SE adjusted)"
gstats winsor PriceDelayAdj, by(time_avail_m) trim cuts(10 90) replace  // Trim very aggressively because coefficient/se not very well-behaved

// SAVE 
do "$pathCode/savepredictor" PriceDelay
do "$pathCode/savepredictor" PriceDelayRsq
do "$pathCode/savepredictor" PriceDelayAdj