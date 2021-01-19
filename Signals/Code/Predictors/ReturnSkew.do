* -------------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear
// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
gen days = 0 /* help variable because of some weirdness of collapse */
gcollapse (count) ndays = days (skewness) ReturnSkew = ret, by(permno time_avail_m)
replace ReturnSkew = . if ndays < 15
label var ReturnSkew "Return Skewness"
// SAVE
do "$pathCode/savepredictor" ReturnSkew