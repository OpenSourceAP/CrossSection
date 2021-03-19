* --------------
// DATA LOAD
use gvkey permno time_avail_m at lct dlc using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempAvAT = .5*(at + l12.at)
gen DelCOL = (lct - dlc) - (l12.lct - l12.dlc)
replace DelCOL = DelCOL/tempAvAT
label var DelCOL "Change in current operating liabilities"
// SAVE
do "$pathCode/savepredictor" DelCOL