* --------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear
// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
gcollapse (max) MaxRet = ret, by(permno time_avail_m)
label var MaxRet "Maximum return over month"
// SAVE
do "$pathCode/savepredictor" MaxRet