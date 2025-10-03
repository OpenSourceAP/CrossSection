* --------------
// DATA LOAD
use gvkey permno time_avail_m at act che using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempAvAT = .5*(at + l12.at)
gen DelCOA = (act - che) - (l12.act - l12.che)
replace DelCOA = DelCOA/tempAvAT
label var DelCOA "Change in current operating assets"
// SAVE
do "$pathCode/savepredictor" DelCOA