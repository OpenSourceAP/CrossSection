* --------------
// DATA LOAD
use gvkey permno time_avail_m dm using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen securedind = 0
replace securedind = 1 if dm !=. & dm !=0
label var securedind "Secured debt indicator"
// SAVE
do "$pathCode/saveplacebo" securedind