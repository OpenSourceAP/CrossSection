* --------------
// DATA LOAD
use gvkey permno time_avail_m fyear datadate epspx ajex using "$pathDataIntermediate/a_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset gvkey fyear
gen temp = epspx/ajex
gen tempLag = l.temp
asreg temp tempLag, window(fyear 10) min(10) by(gvkey) fitted rmse
rename _b_tempLag EarningsPersistence
gen EarningsPredictability = _rmse^2
drop _* temp*
label var EarningsPersistence "Earnings Persistence"
label var EarningsPredictability "Earnings Predictability"
* Expand to monthly
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations

// SAVE
do "$pathCode/saveplacebo" EarningsPersistence
do "$pathCode/saveplacebo" EarningsPredictability