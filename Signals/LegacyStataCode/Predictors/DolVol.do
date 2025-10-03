* --------------
// DATA LOAD
use permno time_avail_m vol prc using "$pathDataIntermediate/monthlyCRSP", clear
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen DolVol = log(l2.vol*abs(l2.prc))
label var DolVol "Past trading volume"
// SAVE
do "$pathCode/savepredictor" DolVol