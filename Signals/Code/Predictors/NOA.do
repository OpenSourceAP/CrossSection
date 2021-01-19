* --------------
// DATA LOAD
use gvkey permno time_avail_m at che dltt mib dc ceq using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen OA = at - che
gen OL = at - dltt - mib - dc - ceq
gen NOA = (OA - OL)/l12.at
label var NOA "Net Operating Assets"
// SAVE
do "$pathCode/savepredictor" NOA