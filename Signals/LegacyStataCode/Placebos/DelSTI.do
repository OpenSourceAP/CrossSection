* --------------
// DATA LOAD
use gvkey permno time_avail_m ivst at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempAvAT = .5*(at + l12.at)
gen DelSTI = ivst - l12.ivst
replace DelSTI = DelSTI/tempAvAT
label var DelSTI "Change in short-term investment"
// SAVE
do "$pathCode/saveplacebo" DelSTI