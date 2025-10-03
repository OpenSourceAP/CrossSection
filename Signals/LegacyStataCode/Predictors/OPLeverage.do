* --------------
// DATA LOAD
use gvkey permno time_avail_m xsga cogs at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempxsga = 0
replace tempxsga = xsga if xsga !=.
gen OPLeverage = (tempxsga + cogs)/at
label var OPLeverage "Operating Leverage"
// SAVE
do "$pathCode/savepredictor" OPLeverage