* -------------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear
// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
gen double ill = abs(ret)/(abs(prc)*vol)
gcollapse (mean) ill, by(permno time_avail_m)
xtset permno time_avail_m
gen Illiquidity = (ill + l.ill + l2.ill + l3.ill + l4.ill + l5.ill + ///
    l6.ill + l7.ill + l8.ill + l9.ill + l10.ill + l11.ill)/12
    
label var Illiquidity "Illiquidity"
// SAVE
do "$pathCode/savepredictor" Illiquidity