* --------------
// DATA LOAD
use gvkey permno time_avail_m at ivao using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempAvAT = .5*(at + l12.at)
gen DelLTI = ivao - l12.ivao
replace DelLTI = DelLTI/tempAvAT
label var DelLTI "Change in long-term investment"
// SAVE
do "$pathCode/savepredictor" DelLTI